from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

STATE_CHOICES = (

('Maharashtra','Maharashtra'),
)
CITY_CHOICES = (

('Pune','Pune'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(choices=CITY_CHOICES,max_length=50)
    pincode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)

def __str__(self):
    return str(self.id)

CATEGORY_CHOICES = (
    ('d','Digestives'),
    ('hd','HealthDrinks'),
    ('fb','FruitBeverages'),
    ('hw','HealthWellness'),
    ('df','DietFood'),
    ('hp','OtherHealth'),
    ('bc','BiscuitsCookies'),
    ('s','Spices'),
    ('dp', 'DalPulses'),
    ('eo', 'EdibleOil'),
    ('su', 'Sugar'),
    ('fd', 'DryFruits'),
    ('fp', 'OtherFood'),
    ('k', 'Kwath'),
    ('o', 'Oil'),
    ('c', 'Churna'),
    ('a', 'Asava'),
    ('v', 'Vati'),
    ('g', 'Guggul'),
    ('ag', 'Agarbatti'),
    ('dh', 'Dhoop'),
    ('dw', 'DishWasher'),
    ('hm', 'HawanMaterial'),
    ('tc', 'ToiletCleaner'),
    ('wh', 'HandWash'),
    ('cs', 'SkinCare'),
    ('cb', 'BodyCare'),
    ('ch', 'HairCare'),
    ('cd', 'DentalCare'),
    ('ce', 'EyeCare'),
    ('sc', 'ShishuCare'),

)
class Product(models.Model):
    title = models.CharField(max_length=100)
    quantity=models.IntegerField(default=0)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='productimg')

def __str__(self):
    return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
        
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices = STATUS_CHOICES,default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price