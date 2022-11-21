from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView ,ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin ,UserPassesTestMixin
from django.contrib.auth.models import Group ,User
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from app.forms import SignupCustomForm ,PostModelForm,CategoryModelForm ,TagModelForm ,ForbiddenWordModelForm,CommentModelForm,ReplyModelForm
from app.models import Category, Post ,ForbiddenWord ,Tag,Comment,Reply


class SignupView(CreateView):
    form_class = SignupCustomForm
    template_name = "registration/signup.html"
    success_url = "/login"

# ----------------- for normal users --------------------------

# @login_required(login_url='/login')
# def home_view(request):
#     posts = Post.objects.all()
#     categories = Category.objects.all()
#     return render(request, "app/posts/all.html",context={"categories":categories,"posts":posts})

#  post
class CreatePostGenericView(LoginRequiredMixin,CreateView):
    login_url = '/login'
    form_class = PostModelForm
    template_name = "app/posts/create.html"
    success_url = "/home"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

class PostDetailsGenericView(LoginRequiredMixin,DetailView):
    login_url = '/login'
    model = Post
    template_name = "app/posts/details.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super(PostDetailsGenericView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

class PostUpdateGenericView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = '/login'
    form_class = PostModelForm
    model = Post
    template_name = "app/posts/update.html"
    success_url = "/home"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False
    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

    # def get_queryset(self):
    #     queryset = super(PostUpdateGenericView, self).get_queryset()
    #     queryset = queryset.filter(author=self.request.user)
    #     return queryset


class PostDeleteGenericView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = '/login'
    model= Post
    template_name = "app/posts/delete.html"
    success_url = "/home"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False
    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

class PostsGenericListView(LoginRequiredMixin,ListView):
    login_url = '/login'
    model = Post
    template_name = "app/posts/all.html"
    context_object_name = "posts"
    queryset = Post.objects.order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super(PostsGenericListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
        
    def get_template_names(self):
        # if self.request.user.is_superuser:
        #     template_name = 'app/admin/home.html'
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]
    def get(self, *args, **kwargs):
        if len(self.request.user.groups.filter(name='blocked')):
            return redirect("/login")
        return super(PostsGenericListView, self).get(*args, **kwargs)

@login_required(login_url='/login')
def catPosts(request,cat_name):
    if len(request.user.groups.filter(name='blocked')):
        return render(request,'app/blockeduser.html')
    else:
        cat = Category.objects.filter(cat_name=cat_name).first()
        print(cat ,"====================================")
        cat_posts = Post.objects.filter(category=cat).order_by('-updated_at')
        print(cat_posts)
        categories = Category.objects.all()
        return render(request, 'app/posts/all.html', {"posts":cat_posts,"categories":categories})

@login_required(login_url='/login')
def subscribeToCategory(request, catgory_name):
    print("==================subscribeToCategory============")
    if len(request.user.groups.filter(name='blocked')):
        return render(request,'app/blockeduser.html')

    current_user = request.user
    found = False
    all_categories = Category.objects.all()
    for cat in all_categories:
        if cat.cat_name == catgory_name:
            cat_subscribers = cat.subscribers.all()
            for subscriber in cat_subscribers:
                if subscriber == current_user:
                    found = True
                    # messages.info( request, "This User already subscribed to this Category")
                    return redirect('catPosts',cat_name=catgory_name)
                else:
                    found = False
    if found == False:
        print("flase")
        print(Category.objects.get(cat_name=catgory_name))
        print(Category.objects.get(cat_name=catgory_name).subscribers)
        Category.objects.get(cat_name=catgory_name).subscribers.add(current_user)
        print(Category.objects.get(cat_name=catgory_name).show_subscribers())
        # messages.info(request, f'Successfully Subscribed to {catgory_name}')
        return redirect('catPosts',cat_name=catgory_name)


@login_required(login_url='/login')
def unsubscribeToCategory(request, catgory_name):
    print("==================unsubscribeToCategory============")
    if len(request.user.groups.filter(name='blocked')):
        return render(request,'app/blockeduser.html')

    current_user = request.user
    found = False
    all_categories = Category.objects.all()
    for cat in all_categories:
        if cat.cat_name == catgory_name:
            cat_subscribers = cat.subscribers.all()
            for subscriber in cat_subscribers:
                if subscriber == current_user:
                    found = True
                    Category.objects.get(cat_name=catgory_name).subscribers.remove(current_user)
                    # messages.info( request, "unsubscribed to this Category successfully")
                return redirect('catPosts',cat_name=catgory_name)
                


def cleanCommentsandReplies(content,forbiddenList):
        cleanedcontent=""
        for word in  content.split():
            if word.lower() in forbiddenList:
                print("yes  ",word)
                for i in word:
                    cleanedcontent+="*"
            else:
                cleanedcontent+=word
            cleanedcontent+=" "
        print("cleanedcontent:",cleanedcontent)
        return cleanedcontent
#  comment
class CreateCommentGenericView(LoginRequiredMixin,CreateView):
    login_url = '/login'
    form_class = CommentModelForm
    template_name = "app/comments/create.html"
    success_url = "/home"
    
    def form_valid(self, form):
        if self.kwargs["post_id"]:
            post = Post.objects.get(id=self.kwargs["post_id"])
            form.instance.post = post
        
        form.instance.author = self.request.user

        forbiddenwordsall = ForbiddenWord.objects.all()
        forbiddenList=[]
        for obj in forbiddenwordsall:
            forbiddenList.append(obj.word.lower())
        cleanedcontent = cleanCommentsandReplies(form.instance.content,forbiddenList)
        form.instance.content= cleanedcontent        
        return super().form_valid(form)

    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]


class UpdateCommentGenericView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = '/login'
    form_class = CommentModelForm
    model = Comment
    template_name = "app/comments/update.html"
    success_url = "/home"

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author or self.request.user.is_superuser:
            return True
        return False
    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

class DeleteCommentGenericView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = '/login'
    model= Comment
    template_name = "app/comments/delete.html"
    success_url = "/home"

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author or self.request.user.is_superuser:
            return True
        return False
    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]
# reply
class CreateReplyGenericView(LoginRequiredMixin,CreateView):
    login_url = '/login'
    form_class = ReplyModelForm
    template_name = "app/replies/create.html"
    success_url = "/home"
    
    def form_valid(self, form):
        if self.kwargs["comment_id"]:
            comment = Comment.objects.get(id=self.kwargs["comment_id"])
            form.instance.comment = comment
        
        form.instance.author = self.request.user

        forbiddenwordsall = ForbiddenWord.objects.all()
        forbiddenList=[]
        for obj in forbiddenwordsall:
            forbiddenList.append(obj.word.lower())
        cleanedcontent = cleanCommentsandReplies(form.instance.content,forbiddenList)
        form.instance.content= cleanedcontent        
        return super().form_valid(form)

    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

class UpdateReplyGenericView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = '/login'
    form_class = ReplyModelForm
    model = Reply
    template_name = "app/replies/update.html"
    success_url = "/home"

    def test_func(self):
        reply = self.get_object()
        if self.request.user == reply.author or self.request.user.is_superuser:
            return True
        return False
    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]
class DeleteReplyGenericView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = '/login'
    model= Reply
    template_name = "app/replies/delete.html"
    success_url = "/home"

    def test_func(self):
        reply = self.get_object()
        if self.request.user == reply.author or self.request.user.is_superuser:
            return True
        return False
    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

# like
@login_required(login_url='/login')
def likePost(request, post_id):
    liked = False
    if len(request.user.groups.filter(name='blocked')):
            return render(request,'app/blockeduser.html')
    post = Post.objects.get(id=post_id)   
    if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user) #remove like
            liked = False
    else:
            post.likes.add(request.user) #like
            if post.unlikes.filter(id=request.user.id).exists():
                post.unlikes.remove(request.user) # remove unlike
            liked= True
            
    # request.session['liked'] = liked

    if request.META.get('HTTP_REFERER') == "http://127.0.0.1:8000/home" :
        return redirect('app.home')
    else:
        return redirect('post.details',pk=post_id)



@login_required(login_url='/login')
def unLikePost(request, post_id):
    if len(request.user.groups.filter(name='blocked')):
            return render(request,'app/blockeduser.html')

    post = Post.objects.get(id=post_id)   
    if post.unlikes.filter(id=request.user.id).exists():
            post.unlikes.remove(request.user) # remove unlike
    else:
            post.unlikes.add(request.user) #unlike

            if post.unlikes_number() > 5:
                print("unlikes_number > 5")
                post.delete()
                return redirect('app.home')


            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user) # remove like
            
    if request.META.get('HTTP_REFERER') == "http://127.0.0.1:8000/home" :
        return redirect('app.home')
    else:
        return redirect('post.details',pk=post_id)
#  ------------------------- for admin users --------

@login_required(login_url='/login')
def manageblog(request):
    if request.user.is_superuser:
       return  render(request,"app/admin/home.html")
    else:
         raise PermissionDenied


class UsersGenericListView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    login_url = '/login'
    model = User
    template_name = "app/admin/users.html"
    context_object_name = "users"
        
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

@login_required(login_url='/login')
def blockUser(request, user_id):
    if request.user.is_superuser:
        # group = Group.objects.get(name='blocked')
        group, created = Group.objects.get_or_create(name='blocked')
        user = User.objects.get(id=user_id)
        if user.is_superuser:
            raise PermissionDenied
        else:
            group.user_set.add(user)
            return  redirect("admin.show.users")
    else:
         raise PermissionDenied

@login_required(login_url='/login')
def promoteUser(request, user_id):
    if request.user.is_superuser:
        user = User.objects.get(id = user_id) 
        user.is_staff=True 
        user.is_superuser=True
        user.save()
        return  redirect("admin.show.users")
    else:
         raise PermissionDenied


@login_required(login_url='/login')
def unblockUser(request, user_id):
    if request.user.is_superuser:
        group = Group.objects.get(name='blocked')
        user = User.objects.get(id=user_id)
        group.user_set.remove(user)
        return  redirect("admin.show.users")
    else:
         raise PermissionDenied
# ------------------------------------------------------------------

class CategoriesGenericListView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    login_url = '/login'
    model = Category
    template_name = "app/admin/categories/all.html"
    context_object_name = "categories"
        
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

class CreateCategoryGenericView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    login_url = '/login'
    form_class = CategoryModelForm
    template_name = "app/admin/categories/create.html"
    success_url = "/categories"

    
    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

class UpdateCategoryGenericView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = '/login'
    form_class = CategoryModelForm
    model = Category
    template_name = "app/admin/categories/update.html"
    success_url = "/categories"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

class DeleteCategoryGenericView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = '/login'
    model= Category
    template_name = "app/admin/categories/delete.html"
    success_url = "/categories"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

# --------------------------------------------------------------
class TagsGenericListView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    login_url = '/login'
    model = Tag
    template_name = "app/admin/tags/all.html"
    context_object_name = "tags"
        
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

class CreateTagGenericView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    login_url = '/login'
    form_class = TagModelForm
    template_name = "app/admin/tags/create.html"
    success_url = "/tags"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

class UpdateTagGenericView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = '/login'
    form_class = TagModelForm
    model = Tag
    template_name = "app/admin/tags/update.html"
    success_url = "/tags"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

class DeleteTagGenericView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = '/login'
    model= Tag
    template_name = "app/admin/tags/delete.html"
    success_url = "/tags"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

# --------------------------------------------------------------
class ForbiddenWordsGenericListView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    login_url = '/login'
    model = ForbiddenWord
    template_name = "app/admin/forbiddenwords/all.html"
    context_object_name = "forbiddenwords"
        
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False



class CreateForbiddenWordGenericView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    login_url = '/login'
    form_class = ForbiddenWordModelForm
    template_name = "app/admin/forbiddenwords/create.html"
    success_url = "/forbiddenwords"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

class UpdateForbiddenWordGenericView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = '/login'
    form_class = ForbiddenWordModelForm
    model = ForbiddenWord
    template_name = "app/admin/forbiddenwords/update.html"
    success_url = "/forbiddenwords"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

class DeleteForbiddenWordGenericView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = '/login'
    model= ForbiddenWord
    template_name = "app/admin/forbiddenwords/delete.html"
    success_url = "/forbiddenwords"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_template_names(self):
        if len(self.request.user.groups.filter(name='blocked')):
            template_name = 'app/blockeduser.html'
        else:
            template_name = self.template_name
        return [template_name]

@login_required(login_url='/login')
def searchby_tag_or_title(request):
    if len(request.user.groups.filter(name='blocked')):
            return render(request,'app/blockeduser.html')
    posts = []
    if request.method == 'POST':
        search_about = request.POST['search_about']
        if  search_about:
            allposts = Post.objects.all()
            for post in allposts:
                for tag in post.tags.all():
                    if search_about in tag.tag_name:
                        posts.append(post)
        
                if search_about in post.title:
                    posts.append(post)
            categories = Category.objects.all()
            return render( request, "app/posts/all.html",{"categories":categories,"posts": posts})
        else:
            return redirect("app.home")
    
