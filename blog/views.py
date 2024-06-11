from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm
from taggit.models import Tag
from django.db.models import Count, Q
from django.urls import reverse
from django.views import View
from django.urls import reverse_lazy

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] =  Tag.objects.all()
        context['categories'] = Category.objects.all().annotate(post_count=Count('post_category'))
        return context

    def get_queryset(self):
        queryset = Post.objects.all()
        search_query = self.request.GET.get('q')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query) | queryset.filter(content__icontains=search_query)

        return queryset

    # def get_queryset(self):
    #     name = self.request.GET.get('q','')
        
    #     object_list = Post.objects.filter(
    #         Q(title__icontains=name) | 
    #         Q(content__icontains=name)
    #     )
    #     return object_list
    

class PostDetailView(DetailView):
    model = Post
   

class PostCreateView(LoginRequiredMixin,CreateView):  
    model = Post 
    template_name = 'blog/post_create.html'
    fields = '__all__' 
    success_url ='/blog'

class PostUpdateView(LoginRequiredMixin,UpdateView):  
    model = Post 
    template_name = 'blog/post_edit.html'
    fields = '__all__' 
    success_url =reverse_lazy('blog:post_list')



class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/blog'
    template_name = 'blog/post_confirm_delete.html'


class AddCommentToPostView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm()
        return render(request, 'blog/add_comment_to_post.html', {'form': form})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(post.get_absolute_url())
        return render(request, 'blog/add_comment_to_post.html', {'form': form})