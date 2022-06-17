from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from center.models import Center, Storage
from center.forms import CreateCenterForm, UpdateCenterForm, CreateStorageForm, UpdateStorageForm
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


class CreateCenter(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    """
    Creates a new center
    """
    model = Center
    form_class = CreateCenterForm
    template_name = "center/center-create.html"
    success_url = reverse_lazy("center:center-list")
    success_message = "Center Created Successfully"

    def test_func(self):
        return self.request.user.has_perm("center.add_center")


class CenterList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    List all the center
    """
    model = Center
    template_name = "center/center-list.html"
    paginate_by = 10
    ordering = ["-name"]

    def test_func(self):
        return self.request.user.has_perm("center.view_center")


class CenterDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Returns the details of given center
    """
    model = Center
    template_name = "center/center-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["storage_list"] = Storage.objects.filter(
            center=self.kwargs["pk"])
        return context

    def test_func(self):
        return self.request.user.has_perm("center.view_center")


class CenterDelete(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """
    Deletes the given center
    """
    model = Center
    template_name = "center/center-delete.html"
    success_url = reverse_lazy("center:center-list")
    success_message = "Center Deleted Successfully"

    def test_func(self):
        return self.request.user.has_perm("center.delete_center")


class CenterUpdate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    For Updating the center information
    """
    model = Center
    form_class = UpdateCenterForm
    template_name = "center/center-update.html"
    success_url = reverse_lazy("center:center-list")
    success_message = "Center Updated Successfully"

    def test_func(self):
        return self.request.user.has_perm("center.change_center")


class CreateStorage(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    """
    Creates a new storage in the given center
    """
    model = Storage
    form_class = CreateStorageForm
    template_name = "storage/storage-create.html"
    success_message = "Storage Created Successfully"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["center_id"] = self.kwargs["center_id"]
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial["center"] = Center.objects.get(id=self.kwargs["center_id"])
        return initial

    def get_success_url(self):
        return reverse("center:storage-list", kwargs={"center_id": self.kwargs["center_id"]})

    def test_func(self):
        return self.request.user.has_perm("center.add_storage")


class StorageUpdate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    For updating the storage
    """
    model = Storage
    form_class = UpdateStorageForm
    template_name = "storage/storage-update.html"
    success_message = "Storage Updated Successfully"

    def get_success_url(self):
        return reverse("center:storage-list", kwargs={"center_id": self.get_object().center.id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["center_id"] = self.get_object().center.id
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial["center"] = Center.objects.get(id=self.get_object().center.id)
        return initial

    def test_func(self):
        return self.request.user.has_perm("center.change_storage")


class StorageList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    List all the storage of given center
    """
    model = Storage
    template_name = "storage/storage-list.html"
    paginate_by = 10
    ordering = ["id"]

    def get_queryset(self):
        return super().get_queryset().filter(center=self.kwargs["center_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["center_id"] = self.kwargs["center_id"]
        return context

    def test_func(self):
        return self.request.user.has_perm("center.view_storage")


class StorageDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Returns the details of given storage
    """
    model = Storage
    template_name = "storage/storage-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_quantity"] = self.get_object(
        ).total_quantity - self.get_object().booked_quantity
        return context

    def test_func(self):
        return self.request.user.has_perm("center.view_storage")


class StorageDelete(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """
    Deletes the given storage
    """
    model = Storage
    template_name = "storage/storage-delete.html"
    success_message = "Storage Deleted Successfully"

    def get_success_url(self):
        return reverse("center:storage-list", kwargs={"center_id": self.get_object().center.id})

    def test_func(self):
        return self.request.user.has_perm("center.delete_storage")
