from re import template
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from vaccination.models import Slot, Vaccination, Vaccination_Campaign
from django.urls import reverse_lazy, reverse
from vaccination.forms import CampaignCreateForm, CampaignUpdateForm, SlotCreateForm, SlotUpdateForm, VaccinationForm
from vaccine.models import Vaccine
from django.shortcuts import render
from user.models import Patient
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from user.models import Admin
import datetime


class CampaignCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Vaccination_Campaign
    form_class = CampaignCreateForm
    template_name = "vaccination/campaign-create.html"
    success_url = reverse_lazy("vaccination:campaign-list")

    def test_func(self):
        return self.request.user.is_admin()


class CampaignUpdateForm(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vaccination_Campaign
    form_class = CampaignUpdateForm
    template_name = "vaccination/campaign-update.html"
    success_url = reverse_lazy("vaccination:campaign-list")

    def test_func(self):
        return self.request.user.is_admin()


class CampaignListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Vaccination_Campaign
    template_name = "vaccination/campaign-list.html"

    def test_func(self):
        return self.request.user.is_admin()


class CampaignDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Vaccination_Campaign
    template_name = "vaccination/campaign-detail.html"

    def test_func(self):
        return self.request.user.is_admin() or self.request.user.is_agent()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vaccination_list"] = Vaccination.objects.filter(campaign = self.kwargs["pk"])
        return context


class CampaignDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vaccination_Campaign
    template_name = "vaccination/campaign-delete.html"
    success_url = reverse_lazy("vaccination:campaign-list")

    def test_func(self):
        return self.request.user.is_admin()


class SlotCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Slot
    form_class = SlotCreateForm
    template_name = "vaccination/slot-create.html"
    success_url = reverse_lazy("vaccination:slot-list")

    def test_func(self):
        return self.request.user.is_admin()


class SlotUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Slot
    form_class = SlotUpdateForm
    template_name = "vaccination/slot-update.html"
    success_url = reverse_lazy("vaccination:slot-list")

    def test_func(self):
        return self.request.user.is_admin()


class SlotListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Slot
    template_name = "vaccination/slot-list.html"
    success_url = reverse_lazy("vaccination:slot-list")

    def test_func(self):
        return self.request.user.is_admin()


class SlotDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Slot
    template_name = "vaccination/slot-detail.html"

    def test_func(self):
        return self.request.user.is_admin()


class SlotDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Slot
    template_name = "vaccination/slot-delete.html"
    success_url = reverse_lazy("vaccination:slot-list")

    def test_func(self):
        return self.request.user.is_admin()


def choose_vaccine(request):
    context = {
        "vaccine_list": Vaccine.objects.all().only("name", "description"),
        "eligible_vaccine": Vaccine.get_eligible_vaccine(user=request.user)
    }
    return render(request, "vaccination/choose-vaccine.html", context)


def check_dose(request, vaccine_id):
    patient = Patient.objects.get(user=request.user)
    vaccine = Vaccine.objects.get(id=vaccine_id)
    dose_taken = Vaccination.get_dose_number(patient, vaccine)
    if dose_taken < vaccine.number_of_doses:
        return HttpResponseRedirect(reverse("vaccination:choose-campaign", kwargs={"vaccine_id": vaccine_id}))
    else:
        return render(request, "vaccination/dose-information.html", {"dose_taken": dose_taken, "dose_required": vaccine.number_of_doses})


def choose_campaign(request, vaccine_id):
    context = {
        "campaign_list": Vaccination_Campaign.objects.filter(vaccine=vaccine_id)
    }
    return render(request, "vaccination/choose-campaign.html", context)


def choose_slot(request, campaign_id):
    context = {
        "slot_list": Slot.objects.filter(campaign=campaign_id, date__gte=datetime.date.today())
    }
    return render(request, "vaccination/choose-slot.html", context)


def confirm_vaccination(request, campaign_id, slot_id):
    if request.method == "POST":
        form = VaccinationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "vaccination/schedule-success.html", {})
    else:
        patient = Patient.objects.get(user=request.user)
        campaign = Vaccination_Campaign.objects.get(id=campaign_id)
        slot = Slot.objects.get(id=slot_id)
        form = VaccinationForm(
            initial={"patient": patient, "campaign": campaign, "slot": slot})
        context = {
            "patient": patient,
            "campaign": campaign,
            "slot": slot,
            "form": form
        }
        return render(request, "vaccination/confirm-vaccination.html", context)


class VaccinationListView(LoginRequiredMixin, ListView):
    model = Vaccination
    template_name = "vaccination/vaccination-list.html"

    def get_queryset(self):
        return Vaccination.objects.filter(patient=Patient.objects.get(user=self.request.user.id))


class VaccinationDetailView(LoginRequiredMixin, DetailView):
    model = Vaccination
    template_name = "vaccination/vaccination-detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(patient=Patient.objects.get(user=self.request.user.id))
