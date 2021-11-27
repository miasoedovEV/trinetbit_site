from django.shortcuts import render


def about_project_view(request):
    return render(request, 'about_project.html')


def faq_view(request):
    return render(request, 'faq.html')


def index_view(request):
    return render(request, 'index.html', {'title': 'Trinetbit'})


def view_404(request):
    return render(request, '404.html', {'title': 'error'})

# Create your views here.
