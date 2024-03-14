
from django.urls import path
from . import views

urlpatterns = [
    path('studentlogin', views.student_home, name="studentlogin"),
    path('studentdashboard',views.student_dashboard,name="studentdashboard"),
    path('createmilestone', views.student_createmilestone, name='createmilestone'),
    path('studentLogout', views.student_Logout, name='studentLogout'),
    path('milestone/<int:milestone_id>/delete/', views.delete_milestone, name='delete_milestone'),
]
