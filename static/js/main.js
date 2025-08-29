document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('cake-form');
  const totalPriceElement = document.getElementById('total-price');

  const updateTotalPrice = () => {
    let totalPrice = 0;

    form.querySelectorAll('input[type="radio"]:checked, input[type="checkbox"]:checked')
      .forEach(el => {
        const price = Number(el.dataset.price || 0);
        if (!Number.isNaN(price)) totalPrice += price;
      });

    totalPriceElement.textContent = `Итого: ${totalPrice.toLocaleString('ru-RU')}₽`;
  };

  updateTotalPrice();
  form.addEventListener('change', updateTotalPrice);
});
