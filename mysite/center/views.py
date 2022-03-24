from pyexpat import model
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from center.models import Center, Storage
from center.forms import CreateCenterForm, UpdateCenterForm, CreateStorageForm, UpdateStorageForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

class CreateCenter(LoginRequiredMixin,CreateView):
    model = Center
    form_class = CreateCenterForm
    template_name = "center/center-create.html"
    success_url = reverse_lazy("center:center-list")


class CenterList(LoginRequiredMixin,ListView):
    model = Center
    template_name = "center/center-list.html"


class CenterDetail(LoginRequiredMixin,DetailView):
    model = Center
    template_name = "center/center-detail.html"


class CenterDelete(LoginRequiredMixin,DeleteView):
    model = Center
    template_name = "center/center-delete.html"
    success_url = reverse_lazy("center:center-list")


class CenterUpdate(LoginRequiredMixin,UpdateView):
    model = Center
    form_class = UpdateCenterForm
    template_name = "center/center-update.html"
    success_url = reverse_lazy("center:center-list")


class CreateStorage(LoginRequiredMixin,CreateView):
    model = Storage
    form_class = CreateStorageForm
    template_name = "storage/storage-create.html"

    def get_success_url(self):
        return reverse("center:storage-list", kwargs={"centerID": self.kwargs["pk"]})


class StorageList(LoginRequiredMixin,ListView):
    model = Storage
    template_name = "storage/storage-list.html"

    def get_queryset(self):
        return super().get_queryset().filter(center=self.kwargs["centerID"])


class StorageDetail(LoginRequiredMixin,DetailView):
    model = Storage
    template_name = "storage/storage-detail.html"

class StorageDelete(LoginRequiredMixin,DeleteView):
    model = Storage
    template_name = "storage/storage-delete.html"
    
    def get_success_url(self):
        return reverse("center:storage-list", kwargs={"centerID": self.get_object().center.id})


class StorageUpdate(LoginRequiredMixin,UpdateView):
    model = Storage
    form_class = UpdateStorageForm
    template_name = "storage/storage-update.html"

    def get_success_url(self):
        return reverse("center:storage-list", kwargs={"centerID": self.get_object().center.id})