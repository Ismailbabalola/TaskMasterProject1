from typing import Any
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.db.models import Case, When, Value, IntegerField





from .forms import *
from .models import Task

# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'registration/dashboard.html', {'section': 'dashboard'})

# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             #Create a new user object but avoid saving it yet
#             new_user = user_form.save(commit=False)
#             #set the chosen password
#             new_user.set_password(
#                 user_form.cleaned_data['password'])
#             #Save the user object
#             new_user.save()
#             return render(request, 'registration/register_done.html', {'new_user': new_user})
#     else:
#         user_form = UserRegistrationForm()
#     return render(request, 'registration/register.html', {'user_form': user_form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # You can redirect to a success page
            return redirect('some_view')
    else:
        user_form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'user_form': user_form})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('login')  # Redirect to the dashboard.
        else:
            # Return an 'invalid login' error message.
            context = {'error': 'Invalid username or password'}
            return render(request, 'registration/login.html', context)  # Update with your login template path.
    else:
        return render(request, 'registration/login.html')  # Update with your login template path.



class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'taskMaster/task_list.html'
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['tasks'] = context['tasks'].filter(user=self.request.user)
    #     context['count'] = context['tasks'].filter(complete=False).count()
        
    #     search_input = self.request.GET.get('search-area') or ''
    #     if search_input:
    #         context['tasks'] = context['tasks'].filter(
    #             title__startswith=search_input)
            
    #     context['search_input'] = search_input
    #     return context
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(user=self.request.user)

        # Annotate tasks with a numerical representation of priority
        tasks = tasks.annotate(
            order_priority=Case(
                When(priority='H', then=Value(1)),
                When(priority='M', then=Value(2)),
                When(priority='L', then=Value(3)),
                default=Value(4),
                output_field=IntegerField()
            )
        )

        # Sort tasks by completion status and annotated priority
        tasks = tasks.order_by('complete', 'order_priority')

        context['tasks'] = tasks
        context['count'] = tasks.filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = tasks.filter(title__startswith=search_input)

        context['search_input'] = search_input
        return context

    
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'taskMaster/task_detail.html'
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'taskMaster/task_form.html' 
    fields = ['title', 'description', 'priority', 'complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task    
    template_name = 'taskMaster/task_form.html'
    fields = ['title', 'description', 'priority', 'complete']
    success_url = reverse_lazy('tasks')
    
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'taskMaster/task_confirm_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
class LoggedOutView(TemplateView):
    template_name = '/Users/ish/Desktop/TaskMasterProject1/TaskMasterSite/authapp/templates/registration/logged_out.html'
    




