from django.urls import path, include
from calendar_google import views as calendar_views

urlpatterns = [
    path('home/show-calendar/', calendar_views.ShowCalendar.as_view(), name='show-calendar'),
    path('show-calendar-teacher/<user_uid>', calendar_views.ShowCalendarTeacher.as_view(), name="show-calendar-teacher"),
    path('show-calendar-student/<user_uid>', calendar_views.ShowCalendarStudent.as_view(), name="show-calendar-student")
]