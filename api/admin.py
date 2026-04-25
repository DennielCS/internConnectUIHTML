from django.contrib import admin
from .models import (
    Category, WorkSetup, Company,
    InternshipListing, ApplicationStatus, Application
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(WorkSetup)
class WorkSetupAdmin(admin.ModelAdmin):
    list_display = ('id', 'label')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'is_verified', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('is_verified',)
    list_editable = ('is_verified',)

@admin.register(InternshipListing)
class InternshipListingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'company', 'category', 'work_setup',
        'deadline', 'slots', 'is_active'
    )
    search_fields = ('title', 'company__name')
    list_filter = ('category', 'work_setup', 'is_active')
    list_editable = ('is_active',)

@admin.register(ApplicationStatus)
class ApplicationStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'label')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'student_name', 'student_number', 'listing',
        'status', 'applied_at'
    )
    search_fields = ('student_name', 'student_email', 'student_number')
    list_filter = ('status',)