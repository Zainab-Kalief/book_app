from django.conf.urls import url
from . import views
app_name = 'books'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<id>\d+)/add_book$', views.add_book, name='add_book'),
    url(r'^(?P<id>\d+)/$', views.create_data, name='create_data'),
    url(r'^(?P<id>\d+)/(?P<book_id>\d+)/book_review$', views.show_book, name='show_book'),
    url(r'^(?P<id>\d+)/(?P<book_id>\d+)/add_review$', views.add_book_review, name='add_book_review'),
]
