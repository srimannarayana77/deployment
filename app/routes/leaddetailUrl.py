from django.urls import path
from app.controllers.leaddetailController import LeadDetailsView

urlpatterns = [
    path('', LeadDetailsView.create_lead),
    path('<int:id>', LeadDetailsView.retrieve_single_lead),
    # path('<int:id>/update', LeadDetailsView.update_lead),
    path('<int:id>/delete',LeadDetailsView.delete_lead),
    path('all', LeadDetailsView.retrieve_all_leads),
]