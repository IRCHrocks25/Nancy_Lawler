from django.contrib import admin
from .models import SurveyResponse

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['email', 'organization', 'role', 'created_at', 'q9_biggest_concern']
    list_filter = ['created_at', 'q9_biggest_concern']
    search_fields = ['email', 'organization', 'role', 'q10_additional_thoughts']
    readonly_fields = ['created_at', 'ip_address', 'raw_data']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('email', 'role', 'organization')
        }),
        ('Visibility', {
            'fields': ('q1_where_ai_used', 'q2_confidence_level')
        }),
        ('Ownership', {
            'fields': ('q3_decision_maker', 'q4_who_knows')
        }),
        ('Controls', {
            'fields': ('q5_policies', 'q6_risk_evaluation')
        }),
        ('Leadership Readiness', {
            'fields': ('q7_leadership_approach', 'q8_what_would_help')
        }),
        ('Forward Looking', {
            'fields': ('q9_biggest_concern', 'q10_additional_thoughts')
        }),
        ('Metadata', {
            'fields': ('created_at', 'ip_address', 'raw_data')
        }),
    )
