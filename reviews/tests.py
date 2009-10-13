# django imports
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

# reviews imports
import reviews.utils
from reviews.models import Review

class DummySession(object):
    session_key = "42"

class DummyRequest(object):
    def __init__(self, method="POST", user=None):
        self.user = user
        self.method = method
        self.session = DummySession()

class UtilsTestCase(TestCase):
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
        self.review = Review.objects.create(content=self.page, score = 4.0)

        # By default the review is not active so there is no average rating
        average = reviews.utils.get_average_for_instance(self.page)
        self.assertEqual(average, (None, 0))

        # Make the review active
        self.review.active = True
        self.review.save()

        average = reviews.utils.get_average_for_instance(self.page)
        self.assertEqual(average, (4.0, 1))

        # Now we add another one
        Review.objects.create(content=self.page, score = 2.0, active = True)

        average = reviews.utils.get_average_for_instance(self.page)
        self.assertEqual(average, (3.0, 2))

    def test_get_reviews_for_instance(self):
        """
        """
        # Add a review to the page
        self.review = Review.objects.create(content=self.page, score = 4.0)

        # By default the review is not active so there is no average rating
        result = reviews.utils.get_reviews_for_instance(self.page)
        self.assertEqual(len(result), 0)

        # Make the review active
        self.review.active = True
        self.review.save()

        result = reviews.utils.get_reviews_for_instance(self.page)
        self.assertEqual(len(result), 1)

        # Now we add another one
        Review.objects.create(content=self.page, score = 2.0, active = True)

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
        Review.objects.create(content=self.page_1, score = 4.0, active=True)

        self.page_2 = FlatPage.objects.create(url="/test-2/", title="Test 2")
        Review.objects.create(content=self.page_2, score = 3.0, active=True)

        # At first page 1 is best
        result = reviews.utils.get_best_rated_for_model(self.page_1)
        self.assertEqual(result[0], self.page_1)

        # Adding one more review to page 2, but page 1 is still the best
        Review.objects.create(content=self.page_2, score = 4.0, active=True)
        result = reviews.utils.get_best_rated_for_model(self.page_1)
        self.assertEqual(result[0], self.page_1)

        # Adding one more review to page 2. Now page 2 is the best rated
        Review.objects.create(content=self.page_2, score = 6.0, active=True)
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
        Review.objects.create(content=self.page_1, score = 4.0, active=True)

        self.page_2 = FlatPage.objects.create(url="/test-2/", title="Test 2")
        Review.objects.create(content=self.page_2, score = 3.0, active=True)

        # At first page 1 is best
        result = reviews.utils.get_best_rated()
        self.assertEqual(result[0], self.page_1)

        # Adding one more review to page 2, but page 1 is still the best
        Review.objects.create(content=self.page_2, score = 4.0, active=True)
        result = reviews.utils.get_best_rated()
        self.assertEqual(result[0], self.page_1)

        # Adding one more review to page 2. Now page 2 is the best rated
        Review.objects.create(content=self.page_2, score = 6.0, active=True)
        result = reviews.utils.get_best_rated()
        self.assertEqual(result[0], self.page_2)
        
    def test_has_rated(self):
        """
        """
        user = AnonymousUser()
        # Create dummy request
        request = DummyRequest(user=user)
        
        # Create some dummy pages
        self.page_1 = FlatPage.objects.create(url="/test-1/", title="Test 1")
        self.page_2 = FlatPage.objects.create(url="/test-2/", title="Test 2")
                
        # At first nobody has rated        
        self.assertEqual(reviews.utils.has_rated(request, self.page_1), False)        
        self.assertEqual(reviews.utils.has_rated(request, self.page_2), False)
        
        # Rate for page 1
        Review.objects.create(content=self.page_1, score = 6.0, active=True, session_id=request.session.session_key)
        self.assertEqual(reviews.utils.has_rated(request, self.page_1), True)
        self.assertEqual(reviews.utils.has_rated(request, self.page_2), False)

        # Rate for page 2        
        Review.objects.create(content=self.page_2, score = 6.0, active=True, session_id=request.session.session_key)
        self.assertEqual(reviews.utils.has_rated(request, self.page_1), True)
        self.assertEqual(reviews.utils.has_rated(request, self.page_2), True)