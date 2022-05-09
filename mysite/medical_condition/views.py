from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from medical_condition.models import Medical_Condition
from medical_condition.forms import MedicalConditionCreateForm, MedicalConditionUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class MedicalConditionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Medical_Condition
    form_class = MedicalConditionCreateForm
    template_name = "medical_condition/medical-condition-create.html"
    success_url = reverse_lazy("medical_condition:list")

    def test_func(self):
        return self.request.user.is_admin()


class MedicalConditionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Medical_Condition
    form_class = MedicalConditionUpdateForm
    template_name = "medical_condition/medical-condition-update.html"
    success_url = reverse_lazy("medical_condition:list")

    def test_func(self):
        return self.request.user.is_admin()


class MedicalConditionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Medical_Condition
    template_name = "medical_condition/medical-condition-list.html"

    def test_func(self):
        return self.request.user.is_admin()


class MedicalConditionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Medical_Condition
    template_name = "medical_condition/medical-condition-detail.html"

    def test_func(self):
        return self.request.user.is_admin()


class MedicalConditionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Medical_Condition
    template_name = "medical_condition/medical-condition-delete.html"
    success_url = reverse_lazy("medical_condition:list")

    def test_func(self):
        return self.request.user.is_admin()
