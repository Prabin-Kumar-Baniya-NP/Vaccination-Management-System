from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from vaccine.models import Vaccine
from vaccine.forms import VaccineCreateForm, VaccineUpdateForm
from django.urls import reverse_lazy


class VaccineCreateView(CreateView):
    model = Vaccine
    form_class = VaccineCreateForm
    template_name = "vaccine/vaccine-create.html"
    success_url = reverse_lazy("vaccine:vaccine-list")


class VaccineUpdateView(UpdateView):
    model = Vaccine
    form_class = VaccineUpdateForm
    template_name = "vaccine/vaccine-update.html"
    success_url = reverse_lazy("vaccine:vaccine-list")


class VaccineListView(ListView):
    model = Vaccine
    template_name = "vaccine/vaccine-list.html"


class VaccineDetailView(DetailView):
    model = Vaccine
    template_name = "vaccine/vaccine-detail.html"


class VaccineDeleteView(DeleteView):
    model = Vaccine
    template_name = "vaccine/vaccine-delete.html"
    success_url = reverse_lazy("vaccine:vaccine-list")
