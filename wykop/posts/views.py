from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView, View)

from wykop.posts.models import Post, Vote


class HomeView(TemplateView):
    template_name = 'home.html'


class PostListView(ListView):
    model = Post
    template_name = 'posts_list.html'
    context_object_name = 'posts'
    ordering = '-created'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.get_object()
        all_posts = Post.objects.order_by('-created')

        next_post = all_posts.filter(created__lt=post.created).first()
        prev_post = all_posts.filter(created__gt=post.created).last()

        context["next_post"] = next_post
        context["prev_post"] = prev_post
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'post_create.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author=self.request.user)

        now = timezone.now()  # from django.utils import timezone (!)
        half_hour_ago = now - timedelta(minutes=30)

        qs = qs.filter(created__gt=half_hour_ago)

        return qs


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:list')
    context_object_name = 'post'
    template_name = 'post_delete.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author=self.request.user)
        return qs


class VoteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['post_pk'])
        value = request.POST.get('value')

        if post.author == request.user:
            raise Http404

        Vote.objects.create(
            post=post,
            user=request.user,
            value=value
        )

        return HttpResponseRedirect(request.META['HTTP_REFERER'])
