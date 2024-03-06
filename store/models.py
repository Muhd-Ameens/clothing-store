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

    @property
    def cart_items(self):
        return self.cartitem.filter(is_order_placed=False)
    @property
    def cart_item_count(self):
        return self.cart_items.count()
    
    @property
    def basket_total(self):
        basket_items=self.cart_items
        if basket_items:
            total=sum([bi.item_total for bi in basket_items])
            return total
        return 0


class BasketItem(models.Model):
    product_object=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.PositiveIntegerField(default=1)
    basket_object=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name="cartitem")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    size_object=models.ForeignKey(Size,on_delete=models.CASCADE,null=True)
    is_order_placed=models.BooleanField(default=False)
    
    @property
    def item_total(self):
        return self.qty*self.product_object.price


def create_basket(sender,instance,created,**kwargs):
    # created=T|F
    # sender=user
    # instance=the user
    if created:
        Basket.objects.create(owner=instance)

post_save.connect(create_basket,sender=User)

class Order(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="purchase")
    delivery_address=models.CharField(max_length=200)
    phone=models.CharField(max_length=12)
    email=models.CharField(max_length=200,null=True)
    is_paid=models.BooleanField(default=False)
    total=models.PositiveIntegerField()

class OrderItems(models.Model):
    order_object=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="purchaseitems")
    basket_item_object=models.ForeignKey(BasketItem,on_delete=models.CASCADE)
    option=(
        ("order-placed","order-placed"),
        ("intransit","intransit"),
        ("dispatched","dispatched"),
        ("delivered","delivered"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=200,choices=option,default="order-placed")