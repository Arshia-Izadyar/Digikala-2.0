from django.core.exceptions import ValidationError
from datetime import datetime


def validate_rate(rate):
    if rate > 5 or rate < 0:
        raise ValidationError("rate should be 0-5")
    
    
def validated_date(date):
    if date < datetime.now().date():
        raise ValidationError("Invalid Date")
    