from django.urls import path
from myapp import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index',views.index_pg),
    path('home',views.home ),
    path('aboutUs',views.aboutUs),
    path('contactUs',views.contactUs),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('filterbytype/<tyname>',views.filterByType),
    path('sort/<ord>',views.sortGames),
    path('range',views.rangeSearch),
    path('details/<gid>',views.showDetails),
    path('addtocart/<gid>',views.addToCart),
    path('viewcart',views.viewcart),
    path('delete/<cid>',views.deleteFromCart),
    path('updateqty/<incr>/<cid>',views.updateQuantity),
    path('placeorder',views.placeOrder),
    path('makepayment',views.makepayment),
    path('download/<token>/<int:game_id>/', views.download_view, name='download'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)