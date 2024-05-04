from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from pytils.translit import slugify

import blog
from blog.models import Post


# Create your views here.


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'content', 'preview', 'is_published')
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.add_post'

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()

        return super().form_valid(form)


class PostListView(LoginRequiredMixin, ListView):
    model = Post

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ('title', 'content', 'preview')
    permission_required = 'blog.change_post'

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()

        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        if self.object.views_count == 10:
            send_mail('Ура!!!', 'У тебя 100 просмотров', '79117241625@yandex.ru', ['79117241625@yandex.ru'], fail_silently=False)
        self.object.save()
        return self.object


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.delete_post'
