from unicodedata import name
from django.urls import path
from medical_condition import views
app_name = "medical_condition"

urlpatterns = [
    path("", views.MedicalConditionListView.as_view(),
         name="list"),
    path("create/", views.MedicalConditionCreateView.as_view(),
         name="create"),
    path("update/<int:pk>/", views.MedicalConditionUpdateView.as_view(),
         name="update"),
    path("<int:pk>/", views.MedicalConditionDetailView.as_view(),
         name="detail"),
    path("delete/<int:pk>/", views.MedicalConditionDeleteView.as_view(),
         name="delete"),
]
