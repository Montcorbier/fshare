Dropzone.autoDiscover = false;

var page_title = document.title;

/* When displaying link to download an encrypted file, 
   user can include or not the key parameter to the url
   by clicking on a button */
var toggle_key = function(href, key) {
    /* Toggling button element */
    var btn = $("#show-key-btn");
    /* If active, ie if key is being displayed */
    if (btn.hasClass("active")) {
        /* Change button text */
        btn.val("include key in url");
        /* Reset the displayed url to href not including key */
        $("#link-modal-input").val(href);
        /* Set the button as inactive */
        btn.removeClass("active");
    /* If inactive, ie if key is not displayed */
    } else {
        /* Change button text */
        btn.val("do not include key in url");
        /* Include key in the displayed url */
        $("#link-modal-input").val(href + key);
        /* Set button as active */
        btn.addClass("active");
    }
}

/* Initialise and show modal containing download link 
   of the previously uploaded file */
var show_link = function(href, key) {
    /* Modal element */
    var mdl = $("#link-modal");
    /* Toggling butotn element (to display/hide key in url) */
    var btn = $("#show-key-btn");
    /* Unbind all click events previously set on 
       the toggling button (avoid bugs on second, 
       third, etc. uploads) */
    btn.unbind("click");
    /* Set the button text */
    btn.val("do not include key in url");
    /* Set as active by default */
    btn.addClass("active");
    /* If a key was set */
    if (key != "") {
        /* Redefine key as a GET parameter (encoded for URI) */
        key = "?key=" + encodeURIComponent(key);
        /* Set the click event to toggle the key in url */
        $("#show-key-btn").click(function() { toggle_key(href, key); });
        /* Show the toggling button */
        $("#show-key-btn").parent().removeClass("hidden");
    /* If no key provided */
    } else {
        /* Hide the toggling button */
        $("#show-key-btn").parent().addClass("hidden");
    }
    /* Set the default displayed url (including key if any) */
    $("#link-modal-input").val(href + key);
    /* Activate modal */
    mdl.modal({clickClose: false});
}

/* Generate a random key for upload */
var generate_key = function() {
    var key = "";
    var char_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    var len = 20;

    for (var i=0; i < len; i++)
        key += char_set.charAt(Math.floor(Math.random() * char_set.length));

    return key;
}

$(document).ready(function () {

    /* Init key generation button */
    $("#gen-key-btn").click(function() {
        var key = generate_key();
        key = generate_key();
        $("#id_key").val(key);
    });

    var fDropzone = new Dropzone('#upload-form'),
        form = $("#upload-form");

    fDropzone.options.maxFilesize = max_file_size;
    fDropzone.options.accept = function (file, done) {
        var size = 0;
        $.get(form.attr('data-size'), function( data ) {
            size = parseInt(data);
            if (file.size <= size) {
                done();
            } else {
                done("There is not enough available space.")
            }
        });
    }

    var nanobar;
    var options = {
        id : "upload-progression",
        bg: "#8D608C"
    }
    var nanobar =  new Nanobar( options );

    fDropzone.on('addedfile', function (file) {
        nanobar.go(0);
        $(filter).removeClass("hidden");
        routine = setInterval(waiting_for_file, 1000);
    }).on('uploadprogress', function(file) {
        nanobar.go(file.upload.progress);
        document.title = "FShare - Uploading " + Math.round(file.upload.progress) + "%";
        if (file.upload.progress == 100) {
            $(".text", filter).html("ciphering file ... please wait&nbsp;");
            $.removeCookie("fileReady");
            routine = setInterval(waiting_for_file, 1000);
        }
    }).on('complete', function(file) {
        $(filter).addClass("hidden");
        clearInterval(routine);
        if (file.xhr == undefined)
            return;
        document.title = "FShare - Upload completed"
        var href =  "https://" + document.domain + "/dl/" + file.xhr.response;
        var key = $("input#id_key").val();
        if (key == undefined || key == " ")
            key = "";
        show_link(href, key);
        return;
    }).on('error', function(unk, err) {
        alert(err); 
    });
})
;

$(document).on($.modal.CLOSE, function() {
    document.title = page_title;
});
