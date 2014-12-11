$(document).ready(function() {

	var COLORS = [
		'#38f', '#92b', '#aa8', '#d9b', '#38a', '#77c', '#fed',
		'#deadbf', '#31994', '#90210',
	];

	var SLIDESHOW_PAUSE = 10 * 1000;

	var FONTS = [
		['Chicle'],
		['Bubblegum Sans'],
		['Londrina Solid'],
		['Waiting for the Sunrise'],
		['Pacifico'],
		['Bangers'],
		['Boogaloo'],
		['PassionOne']
	];

	var slideshow = true;
	var State = {
		'index': 0
	};

	$.getJSON('poetry.json', function(data) {
		if (!data || !data.length) {
			console.error('No poetry served.');
			return;
		}

		try {
			if (window.location.href.match(/id=\S+$/)) {
				var currentState = window.location.href.replace(/^.*?id=/, '');
				var state = JSON.parse(decodeURIComponent(currentState));
				if (typeof state == 'object') {
					State = state;
					slideshow = false;
				}
			}
		} catch(e) {throw e}

		var poetry = data;
		render_();
		if (slideshow) setTimeout(update_, SLIDESHOW_PAUSE);

		$('body').click(function() {
			if (!slideshow) {
				slideshow = true;
				update_();
			} else {
				slideshow = false;
			}
		});

		function update_() {
			for (var key in State) {
				State[key] = null;
			}
			State['index'] = Math.floor(Math.random() * poetry.length);
			render_();
		}

		function render_() {
			var image = poetry[State['index']]['image'];
			var url = makeURL_(image);
			var sentences = poetry[State['index']]['sentences'];
			var img = new Image();
			img.src = url;
			img.onload = function() {
				$('#image').attr('src', url);
				var font = State['font'] || getFont_();
				var color = State['color'] || getColor_();
				var size = State['size'] || Math.floor(Math.random() * 4) + 4;
				var align = State['align'] || choice_(['left', 'center', 'right']);
				var padding = State['padding'] || (Math.random() + 0.5);
				var doit = function(id, text) {
					$('#'+id).
						text(text).
						css('font-family', font[0]).
						css('font-size', size + 'em').
						css('text-align', align).
						css('color', color);
				}
				$('body').css('padding', padding + 'em');
				doit('line-1', sentences[0]);
				doit('line-2', sentences[1]);

				State['font'] = font;
				State['color'] = color;
				State['size'] = size;
				State['padding'] = padding;
				State['align'] = align;
				window.history.replaceState(null,
						"Permutation Poetry",
						"?id=" + encodeURIComponent(JSON.stringify(State)));

				if (slideshow) setTimeout(update_, SLIDESHOW_PAUSE);

			}
		}

		function choice_(a) {
			return a[Math.floor(Math.random() * a.length)];
		}

		function getColor_() {
			return choice_(COLORS);
		}

		function getFont_() {
			return choice_(FONTS);
		}

		function makeURL_(image) {
			return [
				'https://farm',
				image.farm,
				'.staticflickr.com/',
				image.server,
				'/',
				image.id, '_', image.secret, '_b.jpg'
			].join('');
		}
	});

	function shuffle_(data) {
		for (var i = data.length-1; i > 0; i--) {
			var s = Math.floor(Math.random() * (i + 1));
			if (s != i) {
				var t = data[s];
				data[s] = data[i];
				data[i] = t;
			}
		}
		return data;
	}


});
