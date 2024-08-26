from django.urls import path
from wowapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home', views.home),
    path('', views.home),
    path('description/<pid>',views.description),
    path('login', views.login_user),
    path('about', views.about),
    path('register', views.register),
    path('logout', views.logout_user),
    path('index', views.base),
    path('addcart/<pid>',views.addCart),
    path('cart',views.cart),
    path('remove/<pid>',views.remove),
    path('updateqty/<qty>/<cid>',views.updateqty),
    path('order',views.order),
    path('payment',views.makepayment),
    path('sendmail',views.sendUserMail),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)