import hashlib
import sha3
import os

from django import forms
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_str

from website.models import User, Permission, FSUser, RegistrationKey, File
from website.renders import CustomRadioRenderer
from website.expiration import compute_expiration_date
from website.encryption import encrypt_file, encrypt_filename, generate_random_path, decrypt_filename


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
        widgets = {
                    'username': forms.TextInput(attrs={'placeholder': "a-z, A-Z, 0-9 and @/./+/-/_", 'class': "form-control"}),
                    'email': forms.TextInput(attrs={'type': 'email', 'placeholder': "not required", 'class': "form-control"}),
                }
        labels = {
                    'username': "Username",
                    'password1': "Password",
                    'password2': "Password (again)",
                    'email': "@email",
                }

    def __init__(self, *args, **kwargs):
        self.base_fields['password1'].widget = forms.TextInput(attrs={'type': 'password', 'placeholder': "e.g. hunter2", 'class': "form-control"})
        self.base_fields['password1'].label = "Password"
        self.base_fields['password2'].widget = forms.TextInput(attrs={'type': 'password', 'placeholder': "e.g. hunter2", 'class': "form-control"})
        self.base_fields['password2'].label = "Password (again)"
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Add field for registration key
        self.fields['registration_key'] = forms.CharField(
                                                            label="Registration Key", 
                                                            widget=forms.TextInput(attrs={
                                                                'type': "text",
                                                                'placeholder': "required",
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
        if key.used or key.revoked:
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


class UploadFileForm(forms.ModelForm):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'superDropzone'}), label='')

    class Meta:
        model = File
        fields = [
                    # 'title', 
                    # 'private_label', 
                    # 'description', 
                    # 'is_private', 
                    # 'pwd',
                    'key',
                ]
        widgets = {
                    'title': forms.TextInput(attrs={'placeholder': "not required", 'class': "form-control"}),
                    'key': forms.TextInput(attrs={'placeholder': "recommanded (used to encrypt file)", 'class': "form-control"}),
                    'private_label': forms.TextInput(attrs={'placeholder': "e.g. \"Top secret text file for the General\""}),
                    'description': forms.TextInput(attrs={'placeholder': "e.g. \"Just some reports\"", 'class': "form-control"}),
                    'is_private': forms.RadioSelect(attrs={'id': "file-public-switch", 'class': "radio"}, choices=[('private', 'Yep'), ('public', 'Nope, don\'t care')], renderer=CustomRadioRenderer),
                    'pwd': forms.TextInput(attrs={'placeholder': "e.g. \"topsecret\", \"9af66498ed73cc90ae\"", 'class': "form-control"}),
                    }
        labels = {
                    'title': "File name",
                    'private_label': "Private title",
                    'description': "Description",
                    'is_private': "Protected by a key",
                    'key': mark_safe("key (<span class=\"link\" id=\"gen-key-btn\">generate random</span>)"),
                    }

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)

    def is_valid(self, user=None):
        """
            Override validation method
            This method performs parent validation, plus check file size

        """
        if not super(UploadFileForm, self).is_valid():
            return False
        if user.is_anonymous():
            return self.cleaned_data.get('file').size <= settings.FILE_MAX_SIZE_ANONYMOUS
        else:
            return user.fshare_user.can_upload(self.cleaned_data.get('file').size)

    def save(self, user):
        if user.is_anonymous():
            folder = settings.UPLOAD_DIRECTORY_ANONYMOUS
            max_dl = settings.FILE_MAX_DL_ANONYMOUS
        else:
            folder = os.path.join(user.fshare_user.permission.base_path, user.username)
            max_dl = self.cleaned_data.get('max_dl') or 1
        if not os.path.exists(folder):
            os.makedirs(folder)

        key = self.cleaned_data.get('key') or None

        uploaded_file = self.cleaned_data.get('file')
        filename_safe = smart_str(uploaded_file.name, "utf-8")

        if key is not None:
            iv, md5, filepath = encrypt_file(filename_safe, uploaded_file, folder, key)
            filename = encrypt_filename(filename_safe, key, iv)
        else:
            filepath = generate_random_path(folder)
            filename = filename_safe
            iv = None
            m = hashlib.md5()
            with open(filepath, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    m.update(chunk)
                    destination.write(chunk)
            md5 = m.hexdigest()

        new_file = File(
            owner=user if not user.is_anonymous() else None,
            title=filename,
            private_label=self.cleaned_data.get('private_label', self.cleaned_data.get('title')),
            description=self.cleaned_data.get('description'),
            path=filepath,
            checksum=md5,
            size=uploaded_file.size,
            expiration_date=compute_expiration_date(uploaded_file.size),
            key = hashlib.sha3_512(key.encode("utf-8")).hexdigest() if key is not None else None,
            iv = iv.decode("utf-8") if iv is not None else None,
            max_dl = max_dl,
        )

        pwd = self.cleaned_data.get('pwd') or None
        if new_file.is_private:
            new_file.pwd = pwd

        new_file.save()
        return new_file

