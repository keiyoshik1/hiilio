let LAST_SELECTED = "";
let LAST_SELECTED_CARAC = "";
let LAST_SELECTED_RES = "";
let LAST_SELECTED_PRICE = "";


/*
 * Gestion de la partie barre de recherche et table des composants
 */

const button = document.getElementById("searchbarbutton");
const textinput = document.getElementById("searchbar");

button.addEventListener("click", (event) => {
    getTable();
});

textinput.addEventListener("keypress", (event) => {
    if(event.key == "Enter"){getTable();}
});

function getTable()
{
    let LAST_SELECTED = ""
    search = document.getElementById('searchbar');
    fetch('/composants/search/'+search.value)
    .then(reponse => reponse.text())
    .then(data => {
        place = document.getElementById("itemstable");
        place.innerHTML = data;
    });
    inittable();
}

function inittable()
{
    let LAST_SELECTED = ""
    tableData = document.querySelectorAll("tr.tr-table");
    tableData.forEach(
        function (item) {
            item.addEventListener("click", (event) => {
                if(LAST_SELECTED != "")
                {
                    document.getElementById(LAST_SELECTED).classList.remove('table-primary');
                }
                document.getElementById(item.id).classList.add("table-primary");
                LAST_SELECTED = item.id;
                getForm(item.getAttribute('aria-id'));
            });
        });

    createForm = document.getElementById("addnewbutton");
    createForm.addEventListener("click", (event) => {
        getForm();
        data = '<div class="alert alert-primary" role="alert">Rien à afficher pour le moment</div>'
        document.getElementById("caractform").innerHTML = data;
        document.getElementById("caractdata").innerHTML = data;
        document.getElementById("ressourceform").innerHTML = data;
        document.getElementById("ressourcedata").innerHTML = data;
        document.getElementById("priceform").innerHTML = data;
        document.getElementById("pricedata").innerHTML = data;
    });
}

inittable();


function getForm(id=null)
{
    if(id!=null)
    {
        fetch('/item/'+id)
        .then(reponse => reponse.text())
        .then(data => {
            place = document.getElementById("item");
            place.innerHTML = data;
        })
        .then(data => {
            function updatebutton(event)
            {
                event.preventDefault();
                fetch('/item/remove/'+id)
                .then(reponse => reponse.text())
                .then(data => {
                    console.log(data);
                    getTable();
                    getForm();
                });
            }

            const formdelete = document.getElementById("supformdel");
            console.log(formdelete);
            formdelete.addEventListener("click", (event) => {
                updatebutton(event);
            });
            formdelete.addEventListener("keypress", (event) => {
                if(event.key == "Enter"){updatebutton(event);}
            });
        });
        getTableCaract(id);
        getFormCaract(id);
        getTableRessource(id);
        getFormRessource(id);
        getTablePrice(id);
        getFormPrice(id);
    }
    else
    {
        fetch('/item/new')
        .then(reponse => reponse.text())
        .then(data => {
            place = document.getElementById("item");
            place.innerHTML = data;
        });
    }
}

function getFormCaract(id, idcaract="")
{
    fetch('/item/'+id+'/caracteristiques/form/'+idcaract)
    .then(reponse => reponse.text())
    .then(data => {
        place = document.getElementById("caractform");
        place.innerHTML = data;
    })
    .then(nothing => {
        //Init button work

        /*
         * Configuration du bouton d'enregistrement
         */
        function save(event)
        {
            if( document.getElementById("id_name").value != "" &&
                document.getElementById("id_unit").value != "" &&
                document.getElementById("id_value").value != ""
            )
            {
                event.preventDefault();
                let formData = new FormData();
                formData.append('name', document.getElementById("id_name").value);
                formData.append('value', document.getElementById("id_value").value);
                formData.append('unit', document.getElementById("id_unit").value);
                formData.append('itemid', document.getElementById("id_itemid").value);
                formData.append('csrfmiddlewaretoken',document.querySelector('.caractform [name=csrfmiddlewaretoken]').value)

                    let url = "";
                if(document.getElementById("caractformrefid").value == "")
                {
                    url = '/item/'+id+'/caracteristiques/add/';
                }
                else
                {
                    url = '/item/'+id+'/caracteristiques/update/'+document.getElementById("caractformrefid").value
                }

                fetch(url, {
                    method: "POST",
                    body: formData,
                    headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                })
                .then(reponse => reponse.text())
                .then(data => {
                    console.log(data);
                    getTableCaract(id);
                    getFormCaract(id);
                })
            }
        }
        caractbutton = document.getElementById("caractsave");
        caractbutton.addEventListener("click", (event) => save(event));
        caractbutton.addEventListener("keypress", (event) => {
            if(event.key == "Enter"){save(event);}
        });

        /*
         * Configuration du bouton de reset
         */
        function reset(event)
        {
            document.getElementById("id_name").value = "";
            document.getElementById("id_unit").value = "";
            document.getElementById("id_value").value = "";
            document.getElementById("caractformrefid").value = "";
            event.preventDefault();
        }

        caractbutton = document.getElementById("caractreset")
        caractbutton.addEventListener("click", (event) => reset(event));
        caractbutton.addEventListener("keypress", (event) => {
            if(event.key == "Enter"){reset(event);}
        });

        /*
         * Configuration du bouton de suppression
         */
        function del(event)
        {
            event.preventDefault();

            if( document.getElementById("caractformrefid").value != "")
            {
                let formData = new FormData();
                formData.append('caractformrefid', document.getElementById("caractformrefid").value);
                formData.append('csrfmiddlewaretoken',document.querySelector('[name=csrfmiddlewaretoken]').value)

                fetch('/item/'+id+'/caracteristiques/delete/'+document.getElementById("caractformrefid").value, {
                    method: "POST",
                    body: formData,
                    headers: {'X-CSRFToken': document.querySelector('.caracform [name=csrfmiddlewaretoken]').value}
                })
                .then(reponse => reponse.text())
                .then(data => {
                    console.log(data);
                    getTableCaract(id);
                    getFormCaract(id);
                })
            }
        }
        caractbutton = document.getElementById("caractdelete")
        caractbutton.addEventListener("click", (event) => del(event));
        caractbutton.addEventListener("keypress", (event) => {
            if(event.key == "Enter"){del(event);}
        });
    });
}

function getTableCaract(id)
{
    LAST_SELECTED_CARAC = "";
    fetch('/item/'+id+'/caracteristiques')
    .then(reponse => reponse.text())
    .then(data => {
        place = document.getElementById("caractdata");
        place.innerHTML = data;
    })
    .then(data => {
        tableData = document.querySelectorAll("tr.tr-table-carac");
        tableData.forEach(
            function (item) {
                item.addEventListener("click", (event) => {
                    if(LAST_SELECTED_CARAC != "")
                    {
                        document.getElementById(LAST_SELECTED_CARAC).classList.remove('table-primary');
                    }
                    document.getElementById(item.id).classList.add("table-primary");
                    LAST_SELECTED_CARAC = item.id;
                    getFormCaract(id, item.getAttribute('aria-id'));
                });
            });

    });
}







function getFormRessource(id, idcaract="")
{
    fetch('/item/'+id+'/ressources/form/'+idcaract)
    .then(reponse => reponse.text())
    .then(data => {
        place = document.getElementById("ressourceform");
        place.innerHTML = data;
    })
    .then(nothing => {
        /*
         * Configuration du bouton d'enregistrement
         */
        function save(event)
        {
            if( document.getElementById("id_ressourcename").value != "" &&
                document.getElementById("id_ressourcetype").value != "" &&
                    (document.getElementById("id_ressourceurl").value != "" ||
                     document.getElementById("id_ressourcefile").value != "")
            )
            {
                event.preventDefault();
                let formData = new FormData();
                formData.append('ressourcename', document.getElementById("id_ressourcename").value);
                formData.append('ressourcetype', document.getElementById("id_ressourcetype").value);
                formData.append('ressourceurl', document.getElementById("id_ressourceurl").value);
                formData.append('ressourcefile', document.getElementById("id_ressourcefile").files[0]);
                formData.append('itemid', document.getElementById("id_itemid").value);
                formData.append('csrfmiddlewaretoken',document.querySelector('.resform [name=csrfmiddlewaretoken]').value)

                console.log(formData);

                    let url = "";
                if(document.getElementById("resformrefid").value == "")
                {
                    url = '/item/'+id+'/ressources/add/';
                }
                else
                {
                    url = '/item/'+id+'/ressources/update/'+document.getElementById("resformrefid").value
                }

                fetch(url, {
                    method: "POST",
                    body: formData,
                    headers: {'X-CSRFToken': document.querySelector('.resform [name=csrfmiddlewaretoken]').value,
                        //'Content-Type':'multipart/form-data; boundary=' + document.querySelector('.resform [name=csrfmiddlewaretoken]').value
                    },
                    //processData: false,//ne pas oublier cette option
                    //contentType: false
                })
                .then(reponse => reponse.text())
                .then(data => {
                    console.log(data);
                    getTableRessource(id);
                    getFormRessource(id);
                })
            }
        }
        caractbutton = document.getElementById("ressave");
        caractbutton.addEventListener("click", (event) => save(event));
        caractbutton.addEventListener("keypress", (event) => {
            if(event.key == "Enter"){save(event);}
        });

        /*
         * Configuration du bouton de reset
         */
        function reset(event)
        {
            event.preventDefault();
            getFormRessource(id);
        }

        caractbutton = document.getElementById("resreset")
        caractbutton.addEventListener("click", (event) => reset(event));
        caractbutton.addEventListener("keypress", (event) => {
            if(event.key == "Enter"){reset(event);}
        });

        /*
         * Configuration du bouton de suppression
         */
        function del(event)
        {
            event.preventDefault();

            if( document.getElementById("resformrefid").value != "")
            {
                let formData = new FormData();
                formData.append('resformrefid', document.getElementById("resformrefid").value);
                formData.append('csrfmiddlewaretoken',document.querySelector('[name=csrfmiddlewaretoken]').value)

                    fetch('/item/'+id+'/ressources/delete/'+document.getElementById("resformrefid").value, {
                        method: "POST",
                        body: formData,
                        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                    })
                    .then(reponse => reponse.text())
                    .then(data => {
                        console.log(data);
                        getTableRessource(id);
                        getFormRessource(id);
                    })
            }
        }
        caractbutton = document.getElementById("resdelete")
        caractbutton.addEventListener("click", (event) => del(event));
        caractbutton.addEventListener("keypress", (event) => {
            if(event.key == "Enter"){del(event);}
        });
    });
}

function getTableRessource(id)
{
    LAST_SELECTED_RES = "";
    fetch('/item/'+id+'/ressources')
    .then(reponse => reponse.text())
    .then(data => {
        place = document.getElementById("ressourcedata");
        place.innerHTML = data;
    })
    .then(data => {
        tableData = document.querySelectorAll("tr.tr-table-res");
        tableData.forEach(
            function (item) {
                item.addEventListener("click", (event) => {
                    if(LAST_SELECTED_RES != "")
                    {
                        document.getElementById(LAST_SELECTED_RES).classList.remove('table-primary');
                    }
                    document.getElementById(item.id).classList.add("table-primary");
                    LAST_SELECTED_RES = item.id;
                    getFormRessource(id, item.getAttribute('aria-id'));
                });
            });

    });
}








function getFormPrice(id, idprice="")
{
    fetch('/item/'+id+'/prix/form/'+idprice)
    .then(reponse => reponse.text())
    .then(data => {
        place = document.getElementById("priceform");
        place.innerHTML = data;
    })
    .then(nothing => {
        /*
         * Configuration du bouton d'enregistrement
         */
        function save(event)
        {
            if( document.getElementById("id_lastprice").value != "" &&
                document.getElementById("id_supplierid").value != "" &&
                document.getElementById("id_taxes").value != "" &&
                document.getElementById("id_supplierreference").value != ""
            )
            {
                event.preventDefault();
                let formData = new FormData();
                formData.append('lastprice', document.getElementById("id_lastprice").value);
                formData.append('supplierid', document.getElementById("id_supplierid").value);
                formData.append('taxes', document.getElementById("id_taxes").value);
                formData.append('supplierreference', document.getElementById("id_supplierreference").value);
                formData.append('itemid', document.getElementById("id_itemid").value);
                formData.append('csrfmiddlewaretoken',document.querySelector('.priceform [name=csrfmiddlewaretoken]').value)

                let url = "";
                if(document.getElementById("priceformrefid").value == "")
                {
                    url = '/item/'+id+'/prix/add/';
                }
                else
                {
                    url = '/item/'+id+'/prix/update/'+document.getElementById("priceformrefid").value
                }

                fetch(url, {
                    method: "POST",
                    body: formData,
                    headers: {'X-CSRFToken': document.querySelector('.priceform [name=csrfmiddlewaretoken]').value,

                    },
                })
                .then(reponse => reponse.text())
                .then(data => {
                    console.log(data);
                    getTablePrice(id);
                    getFormPrice(id);
                })
            }
        }
        caractbutton = document.getElementById("pricesave");
        caractbutton.addEventListener("click", (event) => save(event));
        caractbutton.addEventListener("keypress", (event) => {
            if(event.key == "Enter"){save(event);}
        });

        /*
         * Configuration du bouton de reset
         */
        function reset(event)
        {
            event.preventDefault();
            getFormPrice(id);
        }

        caractbutton = document.getElementById("pricereset")
        caractbutton.addEventListener("click", (event) => reset(event));
        caractbutton.addEventListener("keypress", (event) => {
            if(event.key == "Enter"){reset(event);}
        });

        /*
         * Configuration du bouton de suppression
         */
        function del(event)
        {
            event.preventDefault();

            if( document.getElementById("priceformrefid").value != "")
            {
                let formData = new FormData();
                formData.append('priceformrefid', document.getElementById("priceformrefid").value);
                formData.append('csrfmiddlewaretoken',document.querySelector('[name=csrfmiddlewaretoken]').value)

                    fetch('/item/'+id+'/prix/delete/'+document.getElementById("priceformrefid").value, {
                        method: "POST",
                        body: formData,
                        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                    })
                    .then(reponse => reponse.text())
                    .then(data => {
                        console.log(data);
                        getTablePrice(id);
                        getFormPrice(id);
                    })
            }
        }
        caractbutton = document.getElementById("pricedelete")
        caractbutton.addEventListener("click", (event) => del(event));
        caractbutton.addEventListener("keypress", (event) => {
            if(event.key == "Enter"){del(event);}
        });
    });
}

function getTablePrice(id)
{
    LAST_SELECTED_PRICE = "";
    fetch('/item/'+id+'/prix')
    .then(reponse => reponse.text())
    .then(data => {
        place = document.getElementById("pricedata");
        place.innerHTML = data;
    })
    .then(data => {
        tableData = document.querySelectorAll("tr.tr-table-price");
        tableData.forEach(
            function (item) {
                item.addEventListener("click", (event) => {
                    if(LAST_SELECTED_PRICE != "")
                    {
                        document.getElementById(LAST_SELECTED_PRICE).classList.remove('table-primary');
                    }
                    document.getElementById(item.id).classList.add("table-primary");
                    LAST_SELECTED_PRICE = item.id;
                    getFormPrice(id, item.getAttribute('aria-id'));
                });
            });

    });
}
