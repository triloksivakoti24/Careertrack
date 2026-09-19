from datetime import datetime

def format_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").strftime("%d %b %Y")
    except (TypeError, ValueError):
        return date_string
