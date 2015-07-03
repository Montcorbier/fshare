
var output;

var get_key_callback = function(pclass, key) {
    var class_container = $("#" + pclass);
    /* Get template for key in console */
    var el = $(".unused-key-tpl>p", class_container).clone();
    /* Set key */
    $(".key", el).val(key);
    /* Add it in console view */
    $(".unused-keys", class_container).append(el);
    /* Activate mark & revoke buttons */
    $(el).hover(function() {
            $(".control", this).removeClass("hidden");
    }, function() {
            $(".control", this).addClass("hidden");
    });
    /* Scroll down to see the new key */
    $(".unused-keys", class_container).animate({scrollTop: $(".unused-keys", class_container).prop("scrollHeight")}, 500);
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
        get_key($(el).attr("data-pclass"));
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
    /* Init control buttons on hover */
    $(".content p", output).hover(function() {
            $(".control", this).removeClass("hidden");
    }, function() {
            $(".control", this).addClass("hidden");
    });
    /* Init mark distributed button */
    $(".mark_distrib_btn", output).click(function() {
        var key = $(".key", $(this).parent().parent()).val();
        mark_key(key);
    });
    /* Init revoke button */
    $(".revoke_key_btn", output).click(function() {
        var key = $(".key", $(this).parent().parent()).val();
        revoke_key(key);
    });
}

$(document).ready(init_cockpit);
