
var output;

var get_key_callback = function(pclass, key) {
    output.append(key + " (for " + pclass + " user)\n");
    output.animate({scrollTop: output.prop("scrollHeight")}, 500);
}

var get_key = function(pclass) {
    $.ajax({
                    url: URL_REG_KEY,
                    type: "GET",
                    data: {"class": pclass}, 
                    success: function(key) { get_key_callback(pclass, key) },
            });
}

var init_key_btn = function(el) {
    $(el).click(function() {
        get_key($(el).attr("data-pclass"));
    });
}

var init_cockpit = function() {
    output = $("#reg_key_console");
    $(".reg-key-btn").each(function() {
        init_key_btn(this);
    });
    $(".menu p", output).each(function() {
        $(this).click(function() {
            $(".menu p", output).each(function() {
                $(this).removeClass("active");
            });
            $(this).addClass("active");
            $(".content span", output).each(function() {
                $(this).addClass("hidden");
            });
            $("#" + $(this).attr("for"), output).removeClass("hidden");
        });
    });
    $(".content p", output).hover(function() {
            $(".control", this).removeClass("hidden");
    }, function() {
            $(".control", this).addClass("hidden");
    });
}

$(document).ready(init_cockpit);
