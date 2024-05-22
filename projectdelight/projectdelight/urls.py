"""
URL configuration for projectdelight project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
# from django.contrib.auth import view as auth_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('about/',views.about),
    path('contact/',views.contact,name='contact'),
    path('product/',views.product),
    path('category/<slug:val>',views.CategoryView.as_view(),name='category'),
    path('category_title/<val>',views.CategoryTitle.as_view(),name='category_title'),
    path('product_detail/<int:pk>',views.Productdetail.as_view(),name='product_detail'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path('updateaddress/<int:pk>',views.updateAddress.as_view(),name='updateaddress'),
    #cart url
    path("add-to-cart/",views.add_to_cart, name="add-to-cart"),
    path('cart/',views.show_cart,name='showcart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path("checkout/", views.checkout.as_view(), name="checkout"),
    path("paymentdone/", views.payment_done, name="paymentdone"),
    path('buy_now/<int:product_id>/', views.BuyNowView.as_view(), name='buy_now'),
    path('buy_now/paymentdone/', views.buy_nowpayment_done, name='buypaymentdone'),
    path('orders/',views.orders_cart,name='orders'),
    path('search/',views.search_pr,name='search'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    #login authentication
    path('accounts/login/',views.login_user,name='login'),
    path('register/',views.register_user,name='register'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone'),name='passwordchange'),
    path('logout/',views.logout_user,name='logout'),
    path('accounts/',include("allauth.urls")),
    # reset_password
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset-done/',auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
