from django.urls import path

from .views import my_homepage,history,hist, \
articles, artc, dict,prose,prse, \
mail, forum, discussion, UserRegister, UserLogin, UserLogout, myprofile

urlpatterns=[
    path('', my_homepage),
	path('history/', history),
	path('history/<int:histid>/', hist),
	path('articles/', articles),
	path('articles/<int:artcid>/', artc),	
    path('dict/', dict),
    path('prose/', prose),
    path('prose/<int:prseid>/', prse),

    path('mail/', mail),
    path("forum/",forum, name="Forum"),
    path("discussion/<int:myid>/",discussion, name="Discussions"),
    path("register/",UserRegister, name="Register"),
    path("login/",UserLogin, name="Login"),
    path("logout/",UserLogout, name="Logout"),
    path("myprofile/",myprofile, name="Myprofile"),
]