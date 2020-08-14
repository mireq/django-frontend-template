(function() {

if (window.XMLHttpRequest === undefined || window.DOMParser === undefined) {
	return;
}

var html;
var errorContainer;

function hideError() {
	if (errorContainer !== undefined) {
		errorContainer.remove();
		errorContainer = undefined;
	}
}


function showError(msg) {
	if (errorContainer === undefined) {
		errorContainer = document.createElement('pre');
		errorContainer.className = 'scss-error';
		document.body.appendChild(errorContainer);
	}
	errorContainer.innerHTML = '';
	errorContainer.appendChild(document.createTextNode(msg));
}


function refresh() {
	var xhr = new XMLHttpRequest();
	var parser, doc;
	xhr.onreadystatechange = function () {
		if (xhr.readyState === XMLHttpRequest.DONE) {
			if (xhr.status >= 200 && xhr.status < 300) {
				hideError();
				parser = new DOMParser();
				doc = parser.parseFromString(xhr.responseText, "text/html");
				var newStyles = [];
				var links, element, i, leni, j, lenj, href, newHref;
				links = doc.getElementsByTagName('link');
				for (i = 0, leni = links.length; i < leni; i++) {
					element = links[i];
					if (element.getAttribute('rel') === 'stylesheet') {
						newStyles.push(element);
					}
				}

				links = document.getElementsByTagName('link');
				for (i = 0, leni = links.length; i < leni; i++) {
					element = links[i];
					if (element.getAttribute('rel') === 'stylesheet') {
						href = element.getAttribute('href');
						if (href.match(/\/static\/CACHE\/css\/.*\.css/)) {
							for (j = 0, lenj = newStyles.length; j < lenj; j++) {
								newHref = newStyles[j].getAttribute('href');
								if (newHref.match(/\/static\/CACHE\/css\/.*\.css/)) {
									element.setAttribute('href', newHref);
								}
							}
						}
					}
				}
			}
			else if (xhr.status === 500) {
				parser = new DOMParser();
				doc = parser.parseFromString(xhr.responseText, "text/html");
				var errorMessage = doc.querySelector('.errormsg');
				if (errorMessage === undefined) {
					hideError();
				}
				else {
					showError(errorMessage.innerText);
				}
			}
		}
	};
	xhr.open('GET', '/style/');
	xhr.send();
	document.body.classList.add('autoreload');
}

setInterval(refresh, 1000);

}());
