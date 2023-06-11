 // Wait for the page to load
 window.addEventListener('load', function() {
    // Listen for the beforeunload event
    window.addEventListener('beforeunload', function(event) {
      // Cancel the event
      event.preventDefault();
      // Show the goodbye page
      document.body.style.display = 'none';
      ;
    });
  });