from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import contacts, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, toggle_publish, CategoryListView

app_name = CatalogConfig.name

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='create'),
    path('', ProductListView.as_view(), name='list'),
    path('contacts/', contacts, name='contacts'),
    path('view/<int:pk>/catalog/', cache_page(60)(ProductDetailView.as_view()), name='view'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('publish/<int:pk>/', toggle_publish, name='toggle_publish'),
    path('categories/', CategoryListView.as_view(), name='categories'),

]