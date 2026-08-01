let LAST_SELECTED = "";
let status = "";

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
    search = document.getElementById('searchbar');
    fetch('/emprunter/liste/search/'+search.value)
    .then(reponse => reponse.text())
    .then(data => {
        place = document.getElementById("renttable");
        place.innerHTML = data;
        inittable();
    });
}



/*
 * Gestion des listes d'éléments
 */
function inittable()
{
    LAST_SELECTED=""
    tableData = document.querySelectorAll("#tablerentlist tr");
    tableData.forEach(
        function (item) {
            item.addEventListener("click", (event) => {
                if(LAST_SELECTED != "")
                {
                    document.getElementById(LAST_SELECTED).classList.replace('table-primary', status);
                }
                
                if(document.getElementById(item.id).classList.contains("table-success"))
                {
                    document.getElementById(item.id).classList.remove("table-success");
                    status = "table-success";
                }
                else if(document.getElementById(item.id).classList.contains("table-info"))
                {
                    document.getElementById(item.id).classList.remove("table-info");
                    status="table-info";
                }
                else if(document.getElementById(item.id).classList.contains("table-warning"))
                {
                    document.getElementById(item.id).classList.remove("table-warning");
                    status="table-warning";
                }
                else if(document.getElementById(item.id).classList.contains("table-danger"))
                {
                    document.getElementById(item.id).classList.remove("table-danger");
                    status="table-danger";
                }
                document.getElementById(item.id).classList.add("table-primary");
                
                LAST_SELECTED = item.id;
                getData(item.getAttribute('aria-id'));
            });
        });
}

function getData(id)
{
    if(id!=null)
    {
        fetch('/emprunter/details/'+id)
        .then(reponse => reponse.json())
        .then(data => {
            document.getElementById("refemprunt").innerHTML = data["user"]["first_name"] + " " + data["user"]["last_name"] + " (n° " + data["rent"] + ")";
            document.getElementById("details").innerHTML = 
                        `<table class="table table-hover" aria-id="` + data["rent"] + `"><thead><tr>
                            <th style="display: none;">Id</th>
                            <th>Désignation</th>
                            <th>Quantité</th>
                            <th>Retournés</th>
                            <th>Perdus/Volés</th>
                         </tr></thead><tbody id="tabledetails"></tbody></table>
                         <div class="row">
                            <div class="col-12">
                                <div class="input-group">
                                    <select class="form-select mb-3" id="validmode">
                                        <option id="ATTENTE" value="ATTENTE">En attente de rendu</option>
                                        <option id="COMPLET" value="COMPLET">Le matériel est rendu</option>
                                        <option id="PROJET" value="PROJET">Implémenté dans un projet</option>
                                        <option id="FACTURE" value="FACTURE">Matériel cassé à facturer</option>
                                        <option id="CASSE" value="CASSE">Matériel cassé ou abimé</option>
                                    </select>
                                    <button class="btn btn-primary w-100" id="ValidReturn">Enregistrer</button>
                                </div>
                            </div>
                         </div>`;

            for(item of data["items"])
            {
                if(item["lost_quantity"] == null)
                {
                    item["lost_quantity"] = 0;
                }
                if(item["returned_quantity"] == null)
                {
                    item["returned_quantity"] = 0;
                }
                var row = document.getElementById("tabledetails").appendChild(document.createElement("tr"));
                row.innerHTML = '<td style="display: none;">' + item["id"] + '</td>' +
                                '<td>' + item["designation"] + '</td>' +
                                '<td id="resqt' + item["id"] + '" aria-qte="' + item["quantity"] + '">' + item["quantity"] + '</td>' +
                                '<td><input id="resir' + item["id"] + '" type="number" value="' + Math.max(item["returned_quantity"], 0) + '" min="0" max="' + (item["quantity"]-item["lost_quantity"]) + '"></td>' +
                                '<td><input id="resil' + item["id"] + '" type="number" value="' + Math.max(item["lost_quantity"], 0) + '" min="0" max="' + (item["quantity"]-item["returned_quantity"]) + '"></td>';
                row.id = "res" + item["id"];
                row.setAttribute("aria-id", item["id"]);
                row.setAttribute("aria-item", item["iditem"]);
                
                document.getElementById("resir"+item["id"]).addEventListener("input", (event) =>{
                    control(event.target.parentElement.parentElement.getAttribute("aria-id"));
                });
                document.getElementById("resil"+item["id"]).addEventListener("input", (event) =>{
                    control(event.target.parentElement.parentElement.getAttribute("aria-id"));
                });

                control(item["id"]);
            }
            document.getElementById("ValidReturn").addEventListener("click", (event) => {save();});
            document.getElementById("ValidReturn").addEventListener("keypress", (event) => {if(event.key=="Enter"){save();}});
        })
        .then(data => {
            controlrent();
        });
        
    }
}

function control(id)
{
    var row = document.getElementById("res"+id);
    var resil = document.getElementById("resil"+id);
    var resir = document.getElementById("resir"+id);
    var resqt = parseInt(document.getElementById("resqt"+id).getAttribute("aria-qte"));
    
    resil.max = resqt - parseInt(resir.value);
    resir.max = resqt - parseInt(resil.value);
    
    row.classList.remove("table-danger");
    row.classList.remove("table-warning");
    row.classList.remove("table-success");

    if(parseInt(resil.value) > 0)
    {
        row.classList.add("table-danger");
    }
    else if(parseInt(resir.value) < resqt)
    {
        row.classList.add("table-warning");
    }
    else if(parseInt(resir.value) == resqt)
    {
        row.classList.add("table-success");
    }
    controlrent();
}

function controlrent()
{
    listitems = document.getElementById("tabledetails").rows;
    var isbrokenitem = false;
    var iscomplete = true;
    for(item of listitems)
    {
        nb = parseInt(item.cells[2].getAttribute("aria-qte"));
        correct = parseInt(item.cells[3].firstElementChild.value);
        broken = parseInt(item.cells[4].firstElementChild.value);

        if(broken > 0)
        {
            isbrokenitem = true;
        }
        if(nb != correct + broken)
        {
            iscomplete = false;
        }
    }
    
    if(iscomplete != true)
    {
        document.getElementById("ATTENTE").disabled = false;
        document.getElementById("ATTENTE").selected = true;
        document.getElementById("CASSE").disabled = true;
        document.getElementById("COMPLET").disabled = true;
        document.getElementById("PROJET").disabled = true;
        document.getElementById("FACTURE").disabled = true;
    }
    else if(isbrokenitem)
    {
        document.getElementById("ATTENTE").disabled = true;
        document.getElementById("CASSE").selected = true;
        document.getElementById("CASSE").disabled = false;
        document.getElementById("COMPLET").disabled = true;
        document.getElementById("PROJET").disabled = false;
        document.getElementById("FACTURE").disabled = false;
    }
    else
    {
        document.getElementById("ATTENTE").disabled = true;
        document.getElementById("CASSE").disabled = true;
        document.getElementById("COMPLET").disabled = false;
        document.getElementById("COMPLET").selected = true;
        document.getElementById("PROJET").disabled = true;
        document.getElementById("FACTURE").disabled = true;
    }
}

function save()
{
    object = {
        "rent": parseInt(document.querySelector("#details table").getAttribute("aria-id")),
        "items":[],
        "status": document.getElementById("validmode").value,
    };

    listitems = document.getElementById("tabledetails").rows;
    for(item of listitems)
    {
        id = item.getAttribute("aria-id");
        object["items"].push({
            "id": id,
            "returned": parseInt(document.getElementById("resir"+id).value),
            "loosed": parseInt(document.getElementById("resil"+id).value),
        });
    }

    var data = new FormData();
    data.append( "json", JSON.stringify( object ) );
    fetch('/emprunter/update/', {
                    method: "POST",
                    body: data,
                    headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                })
    .then(reponse => reponse.text())
    .then(data => {
        if(data == "Done")
        {
            document.location.reload();
        }
        else
        {
            div = document.createElement("div");
            div.innerHTML = data;
            document.getElementById("details").prepend(div);
        }
        console.log(data);
    });
}

inittable();
