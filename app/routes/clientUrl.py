from django.urls import path
from app.controllers.clientController  import ClientView

urlpatterns = [
    path('', ClientView.create_client),
    path('<int:id>', ClientView.retrieve_single_client),
    path('<int:id>/update', ClientView.update_client),
    path('<int:id>/delete', ClientView.delete_client),
    path('all', ClientView.retrieve_all_clients),
    path('signin', ClientView.client_sign_in)
]