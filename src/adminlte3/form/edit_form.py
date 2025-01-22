from django import forms
import os

class EditForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=100, required=False)
    password_confirmation = forms.CharField(max_length=100, required=False)
    # role_id = forms.IntegerField(min_value=1, required=True)
    avatar = forms.ImageField(required=False)  # Không yêu cầu file ảnh

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')
        avatar = cleaned_data.get('avatar')

        if password and password_confirmation:
            if password != password_confirmation:
                raise forms.ValidationError("Passwords don't match!")
            
        if avatar:
            if not hasattr(avatar, 'name') or not avatar.name:
                raise forms.ValidationError("File phải là ảnh hợp lệ!")
            
            ext = os.path.splitext(avatar.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                raise forms.ValidationError("File phải là ảnh hợp lệ!")
        
        return cleaned_data