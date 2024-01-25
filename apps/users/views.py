from django.contrib.auth import get_user_model; User = get_user_model()
from .forms import EmailCheckForm, SignupForm
from .backends import CustomModelBackend as CMB  
from .utils import store_otp, check_otp
from .tasks import send_otp_by_email

from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView

from django.contrib.auth import login, logout
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy

    
"""\________________________[FEATURE]________________________/"""
class Profile(View):... # Feature in future
class Dashboard(View):... # Feature in future

"""\________________________[LOGIN]________________________/"""
class UsernameLoginView(LoginView):
    template_name = 'username_login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        if form.get_user().is_active:
            return super().form_valid(form)
        else:
            messages.error(
                self.request,
                "Your account is not active!",
                extra_tags="danger"
            )
            return HttpResponseRedirect('users:login')
        
    def get_success_url(self):
        username = self.request.POST.get("username")
        first_name = User.objects.get(username=username).first_name
            
        messages.success(
            self.request,
            _(
                f"Login Successfuly. " \
                f"Welcome {first_name if first_name else username}."
            )
        )
        
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('core:home')
    

class EmailLoginView(FormView):
    template_name = 'email_login.html'
    form_class = EmailCheckForm

    def post(self, request):
        if user_email:= request.POST.get('email', None):
            form = self.form_class(request.POST)
            if form.is_valid():
                user = CMB().authenticate(request=request, email=user_email)
                if user:
                    if user.is_active == True:
                        otp_code = store_otp(user_email)
                        status = send_otp_by_email(user_email, otp_code) # delay
                        
                        if status:
                            request.session['email'] = user_email
                            messages.success(
                                self.request,
                                _(
                                    f"Code sent Successfuly. " \
                                    f"Check {user_email}."
                                )
                            )
                            return redirect("users:otp")
                        else:
                            messages.error(request, _("Opss! some truble happend! please try again!"), extra_tags="danger")
                    else:
                        messages.error(request, _("your account is not active!"), extra_tags="danger")
                else:
                    messages.error(request, _("you didn't define email or you need to signup!"), extra_tags="danger")
            else:
                messages.error(request, _(form.errors), extra_tags="danger")
        else:
            messages.error(request, _("email field cant Empty!"), extra_tags="danger")
        
        return self.render_to_response(self.get_context_data())
        

class OTPView(TemplateView):
    template_name = 'otp.html'
    
    def post(self, request, *args, **kwargs):
        if otp_code := request.POST.get('otp'):
            email = request.session.get('email')
            if email:
                otp_status = check_otp(email=email, send_otp=otp_code)
                if otp_status:
                    if otp_status != -1:
                        user = User.objects.get(email=email)
                        login(request, user)
                        
                        username = user.username
                        first_name = user.first_name
                        
                        messages.success(
                            self.request,
                            _(
                                f"Login Successfuly. " \
                                f"Welcome {first_name if first_name else username}."
                            )
                        )
                        
                        return redirect('core:home')

                    else:
                        messages.error(request, _("The entered code does not match!!!"), extra_tags="danger")
                else:
                    messages.error(request, _("The OTP code has expired!!!"), extra_tags="danger")
                    return redirect('users:email')
            else:
                messages.error(request, _("Email didn't save in session!"), extra_tags="danger")
        else:
            messages.error(request, _("Sent OTP code can't Empty!"), extra_tags="danger")
        
        return self.render_to_response(self.get_context_data())


"""\________________________[SIGNUP]________________________/"""
class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'signup.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        
        messages.success(
            self.request,
            _(
                f"Signup Successfuly. Welcome {user.username}."
            )
        )
        
        return response
    
    # def get_success_url(self):
    #     username = self.request.POST.get("username")

    #     messages.success(
    #         self.request,
    #         _(
    #             f"Signup Successfuly. Welcome {username}."
    #         )
    #     )

    #     user = self.model.objects.get(username=username)
    #     login(self.request, user)
        
    #     return redirect()
    

"""\________________________[LOGOUT]________________________/"""
class CustomLogoutView(LogoutView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        next_page = request.GET.get('next', None)
        if next_page:
            return redirect(next_page)
        return redirect('core:home')
    