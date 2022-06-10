from user.models import User
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from vaccination.models import Slot, Vaccination, Vaccination_Campaign
from django.urls import reverse_lazy, reverse
from vaccination.forms import CampaignCreateForm, CampaignUpdateForm, SlotCreateForm, SlotUpdateForm, VaccinationForm
from vaccine.models import Vaccine
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from vaccination.utils import reserve_vaccine
from django.db import transaction
import datetime


class CampaignCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Vaccination_Campaign
    form_class = CampaignCreateForm
    template_name = "vaccination/campaign/campaign-create.html"
    success_url = reverse_lazy("vaccination:campaign-list")

    def test_func(self):
        return self.request.user.has_perm("vaccination.add_vaccination_campaign")


class CampaignUpdateForm(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vaccination_Campaign
    form_class = CampaignUpdateForm
    template_name = "vaccination/campaign/campaign-update.html"
    success_url = reverse_lazy("vaccination:campaign-list")

    def test_func(self):
        return self.request.user.has_perm("vaccination.change_vaccination_campaign")


class CampaignListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Vaccination_Campaign
    template_name = "vaccination/campaign/campaign-list.html"

    def test_func(self):
        return self.request.user.has_perm("vaccination.view_vaccination_campaign")


class CampaignDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Vaccination_Campaign
    template_name = "vaccination/campaign/campaign-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["registration"] = Vaccination.objects.filter(
            campaign=self.kwargs["pk"]).count()
        return context

    def test_func(self):
        return self.request.user.has_perm("vaccination.view_vaccination_campaign")


class CampaignDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vaccination_Campaign
    template_name = "vaccination/campaign/campaign-delete.html"
    success_url = reverse_lazy("vaccination:campaign-list")

    def test_func(self):
        return self.request.user.has_perm("vaccination.delete_vaccination_campaign")


class SlotCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Slot
    form_class = SlotCreateForm
    template_name = "vaccination/slot/slot-create.html"
    success_url = reverse_lazy("vaccination:slot-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["campaign_id"] = self.kwargs["campaign_id"]
        return kwargs
    
    def get_success_url(self) -> str:
        return reverse_lazy("vaccination:slot-list", kwargs={"campaign_id": self.kwargs["campaign_id"]})

    def test_func(self):
        return self.request.user.has_perm("vaccination.add_slot")


class SlotUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Slot
    form_class = SlotUpdateForm
    template_name = "vaccination/slot/slot-update.html"
    success_url = reverse_lazy("vaccination:slot-list")

    def test_func(self):
        return self.request.user.has_perm("vaccination.change_slot")


class SlotListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Slot
    template_name = "vaccination/slot/slot-list.html"
    success_url = reverse_lazy("vaccination:slot-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Slot.objects.filter(campaign=self.kwargs["campaign_id"])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["campaign_id"] = self.kwargs["campaign_id"]
        return context

    def test_func(self):
        return self.request.user.has_perm("vaccination.view_slot")


class SlotDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Slot
    template_name = "vaccination/slot/slot-detail.html"

    def test_func(self):
        return self.request.user.has_perm("vaccination.view_slot")


class SlotDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Slot
    template_name = "vaccination/slot/slot-delete.html"
    success_url = reverse_lazy("vaccination:slot-list")

    def test_func(self):
        return self.request.user.has_perm("vaccination.delete_slot")


@login_required
def choose_vaccine(request):
    context = {
        "vaccine_list": Vaccine.objects.all().only("name", "description"),
    }
    return render(request, "vaccination/choose-vaccine.html", context)


@login_required
def check_dose(request, vaccine_id):
    patient = User.objects.get(id=request.user.id)
    vaccine = Vaccine.objects.get(id=vaccine_id)
    dose_taken = Vaccination.get_dose_number(patient, vaccine)
    if dose_taken < vaccine.number_of_doses:
        return HttpResponseRedirect(reverse("vaccination:choose-campaign", kwargs={"vaccine_id": vaccine_id}))
    else:
        return render(request, "vaccination/dose-information.html", {"dose_taken": dose_taken, "dose_required": vaccine.number_of_doses})


@login_required
def choose_campaign(request, vaccine_id):
    context = {
        "campaign_list": Vaccination_Campaign.objects.filter(vaccine=vaccine_id)
    }
    return render(request, "vaccination/choose-campaign.html", context)


@login_required
def choose_slot(request, campaign_id):
    context = {
        "slot_list": Slot.objects.filter(campaign=campaign_id, date__gte=datetime.date.today())
    }
    return render(request, "vaccination/choose-slot.html", context)


@login_required
@transaction.atomic
def confirm_vaccination(request, campaign_id, slot_id):
    if request.method == "POST":
        form = VaccinationForm(request.POST)
        if form.is_valid():
            if reserve_vaccine(slot_id):
                form.save()
                return render(request, "vaccination/schedule-success.html", {})
            else:
                return HttpResponse("Sorry! We are unable to reserve vaccine for you. Please Try Scheduling the vaccination again")
        else:
            return HttpResponse("Unable to process your request! Please enter correct data")
    else:
        patient = User.objects.get(id=request.user.id)
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


class VaccinationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Vaccination
    template_name = "vaccination/vaccination-list.html"

    def get_queryset(self):
        return Vaccination.objects.filter(campaign=self.kwargs["campaign_id"])

    def test_func(self):
        return self.request.user.has_perm("vaccination.view_vaccination_campaign")


class VaccinationListViewForPatient(LoginRequiredMixin, ListView):
    model = Vaccination
    template_name = "vaccination/vaccination-list-patient.html"

    def get_queryset(self):
        return Vaccination.objects.filter(patient=User.objects.get(id=self.request.user.id))


class VaccinationDetailView(LoginRequiredMixin, DetailView):
    model = Vaccination
    template_name = "vaccination/vaccination-detail.html"


@login_required
@transaction.atomic
def approve_vaccination(request, vaccination_id):
    vaccination = Vaccination.objects.get(id=vaccination_id)
    vaccination.is_vaccinated = True
    vaccination.updated_by = User.objects.get(user=request.user.id)
    vaccination.save()
    return HttpResponseRedirect(reverse("vaccination:vaccination-detail", kwargs={"pk": vaccination_id}))
