from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    allcategory = Category.objects.all()
    activeListing = Listing.objects.filter(isActive=True)
    return render(request, "auctions/index.html",{
        'Listings': activeListing,
        'categories' : allcategory,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def addBid(request, id):   
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    ISListingInWatchList = request.user in listingData.watchlist.all()
    allComment = Comment.objects.filter(listing=listingData)
    isOwnwe = request.user.username == listingData.owner.username

    if int(newBid) > listingData.price.bid:
         updateBId = Bid(user=request.user, bid=int(newBid))
         updateBId.save()
         listingData.price = updateBId
         listingData.save()
         return render(request, 'auctions/listing.html',{
            'listing': listingData,
            'message': 'Bid was updated successfully',
            'update': True,
            'isListingInWatchList': ISListingInWatchList,
            'allComments': allComment,
         })
    else:
        return render(request, 'auctions/listing.html',{
            'listing': listingData,
            'message': 'Bid was updated Faild',
            'update': False,
            'isListingInWatchList': ISListingInWatchList,
            'allComments': allComment,
            'isOwner': isOwnwe,

         })



def creatListing(request):
    if request.method == 'GET':
        allcategory = Category.objects.all()
        return render(request, 'auctions/create.html', {
            'categories' : allcategory,
        })
    else:
        title = request.POST['title']
        desc = request.POST['desc']
        imageURL = request.POST['imageURL']
        price = request.POST['price']
        category = request.POST['category']
        # Who is The User
        CurrentUser = request.user
        # get the categery from other db
        cat_data = Category.objects.get(categoryname=category)
        # New List
        bid = Bid(
            bid=int(price),
            user=CurrentUser
        )
        bid.save()



        newListing = Listing(
            title = title,
            description = desc,
            imageUrl = imageURL,
            price = bid,
            category = cat_data,
            owner = CurrentUser,
        )

        newListing.save()
        return HttpResponseRedirect(reverse('index'))




def RemoveWatchList(request, id):
    listData = Listing.objects.get(pk=id)
    currentUser = request.user
    listData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse('listing', args=(id, )))

def AddWatchList(request, id):
    listData = Listing.objects.get(pk=id)
    currentUser = request.user
    listData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse(listing, args=(id, )))



def addComment(request, id):
    CurrentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']
    newComment = Comment(
        author = CurrentUser,
        listing = listingData,
        message = message
    )
    newComment.save()
    return HttpResponseRedirect(reverse(listing, args=(id, )))


# def desplayWatchList(request):
#     CurrentUser = request.user
#     lesting = CurrentUser.listing_WatchList.all()
#     return render(request, 'auctions/watchList.html', {
#         'Listings': lesting
#     })

# views.py
def desplayWatchList(request):
    current_user = request.user
    listings = current_user.listing_WatchList.all()  # تأكد من استخدام 'listing_WatchList' بشكل صحيح
    return render(request, 'auctions/watchlist.html', {
        'Listings': listings
    })



def desplayCat(request):
    if request.method == 'POST':
        CategoryFromForm = request.POST['category']
        category = Category.objects.get(categoryname=CategoryFromForm)
        allcategory = Category.objects.all()
        activeListing = Listing.objects.filter(isActive=True, category = category)
        return render(request, "auctions/index.html",{
            'Listings': activeListing,
            'categories' : allcategory,
        })
    

def listing(request, id):

    listingData = Listing.objects.get(pk=id)
    ISListingInWatchList = request.user in listingData.watchlist.all()
    allComment = Comment.objects.filter(listing=listingData)
    isOwnwe = request.user.username == listingData.owner.username


    return render(request, 'auctions/listing.html', {
        'id': id,
        'listing': listingData,
        'isListingInWatchList': ISListingInWatchList,
        'allComments': allComment,
        'isOwner': isOwnwe,
    })


def closeAuction(request, id): 
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isOwnwe = request.user.username == listingData.owner.username
    ISListingInWatchList = request.user in listingData.watchlist.all()
    allComment = Comment.objects.filter(listing=listingData)
    return render(request, 'auctions/listing.html', {
    'id': id,
    'listing': listingData,
    'isListingInWatchList': ISListingInWatchList,
    'allComments': allComment,
    'isOwner': isOwnwe,
    'update': True,
    'message': 'Congratulations! Your auction is close',
    'isOwner': isOwnwe,
})

