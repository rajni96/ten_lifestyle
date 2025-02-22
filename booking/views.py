from rest_framework import status
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from booking.models import Booking
from booking.services import BookingService
from booking.serializers import BookingSerializer, CancelBookingSerializer


@api_view(["POST"])
def book_item(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        try:
            booking = BookingService.book_item(
                serializer.validated_data["member"],
                serializer.validated_data["inventory"],
            )
            return Response(
                {"message": "Booking successful.", "booking_id": booking.id},
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def cancel_booking(request):
    serializer = CancelBookingSerializer(data=request.data)
    if serializer.is_valid():
        try:
            BookingService.cancel_booking(serializer.validated_data["booking_id"])
            return Response({"message": "Booking canceled."}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
