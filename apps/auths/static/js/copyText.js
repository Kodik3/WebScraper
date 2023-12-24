var copyButton = document.getElementById("copyButton");

function copyToClipboard(e) {
    e.preventDefault();
    /* Получаем текст, который нужно скопировать */
    var copyText = document.getElementById("rData");
    /* Выделяем текст внутри элемента */
    copyText.select();
    /* Копируем выделенный текст в буфер обмена */
    document.execCommand("copy");
}

copyButton.addEventListener("click", copyToClipboard)