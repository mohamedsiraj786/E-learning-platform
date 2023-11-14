    // Retrieve data from localStorage
    var selectedCourses = JSON.parse(localStorage.getItem('selectedCourses'));

    // Send the data to the Flask server

    fetch('/api/update_courses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ selectedCourses: selectedCourses }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error(error);
    });
