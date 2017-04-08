from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^signup/', views.user_sign_up, name='signup'),
    url(r'^filters/', views.filters, name='filters'),
    url(r'^flush_db/', views.flush_db, name='flush_db'),
    url(r'^update_classes/', views.update_classes, name='update_classes'),
    url(r'^upload', views.upload, name='upload'),
    url(r'^mock_major_data', views.load_mock_major_data, name='load_mock_major_data'),
    url(r'^return_all_courses_taken_by_student', views.return_all_courses_taken_by_student, name='return_all_courses_taken_by_student'),
    url(r'^return_all_sections_toward_major/(?:<major>[A-Z]+)?',
        views.return_all_sections_toward_major,
        name='return_all_sections_toward_major'),
    url(r'^return_all_required_sections/(?:<major>[A-Z]+)?',
            views.return_all_required_sections,
            name='return_all_required_sections'),
    url(r'^dpr_parser', views.dpr_parser, name='dpr_parser'),
]
