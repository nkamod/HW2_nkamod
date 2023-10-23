from django.test import TestCase, Client
from .models import Movie, Genre, MoviesGenresLink, Show, Booking
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class MovieModelTest(TestCase):
    """
    Test class for movie model
    """
    def test_movie_creation(self):
        """
        Test function for creating movies in database
        """
        movie = Movie.objects.create(
            title="Test Movie",
            poster="test_poster.jpg",
            trailer="test_trailer.mp4",
            description="Test description",
            rating=8.5,
            cast="Actor1,Actor2",
            runtime=120,
            release_year=2022
        )

        # Check all the fields in movie model
        self.assertIsInstance(movie, Movie)
        self.assertEqual(movie.title, "Test Movie")
        self.assertEqual(movie.poster, "test_poster.jpg")
        self.assertEqual(movie.trailer, "test_trailer.mp4")
        self.assertEqual(movie.description, "Test description")
        self.assertEqual(movie.rating, 8.5)
        self.assertEqual(movie.cast, "Actor1,Actor2")
        self.assertEqual(movie.runtime, 120)
        self.assertEqual(movie.release_year, 2022)

class GenreModelTest(TestCase):
    """
    Test class for genre model
    """
    def test_genre_creation(self):
        """
        Test function for creating genres in database
        """
        genre = Genre.objects.create(title="Action")

        # Check all the fields in genre mode
        self.assertIsInstance(genre, Genre)
        self.assertEqual(genre.title, "Action")

class MoviesGenresLinkModelTest(TestCase):
    """
    Test class for movies genres link (Many to many relation)
    Since a movie can have multiple genres and a genre can be linked to multiple movies we link them with many to many relation.
    This relation allows us to sort the movies by genre. 
    """
    def test_movies_genres_link_creation(self):
        """
        Test function for movies genres link
        """
        
        # Create a movie object
        movie = Movie.objects.create(
            title="Test Movie",
            poster="test_poster.jpg",
            trailer="test_trailer.mp4",
            description="Test description",
            rating=8.5,
            cast="Actor1,Actor2",
            runtime=120,
            release_year=2022
        )
        
        # Create a genre object
        genre = Genre.objects.create(title="Action")
        
        # Link movies and genres together
        movie_genre_link = MoviesGenresLink.objects.create(
            movie=movie,
            genre=genre
        )

        # Check all the feilds in the link
        self.assertIsInstance(movie_genre_link, MoviesGenresLink)
        self.assertEqual(movie_genre_link.movie.title, "Test Movie")
        self.assertEqual(movie_genre_link.genre.title, "Action")

class ShowModelTest(TestCase):
    """
    Test class for show model
    """
    def test_show_creation(self):
        """
        Test function for creating shows in database,
        Since each movie can have multiple shows in a day, we use one to many relation. From movies(1) to shows(M)
        """

        # Create a movie object
        movie = Movie.objects.create(
            title="Test Movie",
            poster="test_poster.jpg",
            trailer="test_trailer.mp4",
            description="Test description",
            rating=8.5,
            cast="Actor1,Actor2",
            runtime=120,
            release_year=2022
        )

        # Create a show object and link it to the movie, here show stores the primary key of movie
        show = Show.objects.create(
            timing=timezone.now(),
            price=10.5,
            movie=movie
        )

        # Test all the fields for show
        self.assertIsInstance(show, Show)
        self.assertEqual(show.movie.title, "Test Movie")
        self.assertEqual(show.price, 10.5)

class BookingModelTest(TestCase):
    """
    Test class for booking model
    """
    def test_booking_creation(self):
        """
        Test function for creating booking in database
        The bookings model is linked with the shows, where shows are linked to movies,
        Again, the relationship between shows(1) and bookings(M) are one to many
        """

        # Bookings are done by user hence we create a test user
        user = User.objects.create_user(username='testuser', password='12345')

        # Since a show needs to be linked to a movie, we create a movie object before
        movie = Movie.objects.create(
            title="Test Movie",
            poster="test_poster.jpg",
            trailer="test_trailer.mp4",
            description="Test description",
            rating=8.5,
            cast="Actor1,Actor2",
            runtime=120,
            release_year=2022
        )

        # Bookings are done on show
        show = Show.objects.create(
            timing=timezone.now(),
            price=10.5,
            movie=movie
        )

        # Creaing booking by a perticular user for a perticular show
        booking = Booking.objects.create(
            date=timezone.now(),
            seat_no="A1",
            show=show,
            user=user
        )

        # Check all the fields
        self.assertIsInstance(booking, Booking)
        self.assertEqual(booking.seat_no, "A1")
        self.assertEqual(booking.show.movie.title, "Test Movie")
        self.assertEqual(booking.user.username, 'testuser')

class MovieTheaterBookingViewsTest(TestCase):
    """
    Test class for views testing
    """
    def setUp(self):
        """
        Function to setup test model objects for testing
        """
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.movie = Movie.objects.create(
            title="Test Movie",
            poster="test_poster.jpg",
            trailer="test_trailer.mp4",
            description="Test description",
            rating=8.5,
            cast="Actor1,Actor2",
            runtime=120,
            release_year=2022
        )
        self.show = Show.objects.create(timing=timezone.now(), price=10.5, movie_id=1)  # Adjust with appropriate data

    def test_index_view(self):
        """
        Test function to check if the base route "/" works and returns valid response
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_register_user_view(self):
        """
        Test function to check if register user "/signup" works and returns valid response
        """
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_login_user_view(self):
        """
        Test function to check if the login user  "/signin" works and retuns valid response
        """
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')

    def test_authenticated_user_can_access_view(self):
        """
        Test function to check if the bookings page is protected against unauthorized access
        """

        # Authenticate user
        self.client.login(username='testuser', password='testpassword')

        # Access the route
        response = self.client.get(reverse('bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings.html')

    def test_unauthenticated_user_redirected_to_login(self):
        """
        Test function to check redirects on unauthorized acces of perticular route
        """
        response = self.client.get(reverse('bookings'))
        self.assertRedirects(response, '/signin?next=/bookings')

    def test_register_user_view_with_valid_data(self):
        """
        Test function to check if registration route works properly for post requests and user is successfully created,
        on success this route redirects to signin page
        """
        response = self.client.post(reverse('signup'), {
            'username': 'testuser2',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertRedirects(response, reverse('signin'))

    def test_login_user_view_with_valid_credentials(self):
        """
        Test function to check if login route works properly for post requests and user is successfully logged in.
        on success this route redirects to index page i.e. home page
        """
        response = self.client.post(reverse('signin'), {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertRedirects(response, reverse('index'))

    def test_login_user_view_with_invalid_credentials(self):
        """
        Test function to to check the reponse of the signin route on invalid credentials,
        It should remain on the same page
        """
        response = self.client.post(reverse('signin'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_book_show(self):
        """
        Test function to check if authenticated users can book the tickets for movie for a perticular show
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('book_show'), data={"pk": 1, "selectedSeats": ["A1", "B2"]}, content_type="application/json")
        self.assertEqual(response.status_code, 200)