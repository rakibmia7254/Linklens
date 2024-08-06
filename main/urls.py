from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views.auth import (
    LoginView,
    logout_view,
    RegisterView,
    ForgotPasswordView,
    resetPass,
    verifyAcc,
    Settings,
)
from .views.links import shorten_link, delete_link, redirect_link, dashboard, test
from .views.analysis import (
    generate_qr_code,
    analysis_page,
    full_annalysis,
)

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("create/", shorten_link, name="shorten_link"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("delete/<str:custom_alias>/", delete_link, name="delete_link"),
    path("redirect/<str:custom_alias>/", redirect_link, name="redirect_link"),
    path("generate_qr/<str:alias>/", generate_qr_code, name="generate_qr_code"),
    path("analysis/<str:custom_alias>", analysis_page, name="analysis"),
    path("analysis/", full_annalysis, name="full_analysis"),
    path("settings/", Settings.as_view(), name="settings"),
    path("forgot_password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset_password/<str:token>/", resetPass.as_view(), name="reset_password"),
    path("verify/<str:token>/", verifyAcc.as_view(), name="verify_acc"),
    path("test/", test, name="test"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
