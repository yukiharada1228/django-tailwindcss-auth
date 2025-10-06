from django.urls import path

from . import views

app_name = "app"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signup_done/", views.SignUpDoneView.as_view(), name="signup_done"),
    path("activate/<uidb64>/<token>/", views.ActivateView.as_view(), name="activate"),
]
