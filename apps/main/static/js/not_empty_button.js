var url_input = document.getElementById('url_input');
var button = document.getElementById('take_url_button');

url_input.addEventListener('input', function() {
    if (url_input.value.length > 0) {
        button.style.display = 'block';
    } else {
        button.style.display = 'none';
    }
});
