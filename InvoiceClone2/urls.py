
from django.contrib import admin
from django.urls import path
from Home import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('add_invoice/', views.add_invoice, name='add_invoice'),
    path('add_invoice2/', views.add_invoice2, name='add_invoice2'),
    path('service-provider/', views.company, name='service_provider'),
    path('update-company/<int:id>/', views.update_company, name='update_company'),
    path('delete-company/<int:id>/', views.delete_company, name='delete_company'),
    path('allList/', views.allList, name='allList'),
    path('review/<int:pk>/', views.review, name='review'),
    path('report_list/', views.report_list, name='report_list'),
    path('pdf-report/<int:pk>/', views.pdf_report, name='pdf_report')
]
