from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.core.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.utils.safestring import mark_safe

from django.conf import settings

from .forms import *
from .models import *

def home(request):
    log = request.user.is_authenticated
    if not log:
        context = {
                "Title":"Accueil",
                "Username": "",
                "Grade": "",
            }
    else:
        context = {
            "Title":"Accueil",
            "Username": request.user.first_name + ' ' + request.user.last_name,
            "Grade": "",
        }

        match(request.user.usertype):
            case CustomUser.STUDENT:
                context["Grade"] = "Élève"

            case CustomUser.TEACHER:
                context["Grade"] = "Enseignant"

            case CustomUser.ADMINISTRATIF:
                context["Grade"] = "Administratif"

    return render(request, "inventaire/home.html", context)

def components(request, page=1):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)
    nbitems = Item.objects.count();
    context = {
        "Title":"Composants",
        "Username": request.user.first_name + ' ' + request.user.last_name,
        "Grade": "",
        "ListItems": mark_safe(componentssearch(request, "", page).content.decode('utf-8')),
    }

    match(request.user.usertype):
        case CustomUser.STUDENT:
            context["Grade"] = "Élève"

        case CustomUser.TEACHER:
            context["Grade"] = "Enseignant"

        case CustomUser.ADMINISTRATIF:
            context["Grade"] = "Administratif"


    return render(request, "inventaire/components.html",context)


def componentssearch(request, search="", page=1):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    results = Item.objects.order_by("-pk").filter(Q(designation__icontains=search) | Q(description__icontains=search) | Q(idbarcodescanner__icontains=search))
    nbpage = (results.count()//100)+1
    context = {
        "ListItems": results[(page-1)*100:page*100],
        "page":{
            "current": page,
            "previous": max(page-1,1),
            "next":min(page+1,nbpage),
            "max":nbpage,
            "maxm1":nbpage-1},
        "FormulaireItem":ItemForm,
    }

    return render(request, "inventaire/component_list.html", context)


def itemproperty(request, id=None):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    itemform = ItemForm;
    if(id != None):
        data = Item.objects.get(pk=id)
        itemform = ItemForm(instance=data)
    context = {
        "FormulaireItem":itemform,
        "FormResponse":"",
        "exist":""
    }

    if id == None:
        context["FormResponse"]="/item/add/"
    else:
        context["FormResponse"]="/item/update/"+str(id)
        context["exist"]="True"

    return render(request, "inventaire/item.html", context)


def itemsave(request, id=None):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        raise PermissionDenied

    form=None
    item=None
    if request.method == 'POST':
        if(id == None):
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('components')
        else:
            item = Item.objects.get(pk=id)
            form = ItemForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                form.save()
                return redirect('components', (item.id//100)+1)
    else:
        raise PermissionDenied

    return HttpResponseBadRequest("Requête incorrecte")


"""

    Gestion des caractéristiques des items

"""
def itemcharacteristics(request, id):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")
    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    context = {
        "Characteristicsdata":Characteristics.objects.filter(itemid__pk = id)
    }

    return render(request, "inventaire/itemcharacteristics.html", context)

def itemcharacteristicsform(request, id, caractid = None):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        return HttpResponse("")

    if caractid == None:
        context = {
            "CharacteristicsForm":CharacteristicsForm({'itemid': id}),
            "id":""
        }
    else:
        data = Characteristics.objects.get(pk=caractid)
        context = {
            "CharacteristicsForm":CharacteristicsForm(instance=data),
            "id":caractid
        }

    return render(request, "inventaire/itemcharacteristicsform.html", context)

def itemcharacteristicsadd(request, id, caractid = None):
    log = request.user.is_authenticated
    if not log:
        raise PermissionDenied

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        raise PermissionDenied

    if request.method == 'POST':
        if(caractid == None):
            form = CharacteristicsForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse("Sauvegarde effectuée")
        else:
            item = Characteristics.objects.get(pk=caractid)
            form = CharacteristicsForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return HttpResponse("Sauvegarde effectuée")

        return HttpResponse("Une erreur d'enregistrement est survenue")



def itemcharacteristicsdelete(request, id, caractid):
    log = request.user.is_authenticated
    if not log:
        raise PermissionDenied

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        raise PermissionDenied

    if request.method == 'POST':
        Characteristics.objects.get(pk = caractid).delete()
        return HttpResponse("Suppression effectuée avec succès")

    return HttpResponse("Echec de la suppression")




"""

    Gestion des ressources des items

"""
def itemressources(request, id):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    context = {
        "RessourcesData":ItemRessource.objects.filter(itemid__pk = id)
    }

    return render(request, "inventaire/itemressources.html", context)

def itemressourcesform(request, id, caractid = None):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        return HttpResponse("")

    if caractid == None:
        context = {
            "RessourcesForm":RessourcesForm({'itemid': id}),
            "id":""
        }
    else:
        data = ItemRessource.objects.get(pk=caractid)
        context = {
            "RessourcesForm":RessourcesForm(instance=data),
            "id":caractid
        }

    return render(request, "inventaire/itemressourcesform.html", context)

def itemressourcesadd(request, id, caractid = None):
    log = request.user.is_authenticated
    if not log:
        raise PermissionDenied

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        raise PermissionDenied

    if request.method == 'POST':
        if(caractid == None):
            form = RessourcesForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponse("Sauvegarde effectuée")
        else:
            item = ItemRessource.objects.get(pk=caractid)
            form = RessourcesForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                form.save()
                return HttpResponse("Sauvegarde effectuée")

        return HttpResponse("Une erreur d'enregistrement est survenue")



def itemressourcesdelete(request, id, caractid):
    log = request.user.is_authenticated
    if not log:
        raise PermissionDenied

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        raise PermissionDenied

    if request.method == 'POST':
        ItemRessource.objects.get(pk = caractid).delete()
        return HttpResponse("Suppression effectuée avec succès")

    return HttpResponse("Echec de la suppression")


def itemdelete(request, id):
    log = request.user.is_authenticated
    if not log:
        raise PermissionDenied

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        raise PermissionDenied

    Item.objects.get(pk = id).delete()
    return HttpResponse("Suppression effectuée avec succès")



"""

    Gestion des prix fournisseurs

"""
def itemprice(request, id):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    context = {
        "SupplierPriceData":ItemSuppliers.objects.filter(itemid__pk = id)
    }

    return render(request, "inventaire/itemprice.html", context)

def itempriceform(request, id, priceid = None):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        return HttpResponse("")

    if priceid == None:
        context = {
            "PriceForm":PriceForm({'itemid': id}),
            "id":""
        }
    else:
        data = ItemSuppliers.objects.get(pk=priceid)
        context = {
            "PriceForm":PriceForm(instance=data),
            "id":priceid
        }

    return render(request, "inventaire/itempriceform.html", context)

def itempriceadd(request, id, priceid = None):
    log = request.user.is_authenticated
    if not log:
        raise PermissionDenied

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        raise PermissionDenied

    if request.method == 'POST':
        if(priceid == None):
            form = PriceForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse("Sauvegarde effectuée")
        else:
            item = ItemSuppliers.objects.get(pk=priceid)
            form = PriceForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return HttpResponse("Sauvegarde effectuée")

        return HttpResponse("Une erreur d'enregistrement est survenue")



def itempricedelete(request, id, priceid):
    log = request.user.is_authenticated
    if not log:
        raise PermissionDenied

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        raise PermissionDenied

    if request.method == 'POST':
        ItemSuppliers.objects.get(pk = priceid).delete()
        return HttpResponse("Suppression effectuée avec succès")

    return HttpResponse("Echec de la suppression")


def itemdelete(request, id):
    log = request.user.is_authenticated
    if not log:
        raise PermissionDenied

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        raise PermissionDenied

    Item.objects.get(pk = id).delete()
    return HttpResponse("Suppression effectuée avec succès")



def seConnecter(request):
    if request.method == "POST":
        try:
            user = authenticate(username=request.POST["login"], password=request.POST["password"])
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                return redirect("/login/")
        except KeyError:
            return HttpResponse("Données invalides fournies")

    else:
        context = {
            'LoginForm': loginForm(),
            "Title":"Se connecter",
        }
        if request.method =="GET" and "msg" in request.GET:
            context["Message"] = request.GET["msg"]
        return render(request, "inventaire/login.html", context)

def seDeconnecter(request):
    logout(request)
    return redirect("/")
