from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Court, Booking
from .forms import CourtForm, BookingForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Courts
@login_required
def court_list(request):
    courts = Court.objects.all()
    return render(request, "courts/list.html", {"courts": courts})

def court_create(request):
    form = CourtForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Court added successfully!")
        return redirect("court_list")
    return render(request, "courts/form.html", {"form": form})

# Bookings
@login_required
def booking_list(request):
    bookings = Booking.objects.all().order_by("start_time")
    return render(request, "bookings/list.html", {"bookings": bookings})

@login_required
def booking_create(request):
    form = BookingForm(request.POST or None)
    if form.is_valid():
        try:
            booking = form.save(commit=False)
            booking.user = request.user  # assign owner
            booking.clean()
            booking.save()
            messages.success(request, "Booking created successfully!")
            return redirect("booking_list")
        except Exception as e:
            messages.error(request, str(e))
    return render(request, "bookings/form.html", {"form": form})

def home(request):
    return render(request, 'home.html')

# COURTS
def court_edit(request, pk):
    court = get_object_or_404(Court, pk=pk)
    form = CourtForm(request.POST or None, instance=court)
    if form.is_valid():
        form.save()
        messages.success(request, "Court updated successfully!")
        return redirect("court_list")
    return render(request, "courts/form.html", {"form": form})


def court_delete(request, pk):
    court = get_object_or_404(Court, pk=pk)
    if request.method == "POST":
        court.delete()
        messages.success(request, "Court deleted!")
        return redirect("court_list")
    return render(request, "courts/confirm_delete.html", {"court": court})


# BOOKINGS
@login_required
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    # Only allow owner
    if booking.user != request.user:
        messages.error(request, "You cannot edit someone else's booking!")
        return redirect("booking_list")

    form = BookingForm(request.POST or None, instance=booking)
    if form.is_valid():
        try:
            booking = form.save(commit=False)
            booking.clean()
            booking.save()
            messages.success(request, "Booking updated successfully!")
            return redirect("booking_list")
        except Exception as e:
            messages.error(request, str(e))
    return render(request, "bookings/form.html", {"form": form})


@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    # Only allow owner
    if booking.user != request.user:
        messages.error(request, "You cannot delete someone else's booking!")
        return redirect("booking_list")

    if request.method == "POST":
        booking.delete()
        messages.success(request, "Booking deleted!")
        return redirect("booking_list")

    return render(request, "bookings/confirm_delete.html", {"booking": booking})

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)  # auto login after signup
            messages.success(request, "Signup successful, you are now logged in!")
            return redirect("booking_list")
    return render(request, "auth/signup.html")

# Login
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("booking_list")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "auth/login.html")

# Logout
def user_logout(request):
    logout(request)
    return redirect("login")
