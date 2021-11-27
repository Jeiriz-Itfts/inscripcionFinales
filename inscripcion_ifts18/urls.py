from django.urls import path
from . import views

# que la app sea modular, una app de inscripcion, otra puede ser reportes
app_name = 'inscripcion_ifts18'
urlpatterns = [
    path('',views.index,name='index'),
    path('reset/', views.reset, name='reset'),
    path('alumno/index/',views.check, name='check'),
    path('reseteado/',views.check_if_mail_exists_and_send_mail, name='check_if_mail_exists_and_send_mail'),
    path('logout/',views.logout, name='logout'),
    path('alumno/inscripcion/',views.inscripcionFinales, name='inscripcionFinales'),

]
