from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from restaurant.models import MenuItem
from restaurant.serializers import MenuSerializer


class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        MenuItem.objects.create(title="IceCream", price=80, inventory=100)
        MenuItem.objects.create(title="Pizza", price=150, inventory=40)
        MenuItem.objects.create(title="Greek Salad", price="12.50", inventory=25)

    def test_getall(self):
        response = self.client.get("/restaurant/menu/")
        items = MenuItem.objects.all()
        serializer = MenuSerializer(items, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)


class BookingAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="tester", password="StrongPass123!")
        self.token = Token.objects.create(user=self.user)

    def test_booking_requires_token(self):
        self.assertEqual(self.client.get("/restaurant/booking/tables/").status_code, 401)

    def test_booking_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        payload = {"name": "Bob", "no_of_guests": 2, "booking_date": "2026-12-05T20:00:00Z"}
        created = self.client.post("/restaurant/booking/tables/", payload, format="json")
        self.assertEqual(created.status_code, 201)
        listing = self.client.get("/restaurant/booking/tables/")
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(len(listing.data), 1)

    def test_djoser_login_returns_token(self):
        response = self.client.post(
            "/auth/token/login/", {"username": "tester", "password": "StrongPass123!"}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("auth_token", response.data)
