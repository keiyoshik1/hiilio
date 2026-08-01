from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.hashers import check_password

from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.utils.safestring import mark_safe

from django.conf import settings

from .forms import *
from .models import *
import time
from datetime import datetime

import json

def rental(request, page=1):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    context = {
        "Title":"Emprunter",
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

    print(request.user.usertype)
    if(request.user.usertype == 1):
        pass

    if(request.user.usertype == 2 or request.user.usertype == 3):
        pass


    if(request.user.usertype < 1 or request.user.usertype >= 4):
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous n'avez pas les droits nécessaires pour accéder à cette ressource.")

    return render(request, "inventaire/rent.html",context)

def rentuserlist(request, search=""):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    result = None
    if CustomUser.objects.filter(cardid=search).exists():
        result = CustomUser.objects.get(cardid=search)
        return JsonResponse({"type":"Unique",
                             "user":getUser(result.pk)
                             })
    else:
        result = CustomUser.objects.order_by("last_name", "first_name").filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(username__icontains=search) | Q(email__icontains=search) | Q(cardid__icontains=search))[:5]
        ret = {"type":"Multiple","values":[]}
        for res in result:
            ret["values"].append(getUser(res.pk))
    return JsonResponse(ret)
    
def getUser(userid):
    if CustomUser.objects.filter(pk=userid).exists():
        result = CustomUser.objects.get(pk=userid)
        return {
                "id":result.pk,
                "first_name":result.first_name,
                "last_name":result.last_name,
                "e-mail":result.email,
                "phone":result.phone,
                "cardid":result.cardid,
                "username":result.username,
                "usertype":result.usertype,
                "NTE":Rental.objects.filter(userid=result).count(),
                "NEC":Rental.objects.filter(userid=result).filter(closestatus="ATTENTE").count(),
                "NER":Rental.objects.filter(userid=result).filter(closestatus="ATTENTE").filter(returndate__lt=datetime.now()).count(),
                "NRD":Rental.objects.filter(userid=result).filter(closestatus="CASSE").count(),
                "NNR":Rental.objects.filter(userid=result).filter(closestatus="FACTURE").count(),
            }
    else:
        return {}



def rentuser(request, userid):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    return JsonResponse(getUser(userid))


def searchcomponent(request, search=""):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    results = Item.objects.order_by("-pk").filter(Q(designation__icontains=search) | Q(description__icontains=search) | Q(idbarcodescanner__icontains=search))
    context = {
        "ListItems": results[:100],
    }

    return render(request, "inventaire/rentcomponentlist.html", context)

def create(request):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    data = json.loads(request.POST["json"])

    if(check_password(data["validator"]["password"], CustomUser.objects.get(pk=data["validator"]["id"]).password)):
        rent = Rental(userid=CustomUser.objects.get(pk=data["rentUser"]), renterid=CustomUser.objects.get(pk=data["validator"]["id"]),
                    returndate=data["rentDate"], comment=data["rentplace"])
        rent.save()

        for item in data["rentitems"]:
            record = RentalItem(rentalid=rent, itemid=Item.objects.get(pk=item["id"]), quantity=item["quantity"])
            record.save()

    else:
        time.sleep(2)
        return HttpResponse(""" <div class="alert alert-danger alert-dismissible fade show" role="alert">
                                <strong>Mot de passe invalide</strong>
                                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fermer"></button>
                                </div>""")

    return HttpResponse("Done")

def listrent(request, page=1):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous n'avez pas les droits nécessaires pour accéder à cette ressource.")
        
    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    nbitems = Rental.objects.count();
    context = {
        "Title":"Emprunts",
        "Username": request.user.first_name + ' ' + request.user.last_name,
        "Grade": "",
        "ListRent": mark_safe(rentsearch(request, "", page).content.decode('utf-8')),
    }

    match(request.user.usertype):
        case CustomUser.STUDENT:
            context["Grade"] = "Élève"

        case CustomUser.TEACHER:
            context["Grade"] = "Enseignant"

        case CustomUser.ADMINISTRATIF:
            context["Grade"] = "Administratif"


    return render(request, "inventaire/rent_page.html",context)


def rentsearch(request, search="", page=1):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous n'avez pas les droits nécessaires pour accéder à cette ressource.")

    results = Rental.objects.order_by("closestatus","-returndate").filter(Q(userid__first_name__icontains=search) | Q(userid__last_name__icontains=search) | 
                                                                        Q(userid__username__icontains=search) | Q(userid__email__icontains=search) | 
                                                                        Q(userid__cardid__icontains=search) | Q(comment__icontains=search))
    nbpage = (results.count()//100)+1
    context = {
        "ListRent": results[(page-1)*100:page*100],
        "page":{
            "current": page,
            "previous": max(page-1,1),
            "next":min(page+1,nbpage),
            "max":nbpage,
            "maxm1":nbpage-1},
    }

    return render(request, "inventaire/rentlist.html", context)

def rentdetail(request, id):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous n'avez pas les droits nécessaires pour accéder à cette ressource.")

    items = RentalItem.objects.filter(rentalid=Rental.objects.get(pk=id)).order_by("itemid__designation")
    items_to_send={
        "user":{
            "first_name":items[0].rentalid.userid.first_name,
            "last_name":items[0].rentalid.userid.last_name,
        },
        "rent":items[0].rentalid.pk,
        "items":[],
    }

    for item in items:
        items_to_send["items"].append({
            "id": item.pk,
            "iditem": item.itemid.pk,
            "designation": item.itemid.designation,
            "quantity": item.quantity,
            "returned_quantity":item.returnedquantity,
            "returned_date": item.returndate,
            "lost_quantity": item.lostquantity,
        })
    return JsonResponse(items_to_send)

def update(request):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous n'avez pas les droits nécessaires pour accéder à cette ressource.")

    data = json.loads(request.POST["json"])

    try:
        rent = Rental.objects.get(pk=data["rent"])
        if(data["status"] != "ATTENTE"):
            rent.closedate = datetime.now()
        rent.closestatus = data["status"]
        rent.save()

        for item in data["items"]:
            ref = RentalItem.objects.get(pk=item["id"])
            if(ref.lostquantity == None):
                ref.lostquantity = 0
            
            if(ref.lostquantity != item["loosed"]):
                diff = ref.lostquantity - item["loosed"]
                ressource = Item.objects.get(pk = ref.itemid.pk)
                ressource.quantity += diff
                print(ressource.quantity)
                ressource.save()

            ref.lostquantity = item["loosed"]
            ref.returnedquantity = item["returned"]

            if(ref.returnedquantity + ref.lostquantity == ref.quantity):
                ref.returndate = datetime.now()

            ref.save()

        return HttpResponse("Done")
    except:
        return HttpResponse(""" <div class="alert alert-danger alert-dismissible fade show" role="alert">
                                        <strong>Une erreur est survenue, merci de réessayer plus tard</strong>
                                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fermer"></button>
                                        </div>""")

    
