$("#clipboard").click(function myFunction() {
    var copyText = document.getElementById("myInput");
    copyText.select();
    copyText.setSelectionRange(0, 99999)
    document.execCommand("copy");
})
document.getElementById("myInput").onclick = function() {
    this.select();
    document.execCommand('copy');
}
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})
