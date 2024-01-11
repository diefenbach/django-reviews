from django.urls import re_path
from reviews import views


urlpatterns = [
    re_path(r"^add/(?P<content_type_id>\d*)/(?P<content_id>\d*)/$", views.add_form, name="reviews_add"),
    re_path(r"^preview/$", views.preview, name="reviews_preview"),
    re_path(r"^re-edit/$", views.reedit_or_save, name="reviews_reedit"),
    re_path(r"^thank-you/$", views.thank_you, name="reviews_thank_you"),
    re_path(r"^already-rated/$", views.already_rated, name="reviews_already_rated"),
]
