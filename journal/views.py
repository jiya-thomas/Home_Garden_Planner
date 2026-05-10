from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JournalEntry
from .forms import JournalEntryForm
from gardens.models import GardenPlot


@login_required
def journal_list(request):
    entries = JournalEntry.objects.filter(
        plot__bed__user=request.user
    ).select_related('plot__plant', 'plot__bed').order_by('-date')
    return render(request, 'journal/journal_list.html', {'entries': entries})


@login_required
def journal_detail(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, plot__bed__user=request.user)
    return render(request, 'journal/journal_detail.html', {'entry': entry})


@login_required
def journal_create(request):
    plot_id = request.GET.get('plot')
    initial = {}
    if plot_id:
        try:
            plot = GardenPlot.objects.get(pk=plot_id, bed__user=request.user)
            initial['plot'] = plot
        except GardenPlot.DoesNotExist:
            pass
    if request.method == 'POST':
        form = JournalEntryForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            entry = form.save()
            messages.success(request, f'📔 Journal entry saved for {entry.plot.plant.name}!')
            return redirect('journal_list')
    else:
        form = JournalEntryForm(request.user, initial=initial)
    return render(request, 'journal/journal_form.html', {'form': form, 'title': 'New Journal Entry'})


@login_required
def journal_update(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, plot__bed__user=request.user)
    if request.method == 'POST':
        form = JournalEntryForm(request.user, request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Entry updated!')
            return redirect('journal_detail', pk=entry.pk)
    else:
        form = JournalEntryForm(request.user, instance=entry)
    return render(request, 'journal/journal_form.html', {'form': form, 'title': 'Edit Entry'})


@login_required
def journal_delete(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, plot__bed__user=request.user)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, '🗑️ Entry deleted.')
        return redirect('journal_list')
    return render(request, 'journal/journal_confirm_delete.html', {'entry': entry})
