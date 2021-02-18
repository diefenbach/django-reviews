# django imports
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.db.models import Count, Avg

# review imports
from reviews.models import Review


def get_best_rated():
    """Returns the best rated instance for all models.
    """
    result = Review.objects \
        .filter(active=True) \
        .values('content_type_id', 'content_id') \
        .annotate(Avg('score')) \
        .order_by('-score__avg') \
        .first()

    try:
        ctype = ContentType.objects.get_for_id(result['content_type_id'])
        content = ctype.model_class().objects.get(pk=result['content_id'])
        return content, result['score__avg']
    except (TypeError, ObjectDoesNotExist):
        return None


def get_best_rated_for_model(instance):
    """Returns the best rated instance for given model or instance of a model.
    """
    ctype = ContentType.objects.get_for_model(instance)

    result = Review.objects \
        .filter(content_type=ctype.id, active=True) \
        .values('content_id') \
        .annotate(Avg('score')) \
        .order_by('-score__avg') \
        .first()

    try:
        content = ctype.model_class().objects.get(pk=result['content_id'])
        return content, result['score__avg']
    except (TypeError, ObjectDoesNotExist):
        return None


def get_reviews_for_instance(instance):
    """Returns active reviews for given instance.
    """
    ctype = ContentType.objects.get_for_model(instance)
    return Review.objects.active().filter(content_type=ctype.id, content_id=instance.id)


def get_average_for_instance(instance):
    """Returns the average score and the amount of reviews for the given
    instance. Takes only active reviews into account.

    Returns (average, amount)
    """
    content_type = ContentType.objects.get_for_model(instance)
    query = Review.objects.filter(content_type=content_type.id, content_id=instance.id, active=True).aggregate(
        Avg('score'), Count('id'))

    return query.get('score__avg'), query.get('id__count')


def has_rated(request, instance):
    """Returns True if the current user has already rated for the given
    instance.
    """
    ctype = ContentType.objects.get_for_model(instance)

    try:
        if request.user.is_authenticated:
            Review.objects.get(
                content_type=ctype.id,
                content_id=instance.id,
                user=request.user
            )
        else:
            Review.objects.get(
                content_type=ctype.id,
                content_id=instance.id,
                session_id=request.session.session_key
            )
    except ObjectDoesNotExist:
        return False
    else:
        return True
