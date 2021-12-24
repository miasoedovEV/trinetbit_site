from django.urls import path
from .views import *

urlpatterns = [
    path('project', about_project_view, name='project'),
    path('faq', faq_view, name='faq'),
    path('index', index_view, name='index'),
    path('Confidentiality', view_private_policity, name='private_policity'),
    path('EULA', view_eula, name='eula'),
    path('guide', view_guide, name='guide'),
]

handler404 = view_404
handler500 = view_500

