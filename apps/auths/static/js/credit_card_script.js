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