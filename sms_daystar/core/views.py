from datetime import date, datetime
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
@login_required
def index(request):
    return render(request, 'core/base.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save();
                return redirect('login')
        else:
            messages.info(request,'Password is not the same')
            return redirect('register')
    else:
        return render(request, 'core/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or Password is Incorrect')
            return redirect('login')
    else:
        return render(request,'core/login.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
def home(request):
    return render(request, 'core/dash.html')


@login_required
def babies(request):
    # babies_data = Baby.objects.annotate(
    
    babies_data = Baby.objects.all()
    checkin = CheckIn.objects.all()
    checkout = CheckOut.objects.all()
    context = {'babies_data':babies_data, 'checkin':checkin , 'checkout':checkout}
    return render(request, 'core/baby/viewbabies.html', context)

@login_required
def record_attendance(request, baby_id):
    baby = Baby.objects.get(id=baby_id)
    if request.method == 'POST':
        form = Baby_AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.baby = baby
            attendance.save()
            return redirect('home')  # Redirect to home after recording attendance
    else:
        form = Baby_AttendanceForm()
    return render(request, 'core/baby/record_attendance.html', {'form': form})


@login_required
def readbaby(request, id):
    baby = Baby.objects.get(id=id)
    return render(request, 'core/baby/readbaby.html', {'baby': baby})

@login_required
def createbaby(request):
    if request.method == 'POST':
        form = BabyForm(request.POST)
        if form.is_valid():
            baby = form.save()
            if not baby.is_subscribed_monthly:
                return redirect('readbaby', id=baby.id)
            else:
                messages.success(request, 'New Baby added successfully')
                return redirect('viewbaby')  # Redirect to the 'babies' view
    else:
        form = BabyForm()
    
    context = {'form': form}
    return render(request, 'core/baby/createbaby.html', context)


@login_required
def updatebaby(request, id):
    baby = Baby.objects.get(id = id)
    if request.method == 'POST':
        form = BabyForm(request.POST, instance=baby)
        if form.is_valid:
            form.save()
            return redirect(reverse('viewbaby'))
    else:
        form = BabyForm(instance=baby)
    return render(request, 'core/baby/createbaby.html', {'form': form, 'baby': baby})


@login_required
def deletebaby(request, id):
    baby = Baby.objects.get(id=id)
    if request.method == 'POST':
        baby.delete()
        return redirect(reverse('viewbaby'))
    return render(request, 'core/baby/deletebaby.html', {'baby': baby})



# def checkin(request, baby_id):
#     baby = Baby.objects.get(id=baby_id)
#     baby.check_in()
#     return redirect('home')  # Redirect to home page or wherever appropriate

# def checkout(request, baby_id):
#     baby = Baby.objects.get(id=baby_id)
#     baby.check_out()
#     return redirect('home') 
def checkin(request, baby_id):
    baby = Baby.objects.get(id=baby_id)
    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            checked_in_by = form.cleaned_data['checked_in_by']
            CheckIn.objects.create(baby=baby, checkin_time=timezone.now(), checked_in_by=checked_in_by)
            # form.save()
            return redirect('viewbaby')  # Redirect to home page or wherever appropriate
    else:
        form = CheckInForm()
    return render(request, 'core/baby/checkin.html', {'form': form, 'baby': baby})


def checkout(request, checkin_id):
    checkin = CheckIn.objects.get(id=checkin_id)
    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.checkin = checkin
            checkout.save()
            baby = checkin.baby
            baby.is_checked_in = False
            baby.save()
            return redirect('viewbaby')
    else:
        form = CheckOutForm()
    return render(request, 'core/baby/checkout.html', {'form': form, 'checkin': checkin})

# def checkout(request, id):    
    # checkin_instance = CheckIn.objects.get( id=id)

    # if request.method == 'POST':
    #     form = CheckOutForm(request.POST)
    #     if form.is_valid(): 
    #         form.instance.checkin = checkin_instance
    #         # form.save()
    #         return redirect('viewbaby')  # Redirect to home page or wherever appropriate
    # else:
    #     form = CheckOutForm()
    # return render(request, 'core/baby/checkout.html', {'form': form})



# SITTER VIEWS
@login_required
def sitter(request):
    sitter = Sitter.objects.all()
    
    # setup pagination
    p = Paginator(Sitter.objects.all(), 5)
    page = request.GET.get('page')
    siter = p.get_page(page)
    nums = 'a' * siter.paginator.num_pages
    
    context = {'sitter':sitter, 'siter':siter, 'nums':nums}
    return render(request, 'core/sitter/viewsitter.html', context)

@login_required
def readsitter(request, id):
    sitter = Sitter.objects.get(id=id)
    baby  = Baby.objects.filter(attendance__a_sitter_id=id)
    context = {'sitter': sitter, 'baby':baby}
    return render(request, 'core/sitter/readsitter.html', context)

@login_required
def createsitter(request):
    if request.method == 'POST':
        form = SitterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Sitter added successfully')
            return redirect('viewsitter')  # Redirect to the 'babies' view
    else:
        form = SitterForm()
    
    context = {'form': form}
    return render(request, 'core/sitter/createsitter.html', context)

@login_required
def updatesitter(request, id):
    sitter = Sitter.objects.get(id = id)
    if request.method == 'POST':
        form = SitterForm(request.POST, instance=sitter)
        if form.is_valid:
            form.save()
            return redirect(reverse('readsitter', kwargs={'id': id}))
    else:
        form = SitterForm(instance=sitter)
    return render(request, 'core/sitter/editsitter.html', {'form': form, 'sitter': sitter})

@login_required
def deletesitter(request, id):
    sitter = Sitter.objects.get(id=id)
    if request.method == 'POST':
        sitter.delete()
        return redirect(reverse('viewsitter'))
    return render(request, 'core/sitter/deletesitter.html', {'sitter': sitter})

def sitter_txt(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=sitters.txt'
    # designate model
    sitter = Sitter.objects.all()
    
    lines = []
    # iterate over it
    for sitters in sitter:
        lines.append(f'{sitters.s_name}\n{sitters.s_location}\n{sitters.s_gender}\n{sitters.s_NIN}\n{sitters.s_religion}\n\n\n\n\n') #call any attributes you want to display here
    response.writelines(lines)
    return response

def schedule_list(request):
    schedules = Schedule.objects.all()
    return render(request, 'core/sitter/schedule_list.html', {'schedules': schedules})

def schedule_create(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('schedule_list'))
    else:
        form = ScheduleForm()
    return render(request, 'core/sitter/schedule_create.html', {'form': form})

def edit_schedule(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('schedule_list')
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, 'core/sitter/edit_schedule.html', {'form': form})

def assign_view(request):
    attendance_list = Attendance.objects.all()
    for attendance in attendance_list:
        attendance.total_payment = attendance.a_baby.all().count()*3000
    return render(request, 'core/sitter/assign_view.html',{'attendance_list':attendance_list})


@login_required
def assignsitter(request, sitter_id):
    current_date = timezone.now()
    
    
    sitter = get_object_or_404(Sitter, pk=sitter_id)
    
    # Check if the sitter is scheduled to work on the current date
    schedule = Schedule.objects.filter(sitter=sitter, date=current_date, is_working=True).first()
    
    if schedule:
        # Check if an Attendance object exists for this sitter and current date
        if not Attendance.objects.filter(a_sitter=sitter, a_payment_date=current_date).exists():
            # Create an Attendance object if one does not exist
            attendance = Attendance.objects.create(a_sitter=sitter, a_payment_date=current_date)
            # Assuming a_baby_id is a foreign key to the Baby model, set the baby_id accordingly
            attendance.a_baby.set([1])

    
    baby = Baby.objects.all()
    
    
    if request.method == 'POST':
        # If the form is submitted via POST, process the assignment
        form = AttendanceForm(request.POST)
        if form.is_valid():
            
            form.save() 
            return redirect('assign_view')  # Redirect to a success URL after assignment
    else:
        # Render the form to assign teachers to the student
        form = AttendanceForm()
    return render(request, 'core/sitter/assign.html', {'form': form, 'baby': baby })



# INVENTORY

@login_required
def inventoryCategory(request):
    inventory = InventoryCategory.objects.all()
    context = {'inventory':inventory}
    return render(request, 'core/inventory/viewinventory.html', context)

@login_required
def inventoryreciept(request):
    inventory = Inventory_Items.objects.all()
    context = {'inventory':inventory}
    return render(request, 'core/inventory/inventoryreciept.html', context)

@login_required
def addinventory(request):
    if request.method == 'POST':
        form = Inventory_ItemsForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request, 'New Item added successfully')
            return redirect('inventory')
    else:
        form = Inventory_ItemsForm()
    context = {'form':form}
    return render(request, 'core/inventory/addinventory.html', context)

# @login_required
# def issue(request, id):
#     issued_item = Inventory_Items.objects.get(id=id) 
#     issue_form = Issue_InventoryForm(request.POST)  

#     if request.method == 'POST':
#         if issue_form.is_valid():
#             new_issue = issue_form.save(commit=False)
#             new_issue.item = issued_item
#             new_issue.save()
#             issued_quantity = int(request.POST['quantity_available'])
#             issued_item.Quantity -= issued_quantity
#             issued_item.save()
#             print(issued_item.item_name)
#             print(request.POST['quantity_available'])
#             print(issued_item.Quantity)
#             return redirect('inventory')
#     return render(request, 'core/inventory/issue.html', {'issue_form': issue_form, 'issued_item': issued_item}) 

def issue_inventory(request, inventory_id):
    inventory_item = Inventory_Items.objects.get(pk=inventory_id)

    if request.method == 'POST':
        quantity_issued = int(request.POST.get('quantity_issued'))
        issued_to = request.POST.get('issued_to')

        if quantity_issued <= inventory_item.quantity:
            Issue_Inventory.objects.create(
                item=inventory_item,
                quantity_issued=quantity_issued,
                issued_To=issued_to
            )
            # Reduce the quantity of the inventory item
            inventory_item.quantity -= quantity_issued
            inventory_item.save()

            messages.success(request, f"{quantity_issued} {inventory_item.name} issued to {issued_to}.")
            return redirect('view_items')  # Redirect to inventory list view
        else:
            messages.error(request, f"Insufficient quantity available for {inventory_item.name}.")
            return redirect('issue_inventory', inventory_id=inventory_id)

    return render(request, 'core/inventory/issue.html', {'inventory_item': inventory_item})

def view_issued_items(request):
    issued_items = Issue_Inventory.objects.all()
    return render(request, 'core/inventory/all_issue_items.html', {'issued_items': issued_items})

# @login_required
# def all_issue_items(request):
#     issues = ResaleItem.objects.all()
#     total_issued_quantity = issues.aggregate(total_issued_quantity=Sum('quantity_available'))['total_issued_quantity'] or 0
#     total_received_quantity = InventorySupplyReceipt.objects.aggregate(total_received_quantity=Sum('quantity'))['total_received_quantity'] or 0
#     net_quantity = total_received_quantity - total_issued_quantity
#     return render(request, 'core/inventory/all_issue_items.html', {'issues': issues, 'total_issued_quantity': total_issued_quantity, 'total_received_quantity': total_received_quantity, 'net_quantity': net_quantity})

@login_required
def dollview(request):
    return render(request, 'core/dolls/dollview.html', {})


@login_required
def financeview(request):
    return render(request, 'core/finance/financeview.html', {})

def make_payment(request):
    if request.method == 'POST':
        form = FeesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after payment
    else:
        form = FeesForm()
    return render(request, 'core/finance/make_payment.html', {'form': form})


