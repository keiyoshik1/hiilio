
/*************************************************************\
|* Étape 1 - Gestion du choix de l'utilisateur               *|
\*************************************************************/

const search1 = document.getElementById("1UserSearch");

/**
 * Fonction permettant de déterminer le type d'utilisateur fourni en entrée
 * @param {int} val la valeur à convertir en texte 
 * @returns Le type d'utilisateur correspondant à la valeur fournie en paramètre
 */
function getUserType(val)
{
    var usertype = "" ;
    switch(val)
    {
        case 1:
            usertype = "Élève";
            break;

        case 2:
            usertype = "Enseignant";
            break;
        
        case 3:
            usertype = "Administratif";
            break;
    }
    return usertype;
}

/**
 * Définit la ligne actuellement sélectionnée dans la barre de recherche
 */
var currentSelected = -1;

/**
 * Fonction récupérant les informations d'un utilisateur pour les afficher dans la page, à l'étape 1
 * @param {json} user L'utilisateur à afficher 
 */
function loadUser(user)
{
    var usertype = getUserType(user["usertype"]);

    var userid = document.getElementById("1Userid");
    userid.textContent = user["id"];

    var name = document.getElementById("1Name");
    name.textContent = user["first_name"] + " " + user["last_name"] + " (" + usertype + ")";
    name.classList.remove("placeholder");

    var username = document.getElementById("1Username");
    username.textContent = user["username"];
    username.classList.remove("placeholder");

    var cardid = document.getElementById("1CardId");
    cardid.textContent = user["cardid"];
    cardid.classList.remove("placeholder");

    var email = document.getElementById("1Email");
    email.textContent = user["e-mail"];
    email.classList.remove("placeholder");

    var phone = document.getElementById("1Phone");
    phone.textContent = user["phone"];
    phone.classList.remove("placeholder");

    document.getElementById("1NTE").textContent = user["NTE"];
    document.getElementById("1NEC").textContent = user["NEC"];
    document.getElementById("1NER").textContent = user["NER"];
    document.getElementById("1NRD").textContent = user["NRD"];
    document.getElementById("1NNR").textContent = user["NNR"];

    document.getElementById("1Valid").classList.remove("disabled");
}

search1.addEventListener("keyup", (event) => {
    rentusersearch(event);
});
search1.addEventListener("click", (event) => {
    rentusersearch(event);
});

/**
 * Fonction gérant concrètement les actions sur la barre de recherche
 * @param {event} event L'événement ayant déclenché l'appel de la fonction
 */
function rentusersearch(event)
{
    if(event.key == 'ArrowUp')
    {
        items = document.querySelectorAll('#searchresults li');
        if(currentSelected > 0)
        {
            items[currentSelected--].classList.remove("active");
            items[currentSelected].classList.add("active");
        }
        else if(items.length > 0)
        {
            currentSelected = 0;
            items[currentSelected].classList.add("active");
        }
    }
    else if(event.key == 'ArrowDown')
    {
        items = document.querySelectorAll('#searchresults li');
        if(currentSelected < items.length - 1)
        {
            if(currentSelected != -1)
            {
                items[currentSelected++].classList.remove("active");
            }
            else
            {
                currentSelected++;
            }
            items[currentSelected].classList.add("active");
        }
        else if(currentSelected >= items.length - 1)
        {
            currentSelected = items.length -1;
            items[currentSelected].classList.add("active");
        }
    }
    else if(event.key == 'Enter')
    {
        items = document.querySelectorAll('#searchresults li');
        if(currentSelected >=0 && currentSelected < items.length)
        {
            items[currentSelected].id
            console.log(items[currentSelected].id);
            fetch('/emprunter/chercherutilisateur/id/'+items[currentSelected].id)
            .then(reponse => reponse.json())
            .then(data => {
                loadUser(data);
                document.getElementById("searchresults").innerHTML = "";
            });
        }
    }
    else
    {
        fetch('/emprunter/chercherutilisateur/'+search1.value)
        .then(reponse => reponse.json())
        .then(data => {
            if(data["type"]=="Unique")
            {
                loadUser(data["user"]);
            }
            else if (data["type"]=="Multiple")
            {
                var searchresults = document.getElementById("searchresults");
                searchresults.innerHTML = "";
                currentSelected = -1;

                data["values"].forEach(element => {
                    var usertype = getUserType(element["usertype"]);

                    var li = searchresults.appendChild(document.createElement('li'));
                    li.classList.add("list-group-item")
                    li.innerHTML = 
                        '<div class="fw-bold">' + 
                            element["first_name"] + " " + element["last_name"] + " (" + usertype + ")" +
                        '</div><span class="fas fa-id-card" style="margin-right: 4px;"></span>' + element["username"] + " - " + element["cardid"];
                    
                    li.addEventListener("click", (event) => {
                        fetch('/emprunter/chercherutilisateur/id/'+element["id"])
                        .then(reponse => reponse.json())
                        .then(data => {
                            loadUser(data);
                            document.getElementById("searchresults").innerHTML = "";
                        });
                        
                    });
                    li.id = element["id"];
                });
            }
            
        });
    }
}

document.getElementById("1Valid").addEventListener("click", (event) => {toStep2();}); 
document.getElementById("1Valid").addEventListener("keypress", (event) => {if(event.key == 'Enter'){toStep2();}}); 

/**
 * Fonction permettant le passage à l'étape 2
 */
function toStep2()
{
    document.getElementById("1UserSearch").hidden = true;
    document.getElementById("1Valid").hidden = true;
    document.getElementById("2Global").hidden = false;
}


/*************************************************************\
|* Étape 2 - Date de retour et lieu d'emprunt                *|
\*************************************************************/
const now = new Date().toISOString().split('T')[0];
document.getElementById("2Date").value = now;
document.getElementById("2Date").min = now;

document.getElementById("2Place").addEventListener("paste", (event) => {checkValid2();});
document.getElementById("2Place").addEventListener("keyup", (event) => {checkValid2();});

function checkValid2()
{
    if(document.getElementById("2Place").value.length >= 15)
    {
        document.getElementById("2Valid").classList.remove("disabled");
    }
    else
    {
        document.getElementById("2Valid").classList.add("disabled");
    }
}

document.getElementById("2Valid").addEventListener("click", (event) => {toStep3();}); 
document.getElementById("2Valid").addEventListener("keypress", (event) => {if(event.key == 'Enter'){toStep3();}}); 

function toStep3()
{
    document.getElementById("2Place").disabled = true;
    document.getElementById("2Place").readonly = true;
    document.getElementById("2Date").disabled = true;
    document.getElementById("2Date").readonly = true;
    document.getElementById("2Valid").hidden = true;
    document.getElementById("3Global").hidden = false;
    document.getElementById("3searchbar").focus();
}


/*************************************************************\
|* Étape 3 - Sélection du matériel                           *|
\*************************************************************/
search3 = document.getElementById("3searchbar");
search3.addEventListener("keyup", (event) => {
    rentitemsearch(event);
});
search3.addEventListener("click", (event) => {
    rentitemsearch(event);
});
search3.addEventListener("paste", (event) => {
    rentitemsearch(event);
});

function rentitemsearch()
{
    let LAST_SELECTED = ""
    search = document.getElementById('3searchbar');
    fetch('/emprunter/composants/search/'+search.value)
    .then(reponse => reponse.text())
    .then(data => {
        place = document.getElementById("3Components");
        place.innerHTML = data;
        items = document.querySelectorAll("#list3 tr")
        items.forEach(element => {
            if (element.id != "init3components")
            {
                btn = element.cells[4].lastElementChild.lastElementChild;
                btn.addEventListener("click", (event) => {
                    moveData(event, element, element.getAttribute('aria-id'));
                });
                btn.addEventListener("keypress", (event) => {
                    if(event.key == 'Enter'){moveData(event, element, element.getAttribute('aria-id'));}
                });
            }
        });
    });
}

function moveData(event, element, id)
{
    if(document.getElementById('res'+id) != null)
    {
        item = document.getElementById('res'+id).cells[4].lastElementChild.firstElementChild;
        item.value = Math.min(parseInt(item.value) + parseInt(element.cells[4].lastElementChild.firstElementChild.value), parseInt(item.max));
    }
    else
    {
        var line = element.cloneNode(true);
        var btn = line.cells[4].lastElementChild.lastElementChild
        btn.innerHTML = '<span class="fas fa-trash-alt"></span>';
        btn.classList.replace("btn-success", "btn-danger");
        btn.addEventListener("click", (event) => {
            deleteRow(id);
        });
        btn.addEventListener("keypress", (event) => {
            if(event.key == 'Enter')
            {
                deleteRow(id);
            }
        });

        line.id = "res" + id;
        line.setAttribute("aria-id", id);
        document.getElementById("3Selected").lastElementChild.appendChild(line);
        document.getElementById("3Valid").classList.remove("disabled");
    }
}

function deleteRow(id)
{
    var item = document.getElementById("res"+id);
    item.remove();
    if(document.getElementById("3Selected").lastElementChild.rows.length < 1)
    {
        document.getElementById("3Valid").classList.add("disabled");
    }
}

rentitemsearch();

document.getElementById("3Valid").addEventListener("click", (event) => {toStep4();}); 
document.getElementById("3Valid").addEventListener("keypress", (event) => {if(event.key == 'Enter'){toStep4();}}); 

function toStep4()
{
    document.getElementById("3Valid").hidden = true;
    document.getElementById("4Global").hidden = false;
    document.getElementById("4UserSearch").focus();
}



/*************************************************************\
|* Étape 4 - Authentification du valideur                    *|
\*************************************************************/

var search4 = document.getElementById("4UserSearch");

search4.addEventListener("keyup", (event) => {
    validatorSearch(event);
});
search4.addEventListener("click", (event) => {
    validatorSearch(event);
});
search4.addEventListener("paste", (event) => {
    validatorSearch(event);
});
search4.addEventListener("input", (event) => {
    validatorSearch(event);
});

/**
 * Fonction gérant concrètement les actions sur la barre de recherche
 * @param {event} event L'événement ayant déclenché l'appel de la fonction
 */
function validatorSearch(event)
{
    fetch('/emprunter/chercherutilisateur/'+search4.value)
    .then(reponse => reponse.json())
    .then(data => {
        if(data["type"]=="Unique" && (data["user"]["usertype"] == 2 || data["user"]["usertype"] == 3))
        {
            document.getElementById('4Name').innerHTML = data["user"]["first_name"] + " " + data["user"]["last_name"];
            document.getElementById('4UserInfo').hidden = false;
            document.getElementById('4id').value = data["user"]["id"];
            document.getElementById('4Valid').addEventListener("click", (event) =>{createRequest()});
            document.getElementById('4Valid').addEventListener("keypress", (event) =>{if(event.key='Enter'){createRequest()}});
        }        
    });
}

function createRequest()
{
    object = {
        "rentUser": parseInt(document.getElementById("1Userid").textContent),
        "rentDate": document.getElementById("2Date").value,
        "rentplace": document.getElementById("2Place").value,
        "validator": {
            "id": parseInt(document.getElementById('4id').value),
            "password": document.getElementById("4pass").value,
        },
        "rentitems":[],
    }
    for (element of document.getElementById("3Selected").lastElementChild.rows)
    {
        object["rentitems"].push({
            "id": parseInt(element.getAttribute("aria-id")),
            "quantity": parseInt(element.cells[4].lastElementChild.firstElementChild.value),
        })
    }

    var data = new FormData();
    data.append( "json", JSON.stringify( object ) );
    fetch('creer/', {
                    method: "POST",
                    body: data,
                    headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                })
    .then(reponse => reponse.text())
    .then(data => {
        if(data == "Done")
        {
            document.location.replace('liste/');
        }
        else
        {
            div = document.createElement("div");
            div.innerHTML = data;
            document.getElementById("4rentuser").prepend(div);
        }
    });
}