document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".filter-btn");
  const cards = document.querySelectorAll(".product-card");
  const search = document.getElementById("searchInput");
  const message = document.getElementById("cartMessage");
  let filter = "Tous";
  function refresh() {
    const query = (search?.value || "").trim().toLowerCase();
    cards.forEach(card => {
      card.hidden = !((filter === "Tous" || card.dataset.category === filter) &&
        (card.dataset.name || "").includes(query));
    });
  }
  buttons.forEach(button => button.addEventListener("click", () => {
    buttons.forEach(item => item.classList.remove("selected"));
    button.classList.add("selected");
    filter = button.dataset.filter || "Tous";
    refresh();
  }));
  search?.addEventListener("input", refresh);
  document.querySelectorAll(".add-btn").forEach(button => button.addEventListener("click", () => {
    const cart = JSON.parse(localStorage.getItem("bl-cart") || "[]");
    cart.push({name:button.dataset.name, price:Number(button.dataset.price || 0)});
    localStorage.setItem("bl-cart", JSON.stringify(cart));
    if (message) message.textContent = button.dataset.name + " ajouté à votre sélection (" + cart.length + " article(s)).";
  }));
});
