from django.core.validators import RegexValidator

validate_username = RegexValidator(r'^[a-zA-Z0-9\_]*$', 'Only alphanumeric characters are allowed.')
validate_gender = RegexValidator(r'^[0-3]*$', 'Gender value not valid')
validate_room_slug = RegexValidator(r'^[a-zA-Z0-9\_]*$', 'Only alphanumeric characters are allowed.')