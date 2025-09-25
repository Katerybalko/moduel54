from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Reply, ReplyStatus, Category
from .forms import PostForm, ReplyForm

class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'board/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        qs = Post.objects.select_related('author')
        cat = self.request.GET.get('category')
        if cat:
            qs = qs.filter(category=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.choices
        ctx['selected'] = self.request.GET.get('category') or ''
        return ctx

class PostDetailView(DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = ReplyForm()
        # Показываем отклики только автору поста
        show_replies = self.request.user.is_authenticated and self.object.author_id == self.request.user.id
        ctx['show_replies'] = show_replies
        if show_replies:
            status = self.request.GET.get('status')
            replies = self.object.replies.select_related('author')
            if status:
                replies = replies.filter(status=status)
            ctx['replies'] = replies
        return ctx

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_form.html'
    success_url = reverse_lazy('board:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author_id == self.request.user.id

class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_form.html'

    def get_success_url(self):
        return reverse_lazy('board:post_detail', kwargs={'pk': self.object.pk})

@login_required
def create_reply(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author_id == request.user.id:
        return redirect('board:post_detail', pk=pk)  # самому себе не отвечаем
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            Reply.objects.create(
                post=post,
                author=request.user,
                text=form.cleaned_data['text']
            )
    return redirect('board:post_detail', pk=pk)

class MyPostRepliesView(LoginRequiredMixin, ListView):
    """Приватная страница со всеми откликами на мои объявления"""
    model = Reply
    template_name = 'board/my_replies.html'
    context_object_name = 'replies'

    def get_queryset(self):
        qs = Reply.objects.select_related('post', 'author').filter(post__author=self.request.user)
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

@login_required
def accept_reply(request, pk):
    reply = get_object_or_404(Reply.objects.select_related('post'), pk=pk)
    if reply.post.author_id != request.user.id:
        return redirect('board:post_detail', pk=reply.post_id)
    reply.status = ReplyStatus.ACCEPTED
    reply.save(update_fields=['status'])
    return redirect('board:my_replies')

@login_required
def decline_reply(request, pk):
    reply = get_object_or_404(Reply.objects.select_related('post'), pk=pk)
    if reply.post.author_id != request.user.id:
        return redirect('board:post_detail', pk=reply.post_id)
    reply.status = ReplyStatus.DECLINED
    reply.save(update_fields=['status'])
    return redirect('board:my_replies')
