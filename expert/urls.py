from django.urls import path

from . import views

app_name = 'expert'

urlpatterns = [
    # path('', views.index, name='index'),
    
    path('expert/list/', views.ExpertList.as_view(), name='expert-list'),
    path('expert/create/', views.ExpertCreate.as_view(), name='expert-create'),
    path('expert/detail/<int:pk>/', views.ExpertDetail.as_view(), name='expert-detail'),
    path('expert/update/<int:pk>/', views.ExpertUpdate.as_view(), name='expert-update'),
    path('expert/delete/<int:pk>/', views.ExpertDelete.as_view(), name='expert-delete'),
]
