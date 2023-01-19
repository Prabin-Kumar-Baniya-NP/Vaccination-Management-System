import datetime
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView
from vaccination.models import Slot, Vaccination, Campaign
from django.urls import reverse
from vaccination.forms import VaccinationForm
from vaccine.models import Vaccine
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from vaccination.utils import generate_pdf
from django.views import View

User = get_user_model()


class ChooseVaccine(LoginRequiredMixin, ListView):
    """
    Lists all the vaccine
    """
    model = Vaccine
    template_name = "vaccination/choose-vaccine.html"
    paginate_by = 10
    ordering = ["name"]

    def get_queryset(self):
        return super().get_queryset().only("name", "number_of_doses", "interval")


class ChooseCampaign(LoginRequiredMixin, ListView):
    """
    Lists all the campaign
    """
    model = Campaign
    template_name = "vaccination/choose-campaign.html"
    paginate_by = 10
    ordering = "start_date"

    def get_queryset(self):
        return super().get_queryset().filter(vaccine=self.kwargs["vaccine_id"]).only("center", "start_date", "end_date").select_related("center")


class ChooseSlot(LoginRequiredMixin, ListView):
    """
    Lists all the campaign
    """
    model = Slot
    template_name = "vaccination/choose-slot.html"
    paginate_by = 10
    ordering = "date"

    def get_queryset(self):
        return super().get_queryset().filter(campaign=self.kwargs["campaign_id"], date__gte=datetime.date.today()).select_related("campaign")


class ConfirmVaccination(View):
    form_class = VaccinationForm

    def get(self, request, *args, **kwargs):
        campaign = Campaign.objects.select_related(
            "center", "vaccine").get(id=self.kwargs["campaign_id"])
        slot = Slot.objects.only("date", "start_time", "end_time").get(
            id=self.kwargs["slot_id"])
        form = self.form_class(
            initial={"patient": request.user, "campaign": campaign, "slot": slot})
        context = {
            "patient": request.user,
            "campaign": campaign,
            "slot": slot,
            "form": form,
            "checks": Vaccination.check_eligibility(request.user, campaign, slot)
        }
        return render(request, "vaccination/confirm-vaccination.html", context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        # Check form is valid
        if form.is_valid():
            # Check the restriction for new vaccination
            checks = Vaccination.check_eligibility(
                request.user, form.cleaned_data["campaign"], form.cleaned_data["slot"])
            if len(checks.keys()) == 0:
                # Reserve the vaccine
                is_reserved = Slot.reserve_vaccine(
                    self.kwargs["campaign_id"], self.kwargs["slot_id"])
                if is_reserved:
                    form.save()
                    return render(request, "vaccination/schedule-success.html", {})
                else:
                    return HttpResponse("Sorry! We are unable to reserve vaccine for you at this moment")
            else:
                messages.error(request, f"{checks}")
                raise PermissionDenied()
        else:
            return HttpResponseBadRequest(f"{form.errors}")


class RegistrationList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Lists all the vaccination registration for given vaccination campaign
    """
    model = Vaccination
    template_name = "vaccination/registration-list.html"
    paginate_by = 10
    permission_required = ("vaccination.view_vaccination", )

    def get_queryset(self):
        return Vaccination.objects.filter(campaign=self.kwargs["campaign_id"]).select_related("patient", "campaign", "slot").order_by("-id")


class VaccinationList(LoginRequiredMixin, ListView):
    """
    Lists all the vaccination registration done by the user
    """
    model = Vaccination
    template_name = "vaccination/vaccination-list-patient.html"
    paginate_by = 10

    def get_queryset(self):
        return Vaccination.objects.filter(patient=self.request.user).prefetch_related("patient", "campaign", "slot").order_by("-id")


class VaccinationDetail(LoginRequiredMixin, DetailView):
    """
    Returns the details of vaccination registration
    """
    model = Vaccination
    template_name = "vaccination/vaccination-detail.html"

    def get_queryset(self):
        if self.request.user.has_perm("vaccination.view_vaccination"):
            return super().get_queryset().select_related("patient", "campaign", "slot")
        else:
            return super().get_queryset().filter(patient=self.request.user).select_related("patient", "campaign", "slot")


@login_required
def approve_vaccination(request, vaccination_id):
    """
    Approves the vaccination of patient
    """
    if request.user.has_perm("vaccination.change_vaccination"):
        vaccination = Vaccination.objects.only("campaign",
                                               "is_vaccinated", "updated_by").get(id=vaccination_id)
        if request.user in vaccination.campaign.agents.all():
            if vaccination.is_vaccinated:
                messages.info(request, "Vaccination is already Approved")
                return HttpResponseRedirect(reverse("vaccination:vaccination-detail", kwargs={"pk": vaccination_id}))
            else:
                vaccination.is_vaccinated = True
                vaccination.date = datetime.date.today()
                vaccination.updated_by = User.objects.get(id=request.user.id)
                vaccination.save()
                messages.success(request, "Vaccination approved successfully")
                return HttpResponseRedirect(reverse("vaccination:vaccination-detail", kwargs={"pk": vaccination_id}))
        else:
            messages.error(
                request, "You are not assigned to approve this vaccination")
        raise PermissionDenied()
    else:
        messages.error(
            request, "You don't have permission to approve vaccination")
        raise PermissionDenied()


@login_required
def appointment_letter(request, vaccination_id):
    vaccination = Vaccination.objects.select_related(
        "patient", "campaign", "slot").get(id=vaccination_id)
    context = {
        "pdf_title": f"{vaccination.patient.get_full_name() } | Vaccination Appointment Letter",
        "date": str(datetime.datetime.now()),
        "title": "Appointment Letter",
        "subtitle": "To Whom It May Concern",
        "content": f"This is to inform that the {vaccination.campaign.vaccine.name } vaccination of Mr/Ms/Mrs {vaccination.patient.get_full_name() } is scheduled on { vaccination.slot.date }, { vaccination.slot.start_time } at { vaccination.campaign.center.name }.",
    }
    return generate_pdf(context)


@login_required
def vaccine_certificate(request, vaccination_id):
    vaccination = Vaccination.objects.select_related(
        "patient", "campaign", "slot").get(id=vaccination_id)
    if vaccination.is_vaccinated:
        context = {
            "pdf_title": f"{vaccination.patient.get_full_name() } | Vaccine Certificate",
            "date": str(datetime.datetime.now()),
            "title": "Vaccine Certificate",
            "subtitle": "To Whom It May Concern",
            "content": f"This is to certify that Mr/Ms/Mrs {vaccination.patient.get_full_name() } has successfuly taken {vaccination.campaign.vaccine.name } vaccine on {vaccination.date}. The vaccination was scheduled on { vaccination.slot.date } { vaccination.slot.start_time } at { vaccination.campaign.center.name } and it was approved by { vaccination.updated_by.get_full_name() }.",
        }
        return generate_pdf(context)
    else:
        return HttpResponse("User Not Vaccinated")
