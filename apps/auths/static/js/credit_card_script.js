function validateForm() {
  var cardNumber = document.getElementById("card_number").value;
  var cardHolder = document.getElementById("card_holder").value;
  var expiryDate = document.getElementById("expiry_date").value;
  var cvv = document.getElementById("cvv").value;

  var errorMessages = "";

  if (cardNumber.length !== 19 || !/^\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}$/.test(cardNumber)) {
      errorMessages += "Неверный номер карты. ";
  }

  if (!/^[a-zA-Z ]+$/.test(cardHolder)) {
      errorMessages += "Неверное имя держателя карты. ";
  }

  if (!/^\d{2}\/\d{2}$/.test(expiryDate)) {
      errorMessages += "Неверный срок действия карты. ";
  }

  if (!/^\d{3}$/.test(cvv)) {
      errorMessages += "Неверный CVV. ";
  }

  var errorContainer = document.getElementById("errorMessages");
  errorContainer.innerHTML = "<p class='error-message'>" + errorMessages + "</p>";

  if (errorMessages === "") {
      document.getElementById("paymentForm").submit();
  }
}

function formatCardNumber() {
  var input = document.getElementById("card_number");
  // Ограничиваем ввод символов
  input.value = input.value.replace(/[^\d]/g, '');
  // Добавляем пробелы после каждых 4 цифр
  input.value = input.value.replace(/(\d{4})/g, '$1 ').trim();
}

function formatExpiryDate() {
  var input = document.getElementById("expiry_date");
  // Ограничиваем ввод символов
  input.value = input.value.replace(/\D/g, '').slice(0, 4);
  // Автоматически добавляем "/"
  if (input.value.length >= 2) {
      input.value = input.value.slice(0, 2) + '/' + input.value.slice(2);
  }
}

// Добавляем обработчики событий input
document.getElementById("card_number").addEventListener("input", formatCardNumber);
document.getElementById("expiry_date").addEventListener("input", formatExpiryDate);

// Ограничиваем ввод символов ccv
document.getElementById("cvv").addEventListener("input", function () {
  this.value = this.value.slice(0, 3);
});
// Ограничиваем ввод символов card_number
document.getElementById("card_number").addEventListener("input", function () {
  this.value = this.value.slice(0, 16 + 3);
});