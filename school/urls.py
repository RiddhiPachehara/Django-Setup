from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('schools/', views.schools, name='schools'),
    path('classrooms/', views.classrooms, name='classrooms'),
    path('teachers/', views.teachers, name='teachers'),
    path('students/', views.students, name='students'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
    "dashboard/schools/",
    views.school_list,
    name="school_list"
),
path(
    "dashboard/schools/add/",
    views.school_add,
    name="school_add"
),
path(
    "dashboard/schools/edit/<int:id>/",
    views.school_edit,
    name="school_edit"
),
path(
    "dashboard/schools/delete/<int:id>/",
    views.school_delete,
    name="school_delete"
),
path("login/", views.login_view, name="login"),
path(
    "dashboard/classrooms/",
    views.classroom_list,
    name="classroom_list"
),
path(
    "dashboard/classrooms/add/",
    views.classroom_add,
    name="classroom_add"
),
path(
    "dashboard/classrooms/edit/<int:id>/",
    views.classroom_edit,
    name="classroom_edit"
),
path(
    "dashboard/classrooms/delete/<int:id>/",
    views.classroom_delete,
    name="classroom_delete"
),
path("dashboard/teachers/", views.teacher_list, name="teacher_list"),
path("dashboard/teachers/add/", views.teacher_add, name="teacher_add"),
path("dashboard/teachers/edit/<int:id>/", views.teacher_edit, name="teacher_edit"),
path("dashboard/teachers/delete/<int:id>/", views.teacher_delete, name="teacher_delete"),
path("dashboard/students/", views.student_list, name="student_list"),
path("dashboard/students/add/", views.student_add, name="student_add"),
path("dashboard/students/edit/<int:id>/", views.student_edit, name="student_edit"),
path("dashboard/students/delete/<int:id>/", views.student_delete, name="student_delete"),
path("logout/", views.logout_view, name="logout"),
path(
    "dashboard/students/<int:id>/photos/",
    views.student_photos,
    name="student_photos",
),
] 