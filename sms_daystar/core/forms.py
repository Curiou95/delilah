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


# class CheckInForm(forms.ModelForm):
#     class Meta:
#         model = CheckIn
#         fields = ['baby', 'checked_in_by']
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

        def clean(self):
            cleaned_data = super().clean()
            s_no = cleaned_data.get("s_no")
            s_name = cleaned_data.get("s_name")
            s_dob = cleaned_data.get("s_dob")
            s_location = cleaned_data.get("s_location")
            s_gender = cleaned_data.get("s_gender")
            s_nok = cleaned_data.get("s_nok")
            s_NIN = cleaned_data.get("s_NIN")
            s_recomender = cleaned_data.get("s_recomender")
            s_religion = cleaned_data.get("s_religion")
            s_educ_level = cleaned_data.get("s_educ_level")
            s_email = cleaned_data.get("s_email")
            s_tel = cleaned_data.get("s_tel")

            if not s_name:
                self.add_error("s_name", "This field is required.")
            elif len(s_name) < 5:
                self.add_error("s_name", "Name should be atleast 6 letters")
            if s_location != "Kabalagala":
                self.add_error("s_location", "People outside Kabalagala are invalid")
            if not s_nok:
                self.add_error("s_nok", "This field is required.")
            elif len(s_nok) < 5:
                self.add_error("s_nok", "Name should be atleast 6 letters")
            if not s_recomender:
                self.add_error("s_recomender", "This field is required.")
            elif len(s_recomender) < 5:
                self.add_error("s_recomender", "Name should be atleast 6 letters")

        widgets = {
            "s_no": forms.TextInput(attrs={"class": "form-control s_no"}),
            "s_name": forms.TextInput(attrs={"class": "form-control s_name"}),
            "s_dob": forms.DateInput(attrs={"class": "form-control s_dob"}),
            "s_location": forms.TextInput(attrs={"class": "form-control s_location"}),
            "s_gender": forms.Select(attrs={"class": "form-control s_gender"}),
            "s_nok": forms.TextInput(attrs={"class": "form-control s_nok"}),
            "s_NIN": forms.TextInput(attrs={"class": "form-control s_NIN"}),
            "s_recomender": forms.TextInput(
                attrs={"class": "form-control s_recomender"}
            ),
            "s_religion": forms.TextInput(attrs={"class": "form-control s_religion"}),
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
        fields = '__all__'


class FeesForm(forms.ModelForm):
    class Meta:
        model = Fees
        fields = "__all__"


class Baby_AttendanceForm(forms.ModelForm):
    class Meta:
        model = Baby_Attendance
        fields = ["arrival_time", "departure_time", "brought_by", "picked_by"]


class AttendanceForm(forms.ModelForm):
    payment = forms.DecimalField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Attendance
        fields = ["a_sitter", "a_baby", "a_payment_date"]
        widgets = {
            "a_baby": forms.CheckboxSelectMultiple(attrs={"class": "checkbox"}),
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
