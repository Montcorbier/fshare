Dropzone.autoDiscover = false;

function PackData(boundary, data, filename, varname) {
  var datapack = '';
  datapack += '--' + boundary + '\r\n';
  datapack += 'Content-Disposition: form-data; ';
  datapack += 'name="' + varname + '"; filename="' + filename + '"\r\n';
  datapack += 'Content-Type: application/octet-stream\r\n\r\n';
  datapack += data;
  datapack += '\r\n';
  datapack += '--' + boundary + '--';
  return datapack;
}

$(document).ready(function () {
    var fDropzone = new Dropzone('#upload-form'),
        form = $("#upload-form");

    fDropzone.options.maxFilesize = 250;
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
        bg: "white"
    }
    var nanobar =  new Nanobar( options );

    fDropzone.on('addedfile', function (file) {
        nanobar.go(0);
        $(filter).removeClass("hidden");
        routine = setInterval(waiting_for_file, 1000);
    }).on('uploadprogress', function(file) {
        nanobar.go(file.upload.progress);
        if (file.upload.progress == 100) {
            $(".text", filter).html("ciphering file ... please wait&nbsp;");
            $.removeCookie("fileReady");
            routine = setInterval(waiting_for_file, 1000);
        }
    }).on('complete', function(file) {
        /*
        $.get(form.attr('data-size'), function( data ) {
            // TODO: update size available
        });
        */
        var href = "dl/" + file.xhr.response;
        var key = $("input#id_key").val();
        if (key != "" && key != undefined)
            href += "?key=" + key;
        window.location.href = href;
    });
})
;
