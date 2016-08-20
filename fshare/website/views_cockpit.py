
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test 

from website.management.commands.generate_registration_key import Command as GenerateRegistrationKey
from website.views_user import is_admin
from website.models import Permission, RegistrationKey
from website.forms import PermissionForm

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

