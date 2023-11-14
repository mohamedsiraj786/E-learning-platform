
        // Add an event listener to execute the code when the DOM is ready
        document.addEventListener("DOMContentLoaded", function() {
          setTimeout(function() {
            var errorMessage = document.getElementById('error-message');
            errorMessage.style.display = 'none';
          }, 3000);  // Hide the error message after 3 seconds
        });
