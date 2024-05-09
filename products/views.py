import os

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Permission
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.db.models import Value

from obms import settings
from .forms import BookForm, EBookForm, AccessoriesForm, CustomUserCreationForm
from .models import book, ebook, Accessories, Profile, Review
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout as django_logout

from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control

import sys

sys.setrecursionlimit(150)


# Create your views here.

def calculate_average_review(reviews):
    total_score = 0
    num_reviews = 0
    for review in reviews:
        if review.review_choice:
            try:
                total_score += int(review.review_choice)
                num_reviews += 1
            except ValueError:
                # Handle the case where review_choice is not a valid integer
                pass
    if num_reviews > 0:
        return total_score / num_reviews
    else:
        return 0
def useradmin(request):
    return render(request, template_name='user_or_admin.html')


def loginPage(request):
    return render(request, template_name='loginpage.html')


def main(request):
    products = book.objects.all()
    context = {'products': products}
    return render(request, template_name='home.html', context=context)


def ebooks(request):
    products = ebook.objects.all()
    context = {'products': products}
    return render(request, template_name='ebook.html', context=context)


def accessories(request):
    accessories_ins = Accessories.objects.all()
    context = {'accessories_ins': accessories_ins}
    return render(request, template_name='accessories.html', context=context)


def accessories_details(request, id):
    accessories_ins = Accessories.objects.get(pk=id)
    reviews = Review.objects.filter(acc = id)
    average_review = calculate_average_review(reviews)
    context = {'accessories_ins': accessories_ins, 'average_review': average_review}
    return render(request, template_name='accessories_details.html', context=context)


def academic(request):
    products = book.objects.filter(type_choice='Academic')
    context = {'products': products}
    return render(request, template_name='academic.html', context=context)


def admission(request):
    products = book.objects.filter(type_choice='Admission')
    context = {'products': products}
    return render(request, template_name='admission.html', context=context)



def book_details(request, id):
    products = book.objects.get(pk=id)
    reviews = Review.objects.filter(Book=id)
    average_review = calculate_average_review(reviews)
    context = {'products': products, 'average_review': average_review}
    return render(request, template_name='book_details.html', context=context)


def ebook_details(request, id):
    products = ebook.objects.get(pk=id)
    context = {'products': products}
    return render(request, template_name='ebook_details.html', context=context)



def usedBook(request):
    products = book.objects.filter(type_choice='Used')
    context = {'products': products}
    return render(request, template_name='usedBook.html', context=context)




def upload_book(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main')

    context = {'form': form}
    return render(request, template_name='upload_book.html', context=context)


def upload_ebook(request):
    form = EBookForm()
    if request.method == 'POST':
        form = EBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ebook')
    context = {'form': form}
    return render(request, template_name='upload_ebook.html', context=context)


def upload_accessories(request):
    form = AccessoriesForm()
    if request.method == 'POST':
        form = AccessoriesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accessories')
    context = {'form': form}
    return render(request, template_name='upload_accessories.html', context=context)


def update_book(request, id):
    Book = book.objects.get(pk=id)
    form = BookForm(instance=Book)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=Book)
        if form.is_valid():
            form.save()
            return redirect('main')
    context = {'form': form}
    return render(request, template_name='upload_book.html', context=context)


def update_ebook(request, id):
    EBook = ebook.objects.get(pk=id)
    form = EBookForm(instance=EBook)
    if request.method == 'POST':
        form = EBookForm(request.POST, request.FILES, instance=EBook)
        if form.is_valid():
            form.save()
            return redirect('ebook')
    context = {'form': form}
    return render(request, template_name='upload_ebook.html', context=context)


def update_accessories(request, id):
    accessories = Accessories.objects.get(pk=id)
    form = AccessoriesForm(instance=accessories)
    if request.method == 'POST':
        form = AccessoriesForm(request.POST, request.FILES, instance=accessories)
        if form.is_valid():
            form.save()
            return redirect('accessories')
    context = {'form': form}
    return render(request, template_name='upload_accessories.html', context=context)


def delete_book(request, id):
    book_to_delete = book.objects.get(pk=id)
    if request.method == 'POST':
        book_to_delete.delete()
        return redirect('main')



def delete_ebook(request, id):
    ebook_to_delete = ebook.objects.get(pk=id)
    if request.method == 'POST':
        ebook_to_delete.delete()
        return redirect('ebook')


def delete_accessories(request, id):
    accessories = Accessories.objects.get(pk=id)
    if request.method == 'POST':
        accessories.delete()
        return redirect('accessories')


def search(request):
    query = request.GET.get('q')
    if query:
        book_results = book.objects.filter(title__contains=query).annotate(item_type=Value(value='book'))
        ebook_results = ebook.objects.filter(title__contains=query).annotate(item_type=Value(value='ebook'))
        accessories_results = Accessories.objects.filter(title__contains=query).annotate(
            item_type=Value(value='accessories'))

        search_results = list(book_results) + list(ebook_results) + list(accessories_results)
    else:
        search_results = None

    return render(request, template_name='search_results.html',
                  context={'search_results': search_results, 'query': query})


def register(request, user_type):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #profile = Profile.objects.create(user=user)  # Use Profile here (assuming it's your model name)
            if user_type == 'customer':
                user.profile.is_admin = False
                user.profile.save()
                user.save()
            else:
                user.is_staff = True
                user.profile.is_admin = True
                user.profile.save()
                user.save()
            return redirect('login_user')
    context = {'form': form}
    return render(request, 'registration_form.html', context = context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'profile') and user.profile.is_admin:
                    return redirect('main')  # Redirect to admin dashboard
                else:
                    return redirect('home')  # Redirect to customer dashboard
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'loginpage.html', {'form': form})

def logout_admin(request):
    logout(request)
    return redirect('useradmin')



