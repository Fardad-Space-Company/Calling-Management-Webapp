from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ShopInfoUnique4(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    post = models.TextField()
    shop_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    competitor = models.TextField(null=True, blank=True)
    saturday = models.CharField(max_length=255, null=True, blank=True)
    sunday = models.CharField(max_length=255, null=True, blank=True)
    monday = models.CharField(max_length=255, null=True, blank=True)
    tuesday = models.CharField(max_length=255, null=True, blank=True)
    wednesday = models.CharField(max_length=255, null=True, blank=True)
    thursday = models.CharField(max_length=255, null=True, blank=True)
    friday = models.CharField(max_length=255, null=True, blank=True)
    shop_status = models.CharField(max_length=10, null=True, blank=True)
    menu = models.CharField(max_length=100)
    note = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Shopinfo_unique_4'




class Postcode(models.Model):
    City = models.CharField(max_length=50, null=True, blank=True)
    Post_code = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'Postcode' 



class CRMbackend(models.Model):
    DEAL_STATUS_CHOICES = [
        ('hang_up', 'Hang Up'),
        ('not_interested', 'Not Interested'),
        ('gate_keeper', 'Gate Keeper'),
        ('decision_maker', 'Decision Maker'),
        ('call_appointment', 'Call Appointment'),
        ('visit_appointment', 'Visit Appointment'),
        ('follow_up', 'Follow Up'),
        ('visited', 'Visited'),
        ('voice_mail', 'Voice Mail'),
        ('no_answer', 'No Answer'),
    ]
    SHOP_STATUS_CHOICES = [
        ('junk_lead', 'Junk Lead'),
        ('qualified', 'Qualified'),
        ('prospecting', 'Prospecting'),
        ('onboarded', 'Onboarded'),
        ('no_answer', 'No Answer'),
    ]
    EmployeeID = models.CharField(max_length=11, null=False)
    DealStatus = models.CharField(max_length=20, choices=DEAL_STATUS_CHOICES, default='hang_up', null=False)
    ShopName = models.CharField(max_length=100, null=False)
    Date = models.TextField(null=False)
    CallDuration = models.TextField(null=True, blank=True)
    Email = models.CharField(max_length=50, null=True, blank=True)
    Appointement_Date = models.TextField(null=True, blank=True)  # renamed from Appointement_Date to match the SQL definition
    OWname = models.CharField(max_length=20, null=True, blank=True)
    OWnum = models.CharField(max_length=15, null=True, blank=True)
    GKname = models.CharField(max_length=20, null=True, blank=True)
    GKnum = models.CharField(max_length=15, null=True, blank=True)
    Note = models.TextField(null=True, blank=True)
    Shop_Status = models.CharField(max_length=20, choices=SHOP_STATUS_CHOICES, default='junk_lead', null=False)
    AutoId = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'CRMbackend'




class EmployeeID(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    # Add other fields as needed

    def __str__(self):
        return self.employee_id  # Display the employee_id as the representation



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_employee_id(sender, instance, created, **kwargs):
    if created:
        # Generate a unique employee_id, for example based on username
        employee_id = f'{instance.username}_empid'
        while EmployeeID.objects.filter(employee_id=employee_id).exists():
            # If employee_id already exists, modify it slightly
            employee_id = f'{instance.username}_empid_{EmployeeID.objects.count() + 1}'
        
        # Create the EmployeeID instance
        EmployeeID.objects.create(user=instance, employee_id=employee_id)
    else:
        # Update the existing EmployeeID instance
        instance.employeeid.save()