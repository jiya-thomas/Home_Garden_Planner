from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import GardenBed, GardenPlot
from .forms import GardenBedForm, GardenPlotForm
from tasks.models import Task
from schedules.models import CareSchedule


@login_required
def dashboard(request):
    beds = GardenBed.objects.filter(user=request.user, is_active=True)
    upcoming_tasks = Task.objects.filter(user=request.user, is_completed=False).order_by('due_date')[:5]
    overdue_tasks = [t for t in upcoming_tasks if t.is_overdue]
    today = timezone.now().date()
    due_schedules = CareSchedule.objects.filter(
        plot__bed__user=request.user,
        is_active=True,
        next_due_date__lte=today
    ).select_related('plot__plant', 'plot__bed')[:8]
    recent_plots = GardenPlot.objects.filter(
        bed__user=request.user
    ).select_related('plant', 'bed').order_by('-created_at')[:6]
    stats = {
        'total_beds': beds.count(),
        'total_plants': GardenPlot.objects.filter(bed__user=request.user).count(),
        'pending_tasks': Task.objects.filter(user=request.user, is_completed=False).count(),
        'due_today': due_schedules.count(),
    }
    return render(request, 'gardens/dashboard.html', {
        'beds': beds,
        'upcoming_tasks': upcoming_tasks,
        'due_schedules': due_schedules,
        'recent_plots': recent_plots,
        'stats': stats,
        'overdue_count': len(overdue_tasks),
    })


@login_required
def bed_list(request):
    beds = GardenBed.objects.filter(user=request.user)
    return render(request, 'gardens/bed_list.html', {'beds': beds})


@login_required
def bed_detail(request, pk):
    bed = get_object_or_404(GardenBed, pk=pk, user=request.user)
    plots = bed.plots.select_related('plant').all()
    return render(request, 'gardens/bed_detail.html', {'bed': bed, 'plots': plots})


@login_required
def bed_create(request):
    if request.method == 'POST':
        form = GardenBedForm(request.POST)
        if form.is_valid():
            bed = form.save(commit=False)
            bed.user = request.user
            bed.save()
            messages.success(request, f'🌿 Garden bed "{bed.name}" created!')
            return redirect('bed_detail', pk=bed.pk)
    else:
        form = GardenBedForm()
    return render(request, 'gardens/bed_form.html', {'form': form, 'title': 'Create Garden Bed'})


@login_required
def bed_update(request, pk):
    bed = get_object_or_404(GardenBed, pk=pk, user=request.user)
    if request.method == 'POST':
        form = GardenBedForm(request.POST, instance=bed)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ "{bed.name}" updated!')
            return redirect('bed_detail', pk=bed.pk)
    else:
        form = GardenBedForm(instance=bed)
    return render(request, 'gardens/bed_form.html', {'form': form, 'title': f'Edit {bed.name}', 'bed': bed})


@login_required
def bed_delete(request, pk):
    bed = get_object_or_404(GardenBed, pk=pk, user=request.user)
    if request.method == 'POST':
        name = bed.name
        bed.delete()
        messages.success(request, f'🗑️ "{name}" deleted.')
        return redirect('bed_list')
    return render(request, 'gardens/bed_confirm_delete.html', {'bed': bed})


@login_required
def plot_create(request, bed_pk):
    bed = get_object_or_404(GardenBed, pk=bed_pk, user=request.user)
    if request.method == 'POST':
        form = GardenPlotForm(request.POST)
        if form.is_valid():
            plot = form.save(commit=False)
            plot.bed = bed
            plot.save()
            messages.success(request, f'🪴 {plot.plant.name} planted in {bed.name}!')
            return redirect('bed_detail', pk=bed.pk)
    else:
        form = GardenPlotForm()
    return render(request, 'gardens/plot_form.html', {'form': form, 'bed': bed})


@login_required
def plot_update(request, pk):
    plot = get_object_or_404(GardenPlot, pk=pk, bed__user=request.user)
    if request.method == 'POST':
        form = GardenPlotForm(request.POST, instance=plot)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ {plot.plant.name} updated!')
            return redirect('bed_detail', pk=plot.bed.pk)
    else:
        form = GardenPlotForm(instance=plot)
    return render(request, 'gardens/plot_form.html', {'form': form, 'bed': plot.bed, 'plot': plot})


@login_required
def plot_delete(request, pk):
    plot = get_object_or_404(GardenPlot, pk=pk, bed__user=request.user)
    if request.method == 'POST':
        bed_pk = plot.bed.pk
        plot.delete()
        messages.success(request, 'Plant removed from garden.')
        return redirect('bed_detail', pk=bed_pk)
    return render(request, 'gardens/plot_confirm_delete.html', {'plot': plot})
