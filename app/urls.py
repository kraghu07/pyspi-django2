from django.urls import path
from . import views

urlpatterns = [
    path('', views.baseView, name="base"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.loginView, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logoutView, name='logout'),
    path('update/', views.updatePassword, name='update'),
    path('identify/', views.identifyView, name='identify'),
    path('reset/<str:username>/', views.setPassword, name='forgot'),
    path('products/', views.product, name='products'),
    path('product/<slug:slug>/', views.productview, name='product'),
    path('category_home/', views.homeView, name='cat_home'),
    path('category/<slug:slug>/', views.cat, name='categories'),
    path('add_to_cart/<str:productitemslug>/<str:sizeslug>/', views.add_to_cart, name='add_to_cart'),  
    path('increment_quantity/<int:id>/', views.increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:id>/', views.decrement_quantity, name='decrement_quantity'),
]












# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.baseView, name="base"),
#     path('signup/', views.signup, name="signup"),
#     path('login/', views.loginView, name='login'),
#     path('home/', views.home, name='home'),
#     path('logout/', views.logoutView, name='logout'),
#     path('update/', views.updatePassword, name='update'),
#     path('identify/', views.identifyView, name='identify'),
#     path('reset/<str:username>/', views.setPassword, name='forgot'),
#     path('products/', views.product, name='products'),
#     path('product/<slug:slug>/', views.productview, name='product'),
#     path('category_home/', views.homeView, name='cat_home'),
#     path('category/<slug:slug>/', views.cat, name='categories'),
#     path('add_to_cart/<str:productitemslug>/<str:sizeslug>/', views.add_to_cart, name='add_to_cart'), # Add to cart URL 
# ]






# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.baseView, name="base"),
#     path('signup/', views.signup, name="signup"),
#     path('login/', views.loginView, name='login'),
#     path('home/', views.home, name='home'),  # Correct the URL pattern for the home view
#     path('logout/', views.logoutView, name='logout'),
#     path('update/', views.updatePassword, name='update'),
#     path('identify/', views.identifyView, name='identify'),
#     path('reset/<str:username>/', views.setPassword, name='forgot'),
#     path('products/', views.products,name='products'),
#     path('product/<slug:slug>/', views.productview,name='product' ),
#     # path('product/<int:id>/', views.productView),
#     # path('product/<str:slug>/', views.productView),
#     path('categories/', views.category_list, name='category_list'),
#     path('categories/<slug:category_slug>/', views.product_list, name='product_list'),
# ]
