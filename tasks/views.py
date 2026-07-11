from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .ai_engine import analyze_task_priority  

def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def create_task(request):
    """Handles creating a new task and passes content through the AI analysis layer."""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        
        # The AI module parses the input fields to evaluate urgency
        calculated_priority = analyze_task_priority(title, description)
        
        Task.objects.create(
            title=title,
            description=description,
            category=category,
            priority=calculated_priority 
        )
        return redirect('task_list')
        
    return render(request, 'tasks/task_form.html')

# 🚀 Day 6 Additions: Workflow Lifecycle Controls

def complete_task(request, task_id):
    """Updates the task status choice to 'Completed'."""
    task = get_object_or_404(Task, id=task_id)
    task.status = 'Completed'
    task.save()
    return redirect('task_list')

def delete_task(request, task_id):
    """Permanently deletes the task record from the SQLite database."""
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')