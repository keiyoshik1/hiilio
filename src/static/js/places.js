function loadForm(selectionChange)
{
    fetch('/emplacements/'+selectionChange[0].id+'/modifier')
    .then(reponse => reponse.text())
    .then(data => {
        place = document.getElementById('formupdateposition');
        place.innerHTML = data;
    })
    .then(data => {
        function deletebutton(event)
        {
            event.preventDefault();
            fetch('/emplacements/'+document.getElementById("uid").value+'/supprimer/')
            .then(reponse => reponse.text())
            .then(data => {
                console.log(data);
                loadtree();
            });
        }

        const formdelete = document.getElementById("placeformdel");
        formdelete.addEventListener("click", (event) => {
            deletebutton(event);
        });
        formdelete.addEventListener("keypress", (event) => {
            if(event.key == "Enter"){deletebutton(event);}
        });
    });

    fetch('/emplacements/'+selectionChange[0].id+'/ajouter')
    .then(reponse => reponse.text())
    .then(data => {
        place = document.getElementById('formnewposition');
        place.innerHTML = data;
    });
}

function loadrootadd()
{
    fetch('/emplacements/racine/ajouter')
    .then(reponse => reponse.text())
    .then(data => {
        place = document.getElementById('formnewroot');
        place.innerHTML = data;
    });
}

function loadtree()
{
    fetch('/emplacements/list')
    .then(reponse => reponse.json())
    .then(data => {
        console.log(data);
        emplacementdata = data;
        tree.setData(emplacementdata);
    });
}

loadtree();
loadrootadd();
