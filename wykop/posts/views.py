from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, TemplateView

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post_qs = Post.objects.filter(
            votes__gte=0
        ).order_by(
            '-votes'
        ).values_list('pk', flat=True)
        posts_ids = list(post_qs)

        cur_post_pk = self.get_object().pk

        cur_post_index = posts_ids.index(cur_post_pk)
        next_post_index = cur_post_index + 1
        prev_post_index = cur_post_index - 1
        next_post = None
        prev_post = None

        if next_post_index < len(posts_ids):
            next_post = posts_ids[next_post_index]

        if prev_post_index >= 0:
            prev_post = posts_ids[prev_post_index]

        context["next_post_id"] = next_post
        context["prev_post_id"] = prev_post
        return context


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'post_create.html'
