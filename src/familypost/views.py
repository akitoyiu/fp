from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, PostComment, Tag, PostMedia, UserProfile
from .forms import PostForm, EditPostForm, NewPostForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
# Create your views here.

class HomeView(ListView):
    model = Post
    template_name = "home.html"
    ordering = ['-id']
    paginate_by = 5 # for pagination
    context_object_name = 'posts' # for pagination
    

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all().values('name', 'slug')
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

class ArticleDetailView(DetailView):
    model = Post
    template_name = "article_detail.html"
    
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all().values('name', 'slug')
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu

        # Get the total likes of the post
        thisArticle = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = thisArticle.totalLikes()
        context["total_likes"] = total_likes

        liked = False
        if thisArticle.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["liked"] = liked

        return context

class addPostView(CreateView):
    model = Post
    template_name = "new_post.html"
    form_class = NewPostForm
    #fields = '__all__'
    #fields = ('title', 'body')

    def form_valid(self, form):
        user = self.request.user
        tags_obj = []
        files_obj = []
        postmedias = self.request.FILES.getlist('postmedias')
        title = form.cleaned_data.get('title')
        category = form.cleaned_data.get('category')
        body = form.cleaned_data.get('body')
        tags_list = list(form.cleaned_data.get('tags').split(','))

        for tag in tags_list:
            t, created = Tag.objects.get_or_create(title=tag.strip())
            tags_obj.append(t)

        for file in postmedias:
            file_instance = PostMedia(file=file, user=self.request.user)
            file_instance.save()
            files_obj.append(file_instance)

        post, created = Post.objects.update_or_create(author=user, title=title, category=category, body=body)
        post.tags.set(tags_obj)
        post.postmedias.set(files_obj)

        post.save() 
        return HttpResponseRedirect(reverse_lazy('Home'))

def newPostView(request):
    
    user = request.user
    tags_obj = []
    files_obj = []
        
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():

            postmedias = self.request.FILES.getlist('postmedias')
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            body = form.cleaned_data.get('body')
            tags_list = list(form.cleaned_data.get('tags').split(','))

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag.strip())
                tags_obj.append(t)

            for file in postmedias:
                file_instance = PostMedia(file=file, user=self.request.user)
                file_instance.save()
                files_obj.append(file_instance)

            post, created = Post.objects.update_or_create(author=user, title=title, category=category, body=body)
            post.tags.set(tags_obj)
            post.postmedias.set(files_obj)

            post.save() 
            return HttpResponseRedirect(reverse_lazy('Home'))
    else:
        form = NewPostForm()

    context = {
        'form': form
    }
    
    return render(request, 'new_post.html', context)

    
class updatePostView(UpdateView):
    model = Post
    template_name = "update_post.html"
    form_class = NewPostForm
    #fields = '__all__'
    #fields = ('title', 'body')

    def get_context_data(self, **kwargs):
        context = super(updatePostView, self).get_context_data(**kwargs)
        # Get the total likes of the post
        thisArticle = get_object_or_404(Post, id=self.kwargs['pk'])
        tags_line = thisArticle.tag_str()
        context['form'] = self.form_class(instance=thisArticle, initial={'tags':tags_line})
        context['thisPost'] = thisArticle

        return context

    def form_valid(self, form):
        user = self.request.user
        tags_obj = []
        files_obj = []

        postmedias = self.request.FILES.getlist('postmedias')
        title = form.cleaned_data.get('title')
        category = form.cleaned_data.get('category')
        body = form.cleaned_data.get('body')
        tags_list = list(form.cleaned_data.get('tags').split(','))

        for tag in tags_list:
            t, created = Tag.objects.get_or_create(title=tag.strip())
            tags_obj.append(t)

        post, created = Post.objects.update_or_create(id=self.kwargs['pk'])
        post.author = user

        for file in post.postmedias.all():
            files_obj.append(file)
        
        for file in postmedias:
                file_instance = PostMedia(file=file, user=self.request.user)
                file_instance.save()
                files_obj.append(file_instance)

        #post.header_image = header_image
        #if post.header_image == False:
        #    post.header_image = None

        post.title = title
        post.category = category
        post.body = body
        post.tags.set(tags_obj)
        post.postmedias.set(files_obj)

        post.save() 
        return HttpResponseRedirect(reverse_lazy('Home'))


        

class deletePostView(DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy('Home')


class addCategoryView(CreateView):
    model = Category
    template_name = "add_category.html"
    #form_class = PostForm
    #fields = '__all__'
    fields = ('name',)

def categoryPostView(request, cats):
    cats_list = Category.objects.filter(slug=cats).values_list('name')
    cats_name = cats_list[0][0]

    post_full = Post.objects.filter(category=cats_name).order_by('-post_date')
    cat_menu = Category.objects.all().values('name', 'slug')
    
    #numbers_list = range(1, 1000)
    page = request.GET.get('page', 1)
    paginator = Paginator(post_full, 5)
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'category_post.html', {'post_list': post_list, 'cats':cats_name, 'cat_menu':cat_menu})

def likeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    liked = False
    if post.likes.filter(id = request.user.id).exists():
        liked = False
        post.likes.remove(request.user)
    else:
        liked = True
        post.likes.add(request.user)        
    return HttpResponseRedirect(reverse('Article_Detail', args=[str(pk)]))


def EditCommentView(request):    
    if request.method =="POST":
        if request.POST.get("operation") == "editcomment_submit" and request.is_ajax():
            comment_id = request.POST.get("comment_id")
            comment = request.POST.get("comment",None)
            
            postcomment = get_object_or_404(PostComment, id=comment_id)
            postcomment.comment = comment
            postcomment.save()
         
            ctx={"comment_id":comment_id}
            return HttpResponse(json.dumps(ctx), content_type='application/json')


def AddPostCommentView(request, pk):
        
    post = get_object_or_404(Post, id=request.POST.get('post_id'))    
    postcomment, created = PostComment.objects.update_or_create(post=post, commenter=request.user, comment=request.POST.get('postcomment'))
    postcomment.save()

    return HttpResponseRedirect(reverse('Article_Detail', args=[str(pk)]))


def like_button(request):
    if request.method =="POST":
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            like_post_id = request.POST.get("post_id",None)
            post_id=like_post_id.split("_")[1]
            post = get_object_or_404(Post, id=post_id)
            if post.likes.filter(id = request.user.id).exists():
                liked = False
                post.likes.remove(request.user)
            else:
                liked = True
                post.likes.add(request.user)

            total_likes = post.totalLikes()
         
            ctx={"likes_count":total_likes,"liked":liked,"post_id":like_post_id}
            return HttpResponse(json.dumps(ctx), content_type='application/json')

        if request.POST.get("operation") == "likecomment_submit" and request.is_ajax():
            postcomment_id = request.POST.get("postcomment_id",None)
            
            postComment = get_object_or_404(PostComment, id=postcomment_id)
            if postComment.likes.filter(id = request.user.id).exists():
                liked = False
                postComment.likes.remove(request.user)
            else:
                liked = True
                postComment.likes.add(request.user)

            total_likes = postComment.totalLikes()
         
            ctx={"likes_count":total_likes,"liked":liked,"postcomment_id":postcomment_id}
            return HttpResponse(json.dumps(ctx), content_type='application/json')




def delimg_button(request):
    if request.method =="POST":
        if request.POST.get("operation") == "delimg_submit" and request.is_ajax():
            delimg_post_id = request.POST.get("post_id",None)
            postmedia_id=delimg_post_id.split("_")[1]
            postmedia = get_object_or_404(PostMedia, id=postmedia_id)
            postmedia.delete()
         
            ctx={"postmedia_id":postmedia_id}
            return HttpResponse(json.dumps(ctx), content_type='application/json')


def HomePageView(request, pk):    
    post_full = Post.objects.filter(author=pk).order_by('-post_date')
    cat_menu = Category.objects.all().values('name', 'slug')

    userprofile = UserProfile.objects.get(user=pk)
    
    #numbers_list = range(1, 1000)
    page = request.GET.get('page', 1)
    paginator = Paginator(post_full, 5)

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'homepage.html', {'post_list': post_list, 'cat_menu':cat_menu, 'userprofile':userprofile, })


