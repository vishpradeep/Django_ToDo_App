from django.urls import path   
from todoapp import views 
urlpatterns = [
    # path('',views.TaskList,name='tasklist'),
    path('', views.TaskList.as_view(),name='tasklist'),
    path('task/<int:pk>/', views.TaskDetail.as_view(),name='taskdetail'),
    path('taskcreate/', views.TaskCreate.as_view(),name='taskcreate'),
    path('taskupdate/<int:pk>/', views.TaskUpdate.as_view(),name='taskupdate'),
    path('taskdelete/<int:pk>/', views.TaskDelete.as_view(),name='taskdelete'),
    path('login/', views.LoginView.as_view(),name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'),name='logout'),
    path('register/', views.RegisterPage.as_view(),name='register'),
]
