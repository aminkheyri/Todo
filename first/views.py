from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Todo, Comment
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView, FormMixin
from django.views.generic.dates import MonthArchiveView
from .forms import TodoCreateForm, TodoCommentForm
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# class Home(TemplateView):
#     template_name = 'first/home.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['todos']= Todo.objects.all()
#         return context


class Home(ListView):
    template_name = 'first/home.html'
    model = Todo
    ordering = ['created']


class DetailTodo(LoginRequiredMixin, FormMixin, DetailView):
    model = Todo
    form_class = TodoCommentForm
    slug_field = 'slug'
    slug_url_kwarg = 'myslug'

    def get_success_url(self):
        return reverse('first:detail_todo', kwargs={'myslug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = Comment(todo=self.object, name=form.cleaned_data['name'], body=form.cleaned_data['body'])
            comment.save()
            return super().form_valid(form)


# class TodoCreate(FormView):
#     form_class = TodoCreateForm
#     template_name = 'first/todo_create.html'
#     success_url = reverse_lazy('first:home')
#
#     def form_valid(self, form):
#         self.create_todo(form.cleaned_data)
#         return super().form_valid(form)
#
#     def create_todo(self, data):
#         todo = Todo(title=data['title'], slug=slugify(data['title']))
#         todo.save()
#         messages.success(self.request, 'Todo created successfully', 'success')


class TodoCreate(CreateView):
    model = Todo
    fields = ("title",)
    template_name = 'first/todo_create.html'
    success_url = reverse_lazy('first:home')

    def form_valid(self, form):
        todo = form.save(commit=False)
        todo.slug = slugify(form.cleaned_data['title'])
        todo.save()
        messages.success(self.request, 'Todo created successfully', 'success')
        return super().form_valid(form)


class DeleteTodo(DeleteView):
    model = Todo
    template_name = 'first/todo_delete.html'
    success_url = reverse_lazy('first:home')


class UpdateTodo(UpdateView):
    model = Todo
    fields = ('title',)
    success_url = reverse_lazy('first:home')
    template_name = 'first/update_todo.html'


class MonthTodo(MonthArchiveView):
    model = Todo
    date_field = 'created'
    month_format = '%m'
    template_name = 'first/todo_month.html'