/*
 *= require jquery
 *= require jquery.cookie
 *= require handlebars
 */

function add_video(video)
{
    var template = Handlebars.compile($("#video-template").html());
    var div = $("div#content");
    var html = template(video);
    $(html).hide().appendTo(div).fadeIn(1000);
    $("a#video-delete-link-" + video.id).click(function(e) {
        e.preventDefault();
        $.ajax("/videos/" + video.id + "/", {
            type: "DELETE",
            success: function(e) {
                $("#video-" + video.id).hide("slow");
            },
            error: function(e) {
                div.append("<p class='error'>Could not contact the server.</p>");
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
            var div = $("div#messages");
            div.append("<h1>Failure!</h1");
            div.append("<p>Could not contact the server.</p>");
        }
    });

    $("#submit").click(function() {
        var url_value = $("#url").val();
        var desc_value = $("#desc").val();
        var obj = {url: url_value, description: desc_value};
        var post_data = "data=" + JSON.stringify(obj);
        $.post("/videos/", post_data, function(msg) {
            var message = $.parseJSON(msg);
            if (message.status === 0)
            {
                obj.id = messages.message;
                $("div#content").append(add_video(obj));
            }
            else
            {
                $("div#messages").append("<p class='error'>Could not post video: " + message.message + "</p>");
            }
        });
    });
});

