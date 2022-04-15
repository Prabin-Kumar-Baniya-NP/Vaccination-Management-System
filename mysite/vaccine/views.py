from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from vaccine.models import Vaccine
from vaccine.forms import VaccineCreateForm, VaccineUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from user.models import Admin


class VaccineCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Vaccine
    form_class = VaccineCreateForm
    template_name = "vaccine/vaccine-create.html"
    success_url = reverse_lazy("vaccine:vaccine-list")

    def test_func(self):
        return self.request.user.is_admin()


class VaccineUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vaccine
    form_class = VaccineUpdateForm
    template_name = "vaccine/vaccine-update.html"
    success_url = reverse_lazy("vaccine:vaccine-list")

    def test_func(self):
        return self.request.user.is_admin()


class VaccineListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Vaccine
    template_name = "vaccine/vaccine-list.html"

    def test_func(self):
        return self.request.user.is_admin()


class VaccineDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Vaccine
    template_name = "vaccine/vaccine-detail.html"

    def test_func(self):
        return self.request.user.is_admin()


class VaccineDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vaccine
    template_name = "vaccine/vaccine-delete.html"
    success_url = reverse_lazy("vaccine:vaccine-list")

    def test_func(self):
        return self.request.user.is_admin()
