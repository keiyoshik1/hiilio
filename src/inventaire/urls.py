from django.urls import path
from . import views, viewssuppliers, viewsplace, viewsuser, viewrental

urlpatterns = [
    #homepage
    path('', views.home, name="home"),
    path('composants/', views.components, name="components"),
    path('composants/list/<int:page>/', views.components, name="components"),

    # Barre de recherche
    path('composants/search/', views.componentssearch, name="componentssearch"),
    path('composants/search/<str:search>/', views.componentssearch, name="componentssearch"),
    path('composants/search/<str:search>/<int:page>/', views.componentssearch, name="componentssearch"),

    #Configuration des items
    path('item/new/', views.itemproperty, name="itemproperty"),
    path('item/<int:id>/', views.itemproperty, name="itemproperty"),
    path('item/add/', views.itemsave, name="itemadd"),
    path('item/update/<int:id>', views.itemsave, name="itemupdate"),
    path('item/remove/<int:id>', views.itemdelete, name="itemdelete"),

    #Caractéristiques des items
    path('item/<int:id>/caracteristiques', views.itemcharacteristics, name="itemcaract"),
    path('item/<int:id>/caracteristiques/form/', views.itemcharacteristicsform, name="itemcaractform"),
    path('item/<int:id>/caracteristiques/form/<int:caractid>', views.itemcharacteristicsform, name="itemcaractform"),
    path('item/<int:id>/caracteristiques/add/', views.itemcharacteristicsadd, name="itemcharactadd"),
    path('item/<int:id>/caracteristiques/update/<int:caractid>', views.itemcharacteristicsadd, name="itemcharactadd"),
    path('item/<int:id>/caracteristiques/delete/<int:caractid>', views.itemcharacteristicsdelete, name="itemproperty"),

    #Ressources des items
    path('item/<int:id>/ressources', views.itemressources, name="itemcaract"),
    path('item/<int:id>/ressources/form/', views.itemressourcesform, name="itemcaractform"),
    path('item/<int:id>/ressources/form/<int:caractid>', views.itemressourcesform, name="itemcaractform"),
    path('item/<int:id>/ressources/add/', views.itemressourcesadd, name="itemcharactadd"),
    path('item/<int:id>/ressources/update/<int:caractid>', views.itemressourcesadd, name="itemcharactadd"),
    path('item/<int:id>/ressources/delete/<int:caractid>', views.itemressourcesdelete, name="itemproperty"),

    #Fournisseurs
    path('fournisseurs/', viewssuppliers.suppliers, name="suppliers"),
    path('fournisseurs/list/<int:page>/', viewssuppliers.suppliers, name="suppliers"),
    path('fournisseur/new/', viewssuppliers.supplier, name="supplierproperty"),
    path('fournisseur/<int:id>/', viewssuppliers.supplier, name="supplierproperty"),
    path('fournisseur/add/', viewssuppliers.suppliersave, name="suplierupdate"),
    path('fournisseur/update/<int:id>', viewssuppliers.suppliersave, name="supplierupdate"),
    path('fournisseur/remove/<int:id>', viewssuppliers.supplierdelete, name="supplierdelete"),

    # Barre de recherche
    path('fournisseurs/search/', viewssuppliers.supplierssearch, name="supplierssearch"),
    path('fournisseurs/search/<str:search>/', viewssuppliers.supplierssearch, name="supplierssearch"),
    path('fournisseurs/search/<str:search>/<int:page>/', viewssuppliers.supplierssearch, name="supplierssearch"),

    #Tarifs fournisseurs
    path('item/<int:id>/prix', views.itemprice, name="itemprix"),
    path('item/<int:id>/prix/form/', views.itempriceform, name="itemprixform"),
    path('item/<int:id>/prix/form/<int:priceid>', views.itempriceform, name="itemprixform"),
    path('item/<int:id>/prix/add/', views.itempriceadd, name="itemprixadd"),
    path('item/<int:id>/prix/update/<int:priceid>', views.itempriceadd, name="itemprixadd"),
    path('item/<int:id>/prix/delete/<int:priceid>', views.itempricedelete, name="itemprixdelete"),

    #Emplacements
    path('emplacements/', viewsplace.places, name="places"),
    path('emplacements/list', viewsplace.tree, name="placestree"),
    path('emplacements/racine/ajouter/', viewsplace.newroot, name="newroot"),
    path('emplacements/<int:id>/modifier/', viewsplace.placeproperties, name="placeproperties"),
    path('emplacements/<int:id>/ajouter/', viewsplace.newchild, name="newchild"),
    path('emplacements/update/<int:id>/', viewsplace.placeupdate, name="placeupdate"),
    path('emplacements/add/', viewsplace.placeupdate, name="placeupdate"),
    path('emplacements/<int:id>/supprimer/', viewsplace.deletechild, name="deletechild"),

    #Utilisateurs
    path('utilisateurs/', viewsuser.users, name="users"),
    path('utilisateurs/list/<int:page>/', viewsuser.users, name="users"),
    path('utilisateurs/new/', viewsuser.user, name="userproperty"),
    path('utilisateurs/<int:id>/', viewsuser.user, name="userproperty"),
    path('utilisateurs/add/', viewsuser.usersave, name="userupdate"),
    path('utilisateurs/update/<int:id>', viewsuser.usersave, name="usersave"),
    path('utilisateurs/remove/<int:id>', viewsuser.userdelete, name="userdelete"),

    # Barre de recherche
    path('utilisateurs/search/', viewsuser.userssearch, name="userssearch"),
    path('utilisateurs/search/<str:search>/', viewsuser.userssearch, name="userssearch"),
    path('utilisateurs/search/<str:search>/<int:page>/', viewsuser.userssearch, name="userssearch"),

    #Emprunts
    path('emprunter/', viewrental.rental, name="rent"),
    path('emprunter/chercherutilisateur/', viewrental.rentuserlist, name="rentuserlist"),
    path('emprunter/chercherutilisateur/<str:search>', viewrental.rentuserlist, name="rentuserlist"),
    path('emprunter/chercherutilisateur/id/<int:userid>', viewrental.rentuser, name="rentuserlist"),
    path('emprunter/composants/search/', viewrental.searchcomponent, name="rentcomponentfind"),
    path('emprunter/composants/search/<str:search>', viewrental.searchcomponent, name="rentcomponentfind"),
    path('emprunter/creer/', viewrental.create, name="create"),
    path('emprunter/update/', viewrental.update, name="update"),
    path('emprunter/liste/', viewrental.listrent, name="listrent"),
    path('emprunter/liste/<int:page>', viewrental.listrent, name="listrent"),
    path('emprunter/liste/search/', viewrental.rentsearch, name="listrentsearch"),
    path('emprunter/liste/search/<str:search>', viewrental.rentsearch, name="listrentsearch"),
    path('emprunter/details/<int:id>', viewrental.rentdetail, name="rentdetail"),

    # Authentification
    path('login/', views.seConnecter, name="connexion"),
    path('logout/', views.seDeconnecter, name="deconnexion"), #Need an update
]
