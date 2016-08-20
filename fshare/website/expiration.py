from datetime import datetime, timedelta

def compute_expiration_date(ttl):
    """
        Compute the expiration date of a given file 

        @param  ttl     Number of days to live

        @ret    date of expiration of the file 

    """
    if ttl == 0:
        return None
    return datetime.now() + timedelta(days=ttl)

