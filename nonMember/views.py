import math

from django.db.models import Value
from django.shortcuts import render, redirect

from products.models import *


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

def book_non(request):
    Book = book.objects.all()
    context = {'Book': Book}
    return render(request, 'home_non.html', context=context)

def ebook_non(request):
    Ebook = ebook.objects.all()
    context = {'Ebook': Ebook}
    return render(request, 'ebook_non.html', context=context)

def book_details_non(request, id):
    products = book.objects.get(pk=id)
    reviews = Review.objects.filter(Book = id)
    average_review = calculate_average_review(reviews)

    context = {'products': products, 'average_review': math.ceil(average_review)}
    return render(request, template_name='book_details_non.html', context=context)

def ebook_details_non(request, id):
    products = ebook.objects.get(pk=id)
    context = {'products': products}
    return render(request, template_name='ebook_details_non.html', context=context)

def search_non(request):
    query = request.GET.get('q')
    if query:
        book_results = book.objects.filter(title__contains=query).annotate(item_type=Value(value='book_non'))
        ebook_results = ebook.objects.filter(title__contains=query).annotate(item_type=Value(value='ebook_non'))
        accessories_results = Accessories.objects.filter(title__contains=query).annotate(
            item_type=Value(value='accessories_non'))

        search_results = list(book_results) + list(ebook_results) + list(accessories_results)
    else:
        search_results = None

    return render(request, template_name='search_results_non.html',
                  context={'search_results': search_results, 'query': query})

def accessories_non(request):
    accessories_ins = Accessories.objects.all()
    context = {'accessories_ins': accessories_ins}
    return render(request, template_name='accessories_non.html', context=context)

def accessories_details_non(request, id):
    accessories_ins = Accessories.objects.get(pk=id)
    reviews = Review.objects.filter(acc=id)
    average_review = calculate_average_review(reviews)
    context = {'accessories_ins': accessories_ins, 'average_review': math.ceil(average_review)}
    return render(request, template_name='accessories_details_non.html', context=context)