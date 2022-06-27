from django.shortcuts import render, redirect
from .models import User, Item
from django.contrib import messages
import bcrypt


def index(request):

    return render(request, 'index.html')


def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, errorMessage in errors.items():
                messages.error(request, errorMessage)
            return redirect("/")
        else:
            name = request.POST["name"]
            username = request.POST["username"]
            password = request.POST["password"]
            date_hired = request.POST["datehired"]
            passwordHash = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt()).decode()
            newUser = User.objects.create(
                name=name, username=username, password=passwordHash, date_hired=date_hired)
            request.session["loggedInUserId"] = newUser.id
            messages.success(request, "User has been created")

    return redirect('/')


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                request.session["loggedInUserId"] = user.id
                messages.success(request, "You have logged in!")
            else:
                messages.error(request, "User password do not match")
        except User.DoesNotExist:
            messages.error(request, "User not found")
        return redirect("/")
    return redirect("/")


def logout(request):
    request.session.clear()
    return redirect('/')


def createItem(request):
    if "loggedInUserId" not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = Item.objects.basic_validat(request.POST)

        if len(errors) > 0:
            for key, errorMessage in errors.items():
                messages.error(request, errorMessage)
        else:
            item_name = request.POST["item"]
            loggedInUserId = User.objects.get(
                id=request.session["loggedInUserId"])
            item = Item.objects.create(name=item_name, creator=loggedInUserId)
            messages.success(request, "Item have been created!")

    return render(request, "create_Item.html")


def dashboard(request):
    if "loggedInUserId" not in request.session:
        return redirect('/')
    loggedInUserId = User.objects.get(id=request.session["loggedInUserId"])
    context = {
        "user": loggedInUserId,
        "user_items": loggedInUserId.created_items.all(),
        "fav_items": loggedInUserId.fav_items.all(),
        "others_items": Item.objects.exclude(creator=loggedInUserId)
    }
    return render(request, "dashboard.html", context)


def addList(request, item_id):
    loggedInUserId = User.objects.get(id=request.session["loggedInUserId"])
    item = Item.objects.get(id=item_id)
    item.fav_users.add(loggedInUserId)
    loggedInUserId.fav_items.add(item)
    return redirect('/dashboard')


def deleteItem(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect('/dashboard')


def removeList(request, item_id):
    loggedInUserId = User.objects.get(id=request.session["loggedInUserId"])
    item = Item.objects.get(id=item_id)
    item.fav_users.remove(loggedInUserId)

    return redirect('/dashboard')


def itemView(request, item_id):
    item = Item.objects.get(id=item_id)
    context = {
        "item": item,
        "fav_users": item.fav_users.all()
    }
    return render(request, 'view_Item.html', context)