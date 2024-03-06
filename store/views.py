from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,DetailView
from store.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from store.models import Product,BasketItem,Size,Order,OrderItems


#url; localhost:8000/register/
#method:get,post
#formclass:Registrationform
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signup")
        return render(request,"login.html",{"form":form})
    

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                login(request,user_object)
                return redirect("index")
        messages.error(request,"invalid credentials")
        return render(request,"login.html",{"form":form}) 

class IndexView(View):
    def get(self,request,*args,**kwargs):
        qs=Product.objects.all()
        return render(request,"index.html",{"data":qs})
    
# localhost8000/product

class ProductDetailView(DetailView):
    template_name="product_detail.html"
    model=Product
    context_object_name="data"

# class ProductDetailView(DetailView):
#     def get(self,request,*args,**kwargs):
#         id=kwargs.get("pk")
#         qs=Product.objects.get(id=id)
#         return render(request,"product_detail.html",{"data":qs}) 
    

class HomeView(TemplateView):
    template_name="base.html"


#add to basket
#localhost:8000/products/{id}/add_to_baskt 
#method post

class AddToBasketView(View):
    def post(self,request,*args,**kwargs):
        size=request.POST.get("size")
        size_obj=Size.objects.get(name=size)
        qty=request.POST.get("qty")
        id=kwargs.get("pk")
        product_obj=Product.objects.get(id=id)
        BasketItem.objects.create(

            size_object=size_obj,
            qty=qty,
            product_object=product_obj,
            basket_object=request.user.cart
        )
        return redirect("index")
    

#ceating basket item view
    
class BasketItemListView(View):
    def get(self,request,*args,**kwargs):
        qs=request.user.cart.cartitem.filter(is_order_placed=False)

        return render(request,"cart_list.html",{"data":qs})
    

class BasketItemRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        basket_item_object=BasketItem.objects.get(id=id)
        basket_item_object.delete()
        return redirect ("basket-item")

class CartItemUpdateQuantityView(View):

    def post(self, request,*args,**kwargs):
        action=request.POST.get("counterbutton")
        print(action)
        id=kwargs.get("pk")
        basket_item_object=BasketItem.objects.get(id=id)
        if action=="+":
            basket_item_object.qty+=1
            basket_item_object.save()
        else:
            basket_item_object.qty-=1
            basket_item_object.save()

        return redirect("basket-item")


class CheckOutView(View):
    
    def get(self,request,*args,**kwargs):
        return render(request,"checkout.html")
    
    def post(self,request,*args,**kwargs):
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        address=request.POST.get("address")

        #creating order_instance
        order_obj=Order.objects.create(
            user_object=request.user,
            delivery_address=address,
            phone=phone,
            email=email,
            total=request.user.cart.basket_total
        )

        #creating order item instance
        try:
            basket_items=request.user.cart.cart_items
            for bi in basket_items:
                OrderItems.objects.create(
                    order_object=order_obj,
                    basket_item_object=bi,

                )
                bi.is_order_placed=True
                bi.save()
        except:
            order_obj.delete
        
        finally:
            
            return redirect("index")
    


# class OrderSummeryView(View):
#     def get(self,request,*args,**kwargs):





    


