from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


GENDER_CHOICE = (
    ('M', "Male"),
    ('F', "Female"),
)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# class UserBankAccount(models.Model):
#     user = models.OneToOneField(
#         CustomUser,
#         related_name='account',
#         on_delete=models.CASCADE,
#     )
#     account_no = models.PositiveIntegerField(unique=True)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
#     birth_date = models.DateField(null=True, blank=True)
#     balance = models.DecimalField(
#         default=0,
#         max_digits=12,
#         decimal_places=2
#     )
#     interest_start_date = models.DateField(
#         null=True, blank=True,
#         help_text=(
#             'The month number that interest calculation will start from'
#         )
#     )
#     initial_deposit_date = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return str(self.account_no)

#     # def get_interest_calculation_months(self):
#     #     interval = int(
#     #         12 / self.account_type.interest_calculation_per_year
#     #     )
#     #     start = self.interest_start_date.month
#     #     return [i for i in range(start, 13, interval)]
