from django import forms
from auto_reply.models import UserProfile

class SignatureForm(forms.Form):
    signature_html = forms.CharField(widget=forms.Textarea, required=False)
    image = forms.ImageField(required=False)

class UserProfileForm(forms.ModelForm):
    """Form for uploading user profile resume."""
    class Meta:
        model = UserProfile
        fields = ['resume']
        labels = {
            'resume': 'Upload Resume (PDF, DOCX, DOC, etc.)'
        }
        help_texts = {
            'resume': 'Max file size: 10MB. Supported: PDF, DOCX, DOC, TXT'
        }
    
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Validate file size (10MB max)
            if resume.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be less than 10MB.")
            # Validate file type
            allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.rtf']
            file_name = resume.name.lower()
            if not any(file_name.endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError("Only PDF, DOCX, DOC, TXT, and RTF files are allowed.")
        return resume
