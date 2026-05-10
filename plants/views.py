from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Plant
from .forms import PlantForm


def plant_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    plants = Plant.objects.all()
    if query:
        plants = plants.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category:
        plants = plants.filter(category=category)
    categories = Plant.objects.values_list('category', flat=True).distinct()
    return render(request, 'plants/plant_list.html', {
        'plants': plants,
        'query': query,
        'selected_category': category,
        'categories': categories,
    })


def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    return render(request, 'plants/plant_detail.html', {'plant': plant})


@login_required
def plant_create(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            messages.success(request, f'🌱 {plant.name} added to the plant library!')
            return redirect('plant_detail', pk=plant.pk)
    else:
        form = PlantForm()
    return render(request, 'plants/plant_form.html', {'form': form, 'title': 'Add Plant'})


@login_required
def plant_update(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ {plant.name} updated!')
            return redirect('plant_detail', pk=plant.pk)
    else:
        form = PlantForm(instance=plant)
    return render(request, 'plants/plant_form.html', {'form': form, 'title': f'Edit {plant.name}', 'plant': plant})


@login_required
def plant_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == 'POST':
        name = plant.name
        plant.delete()
        messages.success(request, f'🗑️ {name} removed from library.')
        return redirect('plant_list')
    return render(request, 'plants/plant_confirm_delete.html', {'plant': plant})
