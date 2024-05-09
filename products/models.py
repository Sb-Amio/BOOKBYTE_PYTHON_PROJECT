
from django.contrib.auth.models import User
from django.db import models





# Create your models here.



class ebook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='images/default.jpg')
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title


class book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category_type = (('Story', 'Story'), ('Fiction', 'Fiction'), ('Non-Fiction', 'Non-Fiction'), ('Novel', 'Novel'),
                     ('History', 'History'), ('Poetry', 'Poetry'), ('Cookbook', 'Cookbook'),
                     ('Drama', 'Drama'), ('Thriller', 'Thriller'), ('Biography', 'Biography'), ('Action', 'Action'),
                     ('Literature', 'Literature'), ('Adventure', 'Adventure'), ('Others', 'Others'))
    category = models.CharField(max_length=200, choices=category_type, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='images/default.jpg')
    review_choice = models.ForeignKey('Review', on_delete= models.CASCADE, blank=True, null=True)

    type = (('New', 'New'), ('Used', 'Used'), ('Academic', 'Academic'), ('Admission', 'Admission'))

    type_choice = models.CharField(max_length=100, choices=type, blank=True, null=True)

    def __str__(self):

        return self.title


class Accessories(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='images/default.jpg')
    review_choice = models.ForeignKey('Review', on_delete= models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(book, on_delete=models.CASCADE, blank=True, null=True)
    ebook = models.ForeignKey(ebook, on_delete=models.CASCADE, blank=True, null=True)
    accessories = models.ForeignKey(Accessories, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def price(self):
        total_price = 0
        if self.book:
            total_price += self.book.price * self.quantity
        elif self.ebook:
            total_price += self.ebook.price  # Assuming price is per item for ebooks
        elif self.accessories:
            total_price += self.accessories.price * self.quantity
        return total_price


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Book = models.ForeignKey(book, on_delete=models.CASCADE, blank=True, null=True)
    acc = models.ForeignKey(Accessories, on_delete=models.CASCADE, blank=True, null=True)
    review = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    review_choice = models.CharField(max_length=100, choices=review, blank=True, null=True)

    def __str__(self):
        return f"{self.Book} Review: {self.review_choice}"