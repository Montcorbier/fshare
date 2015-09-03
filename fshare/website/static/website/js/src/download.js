
/* routine and filter variables are defined in utils.js */

$(document).ready(function() {
    $(".download").click(function(e) {
        $.removeCookie("fileReady");
        $(filter).removeClass("hidden");
        routine = setInterval(waiting_for_file, 1000);
    });
});
