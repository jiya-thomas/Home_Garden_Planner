from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm


@login_required
def task_list(request):
    filter_type = request.GET.get('filter', 'pending')
    tasks = Task.objects.filter(user=request.user)
    if filter_type == 'completed':
        tasks = tasks.filter(is_completed=True)
    elif filter_type == 'overdue':
        from django.utils import timezone
        tasks = tasks.filter(is_completed=False, due_date__lt=timezone.now().date())
    else:
        tasks = tasks.filter(is_completed=False)
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'filter_type': filter_type})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f'📝 Task "{task.title}" added!')
            return redirect('task_list')
    else:
        form = TaskForm(request.user)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Add Task'})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Task updated!')
            return redirect('task_list')
    else:
        form = TaskForm(request.user, instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Task'})


@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.toggle_complete()
    status = 'completed ✅' if task.is_completed else 'reopened'
    messages.success(request, f'Task "{task.title}" {status}!')
    return redirect('task_list')


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        name = task.title
        task.delete()
        messages.success(request, f'🗑️ "{name}" deleted.')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
