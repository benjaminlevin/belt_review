from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Book, Review
from django.db.models import Count

#login and registration

def index(request):
    #context only for reviewing all registered users
    context = {
        "user" : User.objects.all()
    }
    return render(request, "books/login.html", context)

def register(request):
    if request.method == 'POST':
        user = User.objects.validate(request)
        if user[0] is False:
            return redirect('/')
        else:
            request.session['id'] = user[1].id
            request.session['name'] = user[1].first_name            
            return redirect('/books')
    return redirect("/")

def login(request):
    if request.method == 'POST':
        if User.objects.login(request) is True:
            user = User.objects.get(email=request.POST['email'])
            request.session['id'] = user.id
            request.session['name'] = user.first_name
            return redirect('/books')
        else:
            return redirect('/')
    else:
        return redirect('/')   

def logout(request):
    request.session['id'] = None
    request.session['name'] = None
    return redirect('/books')

def users(request, id):
    user = User.objects.filter(id=id)
    review = Review.objects.filter(user=user).annotate(num_reviews=Count('review'))
    total = review.count()
    context = {
        "user" : user,
        "review" : review,
        "total" : total,
    }
    return render(request, "books/user.html", context)

#books

def books(request):
    list(messages.get_messages(request)) #for clearing messages
    if request.session['id'] != None:
        context = {
            "user" : User.objects.all(),
            "review" : Review.objects.annotate().order_by('-created_at')[:3],
            "book" : Book.objects.all()
        }
        return render(request, "books/books.html", context)
    else:
        return redirect('/')

def add(request):
    context = {
        "user" : User.objects.all(),
        "review" : Review.objects.annotate().order_by('-created_at')[:3],
        "book" : Book.objects.annotate().order_by('title'),
        "author" : Book.objects.values('author').distinct()
    }
    return render(request, "books/add.html", context)

def addbr(request):
    if request.method == "POST":
        new_book = Book.objects.addBook(request)
        if new_book[2] is False:
            if len(request.POST['title'])>0 and len(request.POST['new_author'])>0:
                return redirect('/books/'+str(new_book[3].id))
            elif len(request.POST['title'])>0 and len(request.POST['author'])>0:
                return redirect('/books/'+str(new_book[3].id))
            else:
                return redirect('/add')
        elif new_book[2] is True:
            user = User.objects.get(id=request.session['id'])
            review = Review.objects.addReview(request, new_book[1], user)
            if review[1] is True:
                return redirect('/books/'+str(new_book[1].id))
            else:
                return redirect('/add')
    else:
        return redirect('/books')

def addr(request, id):
    if request.method == "POST":
        book = Book.objects.get(id=id)
        user = User.objects.get(id=request.session['id'])
        review = Review.objects.addReview(request, book, user)
        if review[1] is True:
            return redirect('/books/'+str(book.id))
        else:
            return redirect('/books/'+str(book.id))
    else:
        return redirect('/books/', id)

def delete(request):
    if request.method == "POST":
        review = Review.objects.get(id=request.POST['rid'])
        Review.objects.deleteReview(request)
        return redirect('/books/'+str(review.book.id))
    else:
        return redirect('/books')    

def book(request, id):
    book = Book.objects.filter(id=id)
    context = {
        "user" : User.objects.all(),
        "review" : Review.objects.filter(book=book),
        "book" : book,
    }
    return render(request, "books/book.html", context)

#for clearing entire DB
def deletea(request):
    user = User.objects.all()
    book = Book.objects.all()
    review = Review.objects.all()     
    user.delete()
    book.delete()
    review.delete()
    return redirect('/')
