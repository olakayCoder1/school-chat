from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .forms  import CustomUserCreationForm
from django.contrib.auth import authenticate, login
# Create your views here.
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes , force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  , check_token
from django.core.mail import EmailMessage 
from .models import TokenActivation
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm , SetPasswordForm



def testing(requset):
    send_mail(
    'Subject here',
    'Here is the message.',
    'olakaycoder1@gmail.com',
    ['programmerolakay@gmail.com'],
    fail_silently=False,
    )
    alert = 'Mail sent'
    return render(requset, 'accounts/alert.html' , { 'message': alert })




def register_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account/login')
        return redirect('/account/register')
    form = CustomUserCreationForm()
    return render(request, 'accounts/register-page.html', {'form': form})




#login page view 
def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            #retrieve  the user creadiential for login to occur  
            user = authenticate(username=username, password=password) 
            if user is not None:
                #login user if user is not not none
                login(request, user)
                return redirect('/')
            return HttpResponse('INVALID CREDENTIAL DOES NOT EXIST')
        return HttpResponse('FORM IS INVALID')
    messages.info(request,'Invalid login credentials, try again!')

    return render(request, 'accounts/login-page.html')






def password_reset(request):
    if request.method == 'POST':
        user_email = request.POST['email']
        User = get_user_model()
        confirm_mail = User.objects.filter(email=user_email)
        if confirm_mail.count() > 0 :
            user = User.objects.get(email=user_email)
            #getting the current domain 
            current_site = get_current_site(request) 
            token = account_activation_token() 
            TokenActivation.objects.create(user_id = user, token=token , email=user_email)
            mail_subject = 'Password Reset'  
            message = render_to_string('accounts/password-reset-email.html', {  
                'user': request.user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.id)),  
                'token':token,  
            })  
            to_email = user_email  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()
            alert = 'Please check your email to complete the password reset process'
            return render(request, 'accounts/alert.html' , { 'message': alert })  
    
        return render(request, 'accounts/password-reset.html')
    return render(request, 'accounts/password-reset.html')




def password_reset_confirm(request, uidb64 , token ):
    User = get_user_model() 
    if request.method == 'POST':
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/account/login/')
        else:
            messages.error(request, 'Please correct the error below.')

    else:     
        try:  
            uid = force_str(urlsafe_base64_decode(uidb64))  
            user = User.objects.get(pk=uid)
            email = user.email  
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
            user = None  
        if user is not None and check_token(user, token , email ): 
            
            # return redirect('/account/password_reset/update/')
            form = SetPasswordForm(user)
            return render(request, 'accounts/password-change.html', {'form': form})
        else:
            alert = 'Activation link is invalid or has been used'  
            return render(request, 'accounts/alert.html' , { 'message': alert })



