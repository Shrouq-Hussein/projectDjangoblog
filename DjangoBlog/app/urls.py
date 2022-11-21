from django.urls import path
from app import views


urlpatterns = [
    path('home',views.PostsGenericListView.as_view(),name='app.home'),
    path('signup',views.SignupView.as_view(),name='signup'),
    path('post/create',views.CreatePostGenericView.as_view(),name='post.create'),
    path('post/<int:pk>/',views.PostDetailsGenericView.as_view(),name='post.details'),
    path('post/<int:pk>/delete/',views.PostDeleteGenericView.as_view(),name='post.delete'),
    path('post/<int:pk>/update/',views.PostUpdateGenericView.as_view(),name='post.update'),

    path('manageblog',views.manageblog,name='admin.manageblog'),

    path('users',views.UsersGenericListView.as_view(),name='admin.show.users'),
    path('users/<int:user_id>/block',views.blockUser,name='admin.block.user'),
    path('users/<int:user_id>/unblock',views.unblockUser,name='admin.unblock.user'),
    path('users/<int:user_id>/promote',views.promoteUser,name='admin.promote.user'),

    path('categories',views.CategoriesGenericListView.as_view(),name='admin.show.categories'),
    path('categories/create',views.CreateCategoryGenericView.as_view(),name='admin.create.category'),
    path('categories/<int:pk>/update',views.UpdateCategoryGenericView.as_view(),name='admin.update.category'),
    path('categories/<int:pk>/delete',views.DeleteCategoryGenericView.as_view(),name='admin.delete.category'),

    path('tags',views.TagsGenericListView.as_view(),name='admin.show.tags'),
    path('tags/create',views.CreateTagGenericView.as_view(),name='admin.create.tag'),
    path('tags/<int:pk>/update',views.UpdateTagGenericView.as_view(),name='admin.update.tag'),
    path('tags/<int:pk>/delete',views.DeleteTagGenericView.as_view(),name='admin.delete.tag'),

    path('forbiddenwords',views.ForbiddenWordsGenericListView.as_view(),name='admin.show.forbiddenwords'),
    path('forbiddenwords/create',views.CreateForbiddenWordGenericView.as_view(),name='admin.create.forbiddenwords'),
    path('forbiddenwords/<int:pk>/update',views.UpdateForbiddenWordGenericView.as_view(),name='admin.update.forbiddenwords'),
    path('forbiddenwords/<int:pk>/delete',views.DeleteForbiddenWordGenericView.as_view(),name='admin.delete.forbiddenwords'),

    path('posts/<str:cat_name>',views.catPosts,name='catPosts'),
    path('posts/<str:catgory_name>/subscribe',views.subscribeToCategory,name='subscribetocategory'),
    path('posts/<str:catgory_name>/unsubscribe',views.unsubscribeToCategory,name='unsubscribetocategory'),

    path('posts/<int:post_id>/addcomment',views.CreateCommentGenericView.as_view(),name='post.comment'),
    
    path('comment/<int:comment_id>/addreply',views.CreateReplyGenericView.as_view(),name='comment.reply'),
    path('comment/<int:pk>/update',views.UpdateCommentGenericView.as_view(),name='comment.update'),
    path('comment/<int:pk>/delete',views.DeleteCommentGenericView.as_view(),name='comment.delete'),

    path('reply/<int:pk>/update',views.UpdateReplyGenericView.as_view(),name='reply.update'),
    path('reply/<int:pk>/delete',views.DeleteReplyGenericView.as_view(),name='reply.delete'),

    path('posts/<int:post_id>/like',views.likePost,name='post.like'),
    path('posts/<int:post_id>/unlike',views.unLikePost,name='post.unlike'),
    path('filtered',views.searchby_tag_or_title,name='searchby_tag_or_title'),
    
    

    

    


]
