from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Status(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=50)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(to=User, verbose_name="Vartotojas", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Vardas", max_length=200, null=True)
    email = models.CharField(verbose_name="el.paštas", max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name="Produkto pavadinimas", max_length=200)
    price = models.FloatField(verbose_name="Kaina")
    # digital = models.BooleanField(default=False, null=True, blank=True)
    # image = models.ImageField(verbose_name="Nuotrauka", null=True, blank=True)
    photo = models.ImageField(verbose_name="Nuotrauka", upload_to="products", null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(to=Customer, verbose_name="Klientas", on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(verbose_name="Užsakymo data", auto_now_add=True)
    complete = models.BooleanField(verbose_name="užbaigta", default=False)
    transaction_id = models.CharField(verbose_name="pavedimo id", max_length=100, null=True)
    status = models.ForeignKey(to="Status", verbose_name="Būsena", on_delete=models.SET_NULL, null=True)

    def total(self):
        total = 0
        lines = self.lines.all()
        for line in lines:
            total += line.sum()
        return total

    def __str__(self):
        return f"{self.customer}, {self.date_ordered}, {self.status} "


class OrderItem(models.Model):
    product = models.ForeignKey(to=Product, verbose_name="Produktas", on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(to=Order, verbose_name="Užsakymas", on_delete=models.SET_NULL, null=True, related_name="lines")
    quantity = models.IntegerField(verbose_name="Kiekis", default=0, null=True, blank=True)
    date_added = models.DateTimeField(verbose_name="Pridėjimo data", auto_now_add=True)

    def sum(self):
        return self.product.price * self.quantity




class ShippingAddress(models.Model):
    customer = models.ForeignKey(to=Customer, verbose_name="Klientas", on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(to=Order, verbose_name="Užsakymas", on_delete=models.SET_NULL, null=True)
    address = models.CharField(verbose_name="Adresas", max_length=200, null=False)
    city = models.CharField(verbose_name="Miestas", max_length=200, null=False)
    state = models.CharField(verbose_name="Valstybė", max_length=200, null=False)
    zipcode = models.CharField(verbose_name="Pašto kodas", max_length=200, null=False)
    date_added = models.DateTimeField(verbose_name="Užsakymo data", auto_now_add=True)

    def __str__(self):
        return self.address
