from django import template

register = template.Library()

def format(value:int):
    
    return "{:,}$".format(int(value))
    
register.filter("c_format", format)



# @register.filter(name="custom_format")