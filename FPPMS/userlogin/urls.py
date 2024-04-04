
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('studentlogin', views.student_home, name="studentlogin"),
    path('studentdashboard',login_required(views.student_dashboard),name="studentdashboard"),
    path('createmilestone', views.student_createmilestone, name='createmilestone'),
    path('studentLogout', views.student_Logout, name='studentLogout'),
    path('milestone/<int:milestone_id>/delete/', views.delete_milestone, name='delete_milestone'),
    path('milestone/<int:milestone_id>/update/', views.update_milestone, name='update_milestone'),
    path('studentlogin', LoginView.as_view(), name='redirectlogin'),
]
