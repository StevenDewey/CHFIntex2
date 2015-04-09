import datetime
from django.db import models
from polymorphic import PolymorphicModel
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Address(models.Model):
    '''
        A mailing address (in the USA).
    '''
    street1 = models.TextField(max_length=200)
    street2 = models.TextField(max_length=200, null=True, blank=True)
    city = models.TextField(max_length=100)
    state = models.TextField(max_length=20)
    zip_code = models.TextField(max_length=20)
    country = models.TextField(max_length=100)

    class Meta:
        ordering = ['state', 'city', 'zip_code', 'street1', 'street2']
        verbose_name_plural = 'addresses'

    def __str__(self):
        return '{} {} {}, {}  {}'.format(self.street1, self.street2, self.city, self.state, self.zip_code)


class Photograph(models.Model):
    '''
        A photograph to be used as a user ID photo or a product photo.
    '''
    date_taken = models.DateTimeField()
    place_taken = models.TextField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    image = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.description


class User(AbstractUser):
    '''
        A user within the CHF system.  Extends the built-in AbstractUser, and so we'll
        need to indicate in our settings.py that this is the designated login user.
    '''
    phone = models.TextField(max_length=40, null=True, blank=True)
    security_question = models.TextField(max_length=200, null=True, blank=True)
    security_answer = models.TextField(max_length=200, null=True, blank=True)
    requires_reset = models.BooleanField(default=False)
    organization_name = models.TextField(max_length=200, null=True, blank=True)
    organization_type = models.TextField(max_length=40, null=True, blank=True)
    date_appointed_agent = models.DateField(null=True, blank=True)
    relationship = models.TextField(max_length=200, null=True, blank=True)
    emergency_contact = models.TextField(max_length=200, null=True, blank=True)
    emergency_phone = models.TextField(max_length=200, null=True, blank=True)
    emergency_relationship = models.TextField(max_length=200, null=True, blank=True)
    address = models.ForeignKey(Address, related_name='+', null=True, blank=True)
    photo = models.ForeignKey(Photograph, related_name='+', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Event(models.Model):
    '''
       An event 
    '''
    name = models.TextField(max_length=200)
    description = models.TextField(max_length=1000)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    map_file_name = models.TextField(max_length=200)
    venue_name = models.TextField(max_length=200, null=True)
    address = models.ForeignKey(Address, related_name='+', null=True)
    photo = models.ForeignKey(Photograph, null=True)


class ParticipantRole(models.Model):
    '''
        This class identifies the relationship between a user who is a participant and
        the area(s) in which s/he participates.
    '''
    participant = models.ForeignKey('User')
    area = models.ForeignKey('Area')
    name = models.TextField(max_length=200)
    type = models.TextField(max_length=40)


class Area(models.Model):
    '''
        An area of an event may represent an exhibit, a first aid station, or some other
        distinct element within the event.
    '''
    name = models.TextField(max_length=200)
    description = models.TextField(max_length=1000)
    place_number = models.PositiveIntegerField()
    coordinator = models.ForeignKey(User, related_name='coordinates', null=True)
    supervisor = models.ForeignKey(User, related_name='supervises', null=True)
    event = models.ForeignKey(Event)
    participants = models.ManyToManyField('User', through='ParticipantRole', null=True)
    photo = models.ForeignKey(Photograph, null=True)


class Order(models.Model):
    order_date = models.DateTimeField()
    phone = models.TextField()
    date_packed = models.DateTimeField(null=True)
    date_paid = models.DateTimeField(null=True)
    date_shipped = models.DateTimeField(null=True)
    tracking_number = models.TextField(max_length=50, null=True)
    ships_to = models.ForeignKey('Address', related_name='+')
    packed_by = models.ForeignKey('User', related_name='packedby_set', null=True, blank=True)
    payment_processed_by = models.ForeignKey('User', related_name='paymentprocessedby_set', null=True, blank=True)
    shipped_by = models.ForeignKey('User', related_name='shippedby_set', null=True, blank=True)
    handled_by = models.ForeignKey('User', related_name='handledby_set', null=True, blank=True)
    customer = models.ForeignKey('User', related_name='orders')



class LineItem(models.Model):
    '''
        Abstract base class for line items in an order.  A line item can be one
        of sale item, fee, rental item, or service item.
    '''
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order)

    class Meta:
        abstract = True


class Category(models.Model):
    '''
        Category within the product catalog.
    '''
    description = models.TextField(max_length=200)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.description


class ProductSpecification(models.Model):
    '''
        The specification of a product that is in our catalog.
    '''
    name = models.TextField(max_length=200)
    type = models.TextField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    manufacturer = models.TextField(max_length=80)
    average_cost = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.TextField(max_length=20)
    order_form_name = models.TextField(max_length=200, null=True)
    production_time = models.TextField(max_length=200, null=True)
    category = models.ForeignKey(Category, related_name='+')
    vendor = models.ForeignKey(User, null=True)
    photo = models.OneToOneField(Photograph, null=True)

    def __str__(self):

        return '{} {}'.format(self.name, self.price)


class StockedProduct(PolymorphicModel):
    '''
        A product in our inventory.  This concrete class represents bulk products
        that only need their quantity and location to be tracked.  There are concrete
        subclasses for serialized and rental products.
    '''
    quantity_on_hand = models.IntegerField()
    shelf_location = models.TextField(max_length=40)
    order_file = models.TextField(null=True)
    photo = models.ForeignKey(Photograph, null=True)
    product_specification = models.ForeignKey(ProductSpecification, related_name='+')

    def __str__(self):
        return '{}'.format(self.quantity_on_hand)


class SerializedProduct(StockedProduct):
    '''
        A specific item in our inventory, identified by a serial number.
        Quantity on hand is constrained to be at most one for a
        serialized product.  This is a concrete subclass of StockedProduct,
        and there is a concrete subclass of this class called RentalProduct.
    '''
    serial_number = models.TextField(max_length=100, unique=True, null=True)
    type = models.TextField(max_length=100)
    date_acquired = models.DateField(auto_now_add=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    for_sale = models.BooleanField(default=True)
    condition_new = models.BooleanField(default=True)
    notes = models.TextField()
    owner = models.ForeignKey(User, null=True)
    size = models.TextField(max_length=40, null=True)
    size_modifier = models.TextField(max_length=40, null=True)
    gender = models.TextField(max_length=40, null=True)
    color = models.TextField(max_length=40, null=True)
    pattern = models.TextField(max_length=40, null=True)
    start_year = models.PositiveIntegerField(null=True)
    end_year = models.PositiveIntegerField(null=True)
    note = models.TextField(null=True)

    def __str__(self):
        return '{} {} {}'.format(self.serial_number, self.type, self.status)


class RentalProduct(SerializedProduct):
    '''
        A specific item in our inventory that we are willing to rent.
    '''
    times_rented = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    replacement_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{} {} {}'.format(self.times_rented, self.price_per_day, self.replacement_price)


class RentalItem(LineItem):
    date_out = models.DateTimeField(auto_now_add=True)
    date_in = models.DateTimeField(null=True)
    date_due = models.DateTimeField()
    discount_percent = models.DecimalField(max_digits=3, decimal_places=2)
    rental_product = models.ForeignKey(RentalProduct, related_name='+')

    def __str__(self):
        return '{} {} {}'.format(self.date_out, self.date_due, self.date_in)


class Fee(LineItem):
    '''
        Abstract base class for the various fee types.  Concrete fee types
        include late and damage fees.  The maximum fee amount should be the purchase
        price of the rental product less the rental fee.
    '''
    waived = models.BooleanField(default=False)
    rental_item = models.ForeignKey(RentalItem, related_name='+')

    class Meta:
        abstract = True


class LateFee(Fee):
    '''
        A late fee for an item rental.  This is a concrete subclass of Fee.
        For now we use the daily rental price as the per-day late fee.
    '''
    days_late = models.PositiveIntegerField()

    def __str__(self):
        return '{} {} {}'.format(self.amount, self.days_late, self.waived)


class DamageFee(Fee):
    '''
        A damage fee for an item rental.  This is a concrete subclass of Fee.
    '''
    description = models.TextField()

    def __str__(self):
        return '{} {} {}'.format(self.amount, self.description, self.waived)


class SaleItem(LineItem):
    '''
        A sale item for either a bulk or a serialized product.
    '''
    quantity = models.IntegerField()
    product = models.ForeignKey(StockedProduct, related_name='+')

    def __str__(self):
        return '{} {}'.format(self.amount, self.quantity)


class ConfigurationParameters(models.Model):
    sales_tax_rate = models.DecimalField(max_digits=5, decimal_places=4)

# class Session(models.Model):
#     '''
#         A period of time a user is shopping online.
#         Expire_date is when the user's selections are deleted from memory
#     '''
#     session_key = models.TextField(max_length=100, unique=True)
#     expire_date = models.DateTimeField()
#     session_data = models.TextField(max_length=1000)
#     customer = models.ForeignKey(User)
#
# class ShoppingCart(models.Model):
#     '''
#         A bunch of items the user put into his/her cart.
#         They can come back to it later
#     '''
#     session = models.ForeignKey(Session)
#
class CartLineItem(models.Model):
    '''
        An item that has been added to a shopping cart
    '''
    quantity = models.PositiveIntegerField()
    stocked_product = models.ForeignKey(StockedProduct)
    user = models.ForeignKey(User)
    # shopping_cart = models.ForeignKey(ShoppingCart)

