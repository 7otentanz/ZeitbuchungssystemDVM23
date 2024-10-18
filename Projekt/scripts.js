function datumEinfuegen() {
    var jetzt = new Date();
    var datumUhrzeit = jetzt.toLocaleString();
    
    document.getElementById("datumUhrzeit").innerHTML = datumUhrzeit;
}