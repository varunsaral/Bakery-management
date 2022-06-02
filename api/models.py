from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Custom user Model manager
class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None):

        # Creates and saves a User with the given email, name and password.

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, password2=None):
        # Create superuser with email , name and password
        user = self.create_user(
            email,
            name=name,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# Custom User Model
class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Ingredients(models.Model):
    item_name = models.CharField(max_length=255)
    item_cost_price = models.IntegerField()
    item_selling_price = models.IntegerField()
    item_quantity = models.IntegerField()


class BakeryItems(models.Model):
    item_name = models.CharField(max_length=255)
    item_ingredients = models.ManyToManyField(
        Ingredients, related_name="ingredient")
    item_description = models.TextField()


# Inventory for different admins
class Inventory(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="admins")


# Inventory items and Inventory owner for seperate inventories
class InventoryItems(models.Model):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="inventory")
    Ingredients = models.ManyToManyField(
        'Ingredients', related_name="ingredients")


class Cart(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="customer")


class CartOrders(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart')
    items = models.ManyToManyField(BakeryItems, related_name="bakeryitems")
    order_total = models.IntegerField()
