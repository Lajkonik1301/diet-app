from django.shortcuts import render

def index(request):
    return render(request, 'core/index.html')

def login_page(request):
    return render(request, 'core/login_page.html')
