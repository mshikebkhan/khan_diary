function followUser(user_id, button) {
  // Update follow user button on frontend & send request to server.
  var user_id = user_id;
  var action = button.name;

  if (action == "follow") {
    // If user not followed.

    // Add Follow button with text Following Class Success.
    var button_text = document.getElementById("id_user_follow_button_text_" + user_id);
    button_text.innerHTML = "Following";

    button.setAttribute("class", "button is-rounded is-success");

    // Set action to unfollow.
    button.setAttribute("name", "unfollow");

  } else if (action == "unfollow") {
    // If user already followed.

    // Add Follow button with text Follow Class Light.
    var button_text = document.getElementById("id_user_follow_button_text_" + user_id);
    button_text.innerHTML = "Follow";

    button.setAttribute("class", "button is-rounded is-light");
    

    // Set action to follow.
    button.setAttribute("name", "follow");
  }

  $.ajax({
    // Send data packet including user id to the server.
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    type: 'POST',
    url: '../../../follow_user/' + user_id + '/',

    success: function(json) {
      // Show alerts on the response of server.

      if (json.status == "private_profile") {
        // If error then remove set button to follow.
        setTimeout(function() {
          alert('Private Profile !')
        }, 10)

        // Add Follow button with text Follow Class Light.
        var button_text = document.getElementById("id_user_follow_button_text_" + user_id);
        button_text.innerHTML = "Follow";

        button.setAttribute("class", "button is-rounded is-light");
        

        // Set action to follow.
        button.setAttribute("name", "follow");

      }

      if (json.status == "not_exists") {
        // If error then remove set button to follow.
        setTimeout(function() {
          alert('User does not exists !')
        }, 10)

        // Add Follow button with text Follow Class Light.
        var button_text = document.getElementById("id_user_follow_button_text_" + user_id);
        button_text.innerHTML = "Follow";

        button.setAttribute("class", "button is-rounded is-light");
        

        // Set action to follow.
        button.setAttribute("name", "follow");

      }

      // Update followers count.
      if (document.getElementById("id_followers_count")) {
        var followers_count = document.getElementById("id_followers_count");
        followers_count.innerHTML = json.followers_count;
      }

      // Update following count.
      if (document.getElementById("id_following_count")) {
        var following_count = document.getElementById("id_following_count");
        following_count.innerHTML = json.following_count;
      }

    },
  });
};