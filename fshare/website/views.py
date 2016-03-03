import hashlib
import sha3
import mimetypes

from django.shortcuts import render, redirect, HttpResponse, Http404, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt

from website.management.commands.generate_registration_key import Command as GenerateRegistrationKey
from website.models import Permission, FSUser, RegistrationKey, File
from website.forms import RegisterForm, PermissionForm, UploadFileForm
from website.encryption import decrypt_file


def index(request):
    """
        Home page - presentation of FShare

    """
    if not request.user.is_anonymous() and request.user.is_authenticated():
        return upload(request)
    ctxt = dict()
    ctxt["title"] = "Index"
    ctxt["size_limit"] = settings.FILE_MAX_SIZE_ANONYMOUS
    ctxt["day_limit"] = settings.FILE_MAX_DAYS_ANONYMOUS
    ctxt["dl_limit"] = settings.FILE_MAX_DL_ANONYMOUS
    ctxt["contact"] = settings.CONTACT
    tpl = "website/index.html"
    ctxt["form"] = UploadFileForm(request.POST, request.FILES, label_suffix='')
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
    reg_form = RegisterForm(request.POST or None, label_suffix='')
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


def check_pwd(request, fid, target):
    """
        Check if the file is protected by a key.
        If yes, check the password and redirect 
        to the password template if wrong.

    """
    # Get the file description
    f = get_object_or_404(File, id=fid)
    # If it is protected by a password
    if f.key is not None:
        # Try to get the password from GET
        if "key" in request.GET.keys():
            pwd = request.GET["key"]
        # Try to get the password from POST
        elif "key" in request.POST.keys():
            pwd = request.POST["key"]
        # If no password provided, return password view
        else:
            ctxt = dict()
            ctxt["target"] = target
            return (False, render(request, "website/enter_pwd.html", ctxt))
        # If the password is not correct, return an error
        if hashlib.sha3_512(pwd.encode("utf-8")).hexdigest() != f.key:
            ctxt = dict()
            ctxt["target"] = reverse('download', kwargs={ 'fid': fid})
            ctxt["wrong_pwd"] = True
            return (False, render(request, "website/enter_pwd.html", ctxt))
        return (True, pwd)
    return (True, "")


@csrf_exempt
def upload(request):
    """
        Handle the file upload
        (first version one file handled)

    """
    context = {}
    tpl = "website/upload.html"

    context["title"] = "Upload"

    if request.method == "GET":
        context["form"] = UploadFileForm(request.POST, request.FILES, label_suffix='')
        return render(request, tpl, context)
    elif request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES, label_suffix='')
        if form.is_valid(request.user):
            f = form.save(request.user)
            return HttpResponse(f.id)
        else:
            return redirect('index')
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
    # Check password
    ok, val = check_pwd(request, fid, reverse('download', kwargs={ 'fid': fid}))
    if not ok:
        return val
    # Get the file description
    f = get_object_or_404(File, id=fid)
    # At this point, either the file is public or 
    # the correct password was provided
    if f.key is not None:
        # Set the password in context to pass it to get_file
        # view through GET parameter
        ctxt["key"] = val
    # Set file meta in context
    ctxt["f"] = f
    return render(request, tpl, ctxt)
    

@login_required(login_url="login")
def delete(request, fid):
    """
        Asynchronously delete a file.
        This view performs the permission verifications.

    """
    # Get the file description
    f = get_object_or_404(File, id=fid)
    if f.owner != request.user:
        return HttpResponse("KO")
    f.delete()
    # Response 
    return HttpResponse("OK")


def get_file(request, fid):
    """
        Handle file download. @param fid is the id of the file to
        be downloaded. If the file is protected, the password given 
        as POST or GET parameter is checked before returning the file.

    """
    # Check password
    ok, val = check_pwd(request, fid, reverse('get_file', kwargs={ 'fid': fid}))
    if not ok:
        return val
    # Get file description
    f = File.objects.get(id=fid)
    # Increase number of downloads
    f.nb_dl += 1
    f.save()
    # Send file
    content = ""
    if f.iv is not None:
        content = decrypt_file(f, request.GET["key"])
    else:
        with open(f.path, 'rb+') as fl:
            content = fl.read()
    response = HttpResponse(content_type=mimetypes.guess_type(f.title)[0], content=content)
    response['Content-Disposition'] = 'attachment; filename="%s"' % smart_str(f.title)
    response['Content-Length'] = f.size
    response.set_cookie(key="fileReady", value=1, path="/dl")
    # If the file has reached the max number of dl
    if f.nb_dl >= f.max_dl:
        # We delete it
        f.delete()
        pass
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
    perm_form = PermissionForm(request.POST or None, label_suffix='')
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


def size_available(request):
    if request.user.is_anonymous():
        return HttpResponse(settings.FILE_MAX_SIZE_ANONYMOUS)
    else:
        return HttpResponse(FSUser.objects.get(user=request.user).storage_left)

