from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from vaccination.models import Vaccination_Campaign
from django.urls import reverse_lazy
from vaccination.forms import CampaignCreateForm, CampaignUpdateForm


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
