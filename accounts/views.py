from django.shortcuts import render , redirect
from .models import Profile
from .forms import SignupForm , UserForm , ProfileForm
from django.contrib.auth import authenticate , login



# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             # Create a new user object but avoid saving it yet
#             new_user = user_form.save(commit=False)
#             # Set the chosen password
#             new_user.set_password(user_form.cleaned_data['password'])
#             # Save the User object
#             new_user.save()
#             # Create the user profile
#             Profile.objects.create(user=new_user)
#             return render(
#                 request,
#                 'account/register_done.html',
#                 {'new_user': new_user},
#             )
#     else:
#         user_form = UserRegistrationForm()
#     return render(
#         request,
#         'account/register.html',
#         {'user_form': user_form}
#     )



def signup(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)
            return redirect('/accounts/profile')
    else:
        form=SignupForm()
        
    return render(request,'registration/signup.html',{'form':form})







def profile(request):
    profile=Profile.objects.get(user=request.user)
    return render(request,'profile/profile.html',{'profile':profile})

def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        userform = UserForm(request.POST , instance=request.user)
        profile_form = ProfileForm(request.POST , instance=profile)
        if userform.is_valid() and profile_form.is_valid():
            userform.save()
            profile_form.save()
            return redirect('/accounts/profile')

    else:  ## show
        userform = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request,'profile/profile_edit.html',{
        'userform' : userform , 
        'profileform' : profile_form ,
        })
