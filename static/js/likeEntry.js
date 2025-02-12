function likeEntry(entry_id, button) {
  // Update like entry button on frontend & send request to server.
  var entry_id = entry_id;
  var action = button.name;

  if (action == "like") {
    // If entry not liked.

    // Add Like button heartfill icon.
    var button_icon = document.getElementById("id_entry_like_button_icon_" + entry_id);
    button_icon.setAttribute("class", "fas fa-heart");

    // Set action to unlike.
    button.setAttribute("name", "unlike");

  } else if (action == "unlike") {
    // If entry already liked.

    // Add Like button heartempty icon.
    var button_icon = document.getElementById("id_entry_like_button_icon_" + entry_id);
    button_icon.setAttribute("class", "far fa-heart");

    // Set action to like.
    button.setAttribute("name", "like");
  }

  $.ajax({
    // Send data packet including entry id to the server.
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    type: 'POST',
    url: '../../../like_entry/' + entry_id + '/',

    success: function(json) {
      // Show alerts on the response of server.
      if (json.status == "error") {
        // If error then remove set button to like.
        setTimeout(function() {
          alert('Something went wrong')
        }, 10)

        // Add like button with heartempty icon.
        var button_icon = document.getElementById("id_entry_like_button_icon_" + entry_id);
        button_icon.setAttribute("class", "far fa-heart");

        // Set action to like.
        button.setAttribute("name", "like");

      } else {
        var button_text = document.getElementById("id_entry_like_button_text_" + entry_id);
        button_text.innerHTML = "&nbsp " + json.likes_count;
      }

      // Update liked entries count.
      if (document.getElementById("id_liked_entries_count")) {
        var entries_count = document.getElementById("id_liked_entries_count");
        entries_count.innerHTML = json.liked_entries_count;
      }

    },
  });
};