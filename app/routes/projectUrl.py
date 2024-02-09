from django.urls import path
from app.controllers.projectController import ProjectView

urlpatterns = [
    path('', ProjectView.create_project),
    path('<int:id>', ProjectView.retrieve_single_project),
    path('<int:id>/update', ProjectView.update_project),
    path('<int:id>/delete', ProjectView.delete_project),
    path('all', ProjectView.retrieve_all_projects),
]