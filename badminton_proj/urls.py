from django.contrib import admin
from django.urls import path, include
from booking import views


urlpatterns = [
    path("admin/", admin.site.urls), 
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("courts/", views.court_list, name="court_list"),
    path("courts/add/", views.court_create, name="court_create"),
    path("courts/<int:pk>/edit/", views.court_edit, name="court_edit"),
    path("courts/<int:pk>/delete/", views.court_delete, name="court_delete"),
    path("bookings/", views.booking_list, name="booking_list"),
    path("bookings/add/", views.booking_create, name="booking_create"),
    path("bookings/<int:pk>/edit/", views.booking_edit, name="booking_edit"),
    path("bookings/<int:pk>/delete/", views.booking_delete, name="booking_delete"),
]
