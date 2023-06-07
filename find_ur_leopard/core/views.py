from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
import string

from .models import UploadedImage

from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C://Program Files//Tesseract-OCR//tesseract.exe'


def upload_image(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        uploaded_image = request.FILES['image']
        image_object = UploadedImage.objects.create(image=uploaded_image)
        ocr_text = pytesseract.image_to_string(Image.open(uploaded_image))

        return render(request, 'result.html',
                      {'image': image_object.image, 'ocr_text': ocr_text, 'user_profile': user_profile})

    return render(request, 'upload.html', {'user_profile': user_profile})


'''
This is our view for the community feed
- It will grab the user who is logged in
- It will grab all the the posts created by everyone, which then gets passed into the community feed view
'''


@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)

    user_profile = Profile.objects.get(user=user_object)

    return render(request, 'index.html', {'user_profile': user_profile})


'''
This is our view for a user being able to sign up
This is how all of the user information is stored when the user signs up for the application
'''


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check to make sure the user has a wit email
        if '@wit' not in email:
            messages.info(request, 'Not a Wentworth Email')
            return redirect('signup')
            # return redirect('signup.html')

        # Check to make sure the users password is at least 8 characters
        if len(password) < 8:
            messages.info(request, 'Password must be at least 8 characters')
            return redirect('signup')

        numbers = set(list(string.digits))
        chars = set(list(password))

        # Check to see that the users password has at least one numerical character
        if not numbers.intersection(chars):
            messages.info(request, 'Password must contain at least one number')
            return redirect('signup')

        # Check to make sure that the users password and repeated password both match
        if password == password2:
            # Check to make sure the email is not already in use in the database
            if User.objects.filter(email=email).exists():
                messages.info(request, "This Email Has Already Been Taken")
                return redirect('signup')
            # Check to make sure the username is not already in use in the database
            elif User.objects.filter(username=username).exists():
                messages.info(request, "This Username Has Already Been Taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # create a profile object for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')

        else:
            messages.info(request, 'Passwords Do Not Match')
            return redirect('signup.html')

    else:
        return render(request, 'signup.html')


'''
This is our view for a user being able to sign in
'''


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticating the user from the database and login information
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Login Credentials')
            return redirect('signin')

    else:
        return render(request, 'signin.html')


'''
This is our view for a user being able to sign out of the application
'''


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


'''
This is our view for a user being able to create there own profile, including bio, gender, etc...
'''


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # if the user does not select a image for their profile, use the default image
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST.get('bio')
            location = request.POST.get('location')
            gender = request.POST.get('gender')
            age = request.POST.get('age')
            sleeping_habits = request.POST.get('sleeping_habits')
            number_of_roommates = request.POST.get('number_of_roommates')
            personality_types = request.POST.get('personality_types')
            interests = request.POST.get('interests')

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.gender = gender
            user_profile.age = age
            user_profile.sleeping_habits = sleeping_habits
            user_profile.number_of_roommates = number_of_roommates
            user_profile.personality_types = personality_types
            user_profile.interests = interests

            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST.get('bio')
            location = request.POST.get('location')
            gender = request.POST.get('gender')
            age = request.POST.get('age')
            sleeping_habits = request.POST.get('sleeping_habits')
            number_of_roommates = request.POST.get('number_of_roommates')
            personality_types = request.POST.get('personality_types')
            interests = request.POST.get('interests')

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.gender = gender
            user_profile.age = age
            user_profile.sleeping_habits = sleeping_habits
            user_profile.number_of_roommates = number_of_roommates
            user_profile.personality_types = personality_types
            user_profile.interests = interests

            # Saving user information in the database
            user_profile.save()

        return redirect('/')
    return render(request, 'setting.html', {'user_profile': user_profile})


'''
This is our view for the user profiles
'''


def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)

    # Passing in all user profile information
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
    }

    return render(request, 'profile.html', context)
