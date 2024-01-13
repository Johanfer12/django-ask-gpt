import openai
import pandas as pd
import os
from docx import Document
import PyPDF2

# OS environment key to use the OpenAI API
openai.api_key = os.environ.get('OPENAI_API_KEY_H')

# source data folder
source_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sources')

# Destination embeddings folder
embeddings_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'embeddings')
os.makedirs(embeddings_folder, exist_ok=True)  # Crea la carpeta embeddings si no existe

files = os.listdir(source_folder)

# Embedding model
EMBEDDING_MODEL = "text-embedding-ada-002"

# Emmbedding function
def get_embedding(text, model=EMBEDDING_MODEL):
    response = openai.Embedding.create(model=model, input=text)
    return response["data"][0]["embedding"]

# Extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page in range(num_pages):
            content = reader.pages[page].extract_text()
            text += content
    return text

# Extract text from TXT
def load_text_from_txt(file_path, max_words):
    with open(file_path, 'r', encoding='utf-8') as file:
        raw_text = file.read()
        paragraphs = split_text(raw_text, max_words)
        return paragraphs

# Split text into paragraphs based on word count limit 
def split_text(text, max_words):
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

for file_name in files:
    file_path = os.path.join(source_folder, file_name)

    # name of the file without extension
    base_name, extension = os.path.splitext(file_name)

    # Output file name
    output_csv = f"{base_name} - embedding.csv"
    output_path = os.path.join(embeddings_folder, output_csv)  # Ruta completa del archivo de salida

    # Check if the output file already exists
    if os.path.exists(output_path):
        print(f"El archivo {output_csv} ya existe. Saltando procesamiento.")
        continue

    # Extract text from the file based on its extension
    if extension == '.docx':
        doc = Document(file_path)
        texts = [para.text for para in doc.paragraphs if para.text]  # Ignora los párrafos vacíos
    elif extension == '.pdf':
        raw_text = extract_text_from_pdf(file_path)
        texts = split_text(raw_text, 150)  # Separar por párrafos de hasta 150 palabras
    elif extension == '.txt':
        max_words_per_paragraph = 150  # Ajusta según sea necesario
        texts = load_text_from_txt(file_path, max_words_per_paragraph)
    else:
        raise ValueError(f"Unsupported file extension: {extension}. This script only supports .docx, .txt, and .pdf files.")

    # Dataframe with texts and empty embeddings
    df = pd.DataFrame(texts, columns=['text'])

    # Calculate embeddings
    df['embedding'] = df['text'].apply(get_embedding)

    # Save to CSV
    df[['text', 'embedding']].to_csv(output_path, sep=';', header=None, index=False)
    print("Procesado: " + output_csv)