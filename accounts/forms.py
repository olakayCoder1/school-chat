from django.forms import ValidationError
from chat.models import CustomUser
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


    def clean_password2(self):
        password = self.cleaned_data['password1']
        confirm_password = self.cleaned_data['password2']
        if password and  confirm_password and password != confirm_password:
            raise ValidationError('Password does not match')
        if len(password) < 8 :
            raise ValidationError('Password must be atleast eigth characters long')
        return confirm_password
    

    def clean_email(self):
        email = self.cleaned_data['email']
        check_mail = CustomUser.objects.filter(email=email)
        if check_mail.count() > 0 :
            raise ValidationError('The email is already in use')
        return email 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user
                


