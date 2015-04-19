# django imports
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms.util import ErrorList
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

# reviews imports
import reviews.signals
from reviews import utils as reviews_utils
from reviews.models import Review
from reviews.settings import SCORE_CHOICES


class ReviewAddForm(ModelForm):
    """Form to add a review.
    """
    class Meta:
        model = Review
        fields = ("user_name", "user_email", "comment", "score")

    def clean(self):
        """
        """
        # For an anonymous user the name is required. Please note that the
        # request has to be passed explicitely to the form object (see add_form)
        msg = _(u"This field is required")

        if self.request.user.is_anonymous():
            if settings.REVIEWS_IS_NAME_REQUIRED:
                if self.cleaned_data.get("user_name", "") == "":
                    self._errors["user_name"] = ErrorList([msg])
            if settings.REVIEWS_IS_EMAIL_REQUIRED:
                if self.cleaned_data.get("user_email", "") == "":
                    self._errors["user_email"] = ErrorList([msg])

        return self.cleaned_data


def add_form(request, content_type_id, content_id, template_name="reviews/review_form.html"):
    """Displays the form to add a review. Dispatches the POST request of the
    form to save or reedit.
    """
    ctype = ContentType.objects.get_for_id(content_type_id)
    object = ctype.get_object_for_this_type(pk=content_id)

    if reviews_utils.has_rated(request, object):
        return HttpResponseRedirect(reverse("reviews_already_rated"))

    scores = []
    for i, score in enumerate(SCORE_CHOICES):
        scores.append({
            "title": score[0],
            "value": score[0],
            "z_index": 10 - i,
            "width": (i + 1) * 25,
        })

    if request.method == "POST":
        form = ReviewAddForm(data=request.POST)
        # "Attach" the request to the form instance in order to get the user
        # out of the request within the clean method of the form (see above).
        form.request = request
        if form.is_valid():
            if settings.REVIEWS_SHOW_PREVIEW:
                return preview(request)
            else:
                return save(request)
    else:
        form = ReviewAddForm()

    return render_to_response(template_name, RequestContext(request, {
        "content_type_id": content_type_id,
        "content_id": content_id,
        "object": object,
        "form": form,
        "scores": scores,
        "show_preview": settings.REVIEWS_SHOW_PREVIEW,
    }))


def reedit(request, template_name="reviews/review_form.html"):

    """Displays a form to edit a review. This is used if a reviewer re-edits
    a review after she has previewed it.
    """
    # get object
    content_type_id = request.POST.get("content_type_id")
    content_id = request.POST.get("content_id")

    ctype = ContentType.objects.get_for_id(content_type_id)
    object = ctype.get_object_for_this_type(pk=content_id)

    if reviews_utils.has_rated(request, object):
        return HttpResponseRedirect(reverse("reviews_already_rated"))

    scores = []
    for i, score in enumerate(SCORE_CHOICES):
        scores.append({
            "title": score[0],
            "value": score[0],
            "current": str(score[0]) == request.POST.get("score"),
            "z_index": 10 - i,
            "width": (i + 1) * 25,
        })

    form = ReviewAddForm(data=request.POST)
    return render_to_response(template_name, RequestContext(request, {
        "content_type_id": content_type_id,
        "content_id": content_id,
        "form": form,
        "scores": scores,
        "object": object,
        "show_preview": settings.REVIEWS_SHOW_PREVIEW,
    }))


def reedit_or_save(request):
    """Edits or saves a review dependend on which button has been pressed.
    """
    if request.POST.get("edit"):
        return reedit(request)
    else:
        return save(request)


def save(request):
    """Saves a review.
    """
    form = ReviewAddForm(data=request.POST)
    form.request = request
    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.content_type_id = request.POST.get("content_type_id")
        new_review.content_id = request.POST.get("content_id")
        new_review.session_id = request.session.session_key
        new_review.ip_address = request.META.get("REMOTE_ADDR")
        if request.user.is_authenticated():
            new_review.user = request.user
        new_review.active = not settings.REVIEWS_IS_MODERATED
        new_review.save()

        # Fire up signal
        reviews.signals.review_added.send(new_review)

        # Save object within session
        ctype = ContentType.objects.get_for_id(new_review.content_type_id)
        object = ctype.get_object_for_this_type(pk=new_review.content_id)
        request.session["last-rated-object"] = object

        return HttpResponseRedirect(reverse("reviews_thank_you"))


def preview(request, template_name="reviews/review_preview.html"):
    """Displays a preview of the review.
    """
    content_type_id = request.POST.get("content_type_id")
    content_id = request.POST.get("content_id")

    ctype = ContentType.objects.get_for_id(content_type_id)
    object = ctype.get_object_for_this_type(pk=content_id)

    if request.user.is_authenticated():
        name = request.user.get_full_name()
        email = request.user.email
    else:
        name = request.POST.get("user_name")
        email = request.POST.get("user_email")

    return render_to_response(template_name, RequestContext(request, {
        "score": float(request.POST.get("score", 0)),
        "object": object,
        "name": name,
        "email": email,
    }))


def thank_you(request, template_name="reviews/thank_you.html"):
    """Displays a thank you page.
    """
    if "last-rated-object" in request.session:
        object = request.session.get("last-rated-object")
        del request.session["last-rated-object"]
    else:
        object = None

    return render_to_response(template_name, RequestContext(request, {
        "object": object,
    }))


def already_rated(request, template_name="reviews/already_rated.html"):
    """Displays a alreday rated page.
    """
    return render_to_response(template_name, RequestContext(request))
