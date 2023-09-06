"""p3redes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from sysdomotic.views import AddRelojView, AddSensorView, AddInterruptorView, HomeView, ListRelojesView, RelojDetailView, ListInterruptoresView, InterruptorDetailView, ListSensoresView, SensorDetailView,RelojRemoveView, InterruptorRemoveView,SensorRemoveView, ListEventosView
from sysdomotic.views import AddReglaView, ListReglasView, ReglaRemoveView
from sysdomotic.views import RelojUpdateView, SensorUpdateView, InterruptorUpdateView, ReglaUpdateView

from sysdomotic import views
from django.views.generic import RedirectView
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),

    path('services/', RedirectView.as_view(url='home/', permanent=False), name= 'index'),
    
    path('services/home/', HomeView.as_view(), name = 'home'),
    
    path('add/reloj/', AddRelojView.as_view(), name='add_reloj'),
    path('add/sensor/', AddSensorView.as_view(), name='add_sensor'),
    path('add/interruptor/', AddInterruptorView.as_view(), name='add_interruptor'),
    
    path('list/reloj/', ListRelojesView.as_view(), name = 'list_relojes'),
    path('reloj/<int:pk>', RelojDetailView.as_view(), name = 'reloj_detail'),

    path('list/interruptor/', ListInterruptoresView.as_view(), name = 'list_interruptores'),
    path('interruptor/<int:pk>', InterruptorDetailView.as_view(), name = 'interruptor_detail'),

    path('list/sensor/', ListSensoresView.as_view(), name = 'list_sensores'),
    path('sensor/<int:pk>', SensorDetailView.as_view(), name = 'sensor_detail'),

    path('reloj_remove/<int:pk>', RelojRemoveView.as_view(), name = 'remove_relojes'),
    path('interruptor_remove/<int:pk>', InterruptorRemoveView.as_view(), name = 'remove_interruptores'),
    path('sensor_remove/<int:pk>', SensorRemoveView.as_view(), name = 'remove_sensores'),

    path('add/regla/', AddReglaView.as_view(), name='add_regla'),
    path('list/regla/', ListReglasView.as_view(), name = 'list_reglas'),
    path('regla_remove/<int:pk>', ReglaRemoveView.as_view(), name = 'remove_reglas'),

    path('list/eventos/', ListEventosView.as_view(), name = 'list_eventos'),

    path('interruptorUpdate/<int:pk>', views.InterruptorUpdateView.as_view(),
         name='interruptor_update'),
        
    path('sensorUpdate/<int:pk>', views.SensorUpdateView.as_view(),
         name='sensor_update'),

    path('relojUpdate/<int:pk>', views.RelojUpdateView.as_view(),
         name='reloj_update'),
    
    path('reglaUpdate/<int:pk>', views.ReglaUpdateView.as_view(),
         name='regla_update'),

]



