//for header
let menu = document.querySelector('#menu-btn');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
    menu.classList.toggle('fa-times');
    navbar.classList.toggle('active');

}

//for windows scroll
window.onscroll = () => {
    menu.classList.remove('fa-times');
    navbar.classList.remove('active');

    if(window.scrollY > 0) {
        document.querySelector('.header').classList.add('active');
    } else {
        document.querySelector('.header').classList.remove('active');
    }
}

window.onload = () => {
    if(window.scrollY > 0) {
        document.querySelector('.header').classList.add('active');
} else {
        document.querySelector('.header').classList.remove('active');
    }
}

//for home section
var homeSwiper = new Swiper(".home-slider", {
    spaceBetween: 20,
    effect: "fade",
    grabCursor: true,
    loop: true,
    centeredSlides: true,
    autoplay: {
     delay: 9500,
     disableOnInteraction: false,
   },
  });

  //feature section
  var featureSwiper = new Swiper(".feature-slider", {
    spaceBetween: 20,
    grabCursor: true,
    loop: true,
    centeredSlides: true,
    autoplay: {
     delay: 9500,
     disableOnInteraction: false,
   },

   breakpoints: {
    0: {
        slidesPerView: 1,
    },
    768: {
        slidesPerView: 2,
    },
    991: {
        slidesPerView: 3,
    },
   },
  });

  //trainer slider
  var trainerSwiper = new Swiper(".trainer-slider", {
    spaceBetween: 20,
    grabCursor: true,
    loop: true,
    centeredSlides: true,
    autoplay: {
     delay: 9500,
     disableOnInteraction: false,
   },

   breakpoints: {
    0: {
        slidesPerView: 1,
    },
    768: {
        slidesPerView: 2,
    },
    991: {
        slidesPerView: 3,
    },
   },
  });

  //blogs swiper
  var blogsSwiper = new Swiper(".blogs-slider", {
    spaceBetween: 20,
    grabCursor: true,
    loop: true,
    centeredSlides: true,
    autoplay: {
     delay: 2500,
     disableOnInteraction: false,
   },

   breakpoints: {
    0: {
        slidesPerView: 1,
    },
    768: {
        slidesPerView: 2,
    },
    991: {
        slidesPerView: 3,
    },
   },
  });

  //dashboard setting

  document.addEventListener('DOMContentLoaded', function() {
    const featureSelect = document.getElementById('featureSelect');
    const chartContainer = document.getElementById('chartContainer');
    let myChart = null; // Variable to hold the Chart.js instance

    featureSelect.addEventListener('change', function() {
        const selectedFeature = featureSelect.value;

        fetch('/profile/fetch_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrf_token')  // Ensure you include CSRF token if required
            },
            body: `feature=${selectedFeature}`
        })
        .then(response => response.json())
        .then(data => {
            // Handle the data and update the chartContainer or any other part of your DOM
            console.log(data);
            // Check if a chart instance already exists, destroy it to avoid duplicates
            if (myChart) {
                myChart.destroy();
            }
            // Create a new Chart.js instance based on the received data
            try {
                myChart = new Chart(chartContainer, {
                    type: 'bar', // Set the chart type (e.g., 'bar', 'line', 'pie', etc.)
                    data: {
                        labels: data.labels, // Assuming 'labels' is an array of labels for the chart
                        datasets: [{
                            label: 'Data', // Label for the dataset
                            data: data.values, // Assuming 'values' is an array of data values
                            backgroundColor: 'rgba(54, 162, 235, 0.2)', // Background color for bars/points
                            borderColor: 'rgba(54, 162, 235, 1)', // Border color for bars/points
                            borderWidth: 1 // Border width for bars/points
                        }]
                    },
                    options: {
                        // You can configure additional options for the chart here
                        scales: {
                            y: {
                                beginAtZero: true // Start y-axis from 0
                            }
                        }
                    }
                });
            } catch (error) {
                console.error('Error creating chart:', error);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

// Helper function to get the CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



    //goals setting
    function handleFeatureChange() {
        const feature = document.getElementById('featureSelect').value;
        // Handle the feature change logic here, e.g., update the chart or content based on the selected feature.
    }

    function redirectToGoals() {
        const goalsContainer = document.querySelector('.goals-container');
        const url = goalsContainer.getAttribute('data-url');
        window.location.href = url;
    }

    function redirectToNutrition() {
        const nutritionContainer = document.querySelector('.nutrition-container');
        const url = nutritionContainer.getAttribute('data-url');
        window.location.href = url;
    }

    function redirectToProgress() {
        const progressContainer = document.querySelector('.progress-container');
        const url = progressContainer.getAttribute('data-url');
        window.location.href = url;
    }

    function redirectToSocial() {
        const socialContainer = document.querySelector('.social-container');
        const url = socialContainer.getAttribute('data-url');
        window.location.href = url;
    }

    function redirectToWorkouts() {
        const workoutsContainer = document.querySelector('.workouts-container');
        const url = workoutsContainer.getAttribute('data-url');
        window.location.href = url;
    }