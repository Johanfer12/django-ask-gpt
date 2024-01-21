from django.contrib import admin
from django.urls import path
from askgpt.views import chat_page, ProcessFilesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', chat_page, name='chat_page'),
    path('process_files/', ProcessFilesView.as_view(), name='process_files'),
]