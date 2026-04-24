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
    path("password/change/", views.password_change, name="password_change"),
    path("password/change/done/", views.password_change_done, name="password_change_done"),
    path("profile/analysis/", analysis_views.investment_analysis, name="investment_analysis"),
]