from django.urls import path
from .views import AdListView, AdCreate, AdDetailView, AdEdit, AdDelete, RespCreate
from sign.views import resp_change_status, delete_response, RespList

urlpatterns = [
    path('board/', AdListView.as_view(), name='board'),
    path('board/add', AdCreate.as_view(), name='add_list'),
    path('edit/<int:pk>', AdEdit.as_view(), name='ad_edit'),
    path('delete/<int:pk>', AdDelete.as_view(), name='ad_delete'),
    path('board/<int:pk>', AdDetailView.as_view(), name='ad_detail'),
    path('add_resp/', RespCreate.as_view(), name='resp_create'),
    path('resp_list/', RespList.as_view(), name='resp_list'),
    path('change_resp/', resp_change_status, name='resp_change'),
    path('delete_resp/', delete_response, name='resp_delete')

]
