from django.conf.urls import url
from django.conf.urls import (handler404)
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.mainPage, name='mainPage'),
    url('fakeDriver',views.fakeDriver,name='fakeDriver'),
    url('removeFakeSponsor',views.removeFakeSponsor,name='removeFakeSponsor'),
    url('home', views.home, name='home'),
    url(r'^login_redirect/',views.loginRedirect,name='loginRedirect'),
    url('logout/',views.logout,name="user-logout"),
    url('email/',views.updateEmail,name="user-email"),
    url('address/',views.updateAddress, name = "user-address"),
    url('sponsorProfile/',views.sponsorProfile,name="sponsor-profile"),
    url('incentive/',views.readIncentive,name="sponsor-incentive"),
    url('updateDollarVal/',views.updateDollarVal,name="sponsor-updatedollar"),
    url('addDriver',views.addDriver,name="addDriver"),
    url('removeDriver',views.removeDriver,name="removeDriver"),
    url('removeSponsor',views.removeSponsor,name="removeSponsor"),
    url('paymentmethod',views.paymentmethod,name="paymentmethod"),
    path('profile/', views.profile, name='user-profile'),
    path('addpoint/', views.addpoints, name='user-addpoint'),
    path('PostPoint/', views.PostPoint, name='user-postpoint'),
    path('ViewPoint/', views.PostPoint, name='user-postpoint'),
    path('register/',views.register,name='user-register'),
    path('PostUpdatePassword/', views.PostUpdatePassword, name='user-PostUpdatePassword'),
    path('updatePassword/', views.updatePassword, name='user-updatePassword'),
    path('PostUpdateUsername/', views.PostUpdateUsername, name='user-PostUpdateUsername'),
    path('updateUsername/', views.updateUsername, name='user-updateUsername'),
    #path('<int:id>/', views.index, name='user-index'),
    #path('createCatalog/', views.createCatalog, name='user-createCatalog'),
    path('profile/updateName/',views.updateName,name='user-updateName'),
    path('PostPointDist/', views.PostPointDist ,name='user-PostPointDist'),
]
