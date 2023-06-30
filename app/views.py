from django.http.request import QueryDict
from django.shortcuts import render, redirect
from django.views import View
from .models import CATEGORY_CHOICES, Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import CustomerSerializer, OrderPlacedSerializer,ProductSerializer,CartSerializer

@csrf_exempt
def customer(request):
    if request.method == "GET":
        regis = Customer.objects.all()
        serializer = CustomerSerializer(regis, many=True)
       
        labels = []
        data = []
        for i in serializer.data:
            labels.append(i["locality"])
        
        labels = [*set(labels)]
        for i in labels:
            count = 0
            for j in serializer.data:
                if j["locality"] == i:
                    count = count + 1
            data.append(count)

        return render(request, 'app/report_customer.html', { 'data': serializer.data, 'labels':labels, 'data_chart': data  })
    return HttpResponse("success")

@csrf_exempt
def product(request):
    if request.method == "GET":
        regis = Product.objects.all()
        # print("students = ", regis)
        serializer = ProductSerializer(regis, many=True)
        # print("serializer = ", serializer.data)

        labels = []
        data = []
        for i in serializer.data[:20]:
            labels.append(i["title"])
            data.append(i["selling_price"])

        return render(request, 'app/report_product.html', { 'data': serializer.data, 'labels':labels, 'data_chart': data  })
    return HttpResponse("success")

@csrf_exempt
def carts(request):
    if request.method == "GET":
        regis = Cart.objects.all()
        # print("students = ", regis)
        serializer = CartSerializer(regis, many=True)
        # print("serializer = ", serializer.data)
        return render(request, 'app/report_cart.html', { 'data': serializer.data })
    return HttpResponse("success")

@csrf_exempt
def orderplaced(request):
    if request.method == "GET":
        regis = OrderPlaced.objects.all()
        # print("students = ", regis)
        serializer = OrderPlacedSerializer(regis, many=True)
        # print("serializer = ", serializer.data)
        # return JsonResponse(serializer.data, safe=False, status=200)

        labels = ['Pending','On The Way','Delivered']
        data = []
        
        for i in labels:
            count = 0
            for j in serializer.data:
                if j["status"] == i:
                    count = count + 1
            data.append(count)

        return render(request, 'app/report_order.html', { 'data': serializer.data, 'labels':labels, 'data_chart': data   })

    # elif request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     serializer = RegistraionSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=201)
    #     return JsonResponse(serializer.errors, status=400)
    return HttpResponse("success")

class ProductView(View):
    def get(self, request):
        totalitem = 0
        Digestives = Product.objects.filter(category='d')
        HealthDrinks = Product.objects.filter(category='hd')
        FruitBeverages = Product.objects.filter(category='fb')
        HealthWellness = Product.objects.filter(category='hw')
        DietFood  = Product.objects.filter(category='df')
        OtherHealth  = Product.objects.filter(category='hp')
        BiscuitsCookies  = Product.objects.filter(category='bc')
        Spices = Product.objects.filter(category='s')
        DalPulses = Product.objects.filter(category='dp')
        EdibleOil = Product.objects.filter(category='eo')
        Sugar = Product.objects.filter(category='su')
        DryFruits = Product.objects.filter(category='fd')
        OtherFood = Product.objects.filter(category='fp')




        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'Digestives':Digestives, 'HealthDrinks':HealthDrinks,
                                                 'FruitBeverages':FruitBeverages, 'HealthWellness':HealthWellness,
                                                 'DietFood':DietFood, 'OtherHealth':OtherHealth, 'BiscuitsCookies':BiscuitsCookies,
                                                 'Spices':Spices, 'DalPulses':DalPulses, 'EdibleOil':EdibleOil,
                                                 'Sugar':Sugar, 'DryFruits':DryFruits, 'OtherFood':OtherFood,
                                                'totalitem':totalitem})


class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required
def add_to_cart(request):
    totalitem = 0
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return redirect('/cart',{'totalitem':totalitem})

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        #print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                tax=amount *0.12
                totalamount = (amount+tax + shipping_amount)
            if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
            return render(request,'app/addtocart.html',{'carts':cart, 'totalamount':totalamount, 'amount':amount,'totalitem':totalitem})
        else:
            if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
            return render(request, 'app/emptycart.html',{'totalitem':totalitem})


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            tax=amount *0.12
            amount+=tax

        data = {
            'quantity': c.quantity,
            'amount':amount,
            'totalamount' : amount + shipping_amount
            }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            amount +=amount *0.12
        data = {
            'quantity': c.quantity,
            'amount':amount,
            'totalamount' : amount + shipping_amount
            }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount 

        data = {
            'amount':amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)

@login_required
def buy_now(request):
    totalitem = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/buynow.html',{'totalitem':totalitem})

@login_required
def address(request):
    totalitem = 0
    add = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', {'add':add,'active':'btn-primary','totalitem':totalitem})

@login_required    
def orders(request):
    totalitem = 0
    op = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html', {'order_placed':op,'totalitem':totalitem})

def Digestives(request, data=None):
    totalitem = 0
    if data == None:
        Digestives = Product.objects.filter(category='d')
    elif data== 'Below':
                Digestives = Product.objects.filter(category='d').filter(discounted_price__lt=50)
    elif data== 'Above':
        Digestives = Product.objects.filter(category='d').filter(discounted_price__gt=50)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/Digestives.html', {'Digestives':Digestives,'totalitem':totalitem})

def HealthDrinks(request, data=None):
    totalitem = 0
    if data == None:
        HealthDrinks = Product.objects.filter(category='hd')
    elif data== 'Below':
                HealthDrinks = Product.objects.filter(category='hd').filter(discounted_price__lt=100)
    elif data== 'Above':
        HealthDrinks = Product.objects.filter(category='hd').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/HealthDrinks.html', {'HealthDrinks':HealthDrinks,'totalitem':totalitem})

def FruitBeverages(request, data=None):
    totalitem = 0
    if data == None:
        FruitBeverages = Product.objects.filter(category='fb')
    elif data== 'Below':
                FruitBeverages = Product.objects.filter(category='fb').filter(discounted_price__lt=100)
    elif data== 'Above':
        FruitBeverages = Product.objects.filter(category='fb').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/FruitBeverages.html', {'FruitBeverages':FruitBeverages,'totalitem':totalitem})

def HealthWellness(request, data=None):
    totalitem = 0
    if data == None:
        HealthWellness = Product.objects.filter(category='hw')
    elif data== 'Below':
                HealthWellness = Product.objects.filter(category='hw').filter(discounted_price__lt=100)
    elif data== 'Above':
        HealthWellness = Product.objects.filter(category='hw').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/HealthWellness.html', {'HealthWellness':HealthWellness,'totalitem':totalitem})

def DietFood(request, data=None):
    totalitem = 0
    if data == None:
        DietFood = Product.objects.filter(category='df')
    elif data== 'Below':
                DietFood = Product.objects.filter(category='df').filter(discounted_price__lt=100)
    elif data== 'Above':
        DietFood = Product.objects.filter(category='df').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/DietFood.html', {'DietFood':DietFood,'totalitem':totalitem})

def OtherHealth(request, data=None):
    totalitem = 0
    if data == None:
        OtherHealth = Product.objects.filter(category='hp')
    elif data== 'Below':
                OtherHealth = Product.objects.filter(category='hp').filter(discounted_price__lt=100)
    elif data== 'Above':
        OtherHealth = Product.objects.filter(category='hp').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/OtherHealth.html', {'OtherHealth':OtherHealth,'totalitem':totalitem})


def BiscuitsCookies(request, data=None):
    totalitem = 0
    if data == None:
        BiscuitsCookies = Product.objects.filter(category='bc')
    elif data== 'Below':
                BiscuitsCookies = Product.objects.filter(category='bc').filter(discounted_price__lt=100)
    elif data== 'Above':
        BiscuitsCookies = Product.objects.filter(category='bc').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/BiscuitsCookies.html', {'BiscuitsCookies':BiscuitsCookies,'totalitem':totalitem})

def Spices(request, data=None):
    totalitem = 0
    if data == None:
        Spices = Product.objects.filter(category='s')
    elif data== 'Below':
                Spices = Product.objects.filter(category='s').filter(discounted_price__lt=100)
    elif data== 'Above':
        Spices = Product.objects.filter(category='s').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/Spices.html', {'Spices':Spices,'totalitem':totalitem})

def DalPulses(request, data=None):
    totalitem = 0
    if data == None:
        DalPulses = Product.objects.filter(category='dp')
    elif data== 'Below':
                DalPulses = Product.objects.filter(category='dp').filter(discounted_price__lt=100)
    elif data== 'Above':
        DalPulses = Product.objects.filter(category='dp').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/DalPulses.html', {'DalPulses':DalPulses,'totalitem':totalitem})

def EdibleOil(request, data=None):
    totalitem = 0
    if data == None:
        EdibleOil = Product.objects.filter(category='eo')
    elif data== 'Below':
                EdibleOil = Product.objects.filter(category='eo').filter(discounted_price__lt=100)
    elif data== 'Above':
        EdibleOil = Product.objects.filter(category='eo').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/EdibleOil.html', {'EdibleOil':EdibleOil,'totalitem':totalitem})

def Sugar(request, data=None):
    totalitem = 0
    if data == None:
        Sugar = Product.objects.filter(category='su')
    elif data== 'Below':
                Sugar = Product.objects.filter(category='su').filter(discounted_price__lt=100)
    elif data== 'Above':
        Sugar = Product.objects.filter(category='su').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/Sugar.html', {'Sugar':Sugar,'totalitem':totalitem})

def DryFruits(request, data=None):
    totalitem = 0
    if data == None:
        DryFruits = Product.objects.filter(category='fd')
    elif data== 'Below':
                DryFruits = Product.objects.filter(category='fd').filter(discounted_price__lt=100)
    elif data== 'Above':
        DryFruits = Product.objects.filter(category='fd').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/DryFruits.html', {'DryFruits':DryFruits,'totalitem':totalitem})

def OtherFood(request, data=None):
    totalitem = 0
    if data == None:
        OtherFood = Product.objects.filter(category='fp')
    elif data== 'Below':
                OtherFood = Product.objects.filter(category='fp').filter(discounted_price__lt=100)
    elif data== 'Above':
        OtherFood = Product.objects.filter(category='fp').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/OtherFood.html', {'OtherFood':OtherFood,'totalitem':totalitem})

def Kwath(request, data=None):
    totalitem = 0
    if data == None:
        Kwath = Product.objects.filter(category='k')
    elif data== 'Below':
                Kwath = Product.objects.filter(category='k').filter(discounted_price__lt=100)
    elif data== 'Above':
        Kwath = Product.objects.filter(category='k').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/Kwath.html', {'Kwath':Kwath,'totalitem':totalitem})

def Oil(request, data=None):
    totalitem = 0
    if data == None:
        Oil = Product.objects.filter(category='o')
    elif data== 'Below':
                Oil = Product.objects.filter(category='o').filter(discounted_price__lt=100)
    elif data== 'Above':
        Oil = Product.objects.filter(category='o').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/Oil.html', {'Oil':Oil,'totalitem':totalitem})

def Churna(request, data=None):
    totalitem = 0
    if data == None:
        Churna = Product.objects.filter(category='c')
    elif data== 'Below':
                Churna = Product.objects.filter(category='c').filter(discounted_price__lt=100)
    elif data== 'Above':
        Churna = Product.objects.filter(category='c').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/Churna.html', {'Churna':Churna,'totalitem':totalitem})

def Asava(request, data=None):
    totalitem = 0
    if data == None:
        Asava = Product.objects.filter(category='a')
    elif data== 'Below':
                Asava = Product.objects.filter(category='a').filter(discounted_price__lt=100)
    elif data== 'Above':
        Asava = Product.objects.filter(category='a').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/Asava.html', {'Asava':Asava,'totalitem':totalitem})

def Vati(request, data=None):
    totalitem = 0
    if data == None:
        Vati = Product.objects.filter(category='v')
    elif data== 'Below':
                Vati = Product.objects.filter(category='v').filter(discounted_price__lt=100)
    elif data== 'Above':
        Vati = Product.objects.filter(category='v').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/Vati.html', {'Vati':Vati,'totalitem':totalitem})

def Guggul(request, data=None):
    totalitem = 0
    if data == None:
        Guggul = Product.objects.filter(category='g')
    elif data== 'Below':
                Guggul = Product.objects.filter(category='g').filter(discounted_price__lt=100)
    elif data== 'Above':
        Guggul = Product.objects.filter(category='g').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/Guggul.html', {'Guggul':Guggul,'totalitem':totalitem})



def HandWash(request, data=None):
    totalitem = 0
    if data == None:
        HandWash = Product.objects.filter(category='hw')
    elif data== 'Below':
                HandWash = Product.objects.filter(category='hw').filter(discounted_price__lt=100)
    elif data== 'Above':
        HandWash = Product.objects.filter(category='hw').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/HandWash.html', {'HandWash':HandWash,'totalitem':totalitem})

def ToiletCleaner(request, data=None):
    totalitem = 0
    if data == None:
        ToiletCleaner = Product.objects.filter(category='tc')
    elif data== 'Below':
                ToiletCleaner = Product.objects.filter(category='tc').filter(discounted_price__lt=100)
    elif data== 'Above':
        ToiletCleaner = Product.objects.filter(category='tc').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/ToiletCleaner.html', {'ToiletCleaner':ToiletCleaner,'totalitem':totalitem})

def HawanMaterial(request, data=None):
    totalitem = 0
    if data == None:
        HawanMaterial = Product.objects.filter(category='hm')
    elif data== 'Below':
                HawanMaterial = Product.objects.filter(category='hm').filter(discounted_price__lt=100)
    elif data== 'Above':
        HawanMaterial = Product.objects.filter(category='hm').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/HawanMaterial.html', {'HawanMaterial':HawanMaterial,'totalitem':totalitem})

def Agarbatti(request, data=None):
    totalitem = 0
    if data == None:
        Agarbatti = Product.objects.filter(category='ag')
    elif data== 'Below':
                Agarbatti = Product.objects.filter(category='ag').filter(discounted_price__lt=100)
    elif data== 'Above':
        Agarbatti = Product.objects.filter(category='ag').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/Agarbatti.html', {'Agarbatti':Agarbatti,'totalitem':totalitem})

def Dhoop(request, data=None):
    totalitem = 0
    if data == None:
        Dhoop = Product.objects.filter(category='dh')
    elif data== 'Below':
                Dhoop = Product.objects.filter(category='dh').filter(discounted_price__lt=100)
    elif data== 'Above':
        Dhoop = Product.objects.filter(category='dh').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/Dhoop.html', {'Dhoop':Dhoop,'totalitem':totalitem})

def DishWasher(request, data=None):
    totalitem = 0
    if data == None:
        DishWasher = Product.objects.filter(category='dw')
    elif data== 'Below':
                DishWasher = Product.objects.filter(category='dw').filter(discounted_price__lt=100)
    elif data== 'Above':
        DishWasher = Product.objects.filter(category='dw').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/DishWasher.html', {'DishWasher':DishWasher,'totalitem':totalitem})

def BodyCare(request, data=None):
    totalitem = 0
    if data == None:
        BodyCare = Product.objects.filter(category='cb')
    elif data== 'Below':
                BodyCare = Product.objects.filter(category='cb').filter(discounted_price__lt=100)
    elif data== 'Above':
        BodyCare = Product.objects.filter(category='cb').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/BodyCare.html', {'BodyCare':BodyCare,'totalitem':totalitem})

def DentalCare(request, data=None):
    totalitem = 0
    if data == None:
        DentalCare = Product.objects.filter(category='cd')
    elif data== 'Below':
                DentalCare = Product.objects.filter(category='cd').filter(discounted_price__lt=100)
    elif data== 'Above':
        DentalCare = Product.objects.filter(category='cd').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/DentalCare.html', {'DentalCare':DentalCare,'totalitem':totalitem})

def EyeCare(request, data=None):
    totalitem = 0
    if data == None:
        EyeCare = Product.objects.filter(category='ce')
    elif data== 'Below':
                EyeCare = Product.objects.filter(category='ce').filter(discounted_price__lt=100)
    elif data== 'Above':
        EyeCare = Product.objects.filter(category='ce').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/EyeCare.html', {'EyeCare':EyeCare,'totalitem':totalitem})

def HairCare(request, data=None):
    totalitem = 0
    if data == None:
        HairCare = Product.objects.filter(category='ch')
    elif data== 'Below':
                HairCare = Product.objects.filter(category='ch').filter(discounted_price__lt=100)
    elif data== 'Above':
        HairCare = Product.objects.filter(category='ch').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/HairCare.html', {'HairCare':HairCare,'totalitem':totalitem})

def ShishuCare(request, data=None):
    totalitem = 0
    if data == None:
        ShishuCare = Product.objects.filter(category='sc')
    elif data== 'Below':
                ShishuCare = Product.objects.filter(category='sc').filter(discounted_price__lt=100)
    elif data== 'Above':
        ShishuCare = Product.objects.filter(category='sc').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/ShishuCare.html', {'ShishuCare':ShishuCare,'totalitem':totalitem})

def SkinCare(request, data=None):
    totalitem = 0
    if data == None:
        SkinCare = Product.objects.filter(category='cs')
    elif data== 'Below':
                SkinCare = Product.objects.filter(category='cs').filter(discounted_price__lt=100)
    elif data== 'Above':
        SkinCare = Product.objects.filter(category='cs').filter(discounted_price__gt=100)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/SkinCare.html', {'SkinCare':SkinCare,'totalitem':totalitem})


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! You Have Registered Successfully.')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form}) 

@login_required
def checkout(request):
    totalitem = 0
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        amount +=amount *0.12
    totalamount = amount + shipping_amount
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/checkout.html',{'add': add , 'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity = c.quantity).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request):
        totalitem = 0
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})
    
    def post(self, request):
        totalitem = 0
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, pincode=pincode)
            reg.save()
            messages.success(request, 'Profile Updated Successfully')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form':form,'active':'btn-primary','totalitem':totalitem})

