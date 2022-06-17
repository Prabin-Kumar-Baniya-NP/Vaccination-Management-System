from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from vaccine.models import Vaccine
from vaccine.forms import VaccineCreateForm, VaccineUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin


class VaccineCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    """
    Creates a new vaccine
    """
    model = Vaccine
    form_class = VaccineCreateForm
    template_name = "vaccine/vaccine-create.html"
    success_url = reverse_lazy("vaccine:vaccine-list")
    success_message = "%(name)s was created successfully"

    def test_func(self):
        return self.request.user.has_perm("vaccine.add_vaccine")


class VaccineUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Updates the vaccine
    """
    model = Vaccine
    form_class = VaccineUpdateForm
    template_name = "vaccine/vaccine-update.html"
    success_url = reverse_lazy("vaccine:vaccine-list")
    success_message = "%(name)s was updated successfully"

    def test_func(self):
        return self.request.user.has_perm("vaccine.change_vaccine")


class VaccineListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    List all the vaccines
    """
    model = Vaccine
    template_name = "vaccine/vaccine-list.html"
    paginate_by = 10
    ordering = ["name"]

    def test_func(self):
        return self.request.user.has_perm("vaccine.view_vaccine")


class VaccineDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Returns the details of given vaccine
    """
    model = Vaccine
    template_name = "vaccine/vaccine-detail.html"

    def test_func(self):
        return self.request.user.has_perm("vaccine.view_vaccine")


class VaccineDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """
    Deletes the vaccine
    """
    model = Vaccine
    template_name = "vaccine/vaccine-delete.html"
    success_url = reverse_lazy("vaccine:vaccine-list")
    success_message = "Deleted successfully"

    def test_func(self):
        return self.request.user.has_perm("vaccine.delete_vaccine")
