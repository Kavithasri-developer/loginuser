from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password


# User Registration
def register(request):
    if request.user.is_authenticated:  
        return redirect("profile")  # Redirect logged-in users to profile

    if request.method == "POST": 
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        print(f"📝 Form Submitted: Username={username}, Email={email}")

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # Hash the password before saving
        )

        # ✅ Automatically log in the user
        login(request, user)


        # ✅ Fix: Check if user or email already exists
        user_exists = User.objects.filter(username=username).exists()
        email_exists = User.objects.filter(email=email).exists()

        print(f"🔎 Checking Username '{username}' Exists: {user_exists}")
        print(f"🔎 Checking Email '{email}' Exists: {email_exists}")

        if user_exists:
            messages.error(request, " Username already exists in the database!")
            return redirect("register")

        if email_exists:
            messages.error(request, " Email already exists!")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, " Passwords do not match!")
            return redirect("register")

        # ✅ Fix: Create user after all checks pass
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "✅ Signup successful! You can now log in.")
        print(f"✅ Success: User {username} registered successfully!")

        return redirect("login")  # Redirect to login page

    return render(request, "register.html")

# User Login
def user_login(request):
    if request.user.is_authenticated:  
        return redirect("profile")  # Redirect logged-in users to profile
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "✅ Login successful!")
            return redirect("profile")  # Redirect to profile page
        else:
            messages.error(request, " Invalid username or password!")
            return redirect("login")

    return render(request, "login.html")

# User Logout
def user_logout(request):
    logout(request)
    messages.success(request, "✅ Logged out successfully!")
    return redirect("login")

# Profile Page
def profile(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "profile.html", {"user": request.user})



