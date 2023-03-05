def validate_tag(value):
    from django.core.exceptions import ValidationError
    if " " in value:
        raise ValidationError('Tag not valid')