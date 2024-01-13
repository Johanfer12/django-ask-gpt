# myapp/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import ChatModel
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chat_page(request):
    if request.method == "POST":
        user_question = request.POST.get("user_question")
        response = ChatModel.ask(user_question)
        return JsonResponse({"response": response})

    return render(request, 'chat_page.html')