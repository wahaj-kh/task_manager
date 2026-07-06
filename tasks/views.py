from django.shortcuts import render, redirect
from .models import Task

def task_list(request):
    """Fetches all tasks from the database and displays them."""
    # Retrieve all tasks from the SQLite database
    tasks = Task.objects.all().order_by('-created_at')
    
    # Send the tasks to an HTML template (which we will build tomorrow!)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def create_task(request):
    """Handles creating a new task from a web form."""
    if request.method == 'POST':
        # Grab the data typed into the form fields
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        
        # Save it directly into our database model
        Task.objects.create(
            title=title,
            description=description,
            category=category

        )

        return redirect('task_list')
        
    return render(request, 'tasks/task_form.html')