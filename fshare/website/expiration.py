from datetime import timedelta
from django.utils import timezone

def compute_expiration_date(ttl):
    """
        Compute the expiration date of a given file 

        @param  ttl     Number of days to live

        @ret    date of expiration of the file 

    """
    if ttl == 0:
        return None
    return timezone.now() + timedelta(days=ttl)

def compute_ttl(expiration_date):
    if expiration_date is None:
        return 0
    return (expiration_date - timezone.now()).days
