# from django.contrib.auth.models import AbstractUser
# from django.db import models


# class User(AbstractUser):
#     pass

# class Category(models.Model):
#     categoryname = models.CharField(max_length=30)
#     def __str__(self):
#         return self.categoryname



# class Bid(models.Model):
#     bid = models.IntegerField(default=0)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userBid')
#     def __str__(self):
#         return f"${self.bid:.2f}"


# class Listing(models.Model):
#     title = models.CharField(max_length=30)
#     description = models.CharField(max_length=300)
#     imageUrl = models.CharField(max_length=1000)
#     price = models.ForeignKey(Bid, on_delete=models.CASCADE,  blank=True, null=True, related_name='bidPrice')
#     isActive = models.BooleanField(default=True)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
#     category = models.ForeignKey(Category, on_delete=models.CASCADE , blank=True, null=True, related_name='category')
#     watchlist = models.ManyToManyField(User,blank=True , related_name='listing_WatchList')

#     def __str__(self):
#         return self.title



# class Comment(models.Model):
#     auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userComment')
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing')
#     message = models.CharField(max_length=200)

#     def __str__(self):
#         return f'{self.auther} comment on {self.listing}'












from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryname = models.CharField(max_length=30)

    def __str__(self):
        return self.categoryname


class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userBid')

    def __str__(self):
        return f"${self.bid:.2f}"


class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    imageUrl = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE,  blank=True, null=True, related_name='bidPrice')  # تغيير الحقل إلى FloatField بدلاً من ForeignKey
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_listings')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='listings')
    # watchlist = models.ManyToManyField(User, blank=True, related_name='watchlist')
    watchlist = models.ManyToManyField(User, blank=True, related_name='listing_WatchList')


    def __str__(self):
        return self.title


class Comment(models.Model):
    author  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userComment')  # تأكد أن الاسم صحيح
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing')
    message = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.author} commented on {self.listing}'
