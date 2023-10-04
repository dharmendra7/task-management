from django.shortcuts import render, redirect   
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from tasksweb import forms
from tasks.models import Project, Task, User
from .task import send_email_fun

from django.contrib import messages

from .decorators import project_manager_required

from django.conf import settings


def user_login(request):
    formset = forms.LoginForm()
    if request.method == 'POST':
        formset = forms.LoginForm(request.POST or None)
       
        if formset.is_valid():
            email = formset.cleaned_data.get('email')
            password = formset.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            print('workingd')
            print(user)
            if user is not None:        
                login(request, user)
                print(request.user.id)
                user_obj = User.objects.get(id = request.user.id)
                if user_obj.is_project_manager:
                    return redirect('project-listing')
                else:
                    return redirect('task-listing')
        
    return render(request, 'login.html',context= {'formset': formset}) 

def user_logout(request):
    logout(request)
    messages.success(request, "Logout success!")
    return redirect("login")


@login_required(login_url='login')
@project_manager_required
def project_listing(request):
    project_record = Project.objects.all()
    context = {'project_record': project_record}
    return render(request, 'project-listing.html', context=context)


@login_required(login_url='login')
@project_manager_required
def create_project(request):
    form = forms.CreateProjectForm()

    if request.method == "POST":
        form = forms.CreateProjectForm(request.POST)
        
        if form.is_valid(): 
            obj = form.save(commit=False)
            obj.owner = User.objects.get(id=request.user.id)
            obj.save()
            messages.success(request, "Your project was created!")
            return redirect("project-listing")
        
    context = {'form': form}
    return render(request, 'project-create.html', context=context)


@login_required(login_url='login')
def view_project_details(request, pk):
    projects_records = Project.objects.get(id=pk)
    task_records = Task.objects.filter(project=pk)
    context = {'project_record':projects_records, 'task_records' : task_records}
    return render(request, 'project-details.html', context=context)


@login_required(login_url='login')
@project_manager_required
def edit_project_details(request, pk):
    record = Project.objects.get(id=pk)
    form = forms.CreateProjectForm(instance=record)
    
    if request.method == 'POST':
        form = forms.CreateProjectForm(request.POST, instance=record)

        if form.is_valid():
            form.save()
            messages.success(request, "Your project was updated!")
            return redirect("project-details", pk=record.id)
    
    context = {'form':form}
    return render(request, 'project-edit.html', context=context)


@login_required(login_url='login')
@project_manager_required
def delete_project(request, pk):
    record = Project.objects.get(id=pk)
    record.delete()
    messages.success(request, "Your project was deleted!")
    return redirect("project-listing")


@login_required(login_url='login')
def create_task(request, pk):
    form = forms.CreateTaskForm()
    print('working')
    if request.method == "POST":
        form = forms.CreateTaskForm(request.POST)
        
        if form.is_valid(): 
            obj = form.save(commit=False)
            obj.project = Project.objects.get(id = pk)
            obj.assign_to = User.objects.get(id = form.cleaned_data.get('assign_to').id)
            obj.save()
            messages.success(request, "Your task was created!")
            return redirect("project-details", pk=pk)
        
    context = {'form': form}
    return render(request, 'task-create.html', context=context)


@login_required(login_url='login')
@project_manager_required
def delete_task(request, pk):
    record = Task.objects.get(id=pk)
    record.delete()
    # messages.success(request, "Your project was deleted!")
    return JsonResponse({'text' : 'Your task was deleted!'})


@login_required(login_url='login')
def task_listing_for_assignee(request):
    available_task =  Task.objects.filter(assign_to=request.user.id)
    context = {'available_task': available_task}
    return render(request, 'task-listing.html', context=context)


from django.conf import settings
def change_task_status(request, pk):
    task_record = Task.objects.get(id=pk)
    if task_record.completed:
        task_record.completed = False
        staus = 'pending'   
    else:
        task_record.completed = True
        staus = 'completed'
        task = Task.objects.select_related('project__owner').get(id=pk)
        email = task.project.owner.email

        # Used Celery to sending the mail
        send_email_fun.delay("Task Completion Notification", "your_message", settings.EMAIL_HOST_USER, email)
    task_record.save()
    print(task_record.completed)
    return JsonResponse({'text' : f'Your task markes as {staus}!'})
    
