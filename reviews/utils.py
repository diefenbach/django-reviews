# django imports
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection

# review imports
from reviews.models import Review


def get_best_rated():
    """Returns the best rated instance for all models.
    """
    cursor = connection.cursor()
    cursor.execute("""SELECT avg(score), content_type_id, content_id
                      FROM reviews_review
                      WHERE active=%s
                      GROUP BY content_id
                      ORDER BY score DESC""", [True])

    try:
        score, content_type_id, content_id = cursor.fetchone()
        ctype = ContentType.objects.get_for_id(content_type_id)
        content = ctype.model_class().objects.get(pk=content_id)
        return content, score
    except (TypeError, ObjectDoesNotExist):
        return None


def get_best_rated_for_model(instance):
    """Returns the best rated instance for given model or instance of a model.
    """
    ctype = ContentType.objects.get_for_model(instance)

    cursor = connection.cursor()
    cursor.execute("""SELECT avg(score), content_id
                      FROM reviews_review
                      WHERE content_type_id=%s
                      AND active=%s
                      GROUP BY content_id
                      ORDER BY score DESC""", [ctype.id, True])

    try:
        score, content_id = cursor.fetchone()
        content = ctype.model_class().objects.get(pk=content_id)
        return content, score
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
    # TODO: Check Django 1.1's aggregation
    ctype = ContentType.objects.get_for_model(instance)
    cursor = connection.cursor()
    cursor.execute("""SELECT avg(score), count(*)
                      FROM reviews_review
                      WHERE content_type_id=%s
                      AND content_id=%s
                      AND active=%s""", [ctype.id, instance.id, True])

    return cursor.fetchone()


def has_rated(request, instance):
    """Returns True if the current user has already rated for the given
    instance.
    """
    ctype = ContentType.objects.get_for_model(instance)

    try:
        if request.user.is_authenticated():
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
