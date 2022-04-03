from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from vaccination.models import Slot, Vaccination_Campaign
from django.urls import reverse_lazy
from vaccination.forms import CampaignCreateForm, CampaignUpdateForm, SlotCreateForm, SlotUpdateForm


class CampaignCreateView(CreateView):
    model = Vaccination_Campaign
    form_class = CampaignCreateForm
    template_name = "vaccination/campaign-create.html"
    success_url = reverse_lazy("vaccination:campaign-list")


class CampaignUpdateForm(UpdateView):
    model = Vaccination_Campaign
    form_class = CampaignUpdateForm
    template_name = "vaccination/campaign-update.html"
    success_url = reverse_lazy("vaccination:campaign-list")


class CampaignListView(ListView):
    model = Vaccination_Campaign
    template_name = "vaccination/campaign-list.html"


class CampaignDetailView(DetailView):
    model = Vaccination_Campaign
    template_name = "vaccination/campaign-detail.html"


class CampaignDeleteView(DeleteView):
    model = Vaccination_Campaign
    template_name = "vaccination/campaign-delete.html"
    success_url = reverse_lazy("vaccination:campaign-list")


class SlotCreateView(CreateView):
    model = Slot
    form_class = SlotCreateForm
    template_name = "vaccination/slot-create.html"
    success_url = reverse_lazy("vaccination:slot-list")


class SlotUpdateView(UpdateView):
    model = Slot
    form_class = SlotUpdateForm
    template_name = "vaccination/slot-update.html"
    success_url = reverse_lazy("vaccination:slot-list")


class SlotListView(ListView):
    model = Slot
    template_name = "vaccination/slot-list.html"
    success_url = reverse_lazy("vaccination:slot-list")


class SlotDetailView(DetailView):
    model = Slot
    template_name = "vaccination/slot-detail.html"


class SlotDeleteView(DeleteView):
    model = Slot
    template_name = "vaccination/slot-delete.html"
    success_url = reverse_lazy("vaccination:slot-list")
