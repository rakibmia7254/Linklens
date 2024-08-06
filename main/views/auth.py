from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from uuid import uuid4
from ..utils import mail
from ..models import forgotTokens
import time
import validators


User = get_user_model()


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, "auth/register.html")

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        email = request.POST.get("email")
        password = request.POST.get("password")
        repeatPassword = request.POST.get("repeat_password")

        if password != repeatPassword:
            messages.error(request, "Passwords do not match", "alert-danger")
            return render(request, "auth/register.html")

        if len(password) < 8:
            messages.error(
                request, "Password must be at least 8 characters", "alert-danger"
            )
            return render(request, "auth/register.html")

        if not validators.email(email):
            messages.error(request, "Invalid Email", "alert-danger")
            return render(request, "auth/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists", "alert-danger")
            return render(request, "auth/register.html")
        verifyToken = str(uuid4())
        User.objects.create_user(
            email=email, password=password, verifyToken=verifyToken
        )
        if mail.email_service:
            mail.send_verify_email(email, verifyToken)
            messages.success(request, "Verification email sent", "alert-success")
            return redirect("login")

        messages.success(request, "Registration Success", "alert-success")
        login(request, User.objects.get(email=email))
        return redirect("dashboard")


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, "auth/login.html")

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        email = request.POST.get("email")
        password = request.POST.get("password")
        rememberme = request.POST.get("rememberme")

        if rememberme == "on":
            request.session.set_expiry(60 * 60 * 24 * 7)  # one week
        else:
            request.session.set_expiry(60 * 60 * 1)  # 1 hour
        user = authenticate(request, username=email, password=password)
        if not user:
            messages.error(request, "Invalid email or password", "alert-danger")
            return redirect("login")

        if mail.email_service:
            if not user.is_verified:
                messages.error(request, "Account not verifed", "alert-danger")
                return redirect("login")
            login(request, user)
            messages.success(request, "Login Success", "alert-success")
            return redirect("dashboard")

        login(request, user)
        messages.success(request, "Login Success", "alert-success")
        return redirect("dashboard")


def logout_view(request):
    logout(request)
    return redirect("login")


class ForgotPasswordView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, "auth/forgot-password.html")

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")

        email = request.POST.get("email")

        if mail.email_service:
            messages.error(request, "Email service not configured", "alert-danger")
            return render(request, "auth/forgot-password.html")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email does not exist", "alert-danger")
            return render(request, "auth/forgot-password.html")

        if not user.is_verified:
            messages.error(request, "Account not verifed", "alert-danger")
            return render(request, "auth/forgot-password.html")

        # generate token
        token = str(uuid4())

        try:
            ftoken = forgotTokens.objects.get(user_id=user.id)
            if ftoken.expire_at > time.time():
                mail.send_forgot_password_email(email, ftoken.forgotToken)
            else:
                ftoken.delete()
                forgotTokens.objects.create(user_id=user.id, forgotToken=token).save()
                mail.send_forgot_password_email(email, token)
            messages.success(request, "Verification email sent", "alert-success")
            return render(request, "auth/forgot-password.html")

        except:
            forgotTokens.objects.create(user_id=user, forgotToken=token).save()
            mail.send_forgot_password_email(email, token)
            messages.success(request, "Verification email sent", "alert-success")
            return render(request, "auth/forgot-password.html")


class resetPass(View):
    def get(self, request, token):
        if request.user.is_authenticated:
            return redirect("dashboard")

        ftoken = forgotTokens.objects.filter(forgotToken=token).first()
        if ftoken and ftoken.expire_at < time.time():
            ftoken.delete()
            messages.error(request, "Token expired", "alert-danger")
            return redirect("login")

        return render(request, "auth/resetPass.html", {"ftoken": token})

    def post(self, request, token):
        if request.user.is_authenticated:
            return redirect("dashboard")

        newPassword = request.POST.get("newPassword")
        conFirmPassword = request.POST.get("confirmNewPassword")
        ftokenReq = token

        ftoken = forgotTokens.objects.filter(forgotToken=ftokenReq).first()
        if ftoken and ftoken.expire_at < time.time():
            ftoken.delete()
            messages.error(request, "Token expired", "alert-danger")
            return redirect("reset_password")

        if not newPassword == conFirmPassword:
            messages.error(request, "Passwords do not match", "alert-danger")
            return redirect("reset_password", token=ftokenReq)
        auth = authenticate(
            request, username=ftoken.user_id.email, password=newPassword
        )
        if auth:
            messages.error(
                request, "Old password can't be new passowrd", "alert-danger"
            )
            return redirect("reset_password", token=ftokenReq)

        if len(newPassword) < 8:
            messages.error(
                request, "Password must be at least 8 characters", "alert-danger"
            )
            return redirect("reset_password", token=ftokenReq)
        user = ftoken.user_id
        if not user:
            ftoken.delete()
            messages.error(request, "User not found", "alert-danger")
            return redirect("reset_password", token=ftokenReq)
        user.set_password(newPassword)
        user.save()
        ftoken.delete()
        messages.success(request, "Passoword Changed Successfully", "alert-success")
        return redirect("login")


class verifyAcc(View):
    def get(self, request, token):
        if request.user.is_authenticated:
            return redirect("dashboard")

        user = User.objects.filter(verifyToken=token).first()
        if not user:
            messages.success(request, "verification token not found", "alert-danger")
            return redirect("login")
        if user.is_verified:
            messages.success(request, "Account already verified", "alert-success")
            return redirect("login")
        return render(request, "auth/verifyAcc.html", {"token": token, "user": user})

    def post(self, request, token):
        if request.user.is_authenticated:
            return redirect("dashboard")

        tokenreq = request.POST.get("token")
        if not tokenreq == token:
            messages.error(request, "Token does not match", "alert-danger")
            return redirect("verify_acc", token=token)

        user = User.objects.filter(verifyToken=token).first()
        if not user:
            messages.success(request, "verification token not found", "alert-danger")
            return redirect("login")
        user.is_verified = True
        user.save()
        messages.success(request, "Account verified successfully", "alert-success")
        return redirect("login")


class Settings(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        return render(request, "auth/settings.html")

    def post(self, request):
        password = request.POST.get("password")
        newPassword = request.POST.get("new-password")

        if password == newPassword:
            messages.error(
                request, "Old password can't be new passowrd", "alert-danger"
            )
            return redirect("settings")
        if len(newPassword) < 8:
            messages.error(
                request, "Password must be at least 8 characters", "alert-danger"
            )
            return redirect("settings")

        user = authenticate(request, username=request.user.email, password=password)
        if not user:
            messages.error(request, "Wrong password", "alert-danger")
            return redirect("settings")

        user.set_password(newPassword)
        user.save()
        # login again
        login(request, user)
        messages.success(request, "Password changed successfully", "alert-success")
        return redirect("settings")
