from django.urls import path, include
from lessons import views as lessons_views
from users import views as user_views
import notifications.urls

urlpatterns = [
    path('', user_views.index_view, name='index'),
    path('create-classroom/', lessons_views.CreateClassroom.as_view(), name="create-classroom"),
    path('classroom-created/<classroom_id>', lessons_views.ClassroomCreated.as_view(), name="classroom-created-success"),
    path('show-classrooms/', lessons_views.ShowClassrooms.as_view(), name="show-classrooms"),
    path('show-classrooms/display-classroom/<classroom_id>', lessons_views.DisplayClassroom.as_view(), name="display-classroom"),
    path('show-classrooms/display-classroom/<classroom_id>/display-lesson/<lesson_id>', lessons_views.DisplayLesson.as_view(), name='display-lesson'),
    path('show-classrooms/display-classroom/<classroom_id>/display-lesson/<lesson_id>/delete-lesson', lessons_views.DeleteLesson.as_view(), name='delete-lesson'),
    path('show-classrooms/display-classroom/<classroom_id>/add-lesson', lessons_views.AddLesson.as_view(), name="add-lesson"),
    path('show-classrooms/display-classroom/modify-classroom/<class_id>', lessons_views.ModifyClassroom.as_view(), name='modify-classroom'),
    path('show-classrooms/display-classroom/delete-classroom/<class_id>', lessons_views.DeleteClassroom.as_view(), name="delete-classroom"),
    path('show-classrooms/display-classroom/<classroom_id>/students/<student_id>/delete', lessons_views.RemoveStudent.as_view(), name='remove-student-classroom'),
    path('join-classroom/', lessons_views.JoinClassroom.as_view(), name="join_classroom"),
    path('requests/<join_request_id>/accept/', lessons_views.AcceptJoinClassroom.as_view(), name="accept_join_classroom"),
    path('requests/<join_request_id>/reject/', lessons_views.RejectJoinClassroom.as_view(), name="reject_join_classroom"),
    path('timeslots/add', lessons_views.CreateTimeSlot.as_view(), name='create-timeslot'),
]

