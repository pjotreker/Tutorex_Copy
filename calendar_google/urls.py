from django.urls import path, include
from calendar_google import views as calendar_views

urlpatterns = [
    path('home/show-calendar/', calendar_views.ShowCalendar.as_view(), name='show-calendar'),
    path('show-calendar-teacher/<user_uid>', calendar_views.ShowCalendarTeacher.as_view(), name="show-calendar-teacher"),
    path('show-calendar-student/<user_uid>', calendar_views.ShowCalendarStudent.as_view(), name="show-calendar-student"),
    path('show-calendar-student/show-calendar-week-student/<user_uid>', calendar_views.ShowCalendarWeekStudent.as_view(), name="show-calendar-week-student"),
    path('show-calendar-teacher/show-calendar-week-teacher/<user_uid>', calendar_views.ShowCalendarWeekTeacher.as_view(), name='show-calendar-week-teacher')
]