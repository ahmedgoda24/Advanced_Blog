from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm
from taggit.models import Tag
from django.db.models import Count, Q

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
  
    paginate_by = 3

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
   


# class PostsByCategory(ListView):
#     model = Post

#     def get_queryset(self):
#         objects_list = Post.objects.filter(
#             Q(category__name__icontains=self.kwargs['slug'])
#         )
#         return objects_list
    


# class PostsByTags(ListView):
#     model = Post

#     def get_queryset(self):
#         objects_list = Post.objects.filter(
#             Q(tags__name__icontains=self.kwargs['slug'])
#         )
#         return objects_list



class PostCreateView(LoginRequiredMixin,CreateView):  
    model = Post 
    template_name = 'blog/post_create.html'
    fields = '__all__' 
    success_url ='/blog'

class PostUpdateView(LoginRequiredMixin,UpdateView):  
    model = Post 
    template_name = 'blog/post_edit.html'
    fields = '__all__' 
    success_url ='/blog'


# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = 'blog_app/post_form.html'

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

# class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Post
#     form_class = PostForm
#     template_name = 'blog_app/post_form.html'

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         post = self.get_object()
#         return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

