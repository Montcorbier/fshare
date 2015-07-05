import os
from random import randint

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from website.random_primary import RandomPrimaryIdModel


class File(RandomPrimaryIdModel):
    """
        Base model for files uploaded with fshare

    """

    # Owner of the file
    owner = models.ForeignKey(User, null=False)

    # File Description 

    # Title of the file
    title = models.CharField(max_length=255, null=True, blank=True)
    # Private label : not shown to downloader
    # Only used for the uploader for additional description
    private_label = models.CharField(max_length=255, null=True, blank=True)
    # Public description of the file
    description = models.TextField(null=True, blank=True, default="")

    # File Information

    # Path where the file is stored
    path = models.CharField(max_length=1024, null=False, blank=False)
    # Checksum of the uploaded file
    checksum = models.CharField(max_length=128, null=False, blank=False)
    # Size of the file in bytes
    size = models.IntegerField(null=False, blank=False)
    # Date of upload
    uploaded = models.DateTimeField(auto_now_add=True)
    # Date of last modification of descritions
    edited = models.DateTimeField(auto_now=True)

    # Statistics

    # Number of view of DL page
    nb_hits = models.IntegerField(default=0)
    # Number of DLs
    nb_dl = models.IntegerField(default=0)

    # Privacy

    # Is the file protected with a password/key ?
    is_private = models.BooleanField(default=False)
    # hash of the password
    pwd_hash = models.CharField(max_length=512, blank=True, null=True)


class Permission(models.Model):
    """
        Class of permissions for a given user.
        Defines storage space, location of storage, etc.

    """
    # Name of the permission category
    name = models.CharField(max_length=255, primary_key=True)
    # Max storage space in bytes
    storage_limit = models.IntegerField(default=100000)
    # Location where to store the files
    base_path = models.CharField(max_length=1024, null=False, blank=False, default=os.path.abspath(getattr(settings, "MEDIA_ROOT", "/tmp/")))


class RegistrationKey(models.Model):
    """
        Model for key needed for registration

    """
    # Registration key (can be used only once)
    key = models.CharField(max_length=100, null=False, blank=False)
    # Has it been used yet ?
    used = models.BooleanField(default=False)
    # Has it been distributed yet ?
    distributed = models.BooleanField(default=False)
    # Has it been revoked by admin ?
    revoked = models.BooleanField(default=False)
    # Corresponding permission
    permission = models.ForeignKey(Permission, null=False, blank=False)


class FSUser(models.Model):
    """
        Defines a user with specified permissions

    """
    user = models.OneToOneField(User, related_name="fshare_user")
    permission = models.ForeignKey(Permission, null=False, blank=False)

    def can_upload(self, size):
        """
            Check if a user can upload a file

        """
        # TODO: implements this method
        return True

    @property
    def storage_limit(self):
        return self.permission.storage_limit 

    @property
    def storage_left(self):
        # TODO : change this. Must compute available space
        storage_used = sum([f.size for f in File.objects.all().filter(owner=self.user)])
        return self.storage_limit - storage_used

    @property
    def storage_percent(self):
        return int(100. * (self.storage_limit - self.storage_left) / float(self.storage_limit))
