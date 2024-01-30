# company/urls.py
from django.urls import path
from .views import CompanyCreateView, VerifyUserMappingView 

urlpatterns = [
    path('create/', CompanyCreateView.as_view(), name='company_create'),
    path('verify_user_mapping/<int:mapping_id>/<str:verification_token>/', VerifyUserMappingView.as_view(), name='verify_user_mapping'),
    
]
