from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from vaccine.models import Vaccine
from vaccine.forms import VaccineCreateForm, VaccineUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.utils.decorators import method_decorator


class VaccineCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Creates a new vaccine
    """
    model = Vaccine
    form_class = VaccineCreateForm
    template_name = "vaccine/vaccine-create.html"
    permission_required = ('vaccine.add_vaccine',)
    success_url = reverse_lazy("vaccine:vaccine-list")
    success_message = "%(name)s was created successfully"


class VaccineUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Updates the vaccine
    """
    model = Vaccine
    form_class = VaccineUpdateForm
    template_name = "vaccine/vaccine-update.html"
    permission_required = ("vaccine.change_vaccine",)
    success_url = reverse_lazy("vaccine:vaccine-list")
    success_message = "%(name)s was updated successfully"


@method_decorator(cache_page(60*15), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class VaccineListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    List all the vaccines
    """
    model = Vaccine
    template_name = "vaccine/vaccine-list.html"
    permission_required = ("vaccine.view_vaccine",)
    paginate_by = 10
    ordering = ["name"]


@method_decorator(cache_page(60*15), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class VaccineDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Returns the details of given vaccine
    """
    model = Vaccine
    template_name = "vaccine/vaccine-detail.html"
    permission_required = ("vaccine.view_vaccine",)


class VaccineDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Deletes the vaccine
    """
    model = Vaccine
    template_name = "vaccine/vaccine-delete.html"
    permission_required = ("vaccine.delete_vaccine",)
    success_url = reverse_lazy("vaccine:vaccine-list")
    success_message = "Deleted successfully"
