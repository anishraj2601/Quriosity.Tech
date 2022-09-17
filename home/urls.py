from django.contrib import admin
from django.urls import path
from home import views
# from django.conf.urls import url

# for customizing the admin panel
admin.site.site_header = "Quriosity Administration"
admin.site.site_title = "Quriosity Admin Panel"
admin.site.index_title = "Welcome to Quriosity.tech admin panel"


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    # path('base_copy/',views.base_copy,name="base_copy"),
    # path('base/',views.base,name="base"),
    path('signup/',views.signup,name="signup"),
    path('log_in/',views.log_in,name="log_in"),
    # path('activity/',views.activity,name="activity"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('faq/',views.faq,name="faq"),
    # path('profile/',views.profile,name="profile"),
    # path('settings/',views.settings,name="settings"),
    # path('search/',views.search,name="search"),
    path('404/',views.page404,name="404"),
    path('forgot-username/',views.forgotUsername,name="forgotUsername"),
    path('forgot-password/',views.forgotPassword,name="forgotPassword"),
    # path('email/',views.sendEmail,name="email"),
    # for handling logout
    path('log_out/',views.log_out,name="log_out"),
    # for handling signup
    path('signup/handleSignup/',views.handleSignup,name="handleSignup"),
    # for handling Login
    path('log_in/handleLogin/',views.handleLogin,name="handleLogin"),
    # path('problems/likePost/<int:pk>',views.likePost,name='likePost'),
    path('problems/likePost/<int:pk>',views.ProblemLike,name='likePost'),
    path('problems/ProblemMark/<int:pk>',views.ProblemMark,name='ProblemMark'),
    path('problems/<slug:slug>',views.problems,name="problems"),
    # path to verify email id
    path('verify/<auth_token>',views.verify,name="verify"),
    path('view/<slug:slug>',views.view,name="view"),
]