from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader
from django.core.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.utils.safestring import mark_safe

from django.conf import settings

from .forms import *
from .models import *

def places(request):
    log = request.user.is_authenticated
    if not log:
        raise PermissionDenied

    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    context = {
        "Title":"Emplacements",
        "Username": request.user.first_name + ' ' + request.user.last_name,
        "Grade": "",
        'places': Place.objects.all(),
    }

    match(request.user.usertype):
        case CustomUser.STUDENT:
            context["Grade"] = "Élève"

        case CustomUser.TEACHER:
            context["Grade"] = "Enseignant"

        case CustomUser.ADMINISTRATIF:
            context["Grade"] = "Administratif"

    return render(request, "inventaire/places.html", context)

def newchild(request, id=None):
    return placeproperties(request, id=None, parent=id)

def newroot(request):
    return placeproperties(request, id=None, parent="")


def placeproperties(request, id=None, parent=""):
    log = request.user.is_authenticated
    if not log:
        raise PermissionDenied

    if id != None:
        data = Place.objects.get(pk=id)
        parent = None
        if (data.parent != None):
            parent = data.parent.id
        context = {
            'id': id,
            'designation': data.designation,
            'placetype': data.placetype,
            'lignes': data.lines,
            'colonnes': data.columns,
            'emplacements': data.subpositions,
            'parent': parent,
            'refname': data.referencename,
            'formprefix': 'u',
            'url': '/emplacements/update/'+str(id)+'/'
        }

    else:
        context = {
            'id': '',
            'designation': "",
            'placetype': "",
            'lignes': "",
            'colonnes': "",
            'emplacements': "",
            'parent': parent,
            'refname': "",
            'formprefix': 'n',
            'url': '/emplacements/add/'
        }
        if parent == "":
            context['formprefix']='r'

    return render(request, 'inventaire/placeform.html', context)


def placeupdate(request, id=None):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        raise PermissionDenied


    if request.method == 'POST':

        if(id == None and request.POST['parent'] != ""):
            values = request.POST.copy()
            if(request.POST['lignes'] == ''):
                values['lignes'] = None
            if(request.POST['colonnes'] == ''):
                values['colonnes'] = None
            if(request.POST['emplacement'] == ''):
                values['emplacement'] = None

            Place.objects.create(designation=values['designation'],
                                 lines=values['lignes'],
                                 columns=values['colonnes'],
                                 placetype=values['placetype'],
                                 subpositions=values['emplacement'],
                                 referencename=values['refname'],
                                 parent=Place.objects.get(pk=values['parent'])
                                 )
            return redirect('places')

        elif(id == None):
            values = request.POST.copy()
            if(request.POST['lignes'] == ''):
                values['lignes'] = None
            if(request.POST['colonnes'] == ''):
                values['colonnes'] = None
            if(request.POST['emplacement'] == ''):
                values['emplacement'] = None

            Place.objects.create(designation=values['designation'],
                                 lines=values['lignes'],
                                 columns=values['colonnes'],
                                 placetype=values['placetype'],
                                 subpositions=values['emplacement'],
                                 referencename=values['refname'],
                                 )
            return redirect('places')

        else:
            #return JsonResponse(request.POST, safe=False)
            item = get_object_or_404(Place, pk=id)
            item.designation = request.POST['designation']
            if request.POST['lignes'] == "":
                item.lines=None
            else:
                item.lines = request.POST['lignes']

            if request.POST['colonnes'] == "":
                item.columns=None
            else:
                item.columns = request.POST['colonnes']

            item.placetype=request.POST['placetype']

            if request.POST['emplacement'] == "":
                item.subpositions=None
            else:
                item.subpositions = request.POST['emplacement']
            item.referencename=request.POST['refname']
            if(request.POST['parent'] != 'None' and request.POST['parent'] != ''):
                item.parent=Place.objects.get(pk=request.POST['parent'])
            item.save()
            return redirect('places')
    else:
        raise PermissionDenied

    return HttpResponseBadRequest("Requête incorrecte")

def deletechild(request, id):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        raise PermissionDenied

    Place.objects.get(pk = id).delete()
    return HttpResponse("Suppression effectuée avec succès")

def tree(request):
    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    context = {
        'places': Place.objects.all(),
    }

    return render(request, "inventaire/tree.html", context)
