from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from center.models import Center, Storage
from center.forms import CreateCenterForm, UpdateCenterForm, CreateStorageForm, UpdateStorageForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from user.models import Admin


class CreateCenter(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Center
    form_class = CreateCenterForm
    template_name = "center/center-create.html"
    success_url = reverse_lazy("center:center-list")

    def test_func(self):
        return self.request.user.is_admin()


class CenterList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Center
    template_name = "center/center-list.html"

    def test_func(self):
        return self.request.user.is_admin() or self.request.user.is_agent()


class CenterDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Center
    template_name = "center/center-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["storage_list"] = Storage.objects.filter(
            center=self.kwargs["pk"])
        return context

    def test_func(self):
        return self.request.user.is_admin() or self.request.user.is_agent()


class CenterDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Center
    template_name = "center/center-delete.html"
    success_url = reverse_lazy("center:center-list")

    def test_func(self):
        return self.request.user.is_admin()


class CenterUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Center
    form_class = UpdateCenterForm
    template_name = "center/center-update.html"
    success_url = reverse_lazy("center:center-list")

    def test_func(self):
        return self.request.user.is_admin()


class CreateStorage(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Storage
    form_class = CreateStorageForm
    template_name = "storage/storage-create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["center_id"] = self.kwargs["pk"]
        return kwargs

    def get_success_url(self):
        return reverse("center:storage-list", kwargs={"center_id": self.kwargs["pk"]})

    def test_func(self):
        return self.request.user.is_admin()


class StorageList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Storage
    template_name = "storage/storage-list.html"

    def get_queryset(self):
        return super().get_queryset().filter(center=self.kwargs["center_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["center_id"] = self.kwargs["center_id"]
        return context

    def test_func(self):
        return self.request.user.is_admin() or self.request.user.is_agent()


class StorageDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Storage
    template_name = "storage/storage-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_quantity"] = self.get_object(
        ).total_quantity - self.get_object().booked_quantity
        return context

    def test_func(self):
        return self.request.user.is_admin() or self.request.user.is_agent()


class StorageDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Storage
    template_name = "storage/storage-delete.html"

    def get_success_url(self):
        return reverse("center:storage-list", kwargs={"center_id": self.get_object().center.id})

    def test_func(self):
        return self.request.user.is_admin()


class StorageUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Storage
    form_class = UpdateStorageForm
    template_name = "storage/storage-update.html"

    def get_success_url(self):
        return reverse("center:storage-list", kwargs={"center_id": self.get_object().center.id})

    def test_func(self):
        return self.request.user.is_admin()
