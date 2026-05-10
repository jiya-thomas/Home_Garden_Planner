from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CareSchedule
from .forms import CareScheduleForm


@login_required
def schedule_list(request):
    schedules = CareSchedule.objects.filter(
        plot__bed__user=request.user, is_active=True
    ).select_related('plot__plant', 'plot__bed').order_by('next_due_date')
    return render(request, 'schedules/schedule_list.html', {'schedules': schedules})


@login_required
def schedule_create(request):
    if request.method == 'POST':
        form = CareScheduleForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '📅 Care schedule created!')
            return redirect('schedule_list')
    else:
        form = CareScheduleForm(request.user)
    return render(request, 'schedules/schedule_form.html', {'form': form, 'title': 'Add Care Schedule'})


@login_required
def schedule_update(request, pk):
    schedule = get_object_or_404(CareSchedule, pk=pk, plot__bed__user=request.user)
    if request.method == 'POST':
        form = CareScheduleForm(request.user, request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Schedule updated!')
            return redirect('schedule_list')
    else:
        form = CareScheduleForm(request.user, instance=schedule)
    return render(request, 'schedules/schedule_form.html', {'form': form, 'title': 'Edit Schedule'})


@login_required
def schedule_done(request, pk):
    schedule = get_object_or_404(CareSchedule, pk=pk, plot__bed__user=request.user)
    schedule.mark_done()
    messages.success(request, f'✅ {schedule.get_care_type_display()} marked as done!')
    return redirect('schedule_list')


@login_required
def schedule_delete(request, pk):
    schedule = get_object_or_404(CareSchedule, pk=pk, plot__bed__user=request.user)
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, '🗑️ Schedule removed.')
        return redirect('schedule_list')
    return render(request, 'schedules/schedule_confirm_delete.html', {'schedule': schedule})
