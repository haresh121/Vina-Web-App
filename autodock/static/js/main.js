function makeid() {
    let length = 5
    let result = '';
    let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let charactersLength = characters.length;
    for ( let i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return result;
}
$("#uploadbtn").on("click", function (e){
    e.preventDefault();
    let prot = $("#proteinFiles").prop("files");
    let lig = $("#ligandFiles").prop("files");
    let table = document.getElementById("ptable");
    let rnd = []
    if (prot.length === lig.length){
        for(let i=0;i<prot.length;++i){
            rnd.push(makeid())
            let row = table.insertRow(-1);
            row.insertCell(0).innerHTML = "" + (i+1);
            row.insertCell(1).innerHTML = prot[i].name;
            row.insertCell(2).innerHTML = lig[i].name;
            row.insertCell(3).innerHTML =  "protein_ligand_" + rnd[i] + "_out.pdbqt";
        }
        const formdata = new FormData();
        formdata.append("csvfile", $("#paramFile").prop("files")[0]);
        axios(
            {
                method: "post",
                url: '/getnrows',
                data: formdata,
                config: { headers: { "Content-Type": "multipart/form-data" } }
            }
        )
            .then(function (response){
                if(response.data["nrows"] === prot.length)
                {
                    // this.submit();
                    console.log(rnd);
                    document.getElementById("randomval").value = rnd;
                }
                else
                {
                    console.log("pplease provide similar number of rows as the number of");
                }
            })
            .catch(function (error){
                console.log(error);
            });
        $("#processbtn").on("click", function (){
            $("#plinput").submit();
        });
    }
    else{
        $("#notify").innerHTML = "<div class=\"row d-flex justify-content-center\">\n" +
            "                    <div class=\"col-md-6 alert alert-danger alert-dismissible fade show\" role=\"alert\">\n" +
            "                      <button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">\n" +
            "                        <span aria-hidden=\"true\">&times;</span>\n" +
            "                      </button>\n" +
            "                    </div>\n" +
            "                </div>";
    }
});

// prot = document.getElementById("proteinFiles")
// lig = document.getElementById("ligandFiles")
//
// var names = []
//
// for (let i = 0, p, l; p = prot.files[i], l = lig.files[i], i < prot.files.length; i++)
// {
//     console.log(p.name, l.name)
// }