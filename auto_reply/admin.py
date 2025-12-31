from django.contrib import admin
from auto_reply.models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'has_resume', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    
    def has_resume(self, obj):
        return bool(obj.resume)
    has_resume.short_description = 'Resume Uploaded'
