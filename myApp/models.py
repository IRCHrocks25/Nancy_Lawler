from django.db import models
import json

class SurveyResponse(models.Model):
    """Model to store survey responses"""
    
    # Group 1: Visibility
    q1_where_ai_used = models.CharField(max_length=100, blank=True)
    q2_confidence_level = models.CharField(max_length=100, blank=True)
    
    # Group 2: Ownership
    q3_decision_maker = models.CharField(max_length=100, blank=True)
    q4_who_knows = models.CharField(max_length=100, blank=True)
    
    # Group 3: Controls
    q5_policies = models.CharField(max_length=100, blank=True)
    q6_risk_evaluation = models.CharField(max_length=100, blank=True)
    
    # Group 4: Leadership Readiness
    q7_leadership_approach = models.CharField(max_length=100, blank=True)
    q8_what_would_help = models.CharField(max_length=100, blank=True)
    
    # Group 5: Forward + Prompt
    q9_biggest_concern = models.CharField(max_length=100, blank=True)
    q10_additional_thoughts = models.TextField(blank=True)
    
    # Contact Info
    email = models.EmailField(blank=True)
    role = models.CharField(max_length=200, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # Store raw response data as JSON for flexibility
    raw_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Survey Response'
        verbose_name_plural = 'Survey Responses'
    
    def __str__(self):
        return f"Survey Response - {self.email or 'Anonymous'} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
