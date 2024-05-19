from django import forms
from .models import *


class StayPeriodForm(forms.ModelForm):
    class Meta:
        model = StayPeriod
        fields = "__all__"


class BabyForm(forms.ModelForm):
    class Meta:
        model = Baby
        fields = "__all__"


class CheckInForm(forms.Form):
    checked_in_by = forms.CharField(max_length=100, label="Who brought the baby?")


class CheckOutForm(forms.ModelForm):
    class Meta:
        model = CheckOut
        fields = ["checked_out_by"]


class SitterForm(forms.ModelForm):
    class Meta:
        model = Sitter
        fields = [
            "s_no",
            "s_name",
            "s_dob",
            "s_location",
            "s_gender",
            "s_nok",
            "s_NIN",
            "s_recomender",
            "s_religion",
            "s_educ_level",
            "s_email",
            "s_tel",
        ]

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     # Set the initial value of the checkbox based on s_available
        #     if self.instance.pk and self.instance.s_available:
        #         self.initial['s_available_checkbox'] = True

        # def clean(self):
        #     cleaned_data = super().clean()
        #     s_available_checkbox = cleaned_data.get('s_available_checkbox')
        #     # If the checkbox is checked, set s_available to True, else False
        #     cleaned_data['s_available'] = s_available_checkbox
        #     return cleaned_data

        # def save(self, commit=True):
        #     instance = super().save(commit=False)
        #     instance.s_available = self.cleaned_data['s_available']
        #     if commit:
        #         instance.save()
        #     return instance

        widgets = {
            "s_no": forms.TextInput(attrs={"class": "form-control s_no"}),
            "s_name": forms.TextInput(attrs={"class": "form-control s_name"}),
            "s_dob": forms.DateInput(
                attrs={"class": "form-control s_dob", "type": "date"}
            ),
            "s_location": forms.TextInput(attrs={"class": "form-control s_location"}),
            "s_gender": forms.Select(attrs={"class": "form-control s_gender"}),
            "s_nok": forms.TextInput(attrs={"class": "form-control s_nok"}),
            "s_NIN": forms.TextInput(attrs={"class": "form-control s_NIN"}),
            "s_recomender": forms.TextInput(
                attrs={"class": "form-control s_recomender"}
            ),
            "s_religion": forms.TextInput(attrs={"class": "form-control  s_religion"}),
            "s_educ_level": forms.TextInput(
                attrs={"class": "form-control s_educ_level"}
            ),
            "s_email": forms.EmailInput(attrs={"class": "form-control s_email"}),
            "s_tel": forms.NumberInput(attrs={"class": "form-control s_tel"}),
        }

        fieldsets = (
            (
                "Names",
                {
                    "fields": ("s_no", "s_name"),
                },
            ),
            (
                "More Details",
                {
                    "fields": (
                        "s_dob",
                        "s_location",
                        "s_gender",
                        "s_nok",
                        "s_NIN",
                        "s_recomender",
                        "s_religion",
                        "s_educ_level",
                        "s_email",
                        "s_tel",
                    ),
                },
            ),
        )


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = "__all__"


class FeesForm(forms.ModelForm):
    class Meta:
        model = Fees
        fields = "__all__"


class AttendanceForm(forms.ModelForm):
    payment = forms.DecimalField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Attendance
        fields = ["a_sitter", "status", "a_baby", "a_payment_date"]
        widgets = {
            "a_baby": forms.CheckboxSelectMultiple(attrs={"class": "checkbox"}),
            "a_payment_date": forms.DateInput(
                attrs={"class": "form-control ", "type": "date"}
            ),
        }


class InventorySupplyForm(forms.ModelForm):
    class Meta:
        model = InventoryCategory
        fields = "__all__"


class Inventory_ItemsForm(forms.ModelForm):
    class Meta:
        model = Inventory_Items
        fields = "__all__"


class Issue_InventoryForm(forms.ModelForm):
    class Meta:
        model = Issue_Inventory
        fields = "__all__"


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = [ "inventory_item", "quantity_sold", "sold_to", "total_price"]

        def clean(self):
            cleaned_data = super().clean()
            inventory_item = cleaned_data.get("inventory_item")
            if inventory_item and inventory_item.category.name != "DOLLS":
                raise forms.ValidationError(
                    "Sales can only be made for items in the doll category."
                )
            return cleaned_data
