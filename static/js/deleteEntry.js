function deleteEntry(button) {
  // Delete entry from frontend & send request to server.
  var entry_id = button.name;
  var x = confirm('Are you sure you want to delete this entry?');

  if (x) {
    // If user sure to delete.

    if (document.getElementById("id_entry_" + entry_id)) {
      // Remove entry from the page.
      var entry = document.getElementById("id_entry_" + entry_id);
      entry.remove();
    }

    if (document.getElementById("id_entries_count")) {
      // Decrease entry count on delete.
      var id_entries_count = document.getElementById("id_entries_count");
      var number = id_entries_count.innerHTML;
      number--;
      id_entries_count.innerHTML = number;
    }

    if (document.getElementById("id_entries_count")) {
      // If zero entries, create no entries note (p) on the page.
      var id_entries_count = document.getElementById("id_entries_count");
      var number = id_entries_count.innerHTML;
      if (number == 0) {
        var element = document.getElementById("empty-entry-list-div");
        element.innerHTML = '<center><p class="subtitle warning">No entries</p></center>'
      }
    }

    $.ajax({
      // Send data packet including entry id to the server.
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
      type: 'POST',
      url: '../../../delete_entry/' + entry_id + '/',

      success: function(json) {
        // Show alerts on the response of server.

        if (json.status == "deleted") {
          setTimeout(function() {
            alert('Entry has been deleted successfully! Please refresh the page if it is still appearing on the page.')
          }, 10)
        } else {
          setTimeout(function() {
            alert('Unable to delete, an error occured !')
          }, 10)
        }



        // } else {
        //   setTimeout(function() {
        //     alert('Unable to delete, an error occured !');
        //   }, 10)
        // }

      },
    });
  };
}