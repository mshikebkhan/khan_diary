function reportEntry(button) {
  // Update report entry button on frontend & send request to server.
  var entry_id = button.name;

  // Add Report button with text reported and flagged icon.
  var button_text = document.getElementById("id_entry_report_button_text_" + entry_id);
  button_text.innerHTML = "&nbsp Reported";

  var button_icon = document.getElementById("id_entry_report_button_icon_" + entry_id);
  button_icon.setAttribute("class", "fas fa-flag");

  // Make the "a" dead.
  button.setAttribute("class", "card-footer-item is-idle");

  // Set the onclick none (So it can't be clicked)
  button.setAttribute("onclick", "");


  $.ajax({
    // Send data packet including entry id to the server.
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    type: 'POST',
    url: '../../../report_entry/' + entry_id + '/',

    success: function(json) {
      // Show alerts on the response of server.

      if (json.status == "reported") {
        // Entry Reported Succesfully
        setTimeout(function() {
          alert('This entry has been reported successfully our team will check it further and take action accordingly.')
        }, 10)
      }

      if (json.status == "already_reported") {
        // Entry Already Reported
        setTimeout(function() {
          alert('This entry is already reported.')
        }, 10)
      }

      if (json.status == "error") {
        // If error then remove set button to report.
        setTimeout(function() {
          alert('Something went wrong')
        }, 10)

        // Add Report button with text Report and bookmark icon.
        var button_text = document.getElementById("id_entry_report_button_text_" + entry_id);
        button_text.innerHTML = "&nbsp Report";

        var button_icon = document.getElementById("id_entry_report_button_icon_" + entry_id);
        button_icon.setAttribute("class", "far fa-flag");

        // Make the "a" alive.
        button.setAttribute("class", "card-footer-item");

        // Set the onclick none (So it can't be clicked)
        button.setAttribute("onclick", "reportEntry(this)");

      }

    },
  });
};