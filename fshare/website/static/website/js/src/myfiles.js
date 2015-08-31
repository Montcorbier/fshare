
/* Callback when a file has been deleted */
var deleted = function(fid) {
    $("#file-" + fid).remove();
}

var toggle_pwd = function() {
    var btn = $("#show-pwd-btn");
    if (btn.hasClass("active")) {
        $("#pwd-modal-input").attr("type", "text");
        btn.val("Hide password");
        btn.removeClass("active");
    } else {
        $("#pwd-modal-input").attr("type", "password");
        btn.val("Show password");
        btn.addClass("active");
    }
}

var toggle_link = function() {
    var btn = $("#show-link-btn");
    if (btn.hasClass("active")) {
        $("#link-pwd-modal-input").attr("type", "text");
        btn.val("Hide link");
        btn.removeClass("active");
    } else {
        $("#link-pwd-modal-input").attr("type", "password");
        btn.val("Show link");
        btn.addClass("active");
    }
}

/* Show a modal containing the password of 
   the file and a dl url embedding the pwd */
var show_pwd = function(elt) {
    var mdl = $("#pwd-modal");
    $("#pwd-modal-input").val($(elt).attr("data-pwd"));
    $("#link-pwd-modal-input").val($(elt).attr("data-href"));
    if (!$("#show-pwd-btn").hasClass("active")) {
        toggle_pwd();
    }
    if (!$("#show-link-btn").hasClass("active")) {
        toggle_link();
    }
    mdl.modal();
}

var show_link = function(elt) {
    var mdl = $("#link-modal");
    $("#link-modal-input").val($(elt).attr("data-href"));
    mdl.modal();
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
    $("#show-pwd-btn").click(toggle_pwd);
    $("#show-link-btn").click(toggle_link);
    $(".pwd-btn").each(function() {
        $(this).click(function() {
            show_pwd(this);
        });
    });
    $(".link-btn").each(function() {
        $(this).click(function() {
            show_link(this);
        });
    });
});
