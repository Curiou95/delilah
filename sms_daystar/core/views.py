from datetime import date, datetime
from itertools import zip_longest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F, Min, Max
from django.urls import reverse
from django.db import transaction
from django.db.models import Sum
from django.contrib import messages
from .models import *
from .forms import *

# csvs, text files
from django.http import HttpResponse

# Pagination
from django.core.paginator import Paginator


# Create your views here.



# ======================================================
# LANDING PAGE VIEW
# ======================================================

def index(request):
    return render(request, "core/base.html")




# =================================================================
# AUTHENTICATION VIEWS
# =================================================================


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect("register")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect("register")
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email
                )
                user.save()
                return redirect("login")
        else:
            messages.info(request, "Password is not the same")
            return redirect("register")
    else:
        return render(request, "core/register.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Username or Password is Incorrect")
            return redirect("login")
    else:
        return render(request, "core/login.html")


@login_required
def logout(request):
    auth.logout(request)
    return redirect("login")

# =================================================================
# END AUTHENTICATION
# =================================================================






# =================================================================
# DASHBOARD VIEW
# =================================================================
@login_required
def home(request):
    return render(request, "core/dash.html")


# =================================================================
# BABY VIEWS
# =================================================================

@login_required
def babies(request):
    # babies_data = Baby.objects.annotate(

    babies_data = Baby.objects.all()
    checkin = CheckIn.objects.all()
    checkout = CheckOut.objects.all()

    data = zip_longest(babies_data, checkin, checkout)
    context = {
        "babies_data": babies_data,
        "checkin": checkin,
        "checkout": checkout,
        "data": data,
    }
    return render(request, "core/baby/viewbabies.html", context)


@login_required
def readbaby(request, id):
    baby = Baby.objects.get(id=id)
    return render(request, "core/baby/readbaby.html", {"baby": baby})


@login_required
def createbaby(request):
    if request.method == "POST":
        form = BabyForm(request.POST)
        if form.is_valid():
            baby = form.save()
            if not baby.is_subscribed_monthly:
                return redirect("readbaby", id=baby.id)
            else:
                messages.success(request, "New Baby added successfully")
                return redirect("viewbaby")  # Redirect to the 'babies' view
    else:
        form = BabyForm()

    context = {"form": form}
    return render(request, "core/baby/createbaby.html", context)


@login_required
def updatebaby(request, id):
    baby = Baby.objects.get(id=id)
    if request.method == "POST":
        form = BabyForm(request.POST, instance=baby)
        if form.is_valid:
            form.save()
            return redirect(reverse("viewbaby"))
    else:
        form = BabyForm(instance=baby)
    return render(request, "core/baby/createbaby.html", {"form": form, "baby": baby})


@login_required
def deletebaby(request, id):
    baby = Baby.objects.get(id=id)
    if request.method == "POST":
        baby.delete()
        return redirect(reverse("viewbaby"))
    return render(request, "core/baby/deletebaby.html", {"baby": baby})

def checkin(request, baby_id):
    baby = Baby.objects.get(id=baby_id)
    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            checked_in_by = form.cleaned_data['checked_in_by']
            CheckIn.objects.create(baby=baby, checkin_time=timezone.now(), checked_in_by=checked_in_by)
            # form.save()
            return redirect('viewbaby')  # Redirect to viewbaby page
    else:
        form = CheckInForm()
    return render(request, 'core/baby/checkin.html', {'form': form, 'baby': baby})


def checkout(request, checkin_id):
    checkin = CheckIn.objects.get(id=checkin_id)
    baby = checkin.baby
    if request.method == 'POST':
        
        form = CheckOutForm(request.POST)
        
        if form.is_valid():
            checked_out_by = form.cleaned_data['checked_out_by']
            CheckOut.objects.create(checkin=checkin, checkout_time=timezone.now(), checked_out_by=checked_out_by)
            # checkout = form.save(commit=False)
            # checkout.checkin = checkin
            # checkout.save()
            # baby = checkin.baby
            baby.is_checked_in = False
            baby.save()
            return redirect('viewbaby')
    else:
        form = CheckOutForm()
    return render(request, 'core/baby/checkout.html', {'form': form, 'checkin': checkin})


# ======================================================================
# END BABY
# ======================================================================









# ======================================================================
# SITTER VIEWS
# ======================================================================

@login_required
def sitter(request):
    # sitter = Sitter.objects.all()

    # setup pagination
    p = Paginator(Sitter.objects.all(), 5)
    page = request.GET.get("page")
    siter = p.get_page(page)
    nums = "a" * siter.paginator.num_pages

    context = {"sitter": sitter, "siter": siter, "nums": nums}
    return render(request, "core/sitter/viewsitter.html", context)


@login_required
def readsitter(request, id):
    sitter = Sitter.objects.get(id=id)
    baby = Baby.objects.filter(attendance__a_sitter_id=id)
    context = {"sitter": sitter, "baby": baby}
    return render(request, "core/sitter/readsitter.html", context)


@login_required
def createsitter(request):
    if request.method == "POST":
        form = SitterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New Sitter added successfully")
            return redirect("viewsitter")  # Redirect to the 'babies' view
    else:
        form = SitterForm()

    context = {"form": form}
    return render(request, "core/sitter/createsitter.html", context)


@login_required
def updatesitter(request, id):
    sitter = Sitter.objects.get(id=id)
    if request.method == "POST":
        form = SitterForm(request.POST, instance=sitter)
        if form.is_valid:
            form.save()
            return redirect(reverse("readsitter", kwargs={"id": id}))
    else:
        form = SitterForm(instance=sitter)
    return render(
        request, "core/sitter/editsitter.html", {"form": form, "sitter": sitter}
    )


@login_required
def deletesitter(request, id):
    sitter = Sitter.objects.get(id=id)
    if request.method == "POST":
        sitter.delete()
        return redirect(reverse("viewsitter"))
    return render(request, "core/sitter/deletesitter.html", {"sitter": sitter})


# TEXT FILE DOWNLOAD
def sitter_txt(request):
    response = HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=sitters.txt"
    # designate model
    sitter = Sitter.objects.all()

    lines = []
    # iterate over it
    for sitters in sitter:
        lines.append(
            f"{sitters.s_name}\n{sitters.s_location}\n{sitters.s_gender}\n{sitters.s_NIN}\n{sitters.s_religion}\n\n\n\n\n"
        )  # call any attributes you want to display here
    response.writelines(lines)
    return response

# ==========================================================
# SCEDULING THE SITTER
# ==========================================================

def schedule_list(request):
    schedules = Schedule.objects.all()
    return render(request, "core/sitter/schedule_list.html", {"schedules": schedules})


def schedule_create(request):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("schedule_list"))
    else:
        form = ScheduleForm()
    return render(request, "core/sitter/schedule_create.html", {"form": form})


def edit_schedule(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    if request.method == "POST":
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect("schedule_list")
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, "core/sitter/edit_schedule.html", {"form": form})


# ASSIGNING BABIES TO SITTER
# =================================================================

def assign_view(request):
    attendance_list = Attendance.objects.all()
    for attendance in attendance_list:
        attendance.total_payment = attendance.a_baby.all().count() * 3000
    return render(
        request, "core/sitter/assign_view.html", {"attendance_list": attendance_list}
    )


@login_required
def assignsitter(request):
    # current_date = timezone.now()
    # sitter = get_object_or_404(Sitter, pk=sitter_id)

    # # Check if the sitter is scheduled to work on the current date
    # schedule = Schedule.objects.filter(
    #     sitter=sitter, date=current_date, is_working=True
    # ).first()

    # if schedule:
    #     # Check if an Attendance object exists for this sitter and current date
    #     return redirect("assignsitter"  ) # error

    # attendance = Attendance.objects.filter(
    #     a_sitter=sitter, a_payment_date=current_date
    # ).first()
    # if not attendance:
    #     # Create an Attendance object if one does not exist
    #     attendance = Attendance.objects.create(
    #         a_sitter=sitter, a_payment_date=current_date
    #     )
    #     # Assuming a_baby_id is a foreign key to the Baby model, set the baby_id accordingly
    #     attendance.a_baby.set([1])


    baby = Baby.objects.all()

    if request.method == "POST":
        # If the form is submitted via POST, process the assignment
        form = AttendanceForm(request.POST)
        if form.is_valid():

            form.save()
            return redirect("assign_view")  # Redirect to a success URL after assignment
    else:
        # Render the form to assign teachers to the student
        form = AttendanceForm()
    return render(request, "core/sitter/assign.html", {"form": form, "baby": baby})

# ==============================================================================
# END SITTER
# ==============================================================================


# ============================================================
# INVENTORY VIEWS
# ===============================================================

@login_required
def inventoryCategory(request):
    inventory = InventoryCategory.objects.all()
    context = {"inventory": inventory}
    return render(request, "core/inventory/viewinventory.html", context)


@login_required
def inventoryreciept(request):
    inventory = Inventory_Items.objects.all()
    context = {"inventory": inventory}
    return render(request, "core/inventory/inventoryreciept.html", context)


@login_required
def addinventory(request):
    if request.method == "POST":
        form = Inventory_ItemsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New Item added successfully")
            return redirect("inventory")
    else:
        form = Inventory_ItemsForm()
    context = {"form": form}
    return render(request, "core/inventory/addinventory.html", context)


# new stuff for issuing
@login_required
def issue_inventory(request):
    if request.method == "POST":
        form = Issue_InventoryForm(request.POST)
        if form.is_valid():
            issue = form.save()
            return redirect("view_items")
    else:
        form = Issue_InventoryForm()
    return render(request, "core/inventory/issue.html", {"form": form})

@login_required
def view_issued_items(request):
    issued_items = Issue_Inventory.objects.all()
    return render(
        request, "core/inventory/all_issue_items.html", {"issued_items": issued_items}
    )
# ==============================================================================
# End Inentory
# ==============================================================================




# ==============================================================================
# DOLLS VIEWS
# ==============================================================================

@login_required
def dollview(request):
    dolls = Inventory_Items.objects.filter(category__name='DOLLS')
    return render(
        request, "core/dolls/dollview.html", {"dolls": dolls}
    )

# def readsitter(request, id):
#     sitter = Sitter.objects.get(id=id)
#     baby = Baby.objects.filter(attendance__a_sitter_id=id)
#     context = {"sitter": sitter, "baby": baby}
#     return render(request, "core/sitter/readsitter.html", context)


@login_required
def make_sale(request, id):
    doll = Inventory_Items.objects.get(id=id)
    if request.method == "POST":
        form = SaleForm(request.POST, instance=doll)
        if form.is_valid():
            # form.save()
            sale = form.save(commit=False)
            item = sale.inventory_item
            # check if item is belongs to dolls
            if item.category.name == 'DOLLS':
                sale.save()
                return redirect("dollview")
            else:
                form.add_error(None, 'We only sale dolls!!!!')
    else:
        
        form = SaleForm(instance=doll)
    return render(request, "core/inventory/make_sale.html", {"form": form})

# ==========================================================================
# END DOLLS
# ==========================================================================





# ==========================================================================
# FINANCES VIEWS
# ===========================================================================

@login_required
def financeview(request):
    fee = Fees.objects.all()
    return render(request, "core/finance/financeview.html", {'fee': fee})

@login_required
def make_payment(request):
    if request.method == "POST":
        form = FeesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")  # Redirect to home after payment
    else:
        form = FeesForm()
    return render(request, "core/finance/make_payment.html", {"form": form})



# ==============================================================================
# END PAYMENT
# ==============================================================================
