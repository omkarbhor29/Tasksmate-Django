from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist_app.models import Tasklist
from todolist_app.form import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def todolist(request):
    if request.method =="POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.manager = request.user
            instance.save()
        messages.success(request,('New Task Added'))
        return redirect('todolist')
    else:
        all_tasks = Tasklist.objects.filter(manager=request.user)
        paginator = Paginator(all_tasks, 6)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)

        return render(request, 'todolist.html', {'all_tasks': all_tasks})
 
@login_required   
def delete_task(request,task_id):
    task = Tasklist.objects.get(pk=task_id)
    if task.manager == request.user:
        task.delete()
    else:
        messages.error(request,("Access Restricted.You are Not Allowed!"))
        
    return redirect('todolist')

@login_required
def edit_task(request,task_id):
    if request.method =="POST":
        task = Tasklist.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance = task)
        if form.is_valid():
            form.save()
        
        messages.success(request,("Task Edited"))
        return redirect('todolist')
    else:
        task_obj = Tasklist.objects.get(pk=task_id)
        return render(request,'edit.html',{'task_obj':task_obj})

@login_required
def complete_task(request,task_id):
    task = Tasklist.objects.get(pk=task_id)
    if task.manager == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request,("Access Restricted.You are Not Allowed!"))
    return redirect('todolist')

@login_required
def pending_task(request,task_id):
    task = Tasklist.objects.get(pk=task_id)
    task.done = False
    task.save()
    
    return redirect('todolist')

def index(request):
    context = {
        'index_text':'Welcome To index Page',
    }
    return render(request,'index.html',context)

def contact(request):
    context = {
        'contact_text':'Welcome To Contact Page',
    }
    return render(request,'contact.html',context)

def about(request):
    context = {
        'about_text':'Welcome To About Page',
    }
    return render(request,'about.html',context)