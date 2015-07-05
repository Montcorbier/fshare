from django.shortcuts import render, redirect, HttpResponse, Http404, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist

from website.management.commands.generate_registration_key import Command as GenerateRegistrationKey
from website.models import Permission, FSUser, RegistrationKey, File
from website.forms import RegisterForm, PermissionForm, UploadFileForm


def index(request):
    """
        Home page - presentation of FShare

    """
    if not request.user.is_anonymous() and request.user.is_authenticated():
        return upload(request)
    ctxt = dict()
    ctxt["title"] = "Index"
    tpl = "website/index.html"
    return render(request, tpl, ctxt)


def register(request):
    """
        Registration of new users
        redirect to index if registration succeed

    """
    ctxt = dict()
    ctxt["title"] = "Registration"
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


def about(request):
    return HttpResponse("To Do.")


@login_required(login_url="login")
def myfiles(request):
    """
        Homepage for authenticated users
        Shows the list of uploaded files

    """
    ctxt = dict()
    ctxt["title"] = "My files"
    tpl = "website/myfiles.html"
    ctxt["files"] = File.objects.all().filter(owner=request.user)
    for f in ctxt["files"]:
        print(f)
    return render(request, tpl, ctxt)


def is_admin(user):
    """
        Check whether the user can access admin pages or not
        (admin here points the Permission class, not the django admin)

    """
    fsuser = FSUser.objects.get(user=user)
    return fsuser.permission.name == "admin"


def upload(request):
    """
        Handle the file upload
        (first version one file handled)

    """
    ctxt = dict()
    ctxt["title"] = "Upload"
    tpl = "website/upload.html"

    if request.method == "GET":
        return render(request, tpl, ctxt)
    elif request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid(request.user):
            form.save(request.user)
        return redirect('upload')
    raise Http404


def download(request, fid):
    """
        View of a file for download. If the file is protected, 
        no information is displayed about the file until the password
        has been entered.

    """
    ctxt = dict()
    ctxt["title"] = "Upload"
    tpl = "website/download.html"
    # Get the file description
    f = get_object_or_404(File, id=fid)
    # If it is protected by a password
    if f.is_private:
        # Try to get the password from GET
        if "pwd" in request.GET.keys():
            pwd = request.GET["pwd"]
        # Try to get the password from POST
        elif "pwd" in request.POST.keys():
            pwd = request.POST["pwd"]
        # If no password provided, return an error
        else:
            #TODO
            return HttpResponse("No PWD PROVIDED")
        # If the password is not correct, return an error
        if pwd != f.pwd_hash: 
            #TODO
            return HttpResponse("WRONG PWD")
        # Set the password in context to pass it to get_file
        # view through GET parameter
        ctxt["pwd"] = pwd
    # At this point, either the file is public or 
    # the correct password was provided
    # Set file meta in context
    ctxt["f"] = f
    return render(request, tpl, ctxt)
    

def get_file(request, fid):
    """
        Handle file download. @param fid is the id of the file to
        be downloaded. If the file is protected, the password given 
        as POST or GET parameter is checked before returning the file.

    """
    f = File.objects.get(id=fid)
    response = HttpResponse(content=open(f.path, 'rb').read())
    response['Content-Disposition'] = 'attachment; filename=%s' % f.title
    return response


@login_required(login_url="login")
@user_passes_test(is_admin, login_url="index")
def cockpit(request):
    """
        FShare administration panel
        From here, an admin can :
            - create new permission classes

    """
    ctxt = dict()
    ctxt["title"] = "Cockpit"
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
        # Else, add unused keys to context
        ctxt["unused_keys"] = list()
        ctxt["distributed_keys"] = list()
        ctxt["used_keys"] = list()
        for key in RegistrationKey.objects.all():
            if key.revoked:
                continue
            if not key.used and not key.distributed: 
                ctxt["unused_keys"].append(key)
            elif not key.used:
                ctxt["distributed_keys"].append(key)
            else:
                ctxt["used_keys"].append(key)
        # Show the form
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


@login_required(login_url="login")
@user_passes_test(is_admin, login_url="index")
def mark_key_distributed(request):
    """
        AJAX view to mark a registration key as 'distributed'.
        This is purely for admin UI-purpose and has no impact on
        the semantics of the given key.
        Returns OK if the key was marked correctly, or KO if something went wrong

    """
    # If no parameter was given, return an error code
    if "key" not in request.GET.keys():
        return HttpResponse("KO")
    # Try to get the given key
    try:
        key = RegistrationKey.objects.get(key=request.GET["key"]) 
    # If getting the key has failed, return an error code
    except ObjectDoesNotExist:
        return HttpResponse("KO")
    # Mark the key as distributed
    key.distributed = True
    # Save key in DB
    key.save()
    # Send OK code
    return HttpResponse("OK")


@login_required(login_url="login")
@user_passes_test(is_admin, login_url="index")
def revoke_key(request):
    """
        AJAX view to revoke a key. After that, it will not 
        be possible to use this key for registration. 
        Returns OK if the key was revoked correctly, or KO if something went wrong, 
        and TOO_LATE if the key has already been used for registration.

    """
    # If no parameter was given, return an error code
    if "key" not in request.GET.keys():
        return HttpResponse("KO")
    # Try to get the given key
    try:
        key = RegistrationKey.objects.get(key=request.GET["key"]) 
    # If getting the key has failed, return an error code
    except ObjectDoesNotExist:
        return HttpResponse("KO")
    # Check that it has not been used
    if key.used:
        return HttpResponse("TOO_LATE")
    # Revoke key
    key.revoked = True
    # Save key in DB
    key.save()
    # Send OK code
    return HttpResponse("OK")

