# django imports
from django.contrib import admin

# lfs imports
from reviews.models import Review

class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'user_name',
        'user_email',
        'score',
        'active',
        'ip_address',
        'creation_date',
    )

    list_filter = (
        'creation_date',
        'active',
        'score',
    )

    search_fields = (
        'user_name',
        'user_email',
        'comment',
        'ip_address',
    )


admin.site.register(Review, ReviewAdmin)
