/*
 *= require jquery
 *= require jquery.cookie
 *= require handlebars
 */

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
            var div = $("div#content");
            var template = Handlebars.compile($("#video-template").html());
            var videos = $.parseJSON(data);
            for (i in videos)
            {
                var video = videos[i];
                div.append(template(video));
                console.log(template(video));
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
        },
        error: function() {
            var div = $("div#content");
            div.append("<h1>Failure!</h1");
            div.append("<p>Could not contact the server.</p>");
        }
    });
});

