// Show database function, takes a json database as input. See db/database.json
function show_db(data) {
	// Go over the whole database
	for (index in data.results) {
		const new_row = document.createElement('div');
		// Create a div element to append a tweet in, used for styling later
		document.getElementById('tweet_start').appendChild(new_row);
		new_row.setAttribute('id', index);
		new_row.setAttribute('class', 'tweet_wrapper');
		// Append the tweet element
		const temp_tweet = document.createElement('p');
		temp_tweet.innerHTML = 'Tweet: ' + data.results[index].tweet_html_code;
		document.getElementById(index).appendChild(temp_tweet);
		temp_tweet.setAttribute('class', 'tweet_text');
		// Append the class element
		const temp_class = document.createElement('p');
		temp_class.innerHTML =
			'Predicted Discrimination Type: ' + data.results[index].pred_class;
		document.getElementById(index).appendChild(temp_class);
		temp_class.setAttribute('class', 'tweet_class');
		// Append the probability element
		const temp_prob = document.createElement('p');
		temp_prob.innerHTML = 'Certainty: ' + data.results[index].prob;
		document.getElementById(index).appendChild(temp_prob);
		temp_prob.setAttribute('class', 'tweet_prob');
	}
}

// Function to clear the tweet example, buttons and probability
function clear_warning() {
	$('#reviewed_tweet_text').empty();
	$('#reviewed_tweet_buttons').empty();
	$('#reviewed_tweet_prob').empty();
}

// Load tweets on page load
$(document).ready(function () {
	// Hide loading
	$('.loading').hide();
	// Get the database
	$.getJSON('/load_tweet_db', function (data) {
		// Clear the dom each time the button is pressed
		$('#tweet_start').empty();
		// Reload the database to show on the webpage
		show_db(data);
	});
});

// Process post anyways button click
$(function () {
	$(document).on('click', '.post_anyways', function (e) {
		// Prevent default behaviour
		e.preventDefault();
		$.getJSON('/post_tweet', function (data) {
			// Clear the dom each time the button is pressed
			$('#tweet_start').empty();
			// Reload the database to show on the webpage
			show_db(data);
			// Clear buttons, probability and tweet example
			clear_warning()
			// Set tweet box to empty
			document.getElementById('tweet_text_box').value = '';
		});
		return false;
	});
});

// Put tweet back in textbox when rephrase button is triggered
$(function () {
	$(document).on('click', '.rephrase_button', function (e) {
		// Prevent default behaviour
		e.preventDefault();
		// Clear the button and probability
		$('#reviewed_tweet_buttons').empty();
		$('#reviewed_tweet_prob').empty();
		// Get data from the cache and put it in the text box
		$.getJSON('/rephrase_tweet', function (data) {
			document.getElementById('tweet_text_box').defaultValue =
				data.results['tweet'];
			document.getElementById('reviewed_tweet_buttons').innerHTML = '<p></p>';
		});
		return false;
	});
});

// Handle the Post Tweet button
$(function () {
	$('a#review').on('click', function (e) {
		// Prevent default behaviour
		e.preventDefault();
		// Always remove warning message
		$('#warning-message').empty();
		clear_warning()
		// Show the loading bar
		$('.loading').show();
		$.ajax({
			url: '/review_tweet',
			data: $('form').serialize(),
			type: 'POST',
			success: function (response) {
				const json_resp = JSON.parse(response);
				const terms = ['No', 'Cyberbullying'];
				// Hide the loading bar
				$('.loading').hide();
				// Set the minimum tweet length to 2, maxlength is enforced in HTML
				if (json_resp['org_tweet'].length < 2) {
					// Clear buttons, probability and tweet example
					clear_warning()
					// Show warning as text
					$('#warning-message').text(
						'Your Tweet is too short, minimum of 2 characters.'
					);
				// Check if type is no cyberbullying and post the tweet immediately if it is
				} else if (
					terms.every((term) => json_resp['reviewed_tweet'].includes(term))
				) {
					$.getJSON('/post_tweet', function (data) {
						// Clear warning message if there
						$('#warning-message').empty();
						// Clear the dom each time the button is pressed
						$('#tweet_start').empty();
						// Reload the database to show on the webpage
						show_db(data);
						// Clear buttons, probability and tweet example
						clear_warning()
						// Set tweet box to empty
						document.getElementById('tweet_text_box').value = '';
					});
				// When we detect cyberbullying we show it
				} else {
					// Clear warning message if there
					$('#warning-message').empty();
					// Add the tweet, buttons and class probability
					document.getElementById('reviewed_tweet_text').innerHTML =
						json_resp['reviewed_tweet'];
					document.getElementById('reviewed_tweet_buttons').innerHTML =
						json_resp['buttons'];
					document.getElementById('reviewed_tweet_prob').innerHTML =
						json_resp['class_prob_html'];
					// Change the width of the bar to represent the class probability
					document.getElementById('inside').style.width = json_resp['class_prob'];
				}
			},
			error: function (error) {
				console.log(error);
			},
		});
		return false;
	});
});
