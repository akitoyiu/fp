from django.contrib import admin
from django.urls import path
from .views import HomeView, ArticleDetailView, addPostView, updatePostView, deletePostView, HomePageView
from .views import addCategoryView, categoryPostView, newPostView
from .views import likeView, AddPostCommentView, like_button, delimg_button
from django.conf.urls import url

#app_name="like_button"

urlpatterns = [
    
    path('', HomeView.as_view(), name="Home"),

    path('<int:pk>/HomePage/', HomePageView, name="HomePage"),
    #url(r'^$', HomeView.as_view(), name='Home'),  #Need to use this for pagination

    path('article/<int:pk>', ArticleDetailView.as_view(), name="Article_Detail"),
    path('add_post/', addPostView.as_view(), name="add_post"),
    path('article/Edit/<int:pk>', updatePostView.as_view(), name="update_post"),
    path('article/Delete/<int:pk>', deletePostView.as_view(), name="delete_post"),

    #Category
    path('add_category/', addCategoryView.as_view(), name="add_category"),
    path('category/<str:cats>', categoryPostView, name="category_post"),

    #like
    path('like/<int:pk>', likeView, name='like_post'),

    #Post Comment
    path('postcomment/<int:pk>', AddPostCommentView, name='post_comment'),

    path('likebutton/', like_button, name='like'),
    path('delimgbutton/', delimg_button, name='delimg'),
    #url(r'^likebutton/$',like_button, name='like'),
]
