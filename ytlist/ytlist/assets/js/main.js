/*
 *= require jquery
 *= require jquery.cookie
 *= require handlebars
 */

function add_video(video)
{
    video.description = video.description.split("\n")[0];

    var template = Handlebars.compile($("#video-template").html());
    var html = template(video);

    $(html).hide().appendTo($("#video-list")).fadeIn(1000);

    $("#video-link-" + video.id).click(function(e) {
        e.preventDefault();
        player.loadVideoById(video.url);
    });

    $("#video-delete-" + video.id).click(function(e) {
        e.preventDefault();

        $.ajax("/videos/" + video.id + "/", {
            type: "DELETE",
            success: function(e) {
                $("#video-" + video.id).hide("slow");
            },
            error: function(e) {
                $("#video-" + video.id).
                    append("<p class='error'>Could not contact the server.</p>");
            }
        });
    });
}

function add_video_by_id(id)
{
    $.get("/videos/" + id + "/", function(msg) {
        var video = $.parseJSON(msg);
        add_video(video);
    });
}

function setup_csrf()
{
    var csrftoken = $.cookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)
                && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

function load_all_videos()
{
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
            div.append("<p class='error'>Could not contact the server.</p>");
        }
    });
}

function submit()
{
    var url_value = $("#url").val();
    var re = RegExp("v=(.*?)(&|$)");
    var match = re.exec(url_value);

    if (match)
    {
        url_value = match[1];
    }

    var obj = {url: url_value};
    var post_data = "data=" + JSON.stringify(obj);

    $.ajax("/videos/", {
        type: 'POST',
        data: post_data,
        success: function(msg) {
            var message = $.parseJSON(msg);
            if (message.status === 0)
            {
                add_video_by_id(message.message);
            }
            else
            {
                $("div#add-messages").append("<p class='error'>Could not post video: " + message.message + "</p>");
            }
        },
        error: function(msg) {
            $("div#add-messages").append("<p class='error'>Could not contact the server.</p>");
        }
    });
}

$(document).ready(function() {
    setup_csrf();
    load_all_videos();
    $("#submit-button").click(submit);
});

