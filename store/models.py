from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Category(models.Model):
    name=models.CharField(max_length=200,unique=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    name=models.CharField(max_length=150,unique=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField(null=True)
    image=models.ImageField(upload_to="product_images",default="default.jpg",null=True,blank=True)
    category_object=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="item")
    size_object=models.ManyToManyField(Size)
    price=models.PositiveIntegerField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Basket(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)


class BasketItem(models.Model):
    product_object=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.PositiveIntegerField(default=1)
    basket_object=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name="cartitem")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)


def create_basket(sender,instance,created,**kwargs):
    # created=T|F
    # sender=user
    # instance=the user
    if created:
        Basket.objects.create(owner=instance)

post_save.connect(create_basket,sender=User)