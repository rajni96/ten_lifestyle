from django.db import models

# Create your models here.


class Member(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    booking_count = models.IntegerField()
    date_joined = models.DateTimeField(auto_now_add=True)

    MAX_BOOKINGS = 2

    class Meta:
        db_table = "member"

    def __str__(self):
        return self.name

    def can_book(self):
        return self.booking_count < self.MAX_BOOKINGS


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField()
    remaining_count = models.IntegerField()
    expiration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inventory"

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("cancelled", "Cancelled"),
    ]
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

    class Meta:
        db_table = "booking"

    def __str__(self):
        return self.name
