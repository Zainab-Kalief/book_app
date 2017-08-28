# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from ..user_app.models import User
from .models import Book, Author, Review
from django.core.urlresolvers import reverse
from django.contrib import messages

# Create your views here.
def average():
    for book in Book.objects.all():
        avg = Review.objects.avg_ratings(book)
        Book.objects.filter(id=book.id).update(average_rating=avg)

def home(request):
    average()
    if User.objects.filter(id=int(request.session['user_id'])):
        user = User.objects.get(id=int(request.session['user_id']))
        context = {'user': user, 'reveiws': Review.objects.all().order_by('-created_at')[:4], 'books': Book.objects.all().order_by('created_at')}
        return render(request, 'book_app/home.html', context)
    else:
        return redirect('users:index')

#TO SHOW 5 POSTS --- Entry.objects.all()[:5]

def add_book(request, id):
    user = User.objects.get(id=id)
    context = {'user': user, 'authors': Author.objects.all()}
    return render(request, 'book_app/add_book.html', context)


def create_data(request, id):
    user = User.objects.get(id=id)
    entry = Book.objects.create_book(request.POST, user)
    if type(entry) is dict:
        if 'title' in entry:
            messages.add_message(request, messages.INFO, entry['title'], extra_tags='title')
        if 'author' in entry:
            messages.add_message(request, messages.INFO, entry['author'], extra_tags='author')
        if 'review' in entry:
            messages.add_message(request, messages.INFO, entry['review'], extra_tags='review')
        if 'rating' in entry:
            messages.add_message(request, messages.INFO, entry['rating'], extra_tags='rating')
        return redirect(reverse('books:add_book', kwargs={'id': id }))
    else:
        return redirect(reverse('books:show_book', kwargs={'id': id, 'book_id': entry[0].id}))


def show_book(request, id, book_id):
    book = Book.objects.get(id=book_id)
    reviews = Review.objects.filter(book=book).order_by('-created_at')
    context = {'book': book, 'reviews': reviews, 'user_id': id,}
    return render(request, 'book_app/show_book.html', context)


def add_book_review(request, id, book_id):
    print '&&&&&&&&&&&&&&&&&&&&'
    user = User.objects.get(id=id)
    book = Book.objects.get(id=book_id)
    entry = Review.objects.add_review(request.POST, book, user)
    print entry, '***************'
    print '~~~~~~~~~~~~~~~'
    if type(entry) is dict:
        if 'review' in entry:
            messages.add_message(request, messages.INFO, entry['review'], extra_tags='review')
        if 'rating' in entry:
            messages.add_message(request, messages.INFO, entry['rating'], extra_tags='rating')
        return redirect(reverse('books:show_book', kwargs={'id': id, 'book_id': book.id}))
    else:
        print Review.objects.filter(book=book)
        return redirect(reverse('books:show_book', kwargs={'id': id, 'book_id': book.id}))
