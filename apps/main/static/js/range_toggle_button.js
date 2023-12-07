var toggle_range = document.getElementById('toggle_range'),
    range_text = document.getElementById('range_text'),
    range = document.getElementById('range'),
    range_values = document.getElementsByClassName('range_value'),
    is_range = document.getElementById('is_range_value'),
    to_range = document.getElementById('to');


var isRangeVisible = false;

function find_range() {
    if (isRangeVisible) {
        range_text.style.display = 'none';
        range.style.display = 'none';
        to_range.value = 0;
        is_range.value = 'False';

        for (var i = 0; i < range_values.length; i++) {
            range_values[i].style.display = 'none';
        }
        toggle_range.textContent = 'Несколько страниц';
    } 
    else {
        range_text.style.display = 'block';
        range.style.display = 'flex';
        to_range.value = 1;
        is_range.value = 'True';

        for (var i = 0; i < range_values.length; i++) {
            range_values[i].style.display = 'block';
        }

        toggle_range.textContent = 'Скрыть диапазон';
    }
    isRangeVisible = !isRangeVisible;
}

toggle_range.addEventListener('click', find_range);