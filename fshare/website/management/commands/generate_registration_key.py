from django.core.management.base import BaseCommand, CommandError

import random

from website.models import RegistrationKey, Permission

class Command(BaseCommand):
    help = 'Generate a new registration key for a given user class passed in argument'

    charset = "azertyuiopqsdfghjklmwxcvbn1234567890AZERTYUIOPQSDFGHJKLMWXCVBN"

    def add_arguments(self, parser):
        parser.add_argument('class', nargs='+', type=str)

    def handle(self, *args, **options):
        
        user_class = [perm.name for perm in Permission.objects.all()]

        if len(options["class"]) == 0 or options["class"][0] not in user_class:
            print("You must specify a permission class among the following: ")
            for uc in user_class:
                print(uc)
            print("e.g.: ./manage.py generate_registration_key " + user_class[0])
            return

        key = ''.join(random.choice(self.charset) for _ in range(50))

        self.stdout.write(key)

        new_key = RegistrationKey(key=key, permission=Permission.objects.get(pk=options['class'][0]))
        new_key.save()

        return
