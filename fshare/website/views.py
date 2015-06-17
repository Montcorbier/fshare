from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test

from website.management.commands.generate_registration_key import Command as GenerateRegistrationKey
from website.models import Permission, FSUser
from website.forms import RegisterForm, PermissionForm


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


@login_required(login_url="login")
def myfiles(request):
    """
        Homepage for authenticated users
        Shows the list of uploaded files

    """
    ctxt = dict()
    tpl = "website/myfiles.html"
    return render(request, tpl, ctxt)


def is_admin(user):
    """
        Check whether the user can access admin pages or not
        (admin here points the Permission class, not the django admin)

    """
    fsuser = FSUser.objects.get(user=user)
    return fsuser.permission.name == "admin"


@login_required(login_url="login")
@user_passes_test(is_admin, login_url="index")
def cockpit(request):
    """
        FShare administration panel
        From here, an admin can :
            - create new permission classes

    """
    ctxt = dict()
    tpl = "website/cockpit.html"
    # Get permission form if any
    ctxt["perms"] = [p for p in Permission.objects.all()]
    perm_form = PermissionForm(request.POST or None)
    # Check the permission form
    if perm_form.is_valid():
        # If valid, create a new permission entry
        perm_form.save()
        return redirect('cockpit')
    else:
        # Else, show the form
        ctxt["perm_form"] = perm_form
    return render(request, tpl, ctxt)


@login_required(login_url="login")
@user_passes_test(is_admin, login_url="index")
def generate_registration_key(request):
    """
        AJAX view to generate registration key for a permission class
        given in GET parameter (named 'class')
        Returns the generated key if any, or KO if something went wrong

    """
    # If no parameter was given, return an error code
    if "class" not in request.GET.keys():
        return HttpResponse("KO")
    # Try to generate a key
    key = GenerateRegistrationKey().handle(pclass=request.GET["class"]) 
    # If generation has failed, return an error code
    if key is None:
        return HttpResponse("KO")
    # Otherwise, return the generated key in plaintext
    else:
        return HttpResponse(key.key)

