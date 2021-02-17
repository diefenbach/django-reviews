from django.conf.urls import url
from reviews import views


urlpatterns = [
    url(r'^add/(?P<content_type_id>\d*)/(?P<content_id>\d*)/$', views.add_form, name="reviews_add"),
    url(r'^preview/$', views.preview, name="reviews_preview"),
    url(r'^re-edit/$', views.reedit_or_save, name="reviews_reedit"),
    url(r'^thank-you/$', views.thank_you, name="reviews_thank_you"),
    url(r'^already-rated/$', views.already_rated, name="reviews_already_rated"),
]
