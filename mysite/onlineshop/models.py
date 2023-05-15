from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Status(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=50)


class Customer(models.Model):
    user = models.OneToOneField(to=User, verbose_name="Vartotojas", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Vardas", max_length=200, null=True)
    email = models.CharField(verbose_name="el.paštas", max_length=200)


class Product(models.Model):
    name = models.CharField(verbose_name="Produkto pavadinimas", max_length=200)
    price = models.FloatField(verbose_name="Kaina")
    # digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(verbose_name="Nuotrauka", null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(to=Customer, verbose_name="Klientas", on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(verbose_name="Užsakymo data", auto_now_add=True)
    complete = models.BooleanField(verbose_name="užbaigta", default=False)
    transaction_id = models.CharField(verbose_name="operacijos id", max_length=100, null=True)
    status = models.ForeignKey(to="Status", verbose_name="Būsena", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(to=Product, verbose_name="Produktas", on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(to=Order, verbose_name="Užsakymas", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(verbose_name="Kiekis", default=0, null=True, blank=True)
    date_added = models.DateTimeField(verbose_name="Pridėjimo data", auto_now_add=True)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(to=Customer, verbose_name="Klientas", on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(to=Order, verbose_name="Užsakymas", on_delete=models.SET_NULL, null=True)
    address = models.CharField(verbose_name="Adresas", max_length=200, null=False)
    city = models.CharField(verbose_name="Miestas", max_length=200, null=False)
    state = models.CharField(verbose_name="Valstybė", max_length=200, null=False)
    zipcode = models.CharField(verbose_name="Pašto kodas", max_length=200, null=False)
    date_added = models.DateTimeField(verbose_name="Užsakymo data", auto_now_add=True)
