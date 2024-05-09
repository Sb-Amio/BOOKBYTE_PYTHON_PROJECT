import math

from django.shortcuts import render, redirect
from products.models import *
from django.db.models import Value
from products.forms import OrderForm, ReviewForm
from django.contrib import messages
from django.contrib.auth import logout

import random
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


def home(request):
    Book = book.objects.all()
    context = {'Book': Book}
    return render(request, 'home_user.html', context=context)

def ebook_user(request):
    Ebook = ebook.objects.all()
    context = {'Ebook': Ebook}
    return render(request, 'ebook_user.html', context=context)
def accessories_user(request):
    accessories_ins = Accessories.objects.all()
    context = {'accessories_ins': accessories_ins}
    return render(request, template_name='accessories_user.html', context=context)
def academic_user(request):
    products = book.objects.filter(type_choice='Academic')
    context = {'products': products}
    return render(request, template_name='academic_user.html', context=context)

def admission_user(request):
    products = book.objects.filter(type_choice='Admission')
    context = {'products': products}
    return render(request, template_name='admission_user.html', context=context)

def usedBook_user(request):
    products = book.objects.filter(type_choice='Used')
    context = {'products': products}
    return render(request, template_name='usedBook_user.html', context=context)


def book_details_user(request, id):
    products = book.objects.get(pk=id)
    reviews = Review.objects.filter(Book = id)
    average_review = calculate_average_review(reviews)
    context = {'products': products, 'average_review': average_review}
    return render(request, template_name='book_details_user.html', context=context)

def ebook_details_user(request, id):
    products = ebook.objects.get(pk=id)
    context = {'products': products}
    return render(request, template_name='ebook_details_user.html', context=context)

def accessories_details_user(request, id):
    accessories_ins = Accessories.objects.get(pk=id)
    reviews = Review.objects.filter(acc=id)
    average_review = calculate_average_review(reviews)
    context = {'accessories_ins': accessories_ins, 'average_review': math.ceil(average_review)}
    return render(request, template_name='accessories_details_user.html', context=context)

def search_user(request):
    query = request.GET.get('q')
    if query:
        book_results = book.objects.filter(title__contains=query).annotate(item_type=Value(value='home'))
        ebook_results = ebook.objects.filter(title__contains=query).annotate(item_type=Value(value='ebook_user'))
        accessories_results = Accessories.objects.filter(title__contains=query).annotate(item_type=Value(value='accessories_user'))
        search_results = list(book_results) + list(ebook_results) + list(accessories_results)
    else:
        search_results = None

    return render(request, template_name='search_results_user.html',
                  context={'search_results': search_results, 'query': query})


def create_order_book(request, id):
    book_ins = book.objects.get(pk=id)
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.book = book_ins
            order.user = request.user
            ordered_quantity = form.cleaned_data['quantity']

            if book_ins.quantity < ordered_quantity:
                messages.error(request, 'Insufficient quantity available.')
                return redirect('accessories_user')
            else:
                book_ins.quantity -= ordered_quantity
                book_ins.save()
            order.save()
            return redirect('home')
    else:
        form = OrderForm()


    context = {'form': form, 'book': book_ins}
    return render(request, template_name='order_form_book.html', context=context)

def create_order_ebook(request, id):
    ebook_ins = ebook.objects.get(pk=id)
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.ebook = ebook_ins
            order.user = request.user


            order.save()
            return redirect('ebook_user')
    else:
        form = OrderForm()


    context = {'form': form, 'ebook': ebook_ins}
    return render(request, template_name='order_form_book.html', context=context)

def create_order_accessories(request, id):
    acc_ins = Accessories.objects.get(pk=id)
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.accessories = acc_ins
            order.user = request.user
            ordered_quantity = form.cleaned_data['quantity']

            if acc_ins.quantity < ordered_quantity:
                messages.error(request, 'Insufficient quantity available.')
                return redirect('accessories_user')
            else:
                acc_ins.quantity -= ordered_quantity
                acc_ins.save()
            order.save()
            return redirect('home')
    else:
        form = OrderForm()


    context = {'form': form, 'Accessories': acc_ins}
    return render(request, template_name='order_form_book.html', context=context)


def order_details_user(request):
    order_ins = order.objects.filter(user=request.user)
    context = {'order_ins': order_ins}
    return render(request, template_name='order_details_user.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('useradmin')


def giveReview_Book(request, id):
    # Assuming 'id' refers to the product id
    product = book.objects.get(id=id)  # You might need to adjust this based on your model structure

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            # Assign the product to the review
            review.Book = product  # Assuming 'Book' is the ForeignKey field in the Review model
            review.save()
            return redirect('order_details_user')
    else:
        form = ReviewForm()

    context = {'form': form, 'product': product}
    return render(request, template_name='reviewform.html', context=context)

def giveReview_Accessories(request, id):

    product = Accessories.objects.get(id=id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user

            review.acc = product
            review.save()
            return redirect('order_details_user')
    else:
        form = ReviewForm()

    context = {'form': form, 'product': product}
    return render(request, template_name='reviewform.html', context=context)

def myReview(request):
    review_ins = Review.objects.filter(user=request.user)
    context = {'review_ins': review_ins}
    return render(request, template_name='myreviews.html', context=context)

