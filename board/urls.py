from django.urls import path
from .views import AdListView, AdCreate, AdDetailView

urlpatterns = [
    path('board/', AdListView.as_view(), name='board'),
    path('board/add', AdCreate.as_view(), name='add_list'),
    path('board/<int:pk>', AdDetailView.as_view(), name='ad_detail')

]
