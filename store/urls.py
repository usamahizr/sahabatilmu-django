from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'), #"<slug:category_slug>" jenis category dalam search....rujuk lect 50 minit 3.52
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'), #operasi untuk buat SINGLE PAGE
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]
