# django imports
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.flatpages.models import FlatPage
from django.contrib.sessions.backends.file import SessionStore
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client

# reviews imports
import reviews.utils
from reviews.models import Review


# Taken from "http://www.djangosnippets.org/snippets/963/"
class RequestFactory(Client):
    """
    """
    def request(self, **request):
        environ = {
            'HTTP_COOKIE': self.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
            'SERVER_PROTOCOL': 'HTTP/1.1',
        }
        environ.update(self.defaults)
        environ.update(request)
        return WSGIRequest(environ)


def create_request(user=None):
    """
    """
    rf = RequestFactory()
    request = rf.get('/')
    request.session = SessionStore()
    if user:
        request.user = user
    else:
        request.user = User(first_name="John Doe", email="john@doe.com")

    return request


class ReviewsModelsTestCase(TestCase):
    """
    """
    def setUp(self):
        """
        """
        # Create a dummy page to test
        self.page = FlatPage.objects.create(url="/test/", title="Test")

    def test_review_defaults(self):
        """
        """
        review = Review.objects.create(content=self.page)

        self.assertEqual(review.content, self.page)
        self.assertEqual(review.score, 3.0)
        self.assertEqual(review.comment, "")
        self.assertEqual(review.active, False)
        self.assertEqual(review.ip_address, None)
        self.assertEqual(review.user, None)
        self.assertEqual(review.session_id, None)
        self.assertEqual(review.user_name, "")
        self.assertEqual(review.user_email, "")

    def test_review_methods(self):
        """
        """
        review = Review.objects.create(
            content=self.page,
            user_name="Jane Doe",
            user_email="jane@doe.com",
        )

        self.assertEqual(review.name, "Jane Doe")
        self.assertEqual(review.email, "jane@doe.com")

        review.user = User(first_name="John", last_name="Doe", email="john@doe.com")

        self.assertEqual(review.name, "John Doe")
        self.assertEqual(review.email, "john@doe.com")

    def test_review_manager(self):
        """
        """
        review_1 = Review.objects.create(content=self.page, creation_date="2009-10-16")
        review_2 = Review.objects.create(content=self.page, creation_date="2009-10-15")

        # all is providing all reviews
        result = Review.objects.all()
        self.assertEqual(len(result), 2)

        # active is providing just the active ones
        result = Review.objects.active()
        self.assertEqual(len(result), 0)

        review_1.active = True
        review_1.save()

        # active is providing just the active ones
        result = Review.objects.active()
        self.assertEqual(len(result), 1)

        review_2.active = True
        review_2.save()

        # active is providing just the active ones
        result = Review.objects.active()
        self.assertEqual(len(result), 2)

    def test_review_ordering(self):
        """
        """
        Review.objects.create(content=self.page, id=1)
        Review.objects.create(content=self.page, id=2)
        Review.objects.create(content=self.page, id=3)

        # Last in first out
        result = [r.id for r in Review.objects.all()]
        self.assertEqual(result, [3, 2, 1])


class ReviewsViewsTestCase(TestCase):
    """
    """
    def setUp(self):
        """
        """
        # Create a dummy page to test
        self.page = FlatPage.objects.create(url="/test/", title="Test")

    def test_add_form(self):
        """
        """
        ctype = ContentType.objects.get_for_model(self.page)
        url = reverse("reviews_add", kwargs={"content_type_id": ctype.id, "content_id": self.page.id})

        # The result has to ``Preview`` within it
        result = self.client.get(url)
        self.assertContains(result, "Preview", status_code=200)

        # switching ot no preview
        settings.REVIEWS_SHOW_PREVIEW = False

        # The result must not have ``Preview`` within it
        result = self.client.get(url)
        self.assertNotContains(result, "Preview", status_code=200)


class PortletsUtilsTestCase(TestCase):
    """
    """
    def setUp(self):
        """
        """
        # Create a dummy page to test
        self.page = FlatPage.objects.create(url="/test/", title="Test")

    def test_get_average_for_instance(self):
        """
        """
        # Add a review to the page
        self.review = Review.objects.create(content=self.page, score=4.0)

        # By default the review is not active so there is no average rating
        average = reviews.utils.get_average_for_instance(self.page)
        self.assertEqual(average, (None, 0))

        # Make the review active
        self.review.active = True
        self.review.save()

        average = reviews.utils.get_average_for_instance(self.page)
        self.assertEqual(average, (4.0, 1))

        # Now we add another one
        Review.objects.create(content=self.page, score=2.0, active=True)

        average = reviews.utils.get_average_for_instance(self.page)
        self.assertEqual(average, (3.0, 2))

    def test_get_reviews_for_instance(self):
        """
        """
        # Add a review to the page
        self.review = Review.objects.create(content=self.page, score=4.0)

        # By default the review is not active so there is no average rating
        result = reviews.utils.get_reviews_for_instance(self.page)
        self.assertEqual(len(result), 0)

        # Make the review active
        self.review.active = True
        self.review.save()

        result = reviews.utils.get_reviews_for_instance(self.page)
        self.assertEqual(len(result), 1)

        # Now we add another one
        Review.objects.create(content=self.page, score=2.0, active=True)

        result = reviews.utils.get_reviews_for_instance(self.page)
        self.assertEqual(len(result), 2)

    def test_get_best_rated_for_model(self):
        """
        """
        # Create some dummy pages
        self.page_1 = FlatPage.objects.create(url="/test-1/", title="Test 1")

        # There are no reviews for pages, so it should return None
        result = reviews.utils.get_best_rated_for_model(self.page)
        self.assertEqual(result, None)

        # Start to add reviews
        Review.objects.create(content=self.page_1, score=4.0, active=True)

        self.page_2 = FlatPage.objects.create(url="/test-2/", title="Test 2")
        Review.objects.create(content=self.page_2, score=3.0, active=True)

        # At first page 1 is best
        result = reviews.utils.get_best_rated_for_model(self.page_1)
        self.assertEqual(result[0], self.page_1)

        # Adding one more review to page 2, but page 1 is still the best
        Review.objects.create(content=self.page_2, score=4.0, active=True)
        result = reviews.utils.get_best_rated_for_model(self.page_1)
        self.assertEqual(result[0], self.page_1)

        # Adding one more review to page 2. Now page 2 is the best rated
        Review.objects.create(content=self.page_2, score=6.0, active=True)
        result = reviews.utils.get_best_rated_for_model(self.page_1)
        self.assertEqual(result[0], self.page_2)

    def test_get_best_rated(self):
        """
        """
        # Create some dummy pages
        self.page_1 = FlatPage.objects.create(url="/test-1/", title="Test 1")

        # There are no reviews for pages, so it should return None
        result = reviews.utils.get_best_rated()
        self.assertEqual(result, None)

        # Start to add reviews
        Review.objects.create(content=self.page_1, score=4.0, active=True)

        self.page_2 = FlatPage.objects.create(url="/test-2/", title="Test 2")
        Review.objects.create(content=self.page_2, score=3.0, active=True)

        # At first page 1 is best
        result = reviews.utils.get_best_rated()
        self.assertEqual(result[0], self.page_1)

        # Adding one more review to page 2, but page 1 is still the best
        Review.objects.create(content=self.page_2, score=4.0, active=True)
        result = reviews.utils.get_best_rated()
        self.assertEqual(result[0], self.page_1)

        # Adding one more review to page 2. Now page 2 is the best rated
        Review.objects.create(content=self.page_2, score=6.0, active=True)
        result = reviews.utils.get_best_rated()
        self.assertEqual(result[0], self.page_2)

    def test_has_rated(self):
        """
        """
        request = create_request()
        request.user = AnonymousUser()

        # Create some dummy pages
        self.page_1 = FlatPage.objects.create(url="/test-1/", title="Test 1")
        self.page_2 = FlatPage.objects.create(url="/test-2/", title="Test 2")

        # At first nobody has rated
        self.assertEqual(reviews.utils.has_rated(request, self.page_1), False)
        self.assertEqual(reviews.utils.has_rated(request, self.page_2), False)

        # Rate for page 1
        Review.objects.create(content=self.page_1, score=6.0, active=True, session_id=request.session.session_key)
        self.assertEqual(reviews.utils.has_rated(request, self.page_1), True)
        self.assertEqual(reviews.utils.has_rated(request, self.page_2), False)

        # Rate for page 2
        Review.objects.create(content=self.page_2, score=6.0, active=True, session_id=request.session.session_key)
        self.assertEqual(reviews.utils.has_rated(request, self.page_1), True)
        self.assertEqual(reviews.utils.has_rated(request, self.page_2), True)
