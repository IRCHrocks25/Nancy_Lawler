"""Seed dashboard content, CTAs, testimonials."""
from django.core.management.base import BaseCommand
from dashboard.utils import seed_content_if_empty, seed_ctas_if_empty, seed_testimonials_if_empty


class Command(BaseCommand):
    help = "Seed dashboard content, CTAs, and testimonials from defaults"

    def handle(self, *args, **options):
        seed_content_if_empty()
        seed_ctas_if_empty()
        seed_testimonials_if_empty()
        self.stdout.write(self.style.SUCCESS("Dashboard seeding complete"))
