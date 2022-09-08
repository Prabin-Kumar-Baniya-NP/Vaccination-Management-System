import datetime
import io
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView
from vaccination.models import Slot, Vaccination, Campaign
from django.urls import reverse
from vaccination.forms import VaccinationForm
from vaccine.models import Vaccine
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, HttpResponseForbidden
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle

User = get_user_model()


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


class VaccinationListOfPatient(LoginRequiredMixin, ListView):
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
def choose_vaccine(request):
    """
    Handles the vaccine choose part of vaccination registration
    """
    context = {
        "vaccine_list": Vaccine.objects.all().only("name", "number_of_doses", "interval"),
    }
    return render(request, "vaccination/choose-vaccine.html", context)


@login_required
def choose_campaign(request, vaccine_id):
    """
    Handles the choose vaccination campaign part of vaccination registration
    """
    context = {
        "campaign_list": Campaign.objects.filter(vaccine=vaccine_id).only("center", "start_date", "end_date").select_related("center")
    }
    return render(request, "vaccination/choose-campaign.html", context)


@login_required
def choose_slot(request, campaign_id):
    """
    Lists all the slot for given vaccination campaign to choose for vaccination registration
    """
    context = {
        "slot_list": Slot.objects.filter(campaign=campaign_id, date__gte=datetime.date.today()).select_related("campaign")
    }
    return render(request, "vaccination/choose-slot.html", context)


@login_required
@transaction.atomic
def confirm_vaccination(request, campaign_id, slot_id):
    """
    Handles the final vaccination registration request
    """
    if request.method == "POST":
        form = VaccinationForm(request.POST)
        if form.is_valid():
            checks = Vaccination.check_eligibility(
                request.user, form.cleaned_data["campaign"], form.cleaned_data["slot"])
            if len(checks.keys()) == 0:
                if Slot.reserve_vaccine(campaign_id, slot_id):
                    form.save()
                    return render(request, "vaccination/schedule-success.html", {})
                else:
                    return HttpResponseForbidden("Sorry! We are unable to reserve vaccine for you. Please Try Scheduling the vaccination again")
            else:
                messages.error(request, f"{checks}")
                return HttpResponseForbidden(f"{checks}")
        else:
            return HttpResponseForbidden(f"{form.errors}")
    else:
        campaign = Campaign.objects.select_related(
            "center", "vaccine").get(id=campaign_id)
        slot = Slot.objects.only("date", "start_time",
                                 "end_time").get(id=slot_id)
        form = VaccinationForm(
            initial={"patient": request.user, "campaign": campaign, "slot": slot})
        context = {
            "patient": request.user,
            "campaign": campaign,
            "slot": slot,
            "form": form,
            "checks": Vaccination.check_eligibility(request.user, campaign, slot)
        }
        return render(request, "vaccination/confirm-vaccination.html", context)


@login_required
@transaction.atomic
def approve_vaccination(request, vaccination_id):
    """
    Approves the vaccination of patient
    """
    if request.user.has_perm("vaccination.change_vaccination"):
        vaccination = Vaccination.objects.only("campaign",
                                               "is_vaccinated", "updated_by").get(id=vaccination_id)
        if request.user in vaccination.campaign.agents.all():
            vaccination.is_vaccinated = True
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
def vaccine_certificate(request, vaccination_id):
    vaccination = Vaccination.objects.select_related(
        "patient", "campaign", "slot").get(id=vaccination_id)
    dose_number = Vaccination.get_dose_number(
        request.user, vaccination.campaign.vaccine)
    context = {
        "pdf_title": f"{vaccination.patient.get_full_name() } | Vaccine Certificate",
        "date": str(datetime.datetime.now()),
        "title": "Vaccine Certificate",
        "subtitle": "To Whom It May Concern",
        "content": f"This is to certify that Mr/Ms/Mrs {vaccination.patient.get_full_name() } has successfuly completed dose {dose_number} of {vaccination.campaign.vaccine.name }. The vaccination was scheduled on { vaccination.slot.date }, { vaccination.slot.start_time } at { vaccination.campaign.center.name } and it was approved by { vaccination.updated_by.get_full_name() }.",
    }
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setTitle(context["pdf_title"])
    # Write the date
    p.drawString(40, 800, context["date"])
    # Draw a line
    p.line(20, 795, 570, 795)
    # Write the title
    p.setFont('Helvetica-Bold', 14)
    p.drawCentredString(300, 750, context["title"])
    # Write the subtitle
    p.setFont('Helvetica', 12)
    p.drawCentredString(300, 700, context["subtitle"])
    # Write the paragraph style
    para_style = ParagraphStyle(
        "paraStyle", fontSize=14, leading=20, firstLineIndent=25)
    # Write the paragraph
    para = Paragraph(context["content"], para_style)
    para.wrapOn(p, 500, 200)  # dimension of paragraph (width, height)
    para.drawOn(p, 40, 600)  # location of paragraph (x, y)
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=context["pdf_title"])
