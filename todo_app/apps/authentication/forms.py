from django import forms

from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('tg_id', 'username', 'first_name', 'last_name',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if password := self.cleaned_data['password1']:
            user.set_password(password)
        if commit:
            user.save()
        return user
