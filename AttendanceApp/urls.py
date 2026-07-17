from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	             path('AdminLogin.html', views.AdminLogin, name="AdminLogin"), 
		     path('FacultyLogin.html', views.FacultyLogin, name="FacultyLogin"), 
	             path('AddStudent.html', views.AddStudent, name="AddStudent"),
	             path('AddStudentAction', views.AddStudentAction, name="AddStudentAction"),	
	             path('AdminLoginAction', views.AdminLoginAction, name="AdminLoginAction"),
	             path('FacultyLoginAction', views.FacultyLoginAction, name="FacultyLoginAction"),
	             path('ViewStudent', views.ViewStudent, name="ViewStudent"),
	             path('ViewAttendance', views.ViewAttendance, name="ViewAttendance"),
	             path('ViewAttendanceAction', views.ViewAttendanceAction, name="ViewAttendanceAction"),
	             path('MarkAttendance', views.MarkAttendance, name="MarkAttendance"),
	             path('MarkAttendanceAction', views.MarkAttendanceAction, name="MarkAttendanceAction"),
	             path('ViewStudentAttendance', views.ViewStudentAttendance, name="ViewStudentAttendance"),
	             path('ViewStudentAttendanceAction', views.ViewStudentAttendanceAction, name="ViewStudentAttendanceAction"),
	             path('Graph', views.Graph, name="Graph"), 	
		     path('HodLogin.html', views.HodLogin, name="HodLogin"), 
		     path('HodLoginAction', views.HodLoginAction, name="HodLoginAction"),

]
