from rest_framework import serializers
from .models import (
    Category, WorkSetup, Company,
    InternshipListing, ApplicationStatus, Application
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class WorkSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSetup
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class InternshipListingSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_logo = serializers.ImageField(source='company.logo', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    work_setup_label = serializers.CharField(source='work_setup.label', read_only=True)
    location = serializers.CharField(source='company.location', read_only=True)

    class Meta:
        model = InternshipListing
        fields = [
            'id', 'title', 'description', 'requirements',
            'duration', 'slots', 'deadline', 'is_active',
            'company', 'company_name', 'company_logo', 'location',
            'category', 'category_name',
            'work_setup', 'work_setup_label',
            'created_at',
        ]

class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatus
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    company_name = serializers.CharField(source='listing.company.name', read_only=True)
    status_label = serializers.CharField(source='status.label', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'student_name', 'student_email', 'student_number',
            'cover_letter', 'resume', 'applied_at', 'updated_at',
            'listing', 'listing_title', 'company_name',
            'status', 'status_label',
        ]
        extra_kwargs = {
            'status': {'required': False}
        }