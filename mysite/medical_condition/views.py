from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from medical_condition.models import Medical_Condition
from medical_condition.forms import MedicalConditionCreateForm, MedicalConditionUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class MedicalConditionCreateView(LoginRequiredMixin, CreateView):
    model = Medical_Condition
    form_class = MedicalConditionCreateForm
    template_name = "medical_condition/medical-condition-create.html"
    success_url = reverse_lazy("medical_condition:medical-condition-list")


class MedicalConditionUpdateView(LoginRequiredMixin, UpdateView):
    model = Medical_Condition
    form_class = MedicalConditionUpdateForm
    template_name = "medical_condition/medical-condition-update.html"
    success_url = reverse_lazy("medical_condition:medical-condition-list")


class MedicalConditionListView(LoginRequiredMixin, ListView):
    model = Medical_Condition
    template_name = "medical_condition/medical-condition-list.html"


class MedicalConditionDetailView(LoginRequiredMixin, DetailView):
    model = Medical_Condition
    template_name = "medical_condition/medical-condition-detail.html"


class MedicalConditionDeleteView(LoginRequiredMixin, DeleteView):
    model = Medical_Condition
    template_name = "medical_condition/medical-condition-delete.html"
    success_url = reverse_lazy("medical_condition:medical-condition-list")
