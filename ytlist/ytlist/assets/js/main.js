/*
 *= require jquery
 *= require jquery.cookie
 *= require handlebars
 */

function add_video(video)
{
    var template = Handlebars.compile($("#video-template").html());
    var html = template(video);
    $(html).hide().appendTo($("#videos")).fadeIn(1000);
    $("#video-delete-" + video.id).click(function(e) {
        e.preventDefault();
        $.ajax("/videos/" + video.id + "/", {
            type: "DELETE",
            success: function(e) {
                $("#video-" + video.id).hide("slow");
            },
            error: function(e) {
                $("#video-" + video.id).
                    append("<p>Could not contact the server.</p>");
            }
        });
    });
}

$(document).ready(function() {
    var csrftoken = $.cookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)
                && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax("/videos/", {
        type: "GET",
        success: function(data) {
            var videos = $.parseJSON(data);
            for (i in videos)
            {
                var video = videos[i];
                add_video(video);
            }
        },
        error: function() {
            var div = $("div#videos");
            div.append("<h1>Critical Failure</h1>");
            div.append("<p>Could not contact the server.</p>");
        }
    });

    $("#submit-button").click(function() {
        var url_value = $("#url").val();
        var desc_value = $("#desc").val();
        if (!desc_value)
        {
            desc_value = "Some video.";
        }
        var obj = {url: url_value, description: desc_value};
        var post_data = "data=" + JSON.stringify(obj);
        $.ajax("/videos/", {
            type: 'POST',
            data: post_data,
            success: function(msg) {
                var message = $.parseJSON(msg);
                if (message.status === 0)
                {
                    obj.id = message.message;
                    $("div#content").append(add_video(obj));
                }
                else
                {
                    $("div#add-messages").append("<p>Could not post video: " + message.message + "</p>");
                }
            },
            error: function(msg) {
                $("div#add-messages").append("<p>Could not contact the server.</p>");
            }
        });
    });
});

