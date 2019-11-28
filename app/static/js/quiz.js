$("form").hide();
var questions = {{questions|tojson|safe}};
var answers = {{answers|tojson|safe}};
var result = []
var i = 0;
updateQuiz = function(clicked) {
    return function(){

        result.push(clicked);
        $("#answers").empty();
        $("#question").empty();
           
        if(i==questions.length) {
            $("form").show();
            $("form :text").hide();
            $("form #name").val(name);
            $("form #answers").val(result.join(" "));
        }

        $("#question").html(questions[i]);
        for(var j = 0; j<answers[i].length; j++) {
            $("#answers").append($("<button></button>").html(answers[i][j]).click(updateQuiz(j)));
        }


        i += 1;
       
    }
}
nameSubmitFunc = function() {
    if ($("#name").val().length > 1) {
        $("#name-label").hide();
        $("#name").hide();
        $("#send-name").hide();
        var name = $("#name").val();
        updateQuiz(0)();
        result.pop()
    } else {
        alert("Bitte gebe einen Namen ein");
    }
}
$("#send-name").click(nameSubmitFunc);