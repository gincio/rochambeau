var myUsername;
var oponentUsername;
var myScore;
var oponentScore;
var chosenFigure = '';
var oponentFigure;
var roundScore;
var figureIcons = {
	'paper' 	: 'far fa-hand-paper',
	'rock' 		: 'far fa-hand-rock',
	'scissors' 	: 'far fa-hand-scissors',
	'lizard' 	: 'far fa-hand-lizard',
	'spock' 	: 'far fa-hand-spock',
	''			: 'far fa-question-circle'
}
var figures = ['paper','rock','scissors','lizard','spock'];
var timerInterval;

$('#start-game').on('click', function() {
	myUsername = $('#player-username').val();
	$('#my-username').text(myUsername);
	$.ajax({
		url: 			window.location.href,
		type:			'post',
		data:	{
			action: 	'setConnection',
			nick:		myUsername
		},
		success: function (data) {
			if (data['status'] == 'ok') {
				getOponent();
			}
			else {
				showConnectionErrorDialog();
			}
		},
		error: function() {
			showConnectionErrorDialog();
		},
		complete: function() {
			$('#enter-name-dialog').addClass('hidden');
		}
	});
});

$('.figure').on('click', function() {
	if (chosenFigure == '') {
		chosenFigure = $(this).attr('id');
		$(this).addClass('chosen');
		$(this).siblings().each(function() {
			$(this).addClass('fade-out');
		chooseFigure(chosenFigure);
		});

		// WYŚLIJ NA SERWER INFO CO WYBRAŁEM
		//setTimeout(showScore,Math.floor(Math.random() * 5000));
	}
});

function chooseFigure(figure) {
	$.ajax({
		url: 			window.location.href,
		type:			'post',
		data:	{
			action: 	'chooseFigure',
			figure:		figure
		},
		success: function (data) {
			if (data['status'] == 'ok') {
				oponentFigure = data['oponentFigure'];
				if (data['oponentScore'] > oponentScore) {
					oponentScore = data['oponentScore'];
					roundScore = -1;
				}
				else if (data['myScore'] > myScore) {
					myScore = data['myScore'];
					roundScore = 1;
				}
				else 
					roundScore = 0;
				showScore(roundScore);
			}
			else {
				showConnectionErrorDialog();
			}
		},
		error: function() {
			showConnectionErrorDialog();
		}
	});
}

function getOponent() {
	$('#waiting-for-oponent-dialog').removeClass('hidden');
	$.ajax({
		url: 			window.location.href,
		type:			'post',
		data:	{
			action: 	'getOponent',
		},
		success: function (data) {
			if (data['status'] == 'ok') {
				opponentFound(data['username']);
			}
			else {
				showConnectionErrorDialog();
			}
		},
		error: function() {
			showConnectionErrorDialog();
		},
		complete: function() {
			$('#waiting-for-oponent-dialog').addClass('hidden');
		}
	});
}
function showConnectionErrorDialog() {
	$('#connection-error-dialog').removeClass('hidden');
	setTimeout(function () {
		$('#connection-error-dialog').addClass('hidden');
		$('#enter-name-dialog').removeClass('hidden');
	}, 4000);
}

function showScore(roundScore) {
	stopTimer();
	$('#round-score-dialog').removeClass('hidden');
	animateScoreDialog();
	var myFigureIcon = $(document.createElement('i')).addClass(figureIcons[chosenFigure]);
	$('#my-figure').html(myFigureIcon);
	// TYLKO NA RAZIE Z BRAKU BACKENDU
	// oponentFigure = figures[Math.floor(Math.random() * 5)];
	// KONIEC
	var oponentFigureIcon = $(document.createElement('i')).addClass(figureIcons[oponentFigure]);
	$('#oponent-figure').html(oponentFigureIcon);
	$('.round-score').children().each(function() {$(this).hide()});
	if (roundScore == 1) {
		$('#you-won').show();
		$('#my-score').text(myScore);
	}
	else if (roundScore == -1) {
		$('#you-lost').show();
		$('#oponent-score').text(oponentScore);
	}
	else {
		$('#draw').show();
	}
	setTimeout(newRound,4000);
}
function newRound() {
	$('#waiting-for-oponent-dialog').removeClass('hidden');
	$.ajax({
		url: 			window.location.href,
		type:			'post',
		data:	{
			action: 	'playerReady',
		},
		success: function (data) {
			if (data['status'] == 'ok') {
				('#round-score-dialog').addClass('hidden');
				chosenFigure = '';
				oponentFigure = '';
				roundScore = '';
				$('.figure').each(function() {
					$(this).attr('class','figure');
				});
				startTimer(15);
			}
			else {
				showConnectionErrorDialog();
			}
		},
		error: function() {
			showConnectionErrorDialog();
		},
		complete: function() {
			$('#waiting-for-oponent-dialog').addClass('hidden');
		}
	});
}

function opponentFound(username) {
	oponentUsername = username;
	$('#oponent-username').text(oponentUsername);
	myScore = 0;
	oponentScore = 0;
	$('#my-score').text(myScore);
	$('#oponent-score').text(oponentScore);
	newRound();
}

function setTimer(seconds) {
	var timeLeft = '00:';
	seconds < 10 ? timeLeft += '0' + seconds : timeLeft += seconds;
	$('#time-left').text(timeLeft);
	seconds > 5 ? $('#time-left').removeClass('hurry-up') : $('#time-left').addClass('hurry-up'); 
	if (seconds == 0 && timerInterval) {
		$('#time-left').removeClass('hurry-up');
		showScore();
	}
}

function startTimer(seconds) {
	setTimer(seconds);
	var secondsLeft = seconds;
	timerInterval = setInterval(function() {setTimer(--secondsLeft);},1000);
}

function stopTimer() {
	window.clearInterval(timerInterval);
}

function animateScoreDialog() {
	$('.round-chosen-figure').addClass('slide');
	$('.versus').addClass('fade');
	setTimeout(function() {
		$('.round-chosen-figure').removeClass('slide');
		$('.versus').removeClass('fade');
	}, 1000);
}