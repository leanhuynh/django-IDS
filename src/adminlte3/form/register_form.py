from django import forms
import os

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=100, required=True)
    password_confirmation = forms.CharField(max_length=100, required=True)
    # role_id = forms.IntegerField(min_value=1, required=True)
    avatar = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')
        avatar = cleaned_data.get('avatar')

        if password and password_confirmation:
            if password != password_confirmation:
                raise forms.ValidationError("Passwords don't match!")
        
        if avatar:
            ext = os.path.splitext(avatar.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                raise forms.ValidationError("File phải là ảnh hợp lệ!")
        
        return cleaned_data