from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from website.forms import RegisterForm


def index(request):
    """
        Home page - presentation of FShare

    """
    ctxt = dict()
    tpl = "website/index.html"
    return render(request, tpl, ctxt)


def register(request):
    """
        Registration of new users
        redirect to index if registration succeed

    """
    ctxt = dict()
    tpl = "registration/register.html"
    # Get registration form from POST values
    reg_form = RegisterForm(request.POST or None)
    # Check the form validity
    if reg_form.is_valid():
        # Register the new user
        new_user = reg_form.save()
        # Authenticate
        new_user = authenticate(username=new_user.user.username, password=request.POST["password1"])
        # Log the new user in
        login(request, new_user)
        return redirect("index")
    else:
        # Else we show a registration form
        ctxt["reg_form"] = reg_form
        return render(request, tpl, ctxt)


def myfiles(request):
    ctxt = dict()
    tpl = "website/myfiles.html"
    return render(request, tpl, ctxt)
