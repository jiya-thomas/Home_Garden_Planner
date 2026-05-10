from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Seed, Fertilizer, FarmingTip
from .forms import SeedForm, FertilizerForm, FarmingTipForm

def is_agri_officer(user):
    return hasattr(user, 'profile') and user.profile.role == 'agri_officer'

def hub(request):
    seeds = Seed.objects.all()
    fertilizers = Fertilizer.objects.all()
    tips = FarmingTip.objects.all().order_by('-created_at')
    
    context = {
        'seeds': seeds,
        'fertilizers': fertilizers,
        'tips': tips,
    }
    return render(request, 'agri_department/hub.html', context)

@login_required
@user_passes_test(is_agri_officer, login_url='/')
def manage_hub(request):
    seeds = Seed.objects.all()
    fertilizers = Fertilizer.objects.all()
    tips = FarmingTip.objects.filter(author=request.user).order_by('-created_at')
    
    context = {
        'seeds': seeds,
        'fertilizers': fertilizers,
        'tips': tips,
    }
    return render(request, 'agri_department/manage_hub.html', context)

@login_required
@user_passes_test(is_agri_officer, login_url='/')
def add_seed(request):
    if request.method == 'POST':
        form = SeedForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Seed added successfully!")
            return redirect('manage_agri_hub')
    else:
        form = SeedForm()
    return render(request, 'agri_department/form.html', {'form': form, 'title': 'Add Seed'})

@login_required
@user_passes_test(is_agri_officer, login_url='/')
def add_fertilizer(request):
    if request.method == 'POST':
        form = FertilizerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fertilizer added successfully!")
            return redirect('manage_agri_hub')
    else:
        form = FertilizerForm()
    return render(request, 'agri_department/form.html', {'form': form, 'title': 'Add Fertilizer'})

@login_required
@user_passes_test(is_agri_officer, login_url='/')
def add_tip(request):
    if request.method == 'POST':
        form = FarmingTipForm(request.POST)
        if form.is_valid():
            tip = form.save(commit=False)
            tip.author = request.user
            tip.save()
            messages.success(request, "Farming Tip added successfully!")
            return redirect('manage_agri_hub')
    else:
        form = FarmingTipForm()
    return render(request, 'agri_department/form.html', {'form': form, 'title': 'Add Farming Tip'})
