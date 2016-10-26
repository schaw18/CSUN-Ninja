from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^comp/', views.showSections),
    url(r'^$', views.ShowAll),

]
