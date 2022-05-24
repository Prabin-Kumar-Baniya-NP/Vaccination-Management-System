from django.http import HttpResponseRedirect
from django.shortcuts import render
from vaccination.models import Vaccination
from user.forms import SignupForm, LoginForm, ChangePasswordForm, ProfileUpdateForm, AgentCreateForm, AgentUpdateForm, PatientUpdateForm
from django.contrib.auth import authenticate, login as user_login, logout as user_logout, update_session_auth_hash
from django.urls import reverse, reverse_lazy
from user.models import User, Patient, Agent
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def signup(request):
    """
    Creates a new user based on given email, password and other necessary informations
    """
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            Patient.objects.create(user=user)
            return HttpResponseRedirect(reverse("accounts:login"))
        else:
            return HttpResponseRedirect(reverse("accounts:signup"))
    else:
        context = {
            'form': SignupForm()
        }
        return render(request, "user/signup.html", context)


def login(request):
    """
    Login the user if the given email and password are valid
    """
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                user_login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseRedirect(reverse("accounts:login"))
        else:
            return HttpResponseRedirect(reverse("accounts:login"))
    else:
        context = {
            'form': LoginForm,
        }
        return render(request, "user/login.html", context)


@login_required
def logout(request):
    """
    Logout the user from the current session
    """
    user_logout(request)
    return HttpResponseRedirect(reverse("accounts:login"))


@login_required
def change_password(request):
    """
    Changes the password of the user
    """
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse("accounts:login"))
        else:
            return HttpResponseRedirect(reverse("accounts:change-password"))
    else:
        context = {
            'form': ChangePasswordForm(request.user)
        }
        return render(request, "user/change-password.html", context)


@login_required
def profile_view(request):
    """
    Displays the profile information of user
    """
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("accounts:signup"))
    context = {
        'user': user
    }
    return render(request, "user/profile-view.html", context)


@login_required
def profile_update(request):
    """
    Updates the profile information of user
    """
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("accounts:profile-view"))
        else:
            return HttpResponseRedirect(reverse("accounts:profile-update"))
    else:
        context = {
            "form": ProfileUpdateForm(instance=request.user)
        }
        return render(request, "user/profile-update.html", context)


class AgentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Agent
    form_class = AgentCreateForm
    template_name = "user/agent-create.html"
    success_url = reverse_lazy("accounts:agent-list")

    def test_func(self):
        return self.request.user.is_admin()


class AgentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Agent
    form_class = AgentUpdateForm
    template_name = "user/agent-update.html"
    success_url = reverse_lazy("accounts:agent-list")

    def test_func(self):
        return self.request.user.is_admin()


class AgentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Agent
    template_name = "user/agent-list.html"

    def test_func(self):
        return self.request.user.is_admin() or self.request.user.is_agent()


class AgentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Agent
    template_name = "user/agent-detail.html"

    def test_func(self):
        return self.request.user.is_admin() or self.request.user.is_agent()


class AgentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Agent
    template_name = "user/agent-delete.html"
    success_url = reverse_lazy("accounts:agent-list")

    def test_func(self):
        return self.request.user.is_admin()


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = "user/patient-detail.html"


class PatientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Patient
    form_class = PatientUpdateForm
    template_name = "user/patient-update.html"

    def get_success_url(self) -> str:
        return reverse("accounts:patient-detail", kwargs={"pk": self.kwargs["pk"]})

    def test_func(self):
        return self.request.user.id == self.get_object().id
