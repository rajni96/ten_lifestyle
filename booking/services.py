from django.core.exceptions import ValidationError
from .models import Member, Inventory, Booking


class BookingService:
    @staticmethod
    def book_item(member, inventory):

        if not member.can_book():
            raise ValidationError("Maximum bookings reached.")

        if inventory.remaining_count <= 0:
            raise ValidationError("Inventory depleted.")

        booking = Booking(member=member, inventory=inventory)
        booking.save()

        member.booking_count += 1
        member.save()

        inventory.remaining_count -= 1
        inventory.save()

        return booking

    @staticmethod
    def cancel_booking(booking_id):
        booking = Booking.objects.get(id=booking_id)
        member = booking.member
        inventory = booking.inventory

        booking.delete()

        member.booking_count -= 1
        member.save()

        inventory.remaining_count += 1
        inventory.save()
