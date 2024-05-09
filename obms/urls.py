"""
URL configuration for obms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from products import views as b_views
from user import views as u_views
from nonMember import views as n_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/',b_views.main, name='main'),
    path('',n_views.book_non, name='book_non'),
    path('useradmin/',b_views.useradmin, name='useradmin'),
    path('register/<str:user_type>2', b_views.register, name='register'),
    path('login_user/',b_views.login_user, name='login_user'),
    path('ebook/', b_views.ebooks, name='ebook'),
    path('academic/',b_views.academic, name='academic'),
    path('admission/',b_views.admission, name='admission'),
    path('book_details/<str:id>/',b_views.book_details, name='book_details'),
    path('uploadbook/', b_views.upload_book, name='upload_book'),
    path('uploadebook/', b_views.upload_ebook, name='upload_ebook'),
    path('ebook/<str:id>/', b_views.ebook_details, name='ebook_details'),
    path('usedBook/', b_views.usedBook, name='usedBook'),
    path('update_book/<str:id>', b_views.update_book, name='update_book'),
    path('update_ebook/<str:id>', b_views.update_ebook, name='update_ebook'),
    path('delete_book/<str:id>2', b_views.delete_book, name='delete_book'),
    path('delete_accessories/<str:id>', b_views.delete_accessories, name='delete_accessories'),
    path('delete_ebook/<str:id>/', b_views.delete_ebook, name='delete_ebook'),
    path('accessories/', b_views.accessories, name='accessories'),
    path('uploadaccessories/', b_views.upload_accessories, name='upload_accessories'),
    path('accesseries/<str:id>', b_views.accessories_details, name='accessories_details'),
    path('update_accessories/<str:id>', b_views.update_accessories, name='update_accessories'),
    path('search/', b_views.search, name='search'),
    path('logout_admin/', b_views.logout_admin, name='logout_admin'),



    path('home/', u_views.home, name='home'),
    path('ebook_user/', u_views.ebook_user, name='ebook_user'),
    path('academic_user/', u_views.academic_user, name='academic_user'),
    path('admission_user/', u_views.admission_user, name='admission_user'),
    path('accessories_user/', u_views.accessories_user, name='accessories_user'),
    path('usedBook_user/', u_views.usedBook_user, name='usedBook_user'),
    path('book_details_user/<str:id>/', u_views.book_details_user, name='book_details_user'),
    path('ebook_details_user/<str:id>/', u_views.ebook_details_user, name='ebook_details_user'),
    path('accessories_details_user/<str:id>/', u_views.accessories_details_user, name='accessories_details_user'),
    path('search_user/', u_views.search_user, name='search_user'),
    path('create_order_book/<str:id>/', u_views.create_order_book, name='create_order_book'),
    path('create_order_ebook/<str:id>/', u_views.create_order_ebook, name='create_order_ebook'),
    path('create_order_accessories/<str:id>/', u_views.create_order_accessories, name='create_order_accessories'),
    path('order_details_user/', u_views.order_details_user, name='order_details_user'),
    path('logout_user/', u_views.logout_user, name='logout_user'),
    path('myreview/', u_views.myReview, name='myreview'),
    path('givereview_Book/<str:id>', u_views.giveReview_Book, name='giveReview_Book'),
    path('givereview_Accessories/<str:id>', u_views.giveReview_Accessories, name='giveReview_Accessories'),



    path('ebook_non/', n_views.ebook_non, name='ebook_non'),
    path('book_details_non/<str:id>/', n_views.book_details_non, name='book_details_non'),
    path('ebook_details_non/<str:id>/', n_views.ebook_details_non, name='ebook_details_non'),
    path('search_non/', n_views.search_non, name='search_non'),
    path('accessories_non/', n_views.accessories_non, name='accessories_non'),
    path('accessories_details_non/<str:id>/', n_views.accessories_details_non, name='accessories_details_non'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

