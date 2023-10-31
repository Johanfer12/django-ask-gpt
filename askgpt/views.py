from django.shortcuts import render
from django.http import JsonResponse
from .models import ChatModel
from django.views.decorators.csrf import csrf_exempt  # Importa el decorador CSRF

@csrf_exempt  # Aplica el decorador CSRF a la vista
def chat_page(request):
    chat_model = ChatModel()

    if request.method == "POST":
        # Obtén la pregunta del usuario desde la solicitud POST
        user_question = request.POST.get("user_question")

        # Inicializa el modelo y crea el KDTree (esto debe hacerse una sola vez)
        chat_model.initialize_openai()
        chat_model.create_dataframe()
        chat_model.create_kdtree()

        # Obten la respuesta utilizando el modelo
        response = chat_model.ask(user_question)

        # Devuelve la respuesta como JSON
        return JsonResponse({"response": response})

    return render(request, 'chat_page.html')