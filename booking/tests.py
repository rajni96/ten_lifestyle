# booking/tests.py
from rest_framework import status
from rest_framework.test import APITestCase
from booking.models import Member, Inventory, Booking
from booking.services import BookingService
from django.urls import reverse


class BookingAPITests(APITestCase):
    def setUp(self):
        # Create a member and inventory for testing
        self.member = Member.objects.create(name="John", surname="Doe", booking_count=0)
        self.inventory = Inventory.objects.create(
            title="Test Item", description="A test item", remaining_count=5
        )

        self.valid_booking_data = {
            "member": self.member.id,
            "inventory": self.inventory.id,
        }
        self.invalid_booking_data = {
            "member": "",  # Invalid data
            "inventory": "",  # Invalid data
        }

    def test_book_item_success(self):
        url = reverse("book_item")  # Use the name from urls.py
        response = self.client.post(url, self.valid_booking_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("booking_id", response.data)

    def test_book_item_failure(self):
        url = reverse("book_item")  # Use the name from urls.py
        response = self.client.post(url, self.invalid_booking_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_booking_success(self):
        booking = BookingService.book_item(self.member, self.inventory)
        url = reverse("cancel_booking")  # Use the name from urls.py
        response = self.client.post(url, {"booking_id": booking.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Booking canceled.")

    def test_cancel_booking_not_found(self):
        url = reverse("cancel_booking")  # Use the name from urls.py
        response = self.client.post(
            url, {"booking_id": 9999}
        )  # Non-existent booking ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
