from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)
from vaccine.models import Vaccine
from vaccine.forms import VaccineCreateForm, VaccineUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class VaccineCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    """
    Creates a new vaccine
    """

    model = Vaccine
    form_class = VaccineCreateForm
    template_name = "vaccine/vaccine-create.html"
    permission_required = ("vaccine.add_vaccine",)
    success_url = reverse_lazy("vaccine:vaccine-list")
    success_message = "%(name)s was created successfully"


class VaccineUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    """
    Updates the vaccine
    """

    model = Vaccine
    form_class = VaccineUpdateForm
    template_name = "vaccine/vaccine-update.html"
    permission_required = ("vaccine.change_vaccine",)
    success_url = reverse_lazy("vaccine:vaccine-list")
    success_message = "%(name)s was updated successfully"


class VaccineListView(LoginRequiredMixin, ListView):
    """
    List all the vaccines
    """

    model = Vaccine
    template_name = "vaccine/vaccine-list.html"
    paginate_by = 10
    ordering = ["name"]


class VaccineDetailView(LoginRequiredMixin, DetailView):
    """
    Returns the details of given vaccine
    """

    model = Vaccine
    template_name = "vaccine/vaccine-detail.html"


class VaccineDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView
):
    """
    Deletes the vaccine
    """

    model = Vaccine
    template_name = "vaccine/vaccine-delete.html"
    permission_required = ("vaccine.delete_vaccine",)
    success_url = reverse_lazy("vaccine:vaccine-list")
    success_message = "Deleted successfully"
