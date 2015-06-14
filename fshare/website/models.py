from django.db import models
from django.contrib.auth.models import User

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

