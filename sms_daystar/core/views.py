from datetime import date
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
def readbaby(request, id):
    baby = Baby.objects.get(id=id)
    return render(request, 'core/baby/readbaby.html', {'baby': baby})

@login_required
def createbaby(request):
    if request.method == 'POST':
        form = BabyForm(request.POST)
        if form.is_valid():
            form.save()
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
    checkin_instance = CheckIn.objects.get(id=checkin_id)
    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            form.instance.checkin = checkin_instance
            form.save()
            return redirect('viewbaby')  # Redirect to home page or wherever appropriate
    else:
        form = CheckOutForm()
    return render(request, 'core/baby/checkout.html', {'form': form})



# SITTER VIEWS
@login_required
def sitter(request):
    sitter = Sitter.objects.all()
    attendance_list = Attendance.objects.all()
    for attendance in attendance_list:
        attendance.total_payment = attendance.a_baby.all().count()*3000
    context = {'sitter':sitter, 'attendance_list':attendance_list}
    return render(request, 'core/sitter/viewsitter.html', context)

@login_required
def readsitter(request, id):
    sitter = Sitter.objects.get(id=id)
    payment = sitter.calculate_payment()
    context = {'sitter': sitter, 'payment':payment}
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

@login_required
def assignsitter(request, sitter_id):
    # Retrieve the student object
    baby = Baby.objects.all()
    sitters = Sitter.objects.get(id=sitter_id)
    
    if request.method == 'POST':
        # If the form is submitted via POST, process the assignment
        form = AttendanceForm(request.POST)
        if form.is_valid():
            # selected_babies = form.cleaned_data.get('babies')
            
            # payment = len(selected_babies)*3000
            # instance = form.save(commit=False)
            # instance.payment = payment
            
            # Get the list of teachers selected in the form
            # sitters = form.cleaned_data['sitter']
            # Assign each selected teacher to the student
            # for sitter in sitters:
            #     baby.sitter.add(sitter)
            # Redirect to a success page or view
            form.save()
            return redirect('viewsitter')  # Redirect to a success URL after assignment
    else:
        # Render the form to assign teachers to the student
        form = AttendanceForm()
    
    babies_attended = Attendance.objects.filter(a_sitter=sitters).count()
    print(babies_attended)
    # Render the template with the form and student details
    return render(request, 'core/sitter/assign.html', {'form': form, 'baby': baby, 'sitters':sitters,'babies_attended':babies_attended  })


# INVENTORY

@login_required
def inventorysupply(request):
    inventory = InventoryCategory.objects.all()
    context = {'inventory':inventory}
    return render(request, 'core/inventory/viewinventory.html', context)

@login_required
def inventoryreciept(request):
    inventory = InventorySupplyReceipt.objects.all()
    context = {'inventory':inventory}
    return render(request, 'core/inventory/inventoryreciept.html', context)

@login_required
def addinventory(request):
    if request.method == 'POST':
        form = InventorySupplyReceiptForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Item added successfully')
            return redirect('inventory')
    else:
        form = InventorySupplyReceiptForm()
    context = {'form':form}
    return render(request, 'core/inventory/addinventory.html', context)

@login_required
def issue(request, id):
    issued_item = InventorySupplyReceipt.objects.get(id=id) 
    issue_form = ResaleItemForm(request.POST)  

    if request.method == 'POST':
        if issue_form.is_valid():
            new_issue = issue_form.save(commit=False)
            new_issue.item = issued_item
            new_issue.save()
            issued_quantity = int(request.POST['quantity_available'])
            issued_item.quantity -= issued_quantity
            issued_item.save()
            print(issued_item.item_name)
            print(request.POST['quantity_available'])
            print(issued_item.quantity)
            return redirect('inventory')
    return render(request, 'core/inventory/issue.html', {'issue_form': issue_form}) 

@login_required
def all_issue_items(request):
    issues = ResaleItem.objects.all()
    total_issued_quantity = issues.aggregate(total_issued_quantity=Sum('quantity_available'))['total_issued_quantity'] or 0
    total_received_quantity = InventorySupplyReceipt.objects.aggregate(total_received_quantity=Sum('quantity'))['total_received_quantity'] or 0
    net_quantity = total_received_quantity - total_issued_quantity
    return render(request, 'core/inventory/all_issue_items.html', {'issues': issues, 'total_issued_quantity': total_issued_quantity, 'total_received_quantity': total_received_quantity, 'net_quantity': net_quantity})

@login_required
def dollview(request):
    return render(request, 'core/dolls/dollview.html', {})


@login_required
def financeview(request):
    return render(request, 'core/finance/financeview.html', {})