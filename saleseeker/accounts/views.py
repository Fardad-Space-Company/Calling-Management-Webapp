from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import ProfileUpdateForm
from .models import Profile

# Create your views here.
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}.")
                return redirect('/')  # Redirect to the 'home' URL pattern after successful login
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('login')


# def profile(request):
#     return render(request, 'home/page-user.html')





# @login_required

# def profile(request):
#     if request.method == 'POST':
#         # Handle profile update form
#         form = ImageUploadForm(request.POST, request.FILES, instance=request.user.profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your profile was successfully updated!')
#             return redirect('profile')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         # Initialize the form with the user's current profile data
#         form = ImageUploadForm(instance=request.user.profile)

#     context = {
#         'user': request.user,
#         'form': form
#     }

#     return render(request, 'home/page-user.html', context)


def profile(request):
    profile, created =  Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            profile.user.email = form.cleaned_data['email']
            profile.user.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'home/page-user.html', {'form': form})



# def update_profile(request):
#     try:
#         user_profile = request.user.profile
#     except Profile.DoesNotExist:
#         user_profile = Profile.objects.create(user=request.user)

#     if request.method == 'POST':
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile, user=request.user)
#         if p_form.is_valid():
#             p_form.save()
#             messages.success(request, 'Your profile has been updated!')
#             return redirect('profile')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         p_form = ProfileUpdateForm(instance=user_profile, user=request.user)

#     context = {
#         'p_form': p_form
#     }

#     return render(request, 'home/page-user.html', context)