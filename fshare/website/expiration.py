from datetime import datetime, timedelta

def compute_expiration_date(size):
    """
        Compute the expiration date of a given file 
        regarding its size

        @param  size    size of the related file

        @ret    date of expiration of the file 

    """
    return datetime.now() + timedelta(days=7)

