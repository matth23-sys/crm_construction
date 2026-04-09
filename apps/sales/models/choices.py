from django.db import models


class OpportunityStatus(models.TextChoices):
    OPEN = "open", "Open"
    WON = "won", "Won"
    LOST = "lost", "Lost"


class OpportunitySource(models.TextChoices):
    REFERRAL = "referral", "Referral"
    WEBSITE = "website", "Website"
    WHATSAPP = "whatsapp", "WhatsApp"
    CALL = "call", "Call"
    EMAIL = "email", "Email"
    SOCIAL_MEDIA = "social_media", "Social media"
    WALK_IN = "walk_in", "Walk-in"
    OTHER = "other", "Other"