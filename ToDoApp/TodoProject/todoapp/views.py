from django.shortcuts import render,redirect
from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

# def TaskList(request):
#     tasks = Task.objects.all()
#     context = {'tasks':tasks}
#     return render(request,'todoapp/task_list.html',context)
    

class TaskList(LoginRequiredMixin,ListView):
    model = Task  
    context_object_name = 'tasks'
    template_name = 'todoapp/task_list.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            context['search_input'] = search_input 
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task 
    context_object_name = 'tasks'
    template_name = 'todoapp/task_detail.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task  
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasklist')
    context_object_name = 'tasks'
    template_name = 'todoapp/task_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user   
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task    
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasklist')
    context_object_name = 'tasks'
    template_name = 'todoapp/task_create.html'
    
class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task  
    context_object_name = 'tasks'
    success_url = reverse_lazy('tasklist')

class LoginView(LoginView):
    template_name = 'todoapp/login.html'
    fields = '__all__'
    redirect_authenticated_user = False 
    def get_success_url(self):
        return reverse_lazy('tasklist')    
    
class RegisterPage(FormView):
    template_name = 'todoapp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True  
    success_url = reverse_lazy('tasklist')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasklist')
        return super(RegisterPage, self).get(*args, *kwargs)