# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import User, Book, Author, Review

# Create your views here.
#-------------------------------Login, Registration & Logout--------------------------
def index(request):
	if 'user_id' in request.session:
		return redirect ('/books')
	return render(request, 'review/index.html')

def register(request):
	result = User.objects.register(request.POST)
	if isinstance(result, list):
		for err in result:
			messages.add_message(request, messages.ERROR, err)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
		request.session['alias'] = result.alias
		return redirect('/books')

def login(request):
	result = User.objects.login(request.POST)
	if isinstance(result, list):
		for err in result:
			messages.add_message(request, messages.ERROR, err)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
		request.session['alias'] = result.alias
		print request.session['user_id']
		print request.session['alias']
		return redirect('/books')

def logout(request):
	request.session.flush()
	return redirect('/')
#------------------------------------Homepage--------------------------------------
def success(request):
	if 'user_id' not in request.session:
		return redirect('/')
	result = Review.objects.recent_reviews()
	books = Book.objects.exclude(book_reviews__id__in=result)
	context = {
		'recent_reviews': result,
		'other_books': books
	}
	return render(request, 'review/books.html', context)
#------------------------------------Add & Process Reviews--------------------------------------
def add_review(request):
	authors = Author.objects.all()
	context = {
		'authors': authors
	}
	return render(request, 'review/add_review.html', context)

def process_review(request):
	user = User.objects.get(id=request.session['user_id'])
	if len(request.POST['author']) == 0:
		author = Author.objects.find_author(request.POST['known_author'])
	else:
		author = Author.objects.find_author(request.POST['author'])
	book = Book.objects.find_book(request.POST['title'])
	if author not in book.authors.all():
		book.authors.add(author)
	else:
		pass
	data = {
		'user': user,
		'book': book,
		'review': request.POST['review'],
		'rating': request.POST['rating'],
	}
	redirect_url = "/books/" + str(book.id)
	review = Review.objects.new_review(data)
	return redirect (redirect_url)

def favorite_book(request):
	pass
#------------------------------------User Profile Page--------------------------------------
def user_profile(request, id):
	user = User.objects.get(id=request.session['user_id'])
	reviews = Review.objects.filter(reviewer__id=id)
	num_reviews = len(reviews)
	context = {
		'user': user,
		'reviews': reviews,
		'num_reviews': num_reviews,
	}
	return render(request, 'review/user_profile.html', context)
#------------------------------------Book Profile Page--------------------------------------
def book_reviews(request, id):
	book = Book.objects.get(id=id)
	user = User.objects.get(id = request.session['user_id'])
	context = {
		'favorites': user.favorited_books.all(),
		'book': book,
		'authors': book.authors.all(),
		'first_author': book.authors.all()[0],
		'reviews': book.book_reviews.all().order_by('-rating'),
	}
	return render(request, 'review/book_reviews.html', context)

def delete_review(request, id):
	review = Review.objects.get(id=id)
	review.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#------------------------------------Favorites-------------------------------------


def favorite(request):
	result = Book.objects.new_favorite(request.POST['book_id'], request.session['user_id'])
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def user_favorites(request):
	user = User.objects.get(id=request.session['user_id'])
	context = {
		'favorites': user.favorited_books.all()
	}
	return render(request, 'review/user_favorites.html', context)

def user_non_favorites(request):
	user = User.objects.get(id=request.session['user_id'])
	context = {
		'books': Book.objects.exclude(favorites__id=request.session['user_id']),
	}
	return render(request, 'review/user_non_favorites.html', context)
#------------------------------------Author Directory & Profiles-------------------------------------
def author_directory(request):
	authors = Author.objects.all()
	context = {
		'authors': authors
	}
	return render(request, 'review/authors.html', context)

def author_profile(request, id):
	author = Author.objects.get(id=id)
	context = {
		'author': author,
		'books': author.books_written.all(),
	}
	return render(request, 'review/author_profile.html', context)
