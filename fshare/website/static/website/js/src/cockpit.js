
var output;

var get_key_callback = function(pclass, key) {
    /* Modal element */
    var mdl = $("#key-modal");
    /* Set key */
    $("#key-modal-input").val(key);
    mdl.modal({clockClose: false});
    $("#key-modal-input").select();

}

var mark_key_callback = function(data, key) {
    console.log(data);
}

var revoke_key_callback = function(data, key) {
    console.log(data);
}

var get_key = function(pclass) {
    $.ajax({
                    url: URL_REG_KEY,
                    type: "GET",
                    data: {"class": pclass}, 
                    success: function(key) { get_key_callback(pclass, key) },
            });
}

var mark_key = function(key) {
    $.ajax({
                    url: URL_MARK_KEY,
                    type: "GET",
                    data: {"key": key}, 
                    success: function(data) { mark_key_callback(data, key) },
            });
}

var revoke_key = function(key) {
    $.ajax({
                    url: URL_REVOKE_KEY,
                    type: "GET",
                    data: {"key": key}, 
                    success: function(data) { revoke_key_callback(data, key) },
            });
}

var init_key_btn = function(el) {
    $(el).click(function() {
        get_key($(".pclass", "#registration-key-form").val());
    });
}

var select_pclass = function(pclass) {
    $(".pclass-container").addClass("hidden");
    $("#" + pclass).removeClass("hidden");
}

var init_cockpit = function() {
    output = $(".console");
    /* Init the button to select permission class */
    $("#pclass-select").change(function() {
        select_pclass($(this).val());
    });
    /* Init the button to generate a new key */
    $(".reg-key-btn").each(function() {
        init_key_btn(this);
    });
    /* Init the console menu items */
    $(".menu p", output).each(function() {
        /* On click on a menu button */
        $(this).click(function() {
            /* Disable each menu button */
            $(".menu p", output).each(function() {
                $(this).removeClass("active");
            });
            /* Enable the one clicked */
            $(this).addClass("active");
            /* Disable each page of the console */
            $(".content>div", output).each(function() {
                $(this).addClass("hidden");
            });
            /* Enable the one corresponding to the clicked button */
            $("." + $(this).attr("for"), output).removeClass("hidden");
        });
    });
}

$(document).ready(init_cockpit);
