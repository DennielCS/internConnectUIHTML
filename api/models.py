from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class WorkSetup(models.Model):
    SETUP_CHOICES = [
        ('Onsite', 'Onsite'),
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
    ]
    label = models.CharField(max_length=50, unique=True, choices=SETUP_CHOICES)

    def __str__(self):
        return self.label


class Company(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='companies/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class InternshipListing(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='listings')
    work_setup = models.ForeignKey(WorkSetup, on_delete=models.PROTECT, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    duration = models.CharField(max_length=100)  # e.g. '6 months'
    slots = models.PositiveIntegerField(default=1)
    deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} @ {self.company.name}"


class ApplicationStatus(models.Model):
    label = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.label


class Application(models.Model):
    listing = models.ForeignKey(InternshipListing, on_delete=models.CASCADE, related_name='applications')
    student_name = models.CharField(max_length=200)
    student_email = models.EmailField()
    student_number = models.CharField(max_length=50)
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    status = models.ForeignKey(ApplicationStatus, on_delete=models.PROTECT, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_name} → {self.listing.title}"