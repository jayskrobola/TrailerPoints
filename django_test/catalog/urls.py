from django.urls import path
from . import views

urlpatterns = [
    path('', views.viewCatalogs, name='home'),
    path('view/', views.viewCatalogs, name='view'),
    path('create/', views.createCatalog, name='create'),
    path('<int:id>/', views.index, name='index'),
    path('<int:id>/createCategory/', views.createCategory, name='createCategory'),
    path('<int:id>/createProduct/', views.createProduct, name='createProduct'),
    path('<int:id>/deleteProduct/', views.deleteProduct, name='deleteProduct'),
    path('<int:id>/deleteCatalog/', views.deleteCatalog, name='deleteCatalog'),
    path('<int:id>/makePrimary/', views.makePrimary, name='makePrimary'),
    path('<int:id>/addToCart/', views.addToCart, name='addToCart'),
    path('<int:id>/removeFromCart/', views.removeFromCart, name='removeFromCart'),
    path('viewCart/', views.viewCart, name='viewCart'),
    path('viewDriver/', views.viewCatalogsDriver, name='makePrimary')
]