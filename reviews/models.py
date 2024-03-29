# django imports
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

# reviews imports
from reviews.managers import ActiveManager
from reviews.settings import SCORE_CHOICES


class Review(models.Model):
    """A `review` consists of a comment and a rating."""

    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_("Content type"),
        related_name="content_type_set_for_%(class)s",
        on_delete=models.CASCADE,
    )
    content_id = models.PositiveIntegerField(_("Content ID"), blank=True, null=True)
    content = GenericForeignKey(ct_field="content_type", fk_field="content_id")

    # if the user is authenticated we save the user otherwise the name and the email.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        blank=True,
        null=True,
        related_name="%(class)s_comments",
        on_delete=models.SET_NULL,
    )
    session_id = models.CharField(_("Session ID"), blank=True, max_length=50)

    # ... otherwise the name and the email
    user_name = models.CharField(_("Name"), max_length=50, blank=True)
    user_email = models.EmailField(_("E-mail"), blank=True)

    comment = models.TextField(_("Comment"), blank=True)
    score = models.FloatField(_("Score"), choices=SCORE_CHOICES, default=0.0)
    active = models.BooleanField(_("Active"), default=False)

    creation_date = models.DateTimeField(_("Creation date"), auto_now_add=True)
    ip_address = models.GenericIPAddressField(_("IP address"), blank=True, null=True)

    objects = ActiveManager()

    class Meta:
        ordering = ("-creation_date",)

    def __str__(self):
        return "%s (%s)" % (self.name, self.score)

    @property
    def name(self):
        """Returns the stored user name."""
        if self.user is not None:
            return self.user.get_full_name()
        else:
            return self.user_name

    @property
    def email(self):
        """Returns the stored user email."""
        if self.user is not None:
            return self.user.email
        else:
            return self.user_email
