from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Poke
from django.db.models import Q
import bcrypt


def index(request):
    context = {"users": User.objects.all()}
    return render(request, 'poke_app/index.html', context)

def register(request):
    #get user data from post request form
    result = User.objects.validate_registration(request.POST)

    #check for errors in registration validation and create messages / redirect users if so
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        try:
            del request.session['user_id']
        except KeyError:
            pass

        return redirect(index)

    #if no errors in registration validation, redirect user to the welcome page & set post data
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect(dash)

def login(request):
    #get user data from post request form
    result = User.objects.validate_login(request.POST)

    #check for errors in login validation and create messages / redirect users if so
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect(index)

    #if no errors in registration validation, redirect user to the welcome page & set post data
    request.session['user_id'] = result.id
    messages.success(request, "Successfully logged in!")
    return redirect(dash)

def dash(request):
    context = {
        'loggedin': User.objects.get(id=request.session['user_id']),
        'pokes': Poke.objects.all(),
        'users': User.objects.all().exclude(id=request.session['user_id']),
    }
    print('dashtest')
    return render(request, 'poke_app/dash.html', context)

def createPoke(request, user_id):
    currentuser = request.session['user_id']
    create = Poke.objects.createPoke(currentuser, user_id)

    return redirect(dash)

def pokeResults(request, user_id):

    context = {
        'user': User.objects.all().get(id=user_id),
        'pokes': Poke.objects.all().filter(Q(poker=user_id) | Q(poked=user_id)).order_by('pokedate'),
    }
    return render(request, 'poke_app/pokeresults.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')
