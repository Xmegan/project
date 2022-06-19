from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm
from .filters import PostFilter



class IndexView(generic.ListView):
    template_name = 'blogs/index.html'
    context_object_name = 'blogs_list'

    def get_queryset(self):
        """Return all the blogs."""
        return Post.objects.all()



def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blogs/post_list.html', {'posts': posts})



def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blogs/post_detail.html', {'post': post})



def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blogs/post_edit.html', {'form': form})



def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
        return render(request, 'blogs/post_list.html', {})
    else:
        form = PostForm(instance=post)
    return render(request, 'blogs/post_edit.html', {'form': form})



class SearchView(generic.ListView):
    template_name = 'blogs/search.html'
    context_object_name = 'blogs_list'

    def get_queryset(self):
        """Return all the blogs."""
        return Post.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class UpdateView(generic.edit.UpdateView):
    template_name = 'blogs/update.html'
    model = Post
    fields = ['text', 'title']
    success_url = reverse_lazy('post_list')



class DeleteView(generic.edit.DeleteView):
    template_name = 'blogs/delete.html' 
    model = Post
    success_url = reverse_lazy('post_list')



class OrderDateView(generic.ListView):
    template_name = 'blogs/ordering.html'
    context_object_name = 'blogs_list'

    def get_queryset(self):
        """Return all the blogs."""
        return Post.objects.order_by('-published_date')



class TodayView(generic.ListView):
    template_name = 'blogs/latest.html'
    context_object_name = 'blogs_list'

    def get_queryset(self):
        """Return all the blogs."""
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')