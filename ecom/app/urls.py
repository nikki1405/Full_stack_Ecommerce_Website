from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<str:val>/', views.CategoryView.as_view(), name='category'),
    path('category-title/<str:val>/', views.CategoryTitle.as_view(), name='category-title'),
    path('product-detail/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('profile/', views.profile_view, name='profile'),
    path('address/', views.address, name='address'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove-from-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment, name='paymentdone'),
    path('orders/', views.orders, name='orders'),
    path('update-address/<int:pk>/', views.updateAddress.as_view(), name='update-address'),
    path('register/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    path('password-change/', 
        auth_view.PasswordChangeView.as_view(
            template_name='app/passwordchange.html',
            form_class=MyPasswordChangeForm,
            success_url='/password-change-done/'
        ),
        name='password_change'
    ),
    path('password-change-done/', 
        auth_view.PasswordChangeDoneView.as_view(
            template_name='app/passwordchangedone.html'
        ),
        name='password_change_done'
    ),
    path('logout/', views.logout_view, name='logout'),
    path('update-cart-quantity/', views.update_cart_quantity, name='update-cart-quantity'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
