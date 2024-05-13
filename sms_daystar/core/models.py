from django.db import models
from django.utils import timezone
from datetime import date

# Create your models here.


class StayPeriod(models.Model):
    PERIOD = (
        ("halfday", "HALFDAY"),
        ("fullday", "FULLDAY"),
        ("monthly-halfday", "MONTHLY-HALFDAY"),
        ("monthly-fullday", "MONTHLY-FULLDAY"),
    )
    sp_name = models.CharField(max_length=20, choices=PERIOD)

    def __str__(self):
        return self.sp_name


# BABY MODEL
class Baby(models.Model):
    CHOICES = (
        ("MALE", "male"),
        ("FEMALE", "female"),
    )
    b_no = models.CharField(max_length=45)
    b_name = models.CharField(max_length=100)
    b_dob = models.DateField()
    b_gender = models.CharField(max_length=10, choices=CHOICES, null=True)
    b_location = models.CharField(max_length=15)
    b_parent = models.CharField(max_length=80)
    # b_sitter = models.ForeignKey(Sitter, on_delete=models.CASCADE)
    b_stayperiod = models.ForeignKey(StayPeriod, on_delete=models.CASCADE)
    b_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_subscribed_monthly = models.BooleanField(default=False)

    # def check_in(self):
    #     self.last_checkin_time = timezone.now()
    #     self.save()

    # def check_out(self):
    #     self.last_checkout_time = timezone.now()
    #     self.save()
        
    def __str__(self):
        return self.b_name

class CheckIn(models.Model):
    baby = models.ForeignKey(Baby,related_name='checkins', on_delete=models.CASCADE)
    checkin_time = models.DateTimeField(default=timezone.now)
    checked_in_by = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.baby.b_name} checked in by {self.checked_in_by} at {self.checkin_time}"

class CheckOut(models.Model):
    checkin = models.OneToOneField(CheckIn, related_name='checkouts', on_delete=models.CASCADE)
    checkout_time = models.DateTimeField(default=timezone.now)
    checked_out_by = models.CharField(max_length=100)
    def __str__(self):
            return f" {self.checkin.baby.b_name} checked out by {self.checked_out_by} at {self.checkout_time}"


# SITTER model
class Sitter(models.Model):
    CHOICES = (
        ("MALE", "male"),
        ("FEMALE", "female"),
    )
    s_no = models.CharField(max_length=45)
    s_name = models.CharField(max_length=100)
    s_dob = models.DateField()
    s_location = models.CharField(max_length=50)
    s_gender = models.CharField(max_length=10, null=True, blank=True, choices=CHOICES)
    s_nok = models.CharField(max_length=50)  # next of kin
    s_NIN = models.CharField(max_length=20)
    s_recomender = models.CharField(max_length=150)
    s_religion = models.CharField(max_length=50, null=True, blank=True)
    s_educ_level = models.CharField(max_length=100)
    s_email = models.EmailField(max_length=150)
    s_tel = models.IntegerField()
    def __str__(self):
        return self.s_name


class Attendance(models.Model):
    a_sitter = models.ForeignKey(Sitter, on_delete=models.CASCADE)
    a_baby = models.ManyToManyField(Baby)
    a_payment_date = models.DateTimeField()
    
    class Meta:
        unique_together = ['a_payment_date', 'a_sitter']

    def __str__(self):
        return f"{self.a_sitter.s_name} assigned to {', '.join(str(b) for b in self.a_baby.all())} on {self.a_payment_date}"

# class Day(models.Model):
#     name = models.DateField() # E.g., Monday, Tuesday, etc.

#     def __str__(self):
#         return self.name
    
class Schedule(models.Model):
    sitter = models.ForeignKey(Sitter, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    is_working = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sitter.s_name} : {self.is_working}"




# BABY SCHOOL FEE model



class Fees(models.Model):
    CHOICES = (
        ("HALFDAY","10,000" ),
        ("FULLDAY","15,000" ),
        ("MONTHLY-HALFDAY","300,000" ),
        ("MONTHLY-FULLDAY","450,000" ),
    )
    f_no = models.CharField(max_length=10, blank=True, null=True)
    f_baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    f_stayperiod = models.ForeignKey(StayPeriod, on_delete=models.CASCADE)
    amount = models.CharField(max_length=15, blank=True, null=True,choices=CHOICES)
    payment_date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.f_baby.b_name} "

class Baby_Attendance(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField(null=True, blank=True)
    brought_by = models.CharField(max_length=100)  # Who brought the baby
    picked_by = models.CharField(max_length=100, blank=True, null=True)  # Who picked up the baby

    def __str__(self):
        return f"{self.baby.name} - {self.arrival_time}"

# SITTER PAYMENT model




# inventory


class InventoryCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Inventory_Items(models.Model):
    category = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE, blank=True,null=True)
    name = models.CharField(max_length=80,blank=True, null=True)
    quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    received_date = models.DateField()

    def __str__(self):
        return f"{self.quantity} {self.name} at {self.unit_cost} each received on {self.received_date}"
    
class Issue_Inventory(models.Model):
    item = models.ForeignKey(Inventory_Items, on_delete=models.CASCADE)
    quantity_issued = models.PositiveIntegerField()
    issue_date = models.DateTimeField(auto_now_add=True)
    issued_To = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.quantity_issued} {self.item.name} issued to {self.issued_To} on {self.issue_date}"


# dolls 


# class ResaleItem(models.Model):
#     supply = models.OneToOneField(InventorySupplyReceipt, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity_available = models.PositiveIntegerField()

#     def __str__(self):
#         return f"{self.supply.name} - Price: {self.price} - Available: {self.quantity_available}"




