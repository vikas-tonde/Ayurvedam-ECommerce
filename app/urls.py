from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm


urlpatterns = [
    path ('',views.ProductView.as_view(), name="home" ),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
                  path('customer', views.customer, name="customer_report"),
                  path('orderplaced', views.orderplaced, name="orders_report"),
                  path('carts', views.carts, name="carts_report"),
                  path('product', views.product, name="products_report"),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart, name='showcart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    path('Digestives/', views.Digestives, name='Digestives'),
    path('Digestives/<slug:data>', views.Digestives, name='Digestivesdata'),
    path('HealthDrinks/', views.HealthDrinks, name='HealthDrinks'),
    path('HealthDrinks/<slug:data>', views.HealthDrinks, name='HealthDrinksdata'),
    path('FruitBeverages/', views.FruitBeverages, name='FruitBeverages'),
    path('FruitBeverages/<slug:data>', views.FruitBeverages, name='FruitBeveragesdata'),
    path('HealthWellness/', views.HealthWellness, name='HealthWellness'),
    path('HealthWellness/<slug:data>', views.HealthWellness, name='HealthWellnessdata'),
    path('DietFood/', views.DietFood, name='DietFood'),
    path('DietFood/<slug:data>', views.DietFood, name='DietFooddata'),
    path('OtherHealth/', views.OtherHealth, name='OtherHealth'),
    path('OtherHealth/<slug:data>', views.OtherHealth, name='OtherHealthdata'),
    path('BiscuitsCookies/', views.BiscuitsCookies, name='BiscuitsCookies'),
    path('BiscuitsCookies/<slug:data>', views.BiscuitsCookies, name='BiscuitsCookiesdata'),
    path('Spices/', views.Spices, name='Spices'),
    path('Spices/<slug:data>', views.Spices, name='Spicesdata'),
    path('DalPulses/', views.DalPulses, name='DalPulses'),
    path('DalPulses/<slug:data>', views.DalPulses, name='DalPulsesdata'),
    path('EdibleOil/', views.EdibleOil, name='EdibleOil'),
    path('EdibleOil/<slug:data>', views.EdibleOil, name='EdibleOildata'),
    path('Sugar/', views.Sugar, name='Sugar'),
    path('Sugar/<slug:data>', views.Sugar, name='Sugardata'),
    path('DryFruits/', views.DryFruits, name='DryFruits'),
    path('DryFruits/<slug:data>', views.DryFruits, name='DryFruitsdata'),
    path('OtherFood/', views.OtherFood, name='OtherFood'),
    path('OtherFood/<slug:data>', views.OtherFood, name='OtherFooddata'),

path('Kwath/', views.Kwath, name='Kwath'),
    path('Kwath/<slug:data>', views.Kwath, name='Kwathdata'),
path('Oil/', views.Oil, name='Oil'),
    path('Oil/<slug:data>', views.Oil, name='Oildata'),
path('Guggul/', views.Guggul, name='Guggul'),
    path('Guggul/<slug:data>', views.Guggul, name='Gugguldata'),
path('Vati/', views.Vati, name='Vati'),
    path('Vati/<slug:data>', views.Vati, name='Vatidata'),
path('Churna/', views.Churna, name='Churna'),
    path('Churna/<slug:data>', views.Churna, name='Churnadata'),
path('Asava/', views.Asava, name='Asava'),
    path('Asava/<slug:data>', views.Asava, name='Asavadata'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('HandWash/', views.HandWash, name='HandWash'),
    path('HandWash/<slug:data>', views.HandWash, name='HandWashdata'),
    
    path('ToiletCleaner/', views.ToiletCleaner, name='ToiletCleaner'),
    path('ToiletCleaner/<slug:data>', views.ToiletCleaner, name='ToiletCleanerdata'),
    
    path('HawanMaterial/', views.HawanMaterial, name='HawanMaterial'),
    path('HawanMaterial/<slug:data>', views.HawanMaterial, name='HawanMaterialdata'),

    path('Agarbatti/', views.Agarbatti, name='Agarbatti'),
    path('Agarbatti/<slug:data>', views.Agarbatti, name='Agarbattidata'),

    path('Dhoop/', views.Dhoop, name='Dhoop'),
    path('Dhoop/<slug:data>', views.Dhoop, name='Dhoopdata'),
    
    path('DishWasher/', views.DishWasher, name='DishWasher'),
    path('DishWasher/<slug:data>', views.DishWasher, name='DishWasherdata'),

path('SkinCare/', views.SkinCare, name='SkinCare'),
    path('SkinCare/<slug:data>', views.SkinCare, name='SkinCaredata'),

path('ShishuCare/', views.ShishuCare, name='ShishuCare'),
    path('ShishuCare/<slug:data>', views.ShishuCare, name='ShishuCaredata'),

path('HairCare/', views.HairCare, name='HairCare'),
    path('HairCare/<slug:data>', views.HairCare, name='HairCaredata'),

path('EyeCare/', views.EyeCare, name='EyeCare'),
    path('EyeCare/<slug:data>', views.EyeCare, name='EyeCaredata'),

path('DentalCare/', views.DentalCare, name='DentalCare'),
    path('DentalCare/<slug:data>', views.DentalCare, name='DentalCaredata'),

path('BodyCare/', views.BodyCare, name='BodyCare'),
    path('BodyCare/<slug:data>', views.BodyCare, name='BodyCaredata'),
    
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),

    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),

    path('registration/',views.CustomerRegistrationView.as_view(), name="customerregistration"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
