from datetime import date
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from .models import * 
from .forms import *

# Create your views here.

def index(request):
    return render(request, 'core/base.html')


def babies(request):
    baby = Baby.objects.all()
    context = {'baby':baby}
    return render(request, 'core/baby/viewbabies.html', context)

def readbaby(request, id):
    baby = Baby.objects.get(id=id)
    return render(request, 'core/baby/readbaby.html', {'baby': baby})

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



def deletebaby(request, id):
    baby = Baby.objects.get(id=id)
    if request.method == 'POST':
        baby.delete()
        return redirect(reverse('viewbaby'))
    return render(request, 'core/baby/deletebaby.html', {'baby': baby})


# SITTER VIEWS

def sitter(request):
    sitter = Sitter.objects.all()
    attendance_list = Attendance.objects.all()
    for attendance in attendance_list:
        attendance.total_payment = attendance.a_baby.all().count()*3000
    context = {'sitter':sitter, 'attendance_list':attendance_list}
    return render(request, 'core/sitter/viewsitter.html', context)

def readsitter(request, id):
    sitter = Sitter.objects.get(id=id)
    payment = sitter.calculate_payment()
    context = {'sitter': sitter, 'payment':payment}
    return render(request, 'core/sitter/readsitter.html', context)

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

def updatesitter(request, id):
    sitter = Sitter.objects.get(id = id)
    if request.method == 'POST':
        form = forms.SitterForm(request.POST, instance=sitter)
        if form.is_valid:
            form.save()
            return redirect(reverse('readsitter', kwargs={'id': id}))
    else:
        form = forms.SitterForm(instance=sitter)
    return render(request, 'core/sitter/editsitter.html', {'form': form, 'sitter': sitter})

def deletesitter(request, id):
    sitter = Sitter.objects.get(id=id)
    if request.method == 'POST':
        sitter.delete()
        return redirect(reverse('viewsitter'))
    return render(request, 'core/sitter/deletesitter.html', {'sitter': sitter})

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

def inventorysupply(request):
    inventory = InventorySupply.objects.all()
    context = {'inventory':inventory}
    return render(request, 'core/inventory/viewinventory.html', context)


def inventoryreciept(request):
    inventory = InventorySupply.objects.all()
    context = {'inventory':inventory}
    return render(request, 'core/inventory/inventoryreciept.html', context)