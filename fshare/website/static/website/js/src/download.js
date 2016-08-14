
/* routine and filter variables are defined in utils.js */

$(document).ready(function() {
    $(".download").click(function(e) {
        $.removeCookie("fileReady");
        $(filter).removeClass("hidden");
        routine = setInterval(waiting_for_file, 1000);
    });

    $(".show_content").click(function() {
        $(".show_content").toggleClass("hidden");
        $(".content_file", ".content").each(function() {
            $(this).toggleClass("hidden");
        });
    });
});
