from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from vaccination.models import Slot, Vaccination, Campaign
from django.urls import reverse_lazy
from campaign.forms import CampaignCreateForm, CampaignUpdateForm, SlotCreateForm, SlotUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.utils.decorators import method_decorator


class CampaignCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Creates a new vaccination campaign
    """
    model = Campaign
    form_class = CampaignCreateForm
    permission_required = ("campaign.add_campaign",)
    template_name = "campaign/campaign/campaign-create.html"
    success_url = reverse_lazy("campaign:campaign-list")
    success_message = "Campaign Created Successfully"


class CampaignUpdateForm(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Updates the vaccination campaign
    """
    model = Campaign
    form_class = CampaignUpdateForm
    permission_required = ("campaign.change_campaign",)
    template_name = "campaign/campaign/campaign-update.html"
    success_url = reverse_lazy("campaign:campaign-list")
    success_message = "Campaign Updated Successfully"


@method_decorator(cache_page(60*15), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class CampaignListView(LoginRequiredMixin, ListView):
    """
    Lists all the vaccination campaign
    """
    model = Campaign
    template_name = "campaign/campaign/campaign-list.html"
    paginate_by = 10
    ordering = ["-id"]


@method_decorator(cache_page(60*15), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class CampaignDetailView(LoginRequiredMixin, DetailView):
    """
    Returns the details of vaccination campaign
    """
    model = Campaign
    template_name = "campaign/campaign/campaign-detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related("center", "vaccine")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["registration"] = Vaccination.objects.filter(
            campaign=self.kwargs["pk"]).count()
        return context


class CampaignDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Deletes the vaccination campaign
    """
    model = Campaign
    template_name = "campaign/campaign/campaign-delete.html"
    permission_required = ("campaign.delete_campaign", )
    success_url = reverse_lazy("campaign:campaign-list")
    success_message = "Campaign Deleted Successfully"


class SlotCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Creates a new slot for given vaccination campaign
    """
    model = Slot
    form_class = SlotCreateForm
    template_name = "campaign/slot/slot-create.html"
    permission_required = ("campaign.add_slot", )
    success_url = reverse_lazy("vaccination:slot-list")
    success_message = "Slot Created Successfully"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["campaign_id"] = self.kwargs["campaign_id"]
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial["campaign"] = Campaign.objects.get(
            id=self.kwargs["campaign_id"])
        return initial

    def get_success_url(self) -> str:
        return reverse_lazy("campaign:slot-list", kwargs={"campaign_id": self.kwargs["campaign_id"]})


class SlotUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Updates the slot
    """
    model = Slot
    form_class = SlotUpdateForm
    permission_required = ("campaign.change_slot", )
    template_name = "campaign/slot/slot-update.html"
    success_message = "Slot Updated Successfully"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["campaign_id"] = self.kwargs["campaign_id"]
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial["campaign"] = Campaign.objects.get(
            id=self.kwargs["campaign_id"])
        return initial

    def get_success_url(self):
        return reverse_lazy("campaign:slot-list", kwargs={"campaign_id": self.kwargs["campaign_id"]})


@method_decorator(cache_page(60*15), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class SlotListView(LoginRequiredMixin, ListView):
    """
    Lists all the slot for given vaccination campaign
    """
    model = Slot
    template_name = "campaign/slot/slot-list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Slot.objects.filter(
            campaign=self.kwargs["campaign_id"]).order_by("id")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["campaign_id"] = self.kwargs["campaign_id"]
        return context


@method_decorator(cache_page(60*15), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class SlotDetailView(LoginRequiredMixin, DetailView):
    """
    Returns the details of given slot
    """
    model = Slot
    template_name = "campaign/slot/slot-detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related("campaign")


class SlotDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Deletes the slot 
    """
    model = Slot
    template_name = "campaign/slot/slot-delete.html"
    permission_required = ("campaign.delete_slot", )
    success_message = "Slot Deleted Successfully"

    def get_success_url(self) -> str:
        return reverse_lazy("campaign:slot-list", kwargs={"campaign_id": self.get_object().campaign.id})
