from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['member', 'inventory']

class CancelBookingSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()