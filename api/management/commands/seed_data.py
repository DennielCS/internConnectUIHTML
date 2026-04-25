from django.core.management.base import BaseCommand
from api.models import (
    Category, WorkSetup, Company,
    InternshipListing, ApplicationStatus
)
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Insert demo data'

    def handle(self, *args, **kwargs):
        # Categories
        cats = ['IT', 'Engineering', 'Business', 'Design', 'Healthcare']
        cat_objs = {n: Category.objects.get_or_create(name=n)[0] for n in cats}
        self.stdout.write(self.style.SUCCESS('Categories inserted'))

        # Work Setups
        for s in ['Onsite', 'Remote', 'Hybrid']:
            WorkSetup.objects.get_or_create(label=s)

        onsite = WorkSetup.objects.get(label='Onsite')
        hybrid = WorkSetup.objects.get(label='Hybrid')
        remote = WorkSetup.objects.get(label='Remote')
        self.stdout.write(self.style.SUCCESS('Work Setups inserted'))

        # Application Statuses
        for st in ['Pending', 'Under Review', 'Accepted', 'Rejected']:
            ApplicationStatus.objects.get_or_create(label=st)

        self.stdout.write(self.style.SUCCESS('Application Statuses inserted'))

        # Companies
        companies_data = [
            {'name': 'TechCorp PH', 'location': 'Makati City', 'is_verified': True},
            {'name': 'BizSolutions', 'location': 'BGC, Taguig', 'is_verified': True},
            {'name': 'DesignHub', 'location': 'Ortigas', 'is_verified': True},
            {'name': 'MedTech Inc', 'location': 'Quezon City', 'is_verified': False},
        ]

        company_objs = {}
        for c in companies_data:
            obj, _ = Company.objects.get_or_create(name=c['name'], defaults=c)
            company_objs[c['name']] = obj

        self.stdout.write(self.style.SUCCESS('Companies inserted'))

        # Internship Listings
        deadline = date.today() + timedelta(days=60)
        listings = [
            {
                'title': 'Junior Web Developer Intern',
                'company': 'TechCorp PH', 'category': 'IT',
                'work_setup': hybrid, 'duration': '6 months',
                'slots': 3, 'deadline': deadline
            },
            {
                'title': 'Business Analyst Intern',
                'company': 'BizSolutions', 'category': 'Business',
                'work_setup': onsite, 'duration': '3 months',
                'slots': 2, 'deadline': deadline
            },
            {
                'title': 'UI/UX Design Intern',
                'company': 'DesignHub', 'category': 'Design',
                'work_setup': remote, 'duration': '6 months',
                'slots': 1, 'deadline': deadline
            },
        ]

        for l in listings:
            InternshipListing.objects.get_or_create(
                title=l['title'],
                defaults={
                    'company': company_objs[l['company']],
                    'category': cat_objs[l['category']],
                    'work_setup': l['work_setup'],
                    'description': 'Sample internship description.',
                    'requirements': 'Sample requirements.',
                    'duration': l['duration'],
                    'slots': l['slots'],
                    'deadline': l['deadline'],
                }
            )

        self.stdout.write(self.style.SUCCESS('Listings inserted'))
        self.stdout.write(self.style.SUCCESS('Seed complete'))