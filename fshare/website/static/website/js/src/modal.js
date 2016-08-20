
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
    /* Set handler for modal close */
    // $(document).on($.modal.CLOSE, function() { ui_generate_key(); });
    /* Activate modal */
    mdl.modal({clickClose: false});
    /* Select link */
    $("#link-modal-input").select();
}

