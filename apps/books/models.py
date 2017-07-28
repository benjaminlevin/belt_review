
from __future__ import unicode_literals
from django.db import models
import bcrypt, re, datetime
from django.contrib import messages
from django.db.models import Count

#USERS

class UserManager(models.Manager):
    def validate(self, request):
        post_data = request.POST
        data_is_good = True
        if len(post_data['first_name']) < 2:
            messages.error(request, "First Name must be at least two characters long")
            data_is_good=False
        if re.match('^[A-Za-z]*$', post_data['first_name']) is None:
            messages.error(request, "First Name must contain valid characters")
            data_is_good=False            
        if len(post_data['last_name']) < 2:
            messages.error(request, "Last Name must be at least two characters long")
            data_is_good=False
        if  re.match('^[A-Za-z]*$', post_data['last_name']) is None:
            messages.error(request, "Last Name must contain valid characters")
            data_is_good=False        
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', post_data['email']) is None or len(post_data['email']) < 1:
            messages.error(request, "Valid email format required")
            data_is_good=False
        if len(post_data['password']) < 8 or len(post_data['confirm_password']) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            data_is_good=False
        elif post_data['password'] != post_data['confirm_password']:
            messages.error(request, "Passwords do not match")
            data_is_good=False       
        elif self.filter(email=post_data['email']).exists():
            messages.error(request, "Email address already in use")
            data_is_good=False         
        if data_is_good is True:
            messages.success(request, "Successful registration!")
            hashed = bcrypt.hashpw(post_data['password'].encode(encoding="utf-8", errors="strict"), bcrypt.gensalt())
            user = self.create(
                first_name = post_data['first_name'],
                last_name = post_data['last_name'],
                email = post_data['email'],
                password = hashed
            )
        return data_is_good, user

    def login(self, request):
        post_data = request.POST
        data_is_good = True
        user = User.objects.filter(email=post_data['email'])
        if user:
            hashed = User.objects.get(email=post_data['email']).password.encode(encoding="utf-8", errors="strict")
            password = post_data['password'].encode(encoding="utf-8", errors="strict")
            if bcrypt.checkpw(password, hashed) is True:
                data_is_good = True
            else:
                messages.error(request, "Invalid password")
                data_is_good = False
        else:
            messages.error(request, "Invalid email")
            data_is_good = False
        return data_is_good

class User(models.Model):
    email = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

#BOOKS

class BookManager(models.Manager):
    def addBook(self, request):
        post_data = request.POST
        if len(post_data['title'])>0 and len(post_data['new_author'])<1 and len(post_data['author'])>0:
            new_book = Book.objects.create(title=post_data['title'], author=post_data['author'])
            data_is_good=True 
            return self, new_book, data_is_good
        elif len(post_data['title'])>0 and len(post_data['new_author'])>0:
            new_book = Book.objects.create(title=post_data['title'], author=post_data['new_author'])
            data_is_good=True
            return self, new_book, data_is_good                     
        else:
            new_book = ''
            messages.error(request, "Book title must contain characters and author must be selected")
            data_is_good=False
            return self, new_book, data_is_good

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

#REVIEWS

class ReviewManager(models.Manager):
    def addReview(self, request, book, user):
        post_data = request.POST        
        if len(post_data['review'])<1:
            data_is_good=False            
            messages.error(request, "Review must contain characters")
            return self, data_is_good             
        else:
            data_is_good=True            
            Review.objects.create(review=post_data['review'], stars=post_data['stars'], book=book, user=user)
            return self, data_is_good     

    def deleteReview(self, request):
        post_data = request.POST
        Review.objects.get(id=post_data['rid']).delete()
        return self        

class Review(models.Model):
    review = models.TextField(max_length=1000)
    stars = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    objects = ReviewManager()