from django.conf.urls import url
from . import views
app_name = 'users'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sign_up$', views.signUp_test, name='sign_up'),
    url(r'^log_in$', views.logIn_test, name='log_in'),
    url(r'^user/(?P<user_id>\d+)$', views.show_user, name='show_user'),
]
