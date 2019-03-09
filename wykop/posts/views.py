from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from wykop.posts.models import Post


class HomeView(TemplateView):
    template_name = 'home.html'


class PostListView(ListView):
    model = Post
    template_name = 'posts_list.html'
    context_object_name = 'posts'
    ordering = '-votes'

    def get_queryset(self):
        qs = super().get_queryset()
        # qs = Post.objects.all().order_by('-votes')
        qs = qs.filter(votes__gte=0)
        return qs


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_details.html'
    context_object_name = 'post'
