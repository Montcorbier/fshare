from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm

from website.models import User, Permission, FSUser, RegistrationKey 


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        # Username field 
        self.base_fields['username'].widget = forms.TextInput(attrs={'placeholder': "username", 'class': "form-control"})
        # Password field
        self.base_fields['password1'].widget = forms.TextInput(attrs={'type': 'password', 'placeholder': "password", 'class': "form-control"})
        # Password field (confirmation)
        self.base_fields['password2'].widget = forms.TextInput(attrs={'type': 'password', 'placeholder': "password (again)", 'class': "form-control"})
        # Email field
        self.base_fields['email'].widget = forms.TextInput(attrs={'type': 'email', 'placeholder': "@email (not required)", 'class': "form-control"})
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Add field for registration key
        self.fields['registration_key'] = forms.CharField(
                                                            label="Registration Key", 
                                                            widget=forms.TextInput(attrs={
                                                                'type': "text",
                                                                'placeholder': "registration key (required)",
                                                                'class': "form-control",
                                                                                    })
                                                        )

    def is_valid(self):
        """
            Override validation method
            This method performs parent validation, plus checks the registration key

        """
        # TODO return specific error code
        if not super(RegisterForm, self).is_valid():
            return False
        try:
            key = RegistrationKey.objects.get(key=self.cleaned_data["registration_key"])
        except ObjectDoesNotExist:
            return False
        if key.used:
            return False
        return True

    def save(self):
        """
            Create a user object from form, and a FS user object 
            with permissions relative to registration key

        """
        # Create django user object
        user = super(RegisterForm, self).save()
        # Get the registration key from db
        key = RegistrationKey.objects.get(key=self.cleaned_data["registration_key"])
        # Mark the key as used
        key.used = True
        key.save()
        # Get permissions corresponding to registration key 
        perm = Permission.objects.get(name=key.permission.name)
        # Create FS user object
        fsuser = FSUser(user=user, permission=perm)
        fsuser.save()
        return fsuser


class PermissionForm(forms.ModelForm):
    """
        Form relative to creation of new permissions

    """

    class Meta:
        model = Permission
        fields = ['name', 'storage_limit']
        #TODO handle base path field correctly
        widgets = {
                    'name': forms.TextInput(attrs={'placeholder': "permission class name", 'class': "form-control"}),
                    'storage_limit': forms.NumberInput(attrs={'placeholder': "storage limit (in bytes)", 'class': "form-control"}),
                }

