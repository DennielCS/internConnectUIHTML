from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import (
    Category, WorkSetup, Company,
    InternshipListing, ApplicationStatus, Application
)
from .serializers import (
    CategorySerializer, WorkSetupSerializer, CompanySerializer,
    InternshipListingSerializer, ApplicationStatusSerializer,
    ApplicationSerializer
)


# --- Lookup Views ---

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class WorkSetupListView(generics.ListAPIView):
    queryset = WorkSetup.objects.all()
    serializer_class = WorkSetupSerializer


class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.filter(is_verified=True).order_by('name')
    serializer_class = CompanySerializer


class ApplicationStatusListView(generics.ListAPIView):
    queryset = ApplicationStatus.objects.all()
    serializer_class = ApplicationStatusSerializer


# --- Internship Listing Views ---

class InternshipListView(generics.ListAPIView):
    serializer_class = InternshipListingSerializer

    def get_queryset(self):
        qs = InternshipListing.objects.select_related(
            'company', 'category', 'work_setup'
        ).filter(is_active=True).order_by('-created_at')

        category = self.request.query_params.get('category')
        location = self.request.query_params.get('location')
        work_setup = self.request.query_params.get('work_setup')

        if category:
            qs = qs.filter(category_id=category)
        if work_setup:
            qs = qs.filter(work_setup_id=work_setup)
        if location:
            qs = qs.filter(company__location__icontains=location)

        return qs


class InternshipDetailView(generics.RetrieveAPIView):
    queryset = InternshipListing.objects.select_related(
        'company', 'category', 'work_setup'
    ).all()
    serializer_class = InternshipListingSerializer


# --- Application Views ---

class ApplicationCreateView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def perform_create(self, serializer):
        # Auto-assign 'Pending' status on create
        pending = get_object_or_404(ApplicationStatus, label='Pending')
        serializer.save(status=pending)


class ApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')
        sid = self.request.query_params.get('student_number')

        qs = Application.objects.select_related(
            'listing__company', 'status'
        ).all().order_by('-applied_at')

        if email:
            qs = qs.filter(student_email=email)
        if sid:
            qs = qs.filter(student_number=sid)

        return qs


class ApplicationStatusUpdateView(APIView):
    """Coordinator updates application status."""

    def patch(self, request, pk):
        app = get_object_or_404(Application, pk=pk)
        status_id = request.data.get('status')
        new_status = get_object_or_404(ApplicationStatus, pk=status_id)
        app.status = new_status
        app.save()
        return Response(ApplicationSerializer(app).data)


# --- Coordinator Dashboard View ---

class DashboardSummaryView(APIView):
    def get(self, request):
        return Response({
            'total_listings': InternshipListing.objects.filter(is_active=True).count(),
            'total_companies': Company.objects.filter(is_verified=True).count(),
            'total_applications': Application.objects.count(),
            'pending_applications': Application.objects.filter(status__label='Pending').count(),
        })