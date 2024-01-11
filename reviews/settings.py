# django imports
from django.utils.translation import gettext_lazy as _

SCORE_CHOICES = (
    (1.0, _("*")),
    (2.0, _("**")),
    (3.0, _("***")),
    (4.0, _("****")),
    (5.0, _("*****")),
)
