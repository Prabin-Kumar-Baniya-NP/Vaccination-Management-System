from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("change-password/", views.change_password, name="change-password"),
    path("profile-view/", views.profile_view, name="profile-view"),
    path("profile-update/", views.profile_update, name="profile-update"),
    path("agent/", views.AgentListView.as_view(), name="agent-list"),
    path("agent/<int:pk>/", views.AgentDetailView.as_view(), name="agent-detail"),
    path("agent/create/", views.AgentCreateView.as_view(), name="agent-create"),
    path("agent/update/<int:pk>/",
         views.AgentUpdateView.as_view(), name="agent-update"),
    path("agent/delete/<int:pk>/",
         views.AgentDeleteView.as_view(), name="agent-delete"),
     path("agent/patient/", views.PatientListForAgent.as_view(), name="patient-list-by-agent"),
     path("patient/detail/<int:pk>/", views.PatientDetailView.as_view(), name="patient-detail"),
     path("patient/update/<int:pk>/", views.PatientUpdateView.as_view(), name="patient-update"),
]
