from django.contrib import admin

# Register your models here.

from .models import Listing, Category , User, Comment, Bid

admin.site.site_header = 'Prro.Coders'
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Bid)
