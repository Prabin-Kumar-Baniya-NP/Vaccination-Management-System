from unicodedata import name
from django.urls import path
from center import views

app_name = "center"

urlpatterns = [
    path("", views.CenterList.as_view(), name="center-list"),
    path("<int:pk>/", views.CenterDetail.as_view(), name="center-detail"),
    path("create/", views.CreateCenter.as_view(), name="create-center"),
    path("update/<int:pk>", views.CenterUpdate.as_view(), name="center-update"),
    path("delete/<int:pk>", views.CenterDelete.as_view(), name="center-delete"),
    path("<int:center_id>/storage/",
         views.StorageList.as_view(), name="storage-list"),
    path("storage/<int:pk>/", views.StorageDetail.as_view(), name="storage-detail"),
    path("<int:center_id>/storage/create/",
         views.CreateStorage.as_view(), name="storage-create"),
    path("storage/update/<int:pk>/",
         views.StorageUpdate.as_view(), name="storage-update"),
    path("storage/delete/<int:pk>/",
         views.StorageDelete.as_view(), name="storage-delete"),
]
