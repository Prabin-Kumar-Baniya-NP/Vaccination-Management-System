from django.urls import path
from vaccination import views

app_name = "vaccination"

urlpatterns = [
    path("campaign/", views.CampaignListView.as_view(), name="campaign-list"),
    path("campaign/<int:pk>/", views.CampaignDetailView.as_view(),
         name="campaign-detail"),
    path("campaign/create/", views.CampaignCreateView.as_view(),
         name="campaign-create"),
    path("campaign/update/<int:pk>/",
         views.CampaignUpdateForm.as_view(), name="campaign-update"),
    path("campaign/delete/<int:pk>/",
         views.CampaignDeleteView.as_view(), name="campaign-delete"),
]
