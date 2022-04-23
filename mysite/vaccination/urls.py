from django.urls import path
from vaccination import views

app_name = "vaccination"

urlpatterns = [
    path("", views.VaccinationListView.as_view(),
         name="vaccination-list"),
    path("<int:pk>/", views.VaccinationDetailView.as_view(),
         name="vaccination-detail"),
    path("campaign/", views.CampaignListView.as_view(), name="campaign-list"),
    path("campaign/<int:pk>/", views.CampaignDetailView.as_view(),
         name="campaign-detail"),
    path("campaign/create/", views.CampaignCreateView.as_view(),
         name="campaign-create"),
    path("campaign/update/<int:pk>/",
         views.CampaignUpdateForm.as_view(), name="campaign-update"),
    path("campaign/delete/<int:pk>/",
         views.CampaignDeleteView.as_view(), name="campaign-delete"),
    path("slot/", views.SlotListView.as_view(), name="slot-list"),
    path("slot/<int:pk>/", views.SlotDetailView.as_view(), name="slot-detail"),
    path("slot/create/", views.SlotCreateView.as_view(), name="slot-create"),
    path("slot/update/<int:pk>/", views.SlotUpdateView.as_view(), name="slot-update"),
    path("slot/delete/<int:pk>/", views.SlotDeleteView.as_view(), name="slot-delete"),
    path("choose-vaccine/", views.choose_vaccine, name="choose-vaccine"),
    path("check-dose/<int:vaccine_id>/", views.check_dose, name="check-dose"),
    path("choose-campaign/<int:vaccine_id>/",
         views.choose_campaign, name="choose-campaign"),
    path("choose-slot/<int:campaign_id>/",
         views.choose_slot, name="choose-slot"),
    path("confirm-vaccination/<int:campaign_id>/<int:slot_id>/",
         views.confirm_vaccination, name="confirm-vaccination"),
]
