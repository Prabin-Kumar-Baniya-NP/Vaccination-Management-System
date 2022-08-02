from django.urls import path
from vaccination import views

app_name = "vaccination"

urlpatterns = [
    path("", views.VaccinationListViewForPatient.as_view(),
         name="vaccination-list-patient"),
    path("<int:campaign_id>", views.VaccinationListView.as_view(),
         name="vaccination-list"),
    path("<int:pk>/", views.VaccinationDetailView.as_view(),
         name="vaccination-detail"),
    path("choose-vaccine/", views.choose_vaccine, name="choose-vaccine"),
    path("check-dose/<int:vaccine_id>/", views.check_dose, name="check-dose"),
    path("choose-campaign/<int:vaccine_id>/",
         views.choose_campaign, name="choose-campaign"),
    path("choose-slot/<int:campaign_id>/",
         views.choose_slot, name="choose-slot"),
    path("confirm-vaccination/<int:campaign_id>/<int:slot_id>/",
         views.confirm_vaccination, name="confirm-vaccination"),
    path("approve-vaccination/<int:vaccination_id>/",
         views.approve_vaccination, name="approve-vaccination"),
    path("certificate/<int:vaccination_id>/",
         views.vaccine_certificate, name="get-certificate"),
]
