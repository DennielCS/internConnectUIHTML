from django.urls import path
from .views import (
    CategoryListView, WorkSetupListView, CompanyListView,
    ApplicationStatusListView, InternshipListView, InternshipDetailView,
    ApplicationCreateView, ApplicationListView,
    ApplicationStatusUpdateView, DashboardSummaryView,
)

urlpatterns = [
    # Lookups
    path('categories/', CategoryListView.as_view()),
    path('work-setups/', WorkSetupListView.as_view()),
    path('companies/', CompanyListView.as_view()),
    path('application-statuses/', ApplicationStatusListView.as_view()),

    # Internship Listings
    path('internships/', InternshipListView.as_view()),
    # Added <int:pk> so Django knows which specific internship to retrieve
    path('internships/<int:pk>/', InternshipDetailView.as_view()),

    # Applications
    path('applications/', ApplicationCreateView.as_view()),
    path('applications/track/', ApplicationListView.as_view()),
    # Added <int:pk> so Django knows which specific application status to update
    path('applications/<int:pk>/status/', ApplicationStatusUpdateView.as_view()),

    # Dashboard
    path('dashboard/summary/', DashboardSummaryView.as_view()),
]