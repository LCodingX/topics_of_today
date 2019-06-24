function selectOnlyThis(id) {
    for (var i = 0;i <= 3; i++)
    {
        document.getElementById("Check" + i).checked = false;
    }
    document.getElementById(id).checked = true;
    $(".fields").empty()
    for (i=0;i<parseInt(id[id.length-1]);i++) {
        $(".fields").append(
        "<label for='opinion"+i+"'>Opinion "+i+"</label><input id='opinion"+i+"' name='opinionform-desc"+parseInt(i+1)+"'></input><br>"
        );
    }
    $(".fields input").css("width", "50%")
}