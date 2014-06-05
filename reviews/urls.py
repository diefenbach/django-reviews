from django.conf.urls import patterns, url

# Catalog
urlpatterns = patterns('reviews.views',
    url(r'^add/(?P<content_type_id>\d*)/(?P<content_id>\d*)$', "add_form", name="reviews_add"),
    url(r'^preview$', "preview", name="reviews_preview"),
    url(r'^reedit$', "reedit_or_save", name="reviews_reedit"),
    url(r'^thank-you$', "thank_you", name="reviews_thank_you"),
    url(r'^already-rated$', "already_rated", name="reviews_already_rated"),
)
