from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.template import loader
from django.core.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.utils.safestring import mark_safe

from django.conf import settings

from .forms import *
from .models import *

def suppliers(request, page=1):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    nbitems = Item.objects.count();
    context = {
        "Title":"Fournisseurs",
        "Username": request.user.first_name + ' ' + request.user.last_name,
        "Grade": "",
        "ListSuppliers": mark_safe(supplierssearch(request, "", page).content.decode('utf-8')),
    }

    match(request.user.usertype):
        case CustomUser.STUDENT:
            context["Grade"] = "Élève"

        case CustomUser.TEACHER:
            context["Grade"] = "Enseignant"

        case CustomUser.ADMINISTRATIF:
            context["Grade"] = "Administratif"


    return render(request, "inventaire/suppliers.html",context)



def supplierssearch(request, search="", page=1):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    results = Suppliers.objects.order_by("-pk").filter(Q(email__icontains=search) | Q(name__icontains=search) | Q(website__icontains=search))
    nbpage = (results.count()//100)+1
    context = {
        "ListSuppliers": results[(page-1)*100:page*100],
        "page":{
            "current": page,
            "previous": max(page-1,1),
            "next":min(page+1,nbpage),
            "max":nbpage,
            "maxm1":nbpage-1},
        "FormulaireSupplier":SupplierForm,
    }

    return render(request, "inventaire/suppliers_list.html", context)


def supplier(request, id=None):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    supplierform = SupplierForm
    if(id != None):
        data = Suppliers.objects.get(pk=id)
        supplierform = SupplierForm(instance=data)
    context = {
        "FormulaireItem":supplierform,
        "FormResponse":"",
        "exist":"",
        "id":""
    }

    if id == None:
        context["FormResponse"]="/fournisseur/add/"
    else:
        context["FormResponse"]="/fournisseur/update/"+str(id)
        context["exist"]="True"
        context["id"]=id

    return render(request, "inventaire/supplierform.html", context)


def suppliersave(request, id=None):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        raise PermissionDenied

    form=None
    item=None
    if request.method == 'POST':
        if(id == None):
            form = SupplierForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('suppliers')
        else:
            item = Suppliers.objects.get(pk=id)
            form = SupplierForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return redirect('suppliers', (item.id//100)+1)
    else:
        raise PermissionDenied

    return HttpResponseBadRequest("Requête incorrecte")


def supplierdelete(request, id):
    log = request.user.is_authenticated
    if not log:
        raise PermissionDenied

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        raise PermissionDenied

    Suppliers.objects.get(pk = id).delete()
    return HttpResponse("Suppression effectuée avec succès")


