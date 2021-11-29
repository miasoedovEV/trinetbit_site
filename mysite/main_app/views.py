from django.shortcuts import render


def about_project_view(request):
    return render(request, 'about_project.html', {'title': 'Trinetbit'})


def faq_view(request):
    return render(request, 'faq.html', {'title': 'Trinetbit'})


def index_view(request):
    return render(request, 'index.html', {'title': 'Trinetbit'})


def view_404(request):
    return render(request, '404.html', {'title': 'error'})


def view_private_policity(request):
    return render(request, 'private_policity.html', {'title': 'Trinetbit'})


def view_eula(request):
    return render(request, 'eula.html', {'title': 'Trinetbit'})


def view_guide(request):
    return render(request, 'guide.html', {'title': 'Trinetbit'})

# Create your views here.
