
from django import forms
from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm
from django.contrib.auth.models import User




class ContactForm(forms.Form):
    from_email = forms.EmailField(label="Ваш email:",widget=forms.EmailInput(attrs={'class': 'form-control py-2 line-email',
                                                                                    'placeholder':
        'Введите ваш '
                                                                                                                       'email'}),
                                  required=True)
    subject = forms.CharField(label="Тема сообщения:",widget=forms.TextInput(attrs={'class': 'form-control py-2 line-subject',
                                                                                   "placeholder":
        'Тема сообщения'}),
                              required=True)
    message = forms.CharField(label="Сообщения:",widget=forms.Textarea(attrs={'class': 'form-control py-2', "placeholder": 'Текст '
                                                                                                                                'сообщения'}), required=True)


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email','first_name','last_name')
