from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^books$', views.success),
	url(r'^books/add_review$', views.add_review),
	url(r'^books/process_review$', views.process_review),
	url(r'^books/(?P<id>\d+$)', views.book_reviews),
	url(r'^user/(?P<id>\d+$)', views.user_profile),
	url(r'^authors/(?P<id>\d+$)', views.author_profile),
	url(r'^reviews/delete/(?P<id>\d+$)', views.delete_review),
	url(r'^authors$', views.author_directory),
	url(r'^new_favorite$', views.favorite),
	url(r'^user_favorites$', views.user_favorites),
	url(r'^user_non_favorites$', views.user_non_favorites),
	url(r'^logout$', views.logout),
]
