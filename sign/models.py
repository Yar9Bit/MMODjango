from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm
from django.contrib.auth.models import models, User

# Create your models here.


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    code = models.CharField(unique=True, max_length=128)

    def __str__(self):
        return f'OTP for {self.user}'
