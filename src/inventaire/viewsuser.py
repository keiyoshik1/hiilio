from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.template import loader
from django.core.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.utils.safestring import mark_safe

from django.conf import settings

from .forms import *
from .models import *

def users(request, page=1):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous n'avez pas les droits nécessaires pour accéder à cette ressource.")
        
    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    nbitems = Item.objects.count();
    context = {
        "Title":"Utilisateurs",
        "Username": request.user.first_name + ' ' + request.user.last_name,
        "Grade": "",
        "ListUsers": mark_safe(userssearch(request, "", page).content.decode('utf-8')),
    }

    match(request.user.usertype):
        case CustomUser.STUDENT:
            context["Grade"] = "Élève"

        case CustomUser.TEACHER:
            context["Grade"] = "Enseignant"

        case CustomUser.ADMINISTRATIF:
            context["Grade"] = "Administratif"


    return render(request, "inventaire/users.html",context)


def userssearch(request, search="", page=1):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    results = CustomUser.objects.order_by("-pk").filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(username__icontains=search) | Q(email__icontains=search) | Q(cardid__icontains=search))
    nbpage = (results.count()//100)+1
    context = {
        "ListUsers": results[(page-1)*100:page*100],
        "page":{
            "current": page,
            "previous": max(page-1,1),
            "next":min(page+1,nbpage),
            "max":nbpage,
            "maxm1":nbpage-1},
        "FormulaireSupplier":CustomUserForm,
    }

    return render(request, "inventaire/users_list.html", context)


def user(request, id=None):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    userform = CustomUserForm
    if(id != None):
        data = CustomUser.objects.get(pk=id)
        userform = CustomUserForm(instance=data)
    context = {
        "FormulaireItem":userform,
        "FormResponse":"",
        "exist":"",
        "id":""
    }

    if id == None:
        context["FormResponse"]="/utilisateurs/add/"
    else:
        context["FormResponse"]="/utilisateurs/update/"+str(id)
        context["exist"]="True"
        context["id"]=id

    return render(request, "inventaire/userform.html", context)


def usersave(request, id=None):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        raise PermissionDenied

    form=None
    item=None
    if request.method == 'POST':
        if(id == None):
            form = CustomUserForm(request.POST)
            if form.is_valid():
                user = CustomUser.objects.create_user(form.cleaned_data["username"], form.cleaned_data['email'], form.cleaned_data["password"])
                user.first_name = form.cleaned_data["first_name"]
                user.last_name = form.cleaned_data["last_name"]
                user.cardid = form.cleaned_data["cardid"]
                user.usertype = form.cleaned_data["usertype"]
                user.gender = form.cleaned_data["gender"]
                user.phone = form.cleaned_data["phone"]
                user.save()
                return redirect('users')
        else:
            item = CustomUser.objects.get(pk=id)
            npass = None
            if("password" in request.POST and item.password != request.POST["password"]):
                npass = request.POST["password"]

            form = CustomUserForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                if npass != None:
                    item = CustomUser.objects.get(pk=id)
                    item.set_password(npass)
                    item.save()
                return redirect('users', (item.id//100)+1)
    else:
        raise PermissionDenied

    return HttpResponseBadRequest("Requête incorrecte")


def userdelete(request, id):
    log = request.user.is_authenticated
    if not log:
        raise PermissionDenied

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        raise PermissionDenied

    CustomUser.objects.get(pk = id).delete()
    return HttpResponse("Suppression effectuée avec succès")


