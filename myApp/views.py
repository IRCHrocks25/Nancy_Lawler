from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import SurveyResponse
import json

def home(request):
    """Main landing page"""
    return render(request, 'myApp/index.html')

def orientation(request):
    """Orientation page before survey"""
    return render(request, 'myApp/orientation.html')

def survey(request):
    """Survey page - multi-step form"""
    if request.method == 'POST':
        # Collect all form data
        response_data = {
            'q1': request.POST.get('q1', ''),
            'q2': request.POST.get('q2', ''),
            'q3': request.POST.get('q3', ''),
            'q4': request.POST.get('q4', ''),
            'q5': request.POST.get('q5', ''),
            'q6': request.POST.get('q6', ''),
            'q7': request.POST.get('q7', ''),
            'q8': request.POST.get('q8', ''),
            'q9': request.POST.get('q9', ''),
            'q10': request.POST.get('q10', ''),
            'email': request.POST.get('email', ''),
            'role': request.POST.get('role', ''),
            'organization': request.POST.get('organization', ''),
        }
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Create survey response
        survey_response = SurveyResponse(
            q1_where_ai_used=response_data['q1'],
            q2_confidence_level=response_data['q2'],
            q3_decision_maker=response_data['q3'],
            q4_who_knows=response_data['q4'],
            q5_policies=response_data['q5'],
            q6_risk_evaluation=response_data['q6'],
            q7_leadership_approach=response_data['q7'],
            q8_what_would_help=response_data['q8'],
            q9_biggest_concern=response_data['q9'],
            q10_additional_thoughts=response_data['q10'],
            email=response_data['email'],
            role=response_data['role'],
            organization=response_data['organization'],
            ip_address=ip,
            raw_data=response_data
        )
        survey_response.save()
        
        # Store response ID in session for thank you page
        request.session['survey_response_id'] = survey_response.id
        
        return redirect('thank_you')
    
    return render(request, 'myApp/survey.html')

def thank_you(request):
    """Thank you page after survey submission"""
    return render(request, 'myApp/thank_you.html')

def email_copy(request):
    """Handle email copy request"""
    if request.method == 'POST':
        email = request.POST.get('email', '')
        survey_id = request.session.get('survey_response_id')
        
        if survey_id:
            try:
                survey_response = SurveyResponse.objects.get(id=survey_id)
                # Update email if provided
                if email:
                    survey_response.email = email
                    survey_response.save()
                
                # Here you would typically send an email with the survey responses
                # For now, we'll just return a success message
                # In production, use Django's email functionality:
                # from django.core.mail import send_mail
                # send_mail(...)
                
                return JsonResponse({'status': 'success', 'message': 'Email copy will be sent shortly.'})
            except SurveyResponse.DoesNotExist:
                pass
        
        return JsonResponse({'status': 'error', 'message': 'Survey response not found.'}, status=400)
    
    return redirect('thank_you')
