from django.core.exceptions import ValidationError



def validate_rate(rate):
    if rate > 5 or rate < 0:
        raise ValidationError("rate should be 0-5")