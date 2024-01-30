# company/views.py
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.crypto import get_random_string
from .models import Company, WhatsAppNumber, UserCompanyMapping
from .forms import CompanyForm

@method_decorator(login_required, name='dispatch')
class CompanyCreateView(View):
    def get(self, request):
        form = CompanyForm()
        return render(request, 'company/company_create.html', {'form': form})

    def post(self, request):
        form = CompanyForm(request.POST)

        if form.is_valid():
            company = form.save(commit=False)
            

            # Get WhatsApp number from the form
            
            whatsapp_number = form.cleaned_data['whatsapp_number']
            
            company.save()

            # Create or get the WhatsappNumber instance and associate it with the company
            whatsapp_number_instance, created = WhatsAppNumber.objects.get_or_create(number=whatsapp_number)
            whatsapp_number_instance.companies.add(company)

            # Create UserCompanyMapping for the authenticated user and the created company
            user_company_mapping = UserCompanyMapping.objects.create(user=request.user, company=company)

            # Generate a verification token for user mapping
            verification_token = get_random_string(length=32)
            user_company_mapping.verification_token = verification_token
            user_company_mapping.save()

            # Send confirmation email to the company owner with user mapping verification link
            verification_link = f"http://127.0.0.1:8000/company/verify_user_mapping/{user_company_mapping.id}/{verification_token}/"
            subject = 'Company Confirmation'
            print(verification_link)
            message = render_to_string('company/confirmation_email.html', {'company': company, 'verification_link': verification_link})
            #plain_message = strip_tags(message)
            from_email = 'webappbook@gmail.com'  # Update with your email or use a custom sender
            to_email = company.email
            

            email = EmailMessage(subject, message, from_email, [to_email])
            email.content_subtype = 'html'
            email.send()

            return redirect('account_profile')

        return render(request, 'company/company_create.html', {'form': form})

class VerifyUserMappingView(View):
    def get(self, request, mapping_id, verification_token):
        user_company_mapping = get_object_or_404(UserCompanyMapping, id=mapping_id, verification_token=verification_token)

        # Verify the user mapping
        user_company_mapping.is_user_verified = True
        user_company_mapping.save()

        # Redirect to a success page or display a success message
        return render(request, 'company/user_mapping_verified.html')