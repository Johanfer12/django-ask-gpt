# myapp/views.py

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views import View
from django.conf import settings
from .forms import UploadFileForm
import openai
import pandas as pd
import os
from docx import Document
import PyPDF2
from .models import ChatModel

openai.api_key = os.environ.get('OPENAI_API_KEY_H')


@csrf_exempt
def chat_page(request):
    if request.method == "POST":
        user_question = request.POST.get("user_question")
        response = ChatModel.ask(user_question)
        return JsonResponse({"response": response})

    return render(request, 'chat_page.html')


class ProcessFilesView(View):
    template_name = 'process_files.html'
    allowed_extensions = ['.pdf', '.txt', '.docx']

    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        processed_files = self.get_processed_files()
        uploaded_files = self.get_uploaded_files()  # Get the list of uploaded files
        return render(request, self.template_name, {
            'form': form,
            'processed_files': processed_files,
            'uploaded_files': uploaded_files  # Pass the list to the template
        })
    
    def get_uploaded_files(self):
        sources_folder = os.path.join(settings.BASE_DIR, 'askgpt/sources')
        uploaded_files = [f for f in os.listdir(sources_folder) if os.path.isfile(os.path.join(sources_folder, f))]
        return uploaded_files

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if 'file' in request.FILES:  # Check if a file is being uploaded
            if form.is_valid():
                file = request.FILES['file']
                if self.is_valid_extension(file.name):
                    self.handle_uploaded_file(file)
                else:
                    return HttpResponse("Tipo de archivo no admitido. Solo se permiten archivos PDF, TXT o DOCX.")
        else:  # If no file is being uploaded, process the unprocessed files
            self.process_unprocessed_files()

        processed_files = self.get_processed_files()
        form = UploadFileForm()  # Reset the form
        return render(request, self.template_name, {'form': form, 'processed_files': processed_files})

    def process_unprocessed_files(self):
        sources_folder = os.path.join(settings.BASE_DIR, 'askgpt/sources')
        embeddings_folder = os.path.join(settings.BASE_DIR, 'askgpt/embeddings')
        for filename in os.listdir(sources_folder):
            file_path = os.path.join(sources_folder, filename)
            base_name, extension = os.path.splitext(filename)
            output_csv = f"{base_name}-embedding.csv"
            output_path = os.path.join(embeddings_folder, output_csv)
            if not os.path.exists(output_path) and extension.lower() in self.allowed_extensions:
                self.process_files(file_path)
            else:
                print(f"El archivo {output_csv} ya existe. Saltando procesamiento.")

    def handle_uploaded_file(self, file):
        destination = os.path.join(settings.BASE_DIR, 'askgpt/sources', file.name)
        with open(destination, 'wb+') as destination_file:
            for chunk in file.chunks():
                destination_file.write(chunk)

    def is_valid_extension(self, filename):
        _, extension = os.path.splitext(filename)
        return extension.lower() in self.allowed_extensions

    def get_processed_files(self):
        embeddings_folder = os.path.join(settings.BASE_DIR, 'askgpt/embeddings')
        processed_files = [f for f in os.listdir(embeddings_folder) if f.endswith("-embedding.csv")]
        return processed_files

    def process_files(self, file_path):
        base_name, extension = os.path.splitext(os.path.basename(file_path))  # Use os.path.basename
        output_csv = f"{base_name}-embedding.csv"
        output_path = os.path.join(settings.BASE_DIR, 'askgpt/embeddings', output_csv)

        if os.path.exists(output_path):
            print(f"El archivo {output_csv} ya existe. Saltando procesamiento.")
            return

        if extension == '.docx':
            doc = Document(file_path)
            texts = [para.text for para in doc.paragraphs if para.text]
        elif extension == '.pdf':
            raw_text = self.extract_text_from_pdf(file_path)
            texts = self.split_text(raw_text, 150)
        elif extension == '.txt':
            max_words_per_paragraph = 150
            texts = self.load_text_from_txt(file_path, max_words_per_paragraph)
        else:
            raise ValueError(f"Unsupported file extension: {extension}. This script only supports .docx, .txt, and .pdf files.")

        df = pd.DataFrame(texts, columns=['text'])
        df['embedding'] = df['text'].apply(self.get_embedding)

        df[['text', 'embedding']].to_csv(output_path, sep=';', header=None, index=False)
        print("Procesado: " + output_csv)

    def extract_text_from_pdf(self, file_path):
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            for page in range(num_pages):
                content = reader.pages[page].extract_text()
                text += content
        return text

    def load_text_from_txt(self, file_path, max_words):
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_text = file.read()
            paragraphs = self.split_text(raw_text, max_words)
            return paragraphs

    def split_text(self, text, max_words):
        paragraphs = []
        current_paragraph = []
        word_count = 0
        sentences = text.split('. ')
        for sentence in sentences:
            sentence = sentence.strip()
            words = sentence.split()
            word_count += len(words)
            if word_count <= max_words:
                current_paragraph.append(sentence)
            else:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = [sentence]
                word_count = len(words)
        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))
        return paragraphs

    def get_embedding(self, text, model="text-embedding-ada-002"):
        response = openai.Embedding.create(model=model, input=text)
        return response["data"][0]["embedding"]
