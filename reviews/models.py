# django imports
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# reviews imports
from reviews.managers import ActiveManager
from reviews.settings import SCORE_CHOICES


class Review(models.Model):
    """A ``Review`` consists on a comment and a rating.
    """
    content_type = models.ForeignKey(ContentType, verbose_name=_(u"Content type"), related_name="content_type_set_for_%(class)s")
    content_id = models.PositiveIntegerField(_(u"Content ID"), blank=True, null=True)
    content = GenericForeignKey(ct_field="content_type", fk_field="content_id")

    # if the user is authenticated we save the user otherwise the name and the
    # email.
    user = models.ForeignKey(User, verbose_name=_(u"User"), blank=True, null=True, related_name="%(class)s_comments")
    session_id = models.CharField(_(u"Session ID"), blank=True, max_length=50)

    user_name = models.CharField(_(u"Name"), max_length=50, blank=True)
    user_email = models.EmailField(_(u"E-mail"), blank=True)
    comment = models.TextField(_(u"Comment"), blank=True)
    score = models.FloatField(_(u"Score"), choices=SCORE_CHOICES, default=3.0)
    active = models.BooleanField(_(u"Active"), default=False)

    creation_date = models.DateTimeField(_(u"Creation date"), auto_now_add=True)
    ip_address = models.GenericIPAddressField(_(u"IP address"), blank=True, null=True)

    objects = ActiveManager()

    class Meta:
        ordering = ("-creation_date", )

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.score)

    @property
    def name(self):
        """Returns the stored user name.
        """
        if self.user is not None:
            return self.user.get_full_name()
        else:
            return self.user_name

    @property
    def email(self):
        """Returns the stored user email.
        """
        if self.user is not None:
            return self.user.email
        else:
            return self.user_email
