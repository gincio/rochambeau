var gameId;
var playerId;
var myUsername;
var oponentUsername;
var myScore;
var oponentScore;
var chosenFigure = '';
var oponentFigure = '';
var roundScore = '';
var figures = ['P','R','S','L','K'];
var figureIcons = {
	'P' 	: 'far fa-hand-paper',
	'R' 	: 'far fa-hand-rock',
	'S' 	: 'far fa-hand-scissors',
	'L' 	: 'far fa-hand-lizard',
	'K' 	: 'far fa-hand-spock',
	''		: 'far fa-question-circle'
}
var timerInterval;

$('.figure').on('click', function() {
	if (chosenFigure == '') {
		chosenFigure = $(this).attr('id');
		$(this).addClass('chosen');
		$(this).siblings().each(function() {
			$(this).addClass('fade-out');
		chooseFigure(chosenFigure);
		});
	}
});

$('#start-game').on('click', function() {
	myUsername = $('#player-username').val();
	$('#my-username').text(myUsername);
	console.log('Sending connect request');
	$.ajax({
		url: 			window.location.href,
		type:			'post',
		data:	{
			action: 	'setConnection',
			nick:		myUsername
		},
		success: function (data) {
			if (data['status'] == 'ok') {
				gameId = data['GameId'];
				playerId = data['UserId'];
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

function getOponent() {
	$('#waiting-for-oponent-dialog').removeClass('hidden');
	$.ajax({
		url: 			window.location.href,
		type:			'post',
		data:	{
			action: 	'getOponent',
			GameId: 	gameId,
			UserId: 	playerId
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

function newRound() {
	$('#waiting-for-oponent-dialog').removeClass('hidden');
	$.ajax({
		url: 			window.location.href,
		type:			'post',
		data:	{
			action: 	'playerReady',
			GameId: 	gameId,
			UserId: 	playerId
		},
		success: function (data) {
			if (data['status'] == 'ok') {
				$('#round-score-dialog').addClass('hidden');
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

function chooseFigure(figure) {
	$.ajax({
		url: 			window.location.href,
		type:			'post',
		data:	{
			action: 	'chooseFigure',
			GameId: 	gameId,
			UserId: 	playerId,
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