from django.db import models

# Create your models here.


class StayPeriod(models.Model):
    PERIOD = (
        ("halfday", "HALFDAY"),
        ("fullday", "FULLDAY"),
        ("monthly-halfday", "MONTHLY-HALFDAY"),
        ("monthly-fullday", "MONTHLY-FULLDAY"),
    )
    sp_name = models.CharField(max_length=20, choices=PERIOD)
    sp_fee = models.DecimalField(max_digits=10, decimal_places=2)

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

    def __str__(self):
        return self.b_name


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
    # s_babies = models.ManyToManyField(Baby)
    
    
    def calculate_payment(self):
        attended_babies = self.attendance_set.all()  # Accessing related Attendance objects
        total_payment = 0
        for attendance in attended_babies:
            for baby in attendance.a_baby.all():
                stay_period_fee = baby.b_stayperiod.sp_fee
                print(stay_period_fee)
                total_payment += stay_period_fee
        return total_payment

    # def calculate_payment(self):
    #     # Calculate payment for the sitter based on attended babies
    #     attended_babies = Attendance.objects.filter(a_sitter=self)
    #     total_payment = 0
    #     for baby in attended_babies:
    #         stay_period_fee = baby.a_baby.b_stay_period.fees
    #         total_payment += stay_period_fee
    #     return total_payment

    def __str__(self):
        return self.s_name

    # def assign_baby(self, baby):
    #     # Check if the sitter can be assigned this baby based on availability criteria
    #     # Implement your logic here to check availability, such as checking if the baby's stay period matches the sitter's availability
    #     if baby.b_stayperiod == self.available_stay_period:
    #         self.s_babies.add(baby)

    # @property
    # def available_stay_period(self):
    #     # Implement logic to determine the sitter's available stay period
    #     # For example, you might check the sitter's schedule to see which stay period they are available for
    #     # Return the StayPeriod object representing the available period
    #     # This is just a placeholder; you need to replace it with your actual logic
    #     return StayPeriod.objects.first()


# BABY SCHOOL FEE model
class PaymentCurrency(models.Model):
    CURRENCY_CHOICES = (
        ("ugx", "UGX"),
        ("usd", "USD"),
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)

    def __str__(self):
        return self.currency


class Fees(models.Model):
    f_no = models.CharField(max_length=10, blank=True, null=True)
    f_baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    f_stayperiod = models.ForeignKey(StayPeriod, on_delete=models.CASCADE)
    f_currency = models.ForeignKey(PaymentCurrency, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        return f"{self.f_baby.b_name} "


# SITTER PAYMENT model
class Attendance(models.Model):
    a_sitter = models.ForeignKey(Sitter, on_delete=models.CASCADE)
    a_baby = models.ManyToManyField(Baby)
    a_payment_date = models.DateField()
    
    class Meta:
        unique_together = ['a_payment_date', 'a_sitter']

    def __str__(self):
        return f"{self.a_sitter.s_name} assigned to {', '.join(str(b) for b in self.a_baby.all())} on {self.a_payment_date}"



# inventory


class InventoryCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class InventorySupplyReceipt(models.Model):
    name = models.CharField
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    received_date = models.DateField()

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.supply.name} received on {self.received_date}"


# dolls 


class ResaleItem(models.Model):
    supply = models.OneToOneField(InventoryCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.supply.name} - Price: {self.price} - Available: {self.quantity_available}"




