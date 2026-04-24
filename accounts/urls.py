from django.urls import path
from . import views
from . import profile_views
from . import analysis_views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", profile_views.profile, name="profile"),
    path("profile/analysis/", analysis_views.investment_analysis, name="investment_analysis"),
]