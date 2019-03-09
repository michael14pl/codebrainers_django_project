from django.urls import path

from wykop.posts.views import PostCreateView, PostDetailView, PostListView

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<int:pk>', PostDetailView.as_view(), name='details'),
    path('nowy', PostCreateView.as_view(), name='create')
]
