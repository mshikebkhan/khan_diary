function saveEntry(entry_id, button) {
  // Update save entry button on frontend & send request to server.
  var entry_id = entry_id;
  var action = button.name;

  if (action == "save") {
    // If entry not saved.

    // Add Save button with text Saved and bookmarked icon.
    var button_text = document.getElementById("id_entry_save_button_text_" + entry_id);
    button_text.innerHTML = "&nbsp Saved";

    var button_icon = document.getElementById("id_entry_save_button_icon_" + entry_id);
    button_icon.setAttribute("class", "fas fa-bookmark");

    // Set action to unsave.
    button.setAttribute("name", "unsave");
  } else if (action == "unsave") {
    // If entry already saved.

    // Add Save button with text Save and bookmark icon.
    var button_text = document.getElementById("id_entry_save_button_text_" + entry_id);
    button_text.innerHTML = "&nbsp Save";

    var button_icon = document.getElementById("id_entry_save_button_icon_" + entry_id);
    button_icon.setAttribute("class", "far fa-bookmark");

    // Set action to save.
    button.setAttribute("name", "save");
  }

  $.ajax({
    // Send data packet including entry id to the server.
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    type: 'POST',
    url: '../../../save_entry/' + entry_id + '/',

    success: function(json) {
      // Show alerts on the response of server.

      if (json.status == "error") {
        // If error then remove set button to save.
        setTimeout(function() {
          alert('Something went wrong')
        }, 10)

        // Add Save button with text Save and bookmark icon.
        var button_text = document.getElementById("id_entry_save_button_text_" + entry_id);
        button_text.innerHTML = "&nbsp Save";

        var button_icon = document.getElementById("id_entry_save_button_icon_" + entry_id);
        button_icon.setAttribute("class", "far fa-bookmark");

        // Set action to save.
        button.setAttribute("name", "save");

      }

      // Update saved entries count.
      if (document.getElementById("id_entries_count")) {
        var entries_count = document.getElementById("id_entries_count");
        entries_count.innerHTML = json.saved_entries_count;
      }

    },
  });
};