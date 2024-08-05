from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from enlaces.views import redireccionar_enlace, acortar_enlace, personalizar_enlace
from enlaces.views import analizar_enlace, api_documentacion

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/api/doc/'), name='redirect_api_doc'),
    path('api/doc/', api_documentacion, name='api_documentacion'),
    path('api/acortar/', acortar_enlace, name='acortar_enlace'),
    path('api/personalizar/', personalizar_enlace, name='personalizar_enlace'),
    path('api/analizar/<str:id_url_acortado>/', analizar_enlace, name='analizar_enlace'),
    path('<str:id_url_acortado>/', redireccionar_enlace, name='redireccionar_enlace'),
]
