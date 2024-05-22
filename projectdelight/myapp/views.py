from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login,authenticate,logout
from django.views import View
import razorpay
import re
from .models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .forms import CustomerProfileForm
from django.contrib import messages
from django.conf import settings


def home(request):
    totalitem = 0
    wishlist_length = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"app/home.html",locals())

def about(request):
    totalitem = 0
    wishlist_length = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'app/about.html',locals())

def contact(request):
    totalitem = 0
    wishlist_length = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'app/contact.html',locals())

#for product
def product(request):
    totalitem = 0
    wishlist_length = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'app/products.html',locals())

# for dynamic product add
class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        wishlist_length = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,'app/category.html',locals())

#for category title
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        wishlist_length = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/category.html',locals())
    
#for product detail
class Productdetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        item_already_in_cart = Cart.objects.filter(
            Q(product=product.id) & Q(user=request.user)
        ).exists()
        item_already_in_wishlist = False
        item_already_in_wishlist = Wishlist.objects.filter(
            Q(products=product.id) & Q(user=request.user)
        ).exists()
        totalitem = 0
        wishlist_length = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/productdetail.html',locals())

#register
def register_user(request):
    context={}
    try:
        if request.method == "POST":
            un = request.POST["fusername"]
            em = request.POST['femail']
            ps1 = request.POST["fpassword1"]
            ps2 = request.POST["fpassword2"]
            
            if un=='' or em =='' or ps1 =='' or ps2=='':
                context['errmsg'] = "Fields cannot be empty"
                return render(request,'app/signup.html',context)
            elif len(ps1) < 8:
                context["errmsg"] = "Password must be at least 8 characters long"
                return render(request, 'app/signup.html', context)
            elif ps1 != ps2:
                context["errmsg"]="Password and confirm password didn't match"
                return render(request,'app/signup.html',context)
            # Validate email format
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", em):
                context["errmsg"] = "Invalid email format"
                return render(request, 'app/signup.html', context)
            
            # Check if email contains ".com"
            elif ".com" not in em:
                context["errmsg"] = "Email must contain .com"
                return render(request, 'app/signup.html', context)
            
            else:
                u = User.objects.create(username=un, email=em)
                u.set_password(ps1)
                u.save()
                context['success'] = "Register Successfully !!!"
                return redirect('login')
    except:
        context['errmsg']='User already exist'
        return render(request,'app/signup.html',context)
    return render(request,'app/signup.html')
def login_user(request):
    context={}
    if request.method == 'POST':
        un=request.POST['fusername']
        ps=request.POST['pass1']
        u = authenticate(request,username=un,password=ps)
        if u is not None:
            login(request, u)
            if Customer.objects.filter(user=request.user):
                return redirect('home')
            else:
                return redirect('profile')
        elif un=='' or ps=='':
            context['errmsg']="Fields cannot be empty"
            return render(request,'app/login.html',context)
        else:
            context['errmsg']="Invalid username and password"
            return render(request,'app/login.html',context)
    return render(request,'app/login.html')
def logout_user(request):
    logout(request)
    return redirect('login')

# profile form
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0
        wishlist_length = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user= request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
            return redirect('/address')
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/profile.html',locals())
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishlist_length = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'app/address.html',locals())
class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        totalitem = 0
        wishlist_length = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/updateaddress.html',locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect('address')
#cart 
def add_to_cart(request):
    if request.user.is_authenticated:
        user=request.user
        product_id=request.GET.get('prod_id')
        product=Product.objects.get(id=product_id)
        Cart(user=user,product=product).save()
        return redirect("/cart")
    else:
        return redirect('login')
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity * p.product.discounted_price
        amount=amount + value
    totalamount=amount + 40
    totalitem = 0
    wishlist_length = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'app/addtocart.html',locals())

def update_cart(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('increment_'):
                product_id = int(key.split('_')[1])
                cart_item = Cart.objects.filter(user=request.user, product__id=product_id).first()
                if cart_item:
                    cart_item.quantity += 1
                    cart_item.save()
                    messages.success(request, "Quantity increased successfully.")
                else:
                    messages.error(request, "Cart item not found.")
            elif key.startswith('decrement_'):
                product_id = int(key.split('_')[1])
                cart_item = Cart.objects.filter(user=request.user, product__id=product_id).first()
                if cart_item:
                    if cart_item.quantity > 1:
                        cart_item.quantity -= 1
                        cart_item.save()
                        messages.success(request, "Quantity decreased successfully.")
                    else:
                        cart_item.delete()
                        messages.success(request, "Item removed from cart.")
                else:
                    messages.error(request, "Cart item not found.")
    return redirect('showcart')

def remove_from_cart(request, product_id):
    cart_item = Cart.objects.filter(user=request.user, product__id=product_id).first()
    if cart_item:
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Cart item not found.")
    return redirect('showcart')


#checkout
class checkout(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount += value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount" : razoramount,"currency": "INR","receipt":"order_rcptid_12"}
        payment_response =client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status =='created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status = order_status
            )
            payment.save() 
        return render(request, 'app/checkout.html', locals()) 
    
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')    
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart_items = Cart.objects.filter(user=request.user)
    for cart_item in cart_items:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=cart_item.product,
            quantity=cart_item.quantity,
            payment=payment
        )
        cart_item.delete()
    return redirect("orders")
#buynow
#buy now
class BuyNowView(View):
    def get(self, request, product_id):
        if not request.user.is_authenticated:
            return redirect('login')
        product = get_object_or_404(Product, id=product_id)
        add = Customer.objects.filter(user=request.user)
        totalitem = 0
        wishlist_length = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        amount = product.discounted_price
        totalamount = amount + 40  # Assuming 40 is the shipping cost
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=request.user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        return render(request, 'app/buy_checkout.html', locals())

def buy_nowpayment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    product_id = request.GET.get('product_id')
    user = request.user
    customer = Customer.objects.filter(user=user).first()
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    product = Product.objects.get(id=product_id)
    OrderPlaced.objects.create(
        user=user,
        customer=customer,
        product=product,
        quantity=1,
        payment=payment
    )
    return redirect('order')
#orderscart
def orders_cart(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem =  len(Cart.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/order.html',locals())

#product search via category
def search_pr(request):
    query = request.GET["search"]
    totalitem = 0
    wishlist_length = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    products = Product.objects.filter(title__icontains=query)
    return render(request, "app/search.html", locals())



#wishlist items 
def add_to_wishlist(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    wishlist.products.add(product)
    totalitem = 0
    wishlist_length = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return redirect('wishlist_view')

def wishlist_view(request):
    wishlist = Wishlist.objects.get(user=request.user)
    totalitem = 0
    wishlist_length = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/wishlist.html', {'wishlist': wishlist})

def remove_from_wishlist(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.get(user=user)
    wishlist.products.remove(product)
    return redirect('wishlist_view')