
/* Callback when a file has been deleted */
var deleted = function(fid) {
    $("#file-" + fid).remove();
}

/* Init links to delete files w/ ajax request on click */
$(document).ready(function() {
    $(".delete-btn").each(function() {
        $(this).click(function() {
            var fid = $(this).attr("data-fid");
            jQuery.ajax( {
                url: $(this).attr("data-href"),
                data: { csrf: $(this).attr("data-csrf") },
                success: function() { deleted(fid); },
            });
        });
    });
});
