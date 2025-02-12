function addRead(entry_id) {
  // +1 read to entry after 30sec of page load.
  var entry_id = entry_id;

  $.ajax({
    // Send data packet including entry id to the server.
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    type: 'POST',
    url: '../../../add_read/' + entry_id + '/',

  });
};