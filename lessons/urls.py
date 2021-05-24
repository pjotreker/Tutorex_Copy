from django.urls import path, include
from lessons import views as lessons_views
from users import views as user_views
import notifications.urls

urlpatterns = [
    path('', user_views.index_view, name='index'),
    path('create-classroom/', lessons_views.CreateClassroom.as_view(), name="create-classroom"),
    path('classroom-created/<classroom_id>', lessons_views.ClassroomCreated.as_view(), name="classroom-created-success"),
    path('join-classroom/', lessons_views.JoinClassroom.as_view(), name="join-classroom"),
    path('modify-classroom/<class_id>')

]

