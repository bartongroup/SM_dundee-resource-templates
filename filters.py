from datetime import datetime

def datetime_filter(value, format='%Y-%m-%d %H:%M:%S'):
    """Convert a datetime string into a datetime object."""
    return datetime.strptime(value, format)
