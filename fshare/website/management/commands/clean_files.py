from datetime import datetime

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from website.models import File

class Command(BaseCommand):
    help = 'Remove all files for which the expiration date has passed.'

    def handle(self, *args, **options):
        for f in File.objects.all():
            if f.expiration_date is not None and f.expiration_date < timezone.make_aware(datetime.now(), timezone.get_default_timezone()):
                print("Deleting {0} ...".format(f.path))
                f.delete()

