from django.urls import path
from vaccination import views

app_name = "vaccination"

urlpatterns = [
    path("", views.VaccinationList.as_view(), name="vaccination-list-patient"),
    path(
        "<int:campaign_id>", views.RegistrationList.as_view(), name="registration-list"
    ),
    path("<int:pk>/", views.VaccinationDetail.as_view(), name="vaccination-detail"),
    path("choose-vaccine/", views.ChooseVaccine.as_view(), name="choose-vaccine"),
    path(
        "choose-campaign/<int:vaccine_id>/",
        views.ChooseCampaign.as_view(),
        name="choose-campaign",
    ),
    path(
        "choose-slot/<int:campaign_id>/", views.ChooseSlot.as_view(), name="choose-slot"
    ),
    path(
        "confirm-vaccination/<int:campaign_id>/<int:slot_id>/",
        views.ConfirmVaccination.as_view(),
        name="confirm-vaccination",
    ),
    path(
        "approve-vaccination/<int:vaccination_id>/",
        views.approve_vaccination,
        name="approve-vaccination",
    ),
    path(
        "appointment/<int:vaccination_id>/",
        views.appointment_letter,
        name="appointment-letter",
    ),
    path(
        "certificate/<int:vaccination_id>/",
        views.vaccine_certificate,
        name="get-certificate",
    ),
]
