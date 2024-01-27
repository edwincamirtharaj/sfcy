# company/urls.py
from django.urls import path
from .views import CompanyCreateView, VerifyUserMappingView #company_confirmation_pending, company_mapping_approval, company_mapping_confirmation_sent

urlpatterns = [
    path('create/', CompanyCreateView.as_view(), name='company_create'),
    path('verify_user_mapping/<int:mapping_id>/<str:verification_token>/', VerifyUserMappingView.as_view(), name='verify_user_mapping'),
    #path('confirmation-pending/', company_confirmation_pending, name='company_confirmation_pending'),
    #path('mapping-approval/<int:mapping_id>/', company_mapping_approval, name='company_mapping_approval'),
    #path('mapping-confirmation-sent/', company_mapping_confirmation_sent, name='company_mapping_confirmation_sent'),
    # Add other URLs as needed
]
