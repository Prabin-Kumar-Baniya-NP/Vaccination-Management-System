from django.urls import path
from vaccine import views

app_name = "vaccine"

urlpatterns = [
    path("", views.VaccineListView.as_view(), name="vaccine-list"),
    path("<int:pk>/", views.VaccineDetailView.as_view(), name="vaccine-detail"),
    path("create/", views.VaccineCreateView.as_view(), name="vaccine-create"),
    path("update/<int:pk>/", views.VaccineUpdateView.as_view(), name="vaccine-update"),
    path("delete/<int:pk>/", views.VaccineDeleteView.as_view(), name="vaccine-delete"),
]
