from django.urls import path
from .views import AdListView, AdCreate, AdDetailView, AdEdit, AdDelete, RespCreate

urlpatterns = [
    path('board/', AdListView.as_view(), name='board'),
    path('board/add', AdCreate.as_view(), name='add_list'),
    path('edit/<int:pk>', AdEdit.as_view(), name='ad_edit'),
    path('delete/<int:pk>', AdDelete.as_view(), name='ad_delete'),
    path('board/<int:pk>', AdDetailView.as_view(), name='ad_detail'),
    path('add_resp/', RespCreate.as_view(), name='resp_create'),

]
