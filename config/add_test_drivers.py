import random
from faker import Faker
from driver.models import Driver  # Change 'myapp' to your actual app name

fake = Faker()

TARIFF_CHOICES = ["Standard", "Comfort", "Business", "Premium"]

drivers = []

for _ in range(100):
    phone_number = f"+9989{random.randint(10_000_000, 99_999_999)}"  # Uzbek phone format
    full_name = fake.name()
    car_model = random.choice(["Chevrolet Spark", "Toyota Camry", "Hyundai Sonata", "Kia Sportage"])
    car_plate = f"{random.randint(100, 999)} {random.choice('ABCDEF')} {random.randint(10, 99)}"
    tariff = random.choice(TARIFF_CHOICES)
    balance = random.randint(10_000, 1_000_000)  # Random balance from 10k to 1M

    drivers.append(Driver(
        phone_number=phone_number,
        full_name=full_name,
        car_model=car_model,
        car_plate=car_plate,
        tariff=tariff,
        balance=balance
    ))

# Bulk insert drivers
Driver.objects.bulk_create(drivers)

print("✅ 100 test drivers added successfully!")
