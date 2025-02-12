function followTag(tag_id, button) {
  // Update follow tag button on frontend & send request to server.
  var tag_id = tag_id;
  var action = button.name;

  if (action == "follow") {
    // If tag not followed.

    // Add Follow button with text Following Class Success.
    var button_text = document.getElementById("id_tag_follow_button_text_" + tag_id);
    button_text.innerHTML = "Following";

    button.setAttribute("class", "button is-rounded is-success");

    // Set action to unfollow.
    button.setAttribute("name", "unfollow");

  } else if (action == "unfollow") {
    // If tag already followed.

    // Add Follow button with text Follow Class Light.
    var button_text = document.getElementById("id_tag_follow_button_text_" + tag_id);
    button_text.innerHTML = "Follow";

    button.setAttribute("class", "button is-rounded is-light");
    

    // Set action to follow.
    button.setAttribute("name", "follow");
  }

  $.ajax({
    // Send data packet including tag id to the server.
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    type: 'POST',
    url: '../../../follow_tag/' + tag_id + '/',

    success: function(json) {
      // Show alerts on the response of server.

      if (json.status == "not_exists") {
        // If error then remove set button to follow.
        setTimeout(function() {
          alert('Tag does not exists !')
        }, 10)

        // Add Follow button with text Follow Class Light.
        var button_text = document.getElementById("id_tag_follow_button_text_" + tag_id);
        button_text.innerHTML = "Follow";

        button.setAttribute("class", "button is-rounded is-light");
        

        // Set action to follow.
        button.setAttribute("name", "follow");

      }

      // Update following tags count.
      if (document.getElementById("id_following_tags_count")) {
        var following_tags_count = document.getElementById("id_following_tags_count");
        following_tags_count.innerHTML = json.following_tags_count;
      }

    },
  });
};