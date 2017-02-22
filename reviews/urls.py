from django.conf.urls import url
import reviews.views

# Catalog
urlpatterns = [
    url(r'^add/(?P<content_type_id>\d*)/(?P<content_id>\d*)/$', reviews.views.add_form, name="reviews_add"),
    url(r'^preview/$', reviews.views.preview, name="reviews_preview"),
    url(r'^re-edit/$', reviews.views.reedit_or_save, name="reviews_reedit"),
    url(r'^thank-you/$', reviews.views.thank_you, name="reviews_thank_you"),
    url(r'^already-rated/$', reviews.views.already_rated, name="reviews_already_rated"),
]
