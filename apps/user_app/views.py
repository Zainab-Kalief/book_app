# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from ..book_app.models import Book, Author, Review


# Create your views here.
def index(request):
    return render(request, 'user_app/index.html')

def signUp_test(request):
    entry = User.objects.sign_up(request.POST)
    if not type(entry) is dict:
        request.session['user_id'] = entry.id
        return redirect('books:home') #redirect to the root named index
    else:
        if 'name' in entry:
            messages.add_message(request, messages.INFO, entry['name'], extra_tags='sign_up')
        if 'name_exist' in entry:
            messages.add_message(request, messages.INFO, entry['name_exist'], extra_tags='sign_up')
        if 'email' in entry:
            messages.add_message(request, messages.INFO, entry['email'], extra_tags='sign_up')
        if 'password' in entry:
            messages.add_message(request, messages.INFO, entry['password'], extra_tags='sign_up')
        if 'confirm_password' in entry:
            messages.add_message(request, messages.INFO, entry['confirm_password'], extra_tags='sign_up')
        if 'email_exist' in entry:
            messages.add_message(request, messages.INFO, entry['email_exist'], extra_tags='sign_up')
        return redirect('users:index')

def logIn_test(request):
    entry = User.objects.log_in(request.POST)
    print entry
    if type(entry) is dict:
        if 'password' in entry:
            messages.add_message(request, messages.INFO, entry['password'], extra_tags='log_in')
        if 'email' in entry:
            messages.add_message(request, messages.INFO, entry['email'], extra_tags='log_in')
        return redirect('users:index')
    else:
        request.session['user_id'] = entry.id
        return redirect('books:home')

def show_user(request, user_id):
    user = User.objects.get(id=user_id)
    context = {'user': user}
    return render(request, 'user_app/user.html', context)
