/*
 *= require jquery
 *= require handlebars
 */

$(document).ready(function() {
    $.ajax("/videos/", {
        type: "GET",
        success: function(data) {
            var div = $("div#content");
            var template = Handlebars.compile($("#video-template").html());
            var videos = $.parseJSON(data);
            for (i in videos)
            {
                div.append(template(videos[i]));
            }
        },
        error: function() {
            var div = $("div#content");
            div.append("<h1>Failure!</h1");
            div.append("<p>Could not contact the server.</p>");
        }
    });
});

