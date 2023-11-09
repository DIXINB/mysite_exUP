from django.contrib import admin
from .models import Author, Book, Hist, Dict, Artc,Pros
from .models import Post, Replie, Profile, Ip
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Hist)
admin.site.register(Artc)
admin.site.register(Dict)
admin.site.register(Pros)
admin.site.register(Post)
admin.site.register(Replie)
admin.site.register(Profile)
admin.site.register(Ip)