from django.core.validators import RegexValidator, MinLengthValidator
from django.utils.translation import gettext as _

validate_alpha = RegexValidator(
    regex=r'^[a-zA-Z]*$',
    message=_("Это поле должно содержать только буквы латиницей."),
    code='invalid_alpha'
)

validate_min_length_2 = MinLengthValidator(
    limit_value=2,
    message=_("Это поле должно содержать минимум 2 символа.")
)

validate_password = RegexValidator(
    regex=r'^(?=.*[a-zA-Z])(?=.*\d).{8,}$',
    message=_("Пароль должен содержать минимум 8 символов, включая буквы и цифры."),
    code='invalid_password'
)