from unicodedata import name
from django.urls import path
from medical_condition import views
app_name = "medical_condition"

urlpatterns = [
    path("", views.MedicalConditionListView.as_view(),
         name="medical-condition-list"),
    path("create/", views.MedicalConditionCreateView.as_view(),
         name="medical-condition-create"),
    path("update/<int:pk>/", views.MedicalConditionUpdateView.as_view(),
         name="medical-condition-update"),
    path("<int:pk>/", views.MedicalConditionDetailView.as_view(),
         name="medical-condition-detail"),
    path("delete/<int:pk>/", views.MedicalConditionDeleteView.as_view(),
         name="medical-condition-delete"),
]
