let LAST_SELECTED = "";

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
    fetch('/fournisseurs/search/'+search.value)
    .then(reponse => reponse.text())
    .then(data => {
        place = document.getElementById("supplierstable");
        place.innerHTML = data;
        inittable();
    });
}



/*
 * Gestion des formulaires
 */
function inittable()
{
    LAST_SELECTED=""
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
}

createForm = document.getElementById("addnewbutton");
createForm.addEventListener("click", (event) => {
    getForm();
});
createForm.addEventListener("keypress", (event) => {
    if(event.key == "Enter"){getForm();}
});

function getForm(id=null)
{
    if(id!=null)
    {
        fetch('/fournisseur/'+id)
        .then(reponse => reponse.text())
        .then(data => {
            place = document.getElementById("supplier");
            place.innerHTML = data;
        })
        .then(data => {
            function updatebutton(event)
            {
                event.preventDefault();
                fetch('/fournisseur/remove/'+id)
                .then(reponse => reponse.text())
                .then(data => {
                    console.log(data);
                    getTable();
                    getForm();
                });
            }

            const formdelete = document.getElementById("supformdel");
            formdelete.addEventListener("click", (event) => {
                updatebutton(event);
            });
            formdelete.addEventListener("keypress", (event) => {
                if(event.key == "Enter"){updatebutton(event);}
            });
        });
    }
    else
    {
        fetch('/fournisseur/new')
        .then(reponse => reponse.text())
        .then(data => {
            place = document.getElementById("supplier");
            place.innerHTML = data;
        });
    }
}

inittable();
