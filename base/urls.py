from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('', views.home, name="home"),
    path('product/<str:pk>', views.product, name="product"),
    path('profile/<str:pk/', views.userProfile, name="user-profile"),

    path('new-product/', views.NewProduct, name="new-product"),
    path('update-product/<str:pk>', views.UpdateProduct, name="update-product"),
    path('delete-product/<str:pk>', views.DeleteProduct, name="delete-product"),

]