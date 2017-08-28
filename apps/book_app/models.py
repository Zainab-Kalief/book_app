# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..user_app.models import User

class AuthorManager(models.Manager):
    def create_author(self, name):
        return self.create(name=name)

class ReviewManager(models.Manager):
    def create_review(self, content, rating, book, user):
        return self.create(content=content, rating=rating, book=book, user=user)
    def avg_ratings(self, book):
        total_book_review = self.filter(book=book)
        user_count = total_book_review.count()
        total_ratings = 0
        for val in total_book_review:
            total_ratings += int(val.rating)
        if total_ratings < 4:
            stars = '* * * * * *'
        else:
            average_rating = total_ratings / user_count
            stars = average_rating * ' *'
        return stars
    def add_review(self, data, book, user):
        errors = {}
        if not len(data['review']):
            errors['review'] = 'Enter a reveiw'
        if not len(data['rating']):
            errors['rating'] = 'Select a rating'
        if len(errors):
            return errors
        else:
            return self.create(content=data['review'], rating=data['rating'], book=book, user=user)



class BookManager(models.Manager):
    def create_book(self, data, user):
        errors = {}
        if not len(data['title']):
            errors['title'] = 'Enter a book title'
        if not len(data['new_author']) and not len(data['existing_author']):
            errors['author'] = 'Enter or Select author'
        if not len(data['review']):
            errors['review'] = 'Enter a reveiw'
        if not len(data['rating']):
            errors['rating'] = 'Select a rating'
        if len(errors):
            return errors

        author_data = data['existing_author']
        if len(data['new_author']):
            author_data = data['new_author']
        if Author.objects.filter(name=author_data):
            author = Author.objects.get(name=author_data)
            if self.filter(title=data['title'], author=author):
                this_book = Book.objects.get(title=data['title'])
                review = Review.objects.create_review(data['review'], data['rating'],  this_book, user)
                return [this_book, author, review]
            else:
                book = self.create(title=data['title'], author=author)
                review = Review.objects.create_review(data['review'], data['rating'],  book, user)
                return [book, author, review]
        else:
            new_author = Author.objects.create_author(data['new_author'])
            book = self.create(title=data['title'],  author=new_author)
            review = Review.objects.create_review(data['review'], data['rating'],  book, user)
            return [book, new_author, review]



# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = AuthorManager()


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, related_name='books')
    average_rating = models.CharField(max_length=100)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = BookManager()

class Review(models.Model):
    content = models.TextField()
    rating = models.CharField(max_length=100)
    book = models.ForeignKey(Book, related_name='book_reviews')
    user = models.ForeignKey(User, related_name='user_reviews')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = ReviewManager()
