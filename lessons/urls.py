from django.urls import path, include
from lessons import views as lessons_views
from users import views as user_views
import notifications.urls

urlpatterns = [
    path('', user_views.index_view, name='index'),
    path('create-classroom/', lessons_views.CreateClassroom.as_view(), name="create-classroom"),
    path('class-created/', lessons_views.ClassroomCreated.as_view(), name="class-created-success"),

]

