from django.shortcuts import render
 
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView

from django.urls import reverse_lazy
from .models import Reloj, Sensor, Interruptor, Regla, Evento

class HomeView(TemplateView):
    template_name = 'home.html'

class AddRelojView(CreateView):
    model = Reloj
    fields = ['publicId']
    success_url = reverse_lazy('home')
    template_name = 'add_reloj.html'

class AddSensorView(CreateView):
    model = Sensor
    fields = ['publicId']
    success_url = reverse_lazy('home')
    template_name = 'add_sensor.html'

class AddInterruptorView(CreateView):
    model = Interruptor
    fields = ['publicId', 'state']
    success_url = reverse_lazy('home')
    template_name = 'add_interruptor.html'

class ListRelojesView(ListView):
    model = Reloj
    context_object_name = 'reloj_list'
    template_name = 'reloj_listing.html'

    def get_queryset(self):
        return Reloj.objects.all()

class RelojDetailView(DetailView):
    model = Reloj
    template_name = 'reloj_detail.html'

class ListInterruptoresView(ListView):
    model = Interruptor
    context_object_name = 'interruptor_list'
    template_name = 'interruptor_listing.html'

    def get_queryset(self):
        return Interruptor.objects.all()

class InterruptorDetailView(DetailView):
    model = Interruptor
    template_name = 'interruptor_detail.html'

class ListSensoresView(ListView):
    model = Sensor
    context_object_name = 'sensor_list'
    template_name = 'sensor_listing.html'

    def get_queryset(self):
        return Sensor.objects.all()

class SensorDetailView(DetailView):
    model = Sensor
    template_name = 'sensor_detail.html'

class RelojRemoveView(DeleteView):
    model = Reloj
    template_name = "reloj_remove.html"

    def get_success_url(self):
        return reverse('list_relojes')
    
class InterruptorRemoveView(DeleteView):
    model = Interruptor
    template_name = "interruptor_remove.html"

    def get_success_url(self):
        return reverse('list_interruptores')
    
class SensorRemoveView(DeleteView):
    model = Sensor
    template_name = "sensor_remove.html"

    def get_success_url(self):
        return reverse('list_sensores')
    
class AddReglaView(CreateView):
    model = Regla
    fields = ['regla']
    success_url = reverse_lazy('home')
    template_name = 'add_regla.html'

class ListReglasView(ListView):
    model = Regla
    context_object_name = 'regla_list'
    template_name = 'regla_listing.html'

    def get_queryset(self):
        return Regla.objects.all()

class ReglaRemoveView(DeleteView):
    model = Regla
    template_name = "regla_remove.html"

    def get_success_url(self):
        return reverse('list_reglas')

class ListEventosView(ListView):
    model = Evento
    context_object_name = 'evento_list'
    template_name = 'evento_listing.html'

    def get_queryset(self):
        return Evento.objects.all()

from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django import forms

class RelojForm(forms.ModelForm):
    class Meta:
        model = Reloj
        fields = ['publicId']

class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ['publicId']

class InterruptorForm(forms.ModelForm):
    class Meta:
        model = Interruptor
        fields = ['publicId', 'state']

class ReglaForm(forms.ModelForm):
    class Meta:
        model = Regla
        fields = ['regla']

class RelojUpdateView(UpdateView):
    model = Reloj
    form_class = RelojForm
    template_name = 'reloj_update_form.html'
    success_url = reverse_lazy('list_relojes')

class SensorUpdateView(UpdateView):
    model = Sensor
    form_class = SensorForm
    template_name = 'sensor_update_form.html'
    success_url = reverse_lazy('list_sensores')

class InterruptorUpdateView(UpdateView):
    model = Interruptor
    form_class = InterruptorForm
    template_name = 'interruptor_update_form.html'
    success_url = reverse_lazy('list_interruptores')

class ReglaUpdateView(UpdateView):
    model = Regla
    form_class = ReglaForm
    template_name = 'regla_update_form.html'
    success_url = reverse_lazy('list_reglas')