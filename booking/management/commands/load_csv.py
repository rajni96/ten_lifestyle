import csv
from django.core.management.base import BaseCommand
from booking.models import Inventory, Member
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Upload inventory or members from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)
        parser.add_argument("model_type", type=str, choices=["members", "inventory"])

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        model_type = kwargs["model_type"]

        if model_type == "members":
            self.load_members(file_path)
        elif model_type == "inventory":
            self.load_inventory(file_path)

    def load_members(self, file_path):
        members = []
        with open(file_path, newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    member = Member(
                        name=row["name"],
                        surname=row["surname"],
                        booking_count=row["booking_count"],
                        date_joined=row["date_joined"],
                    )
                    members.append(member)
                except KeyError as e:
                    self.stdout.write(
                        self.style.ERROR(f"Missing key in members CSV: {e}")
                    )
                    continue  # Skip this row if a key is missing

        if members:
            try:
                Member.objects.bulk_create(members)
                self.stdout.write(self.style.SUCCESS("Successfully uploaded members."))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f"Failed to upload members: {e}"))

    def load_inventory(self, file_path):
        inventory_items = []
        with open(file_path, newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    item = Inventory(
                        title=row["title"],
                        description=row["description"],
                        remaining_count=row["remaining_count"],
                        expiration_date=row["expiration_date"],
                    )
                    inventory_items.append(item)
                except KeyError as e:
                    self.stdout.write(
                        self.style.ERROR(f"Missing key in inventory CSV: {e}")
                    )
                    continue  # Skip this row if a key is missing

        if inventory_items:
            try:
                Inventory.objects.bulk_create(inventory_items)
                self.stdout.write(
                    self.style.SUCCESS("Successfully uploaded inventory.")
                )
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f"Failed to upload inventory: {e}"))
