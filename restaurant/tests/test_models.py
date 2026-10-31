from django.test import TestCase

from restaurant.models import Booking, MenuItem


class MenuItemTest(TestCase):
    def test_get_item(self):
        item = MenuItem.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(str(item), "IceCream : 80")

    def test_str_with_decimal_price(self):
        item = MenuItem.objects.create(title="Greek Salad", price="12.50", inventory=20)
        item.refresh_from_db()
        self.assertEqual(str(item), "Greek Salad : 12.50")


class BookingModelTest(TestCase):
    def test_booking_creation(self):
        booking = Booking.objects.create(name="Alice", no_of_guests=4, booking_date="2026-12-01T19:00:00Z")
        self.assertEqual(Booking.objects.count(), 1)
        self.assertIn("Alice", str(booking))
