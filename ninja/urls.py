from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^signup/', views.user_sign_up, name='signup'),
    url(r'^filters/', views.filters, name='filters'),
    url(r'^flush_db/', views.flush_db, name='flush_db'),
    url(r'^update_classes/', views.update_classes, name='update_classes'),

]
