let mybutton = document.getElementById("backToTop");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

async function loadOptions() {
  const coffeeTypes = await fetch('coffeeTypes.json').then(res => res.json());
  const milks = await fetch('milks.json').then(res => res.json());
  const creams = await fetch('flavors.json').then(res => res.json());
  const sweeteners = await fetch('sweeteners.json').then(res => res.json());
  const sizes = await fetch('cupSizes.json').then(res => res.json());

  populateOptions(coffeeTypes, 'coffee-type');
  populateOptions(milks, 'milk-option');
  populateOptions(creams, 'cream-flavors');
  populateOptions(sweeteners, 'sweetener');
  populateOptions(sizes, 'cup-size');
}

function populateOptions(data, sectionId) {
  const section = document.getElementById(sectionId);
  section.innerHTML = data.map(item => `
    <div class="option">
      <input type="radio" name="${sectionId}" value="${item.name}" />
      <label>${item.name} ($${item.price})</label>
    </div>
  `).join('');
}

function submitOrder() {
  const selectedCoffee = document.querySelector('input[name="coffee-type"]:checked')?.value;
  const selectedMilk = document.querySelector('input[name="milk-option"]:checked')?.value;
  const selectedCream = document.querySelector('input[name="cream-flavors"]:checked')?.value;
  const selectedSweetener = document.querySelector('input[name="sweetener"]:checked')?.value;
  const selectedSize = document.querySelector('input[name="cup-size"]:checked')?.value;

  document.getElementById('order-summary').innerText =
    `Your Order: ${selectedCoffee} with ${selectedMilk}, ${selectedCream}, ${selectedSweetener}, in a ${selectedSize} cup.`;
}

window.onload = loadOptions;
