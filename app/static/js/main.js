$("#clipboard").click(function() {
    $("#clipboard")[0].select();
    $("#clipboard")[0].setSelectionRange(0, 99999);
    document.execCommand("copy");
})
