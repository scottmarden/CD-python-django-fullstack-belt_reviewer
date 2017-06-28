# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Count
import re, bcrypt

# Create your models here.
#------------------------------------User & Manager--------------------------
class UserManager(models.Manager):
	def register(self, data):
		errors = []
		name = data['name']
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
		for item in data:
			if len(data[item]) < 1:
				errors.append(item.replace("_", " ").title() + " is a required field")
		if len(data['name']) < 2:
			errors.append("Name must be at least 2 characters long")
		if any (x.isalpha() for x in name) and any(x.isspace() for x in name):
			pass
		else:
			errors.append("Name can only contain letters and spaces")
		try:
			User.objects.get(alias = data['alias'])
			errors.append("That alias is already taken")
		except:
			pass
		if not EMAIL_REGEX.match(data['email']):
			errors.append("Please enter a valid email address")
		try:
			User.objects.get(email = data['email'])
			errors.append("That email is already registered")
		except:
			pass
		try:
			if relativedelta(today, datetime.datetime.strptime(data['birthday'], "%Y-%m-%d")).years < 13:
				errors.append("You must be at least 13 years old to register")
			else:
				pass
		except:
			pass
		if data['password'] != data['pw_confirm']:
			errors.append("Passwords don't match!")
		if len(errors) == 0:
			hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(name=data['name'], alias=data['alias'], email=data['email'], password=hashed_pw)
			return user
		else:
			return errors

	def login(self, data):
		errors = []
		try:
			user = User.objects.get(email = data['email'])
		except:
			errors.append("Email not found")
			return errors
		if bcrypt.hashpw(data['password'].encode(), user.password.encode()) == user.password:
			pass
		else:
			errors.append("Incorrect password")
		if len(errors) == 0:
			return user
		else:
			return errors

class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.alias

	def user_reviews(self):
		reviews = Review.objects.filter(reviewer=self)
		return reviews

	objects = UserManager()
#------------------------------------Author--------------------------------

class AuthorManager(models.Manager):
	def find_author(self, name):
		name.title()
		print name
		try:
			author = Author.objects.get(name=name)
		except:
			author = Author.objects.create(name=name)
		return author

class Author(models.Model):
	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	objects = AuthorManager()
#------------------------------------Book & Manager--------------------------------
class BookManager(models.Manager):
	def find_book(self, title):
		title.title()
		print title
		try:
			book = Book.objects.get(title__contains=title)
		except:
			book = Book.objects.create(title=title)
		return book

	def new_favorite(self, book_id, user_id):
		user = User.objects.get(id=user_id)
		book = Book.objects.get(id=book_id)
		new_like = user.favorited_books.add(book)
		return new_like


class Book(models.Model):
	title = models.CharField(max_length=255)
	authors = models.ManyToManyField(Author, related_name='books_written')
	favorites = models.ManyToManyField(User, related_name='favorited_books')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	objects = BookManager()

#------------------------------------Review & Manager--------------------------------
class ReviewManager(models.Manager):
	def recent_reviews(self):
		reviews = Review.objects.filter().order_by('-created_at')[:3]
		return reviews

	def new_review(self, data):
		new_review = Review.objects.create(review=data['review'], rating=data['rating'], book=data['book'], reviewer=data['user'])
		return new_review

class Review(models.Model):
	review=models.TextField()
	rating=models.IntegerField()
	book=models.ForeignKey(Book, related_name='book_reviews')
	reviewer= models.ForeignKey(User, related_name='reviewed_books')
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.review

	objects = ReviewManager()
