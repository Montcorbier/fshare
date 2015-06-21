import os

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm

from website.models import User, Permission, FSUser, RegistrationKey 


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
        widgets = {
                    'username': forms.TextInput(attrs={'placeholder': "username", 'class': "form-control"}),
                    'email': forms.TextInput(attrs={'type': 'email', 'placeholder': "@email (not required)", 'class': "form-control"}),
                }

    def __init__(self, *args, **kwargs):
        self.base_fields['password1'].widget = forms.TextInput(attrs={'type': 'password', 'placeholder': "password", 'class': "form-control"})
        self.base_fields['password2'].widget = forms.TextInput(attrs={'type': 'password', 'placeholder': "password (again)", 'class': "form-control"})
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
        fields = ['name', 'storage_limit', 'base_path']
        # TODO handle base path field correctly
        widgets = {
                    'name': forms.TextInput(attrs={'placeholder': "permission class name", 'class': "form-control"}),
                    'storage_limit': forms.NumberInput(attrs={'placeholder': "storage limit (in bytes)", 'class': "form-control"}),
                    'base_path': forms.TextInput(attrs={'placeholder': "base path to store files", 'class': "form-control"}),
                }

    def split_path(self):
        """
            From the base path of the permission, try to extract the subpath corresponding
            to the permission name. If permission name was not specified, nothing is done
            and (base_path, '') is returned. Otherwise, remove permission name from base path 
            and returns (base_path_after_removal, permission_name).

            Examples:
                - if base_path = '/tmp/regular' for permission 'regular', 
                    returns ('/tmp', 'regular')
                - if base_path = '/tmp' for permission 'regular',
                    returns ('/tmp', '')

        """
        # Get the base path as specified in the form
        base_path = os.path.normpath(self.cleaned_data["base_path"])
        sub_path = ""
        # Remove '/' at the end of the path if any
        if base_path[-1] == "/":
            base_path = base_path[:-1]
        # Check if base path ends with permission name
        if os.path.basename(base_path) == self.cleaned_data["name"]:
            # sub_path takes the permission name as value
            sub_path = self.cleaned_data["name"]
            # Remove permission name from base_path
            base_path = base_path[:-len(sub_path)]
        return base_path, sub_path

    def is_valid(self):
        if not super(PermissionForm, self).is_valid():
            return False
        base_path, sub_path = self.split_path()
        # TODO specify error (does not exist or cannot read)
        # Check if base_path exists and is writable
        if not os.path.exists(base_path) or not os.access(base_path, os.W_OK):
            print(base_path)
            return False
        if sub_path == "":
            return True
        # TODO specify error (already exists but can't write)
        # If sub_path already exists, check if it is writable
        if os.path.exists(os.path.join(base_path, sub_path)) and not os.access(os.path.join(base_path, sub_path), os.W_OK):
            return False
        return True

    def save(self):
        base_path, sub_path = self.split_path()
        # Create target dir if does not exist
        if not os.path.exists(os.path.join(base_path,sub_path)):
            os.mkdir(os.path.join(base_path, sub_path))
        return super(PermissionForm, self).save()


class UploadFileForm(forms.Form):
    file = forms.FileField()

    def is_valid(self, user=None):
        """
            Override validation method
            This method performs parent validation, plus check file size

        """
        if not super(UploadFileForm, self).is_valid():
            return False
        return user.fshare_user.can_upload(self.cleaned_data.get('file').size)

    def save(self, user):
        folder = os.path.join(user.fshare_user.permission.base_path, user.username)
        if not os.path.exists(folder):
            os.makedirs(folder)

        uploaded_file = self.cleaned_data.get('file')
        filepath = "{0}/{1}".format(folder, uploaded_file)
        with open(filepath, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        return filepath
