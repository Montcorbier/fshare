
var filter = "#filter";
var nb_point = 0;
var routine;

var waiting_for_file = function() {
    if (document.cookie.indexOf("fileReady") >= 0) {
        $(filter).addClass("hidden");
        clearInterval(routine);
    }
    if (nb_point < 3) {
        nb_point++;
        content = "";
        for (var i = 1; i <= 3; i++)
            if (i <= nb_point)
                content += ".";
            else
                content += "&nbsp;";
        $(".points", filter).html(content);
    } else {
        $(".points", filter).html("&nbsp;&nbsp;&nbsp;");
        nb_point = 0;
    }
}

