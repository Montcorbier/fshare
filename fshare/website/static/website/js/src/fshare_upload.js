Dropzone.autoDiscover = false;

$(document).ready(function () {
    var fDropzone = new Dropzone('#upload-form'),
        form = $("#upload-form");

    fDropzone.options.maxFilesize = 1024;
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
        target: document.getElementById("upload-progression"),
        bg: "#9B59B6"
    }
    var nanobar =  new Nanobar( options );

    fDropzone.on('addedfile', function (file) {
        nanobar.go(0);
    }).on('uploadprogress', function(file) {
        nanobar.go(file.upload.progress);
    }).on('complete', function(file) {
        $.get(form.attr('data-size'), function( data ) {
            // TODO: update size available
        });
    });
})
;