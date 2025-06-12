let cartList = []
let selectedDress = null
let selectedTop = null
let selectedShorts = null

var modal = document.getElementById("myModal");
var btn = document.getElementById("cart-button");

// when the user clicks anywhere outside of modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function navBar() {
    
}

// Load cart from localStorage
function loadCartFromLocalStorage() {
  const stored = localStorage.getItem('cart');
  if (stored) {
    cartList = JSON.parse(stored);
  } else {
    cartList = [];
  }
}

// Save cart to localStorage
function saveCartToLocalStorage() {
  localStorage.setItem('cart', JSON.stringify(cartList));
}

function dresses() {
    const dressContainer = document.getElementById('dress-options');
    const topsContainer = document.getElementById('top-options');
    const shortsContainer = document.getElementById('shorts-options');

    dressContainer.classList.toggle('hidden');
    topsContainer.classList.add('hidden');
    shortsContainer.classList.add('hidden');
}

function tops() {
    const dressContainer = document.getElementById('dress-options');
    const topsContainer = document.getElementById('top-options');
    const shortsContainer = document.getElementById('shorts-options');

    topsContainer.classList.toggle('hidden');
    dressContainer.classList.add('hidden');
    shortsContainer.classList.add('hidden');
}

function shorts() {
    const dressContainer = document.getElementById('dress-options');
    const topsContainer = document.getElementById('top-options');
    const shortsContainer = document.getElementById('shorts-options');

    shortsContainer.classList.toggle('hidden');
    dressContainer.classList.add('hidden');
    topsContainer.classList.add('hidden');
}

function hideAllOptions() {
    document.getElementById('dress-options').classList.add('hidden');
    document.getElementById('top-options').classList.add('hidden');
    document.getElementById('shorts-options').classList.add('hidden');
}

function selectDress(dressId) {
    selectedTop = null;
    selectedShorts = null;
    const dressImages = {
        'dress1': '/static/images/black_knotted_h&m_fitted.png'
    };

    const dress = {
        image: dressImages[dressId],
        name: "Black Knotted Dress",
        price: 29.99,
        quantity: 1
    };

    const dressOverlay = document.getElementById('dress-overlay');
    const overlayWrapper = document.getElementById('dress-overlay-wrapper');

    dressOverlay.src = dress.image;
    overlayWrapper.classList.remove('hidden');
    dressOverlay.classList.remove('hidden');

    selectedDress = dress;

    document.getElementById('top-overlay').classList.add('hidden');
    document.getElementById('shorts-overlay').classList.add('hidden');

    hideAllOptions();
}



function selectTop(topId) {
    selectedDress = null;
    const topImages = {
        'top1': '/static/images/crochet_vest_h&m_fitted.png'
        // add more top options here
    };

    const top = {
        image: topImages[topId],
        name: "Crochet Vest",
        price: 29.99,
        quantity: 1
    };

    const topOverlay = document.getElementById('top-overlay');
    const overlayWrapper = document.getElementById('top-overlay-wrapper')

    topOverlay.src = top.image;
    overlayWrapper.classList.remove('hidden');
    topOverlay.classList.remove('hidden');

    selectedTop = top;

    document.getElementById('dress-overlay').classList.add('hidden');

    hideAllOptions();
}

function selectShorts(shortsId) {
    selectedDress = null;
    const shortsOverlay = document.getElementById('shorts-overlay');

    const shortsImages = {
        'shorts1': '/static/images/black_skort_h&m_fitted.png'
        // add more shorts options here
    };

    const shorts = {
        image: shortsImages[shortsId],
        name: "black skort",
        price: 29.99,
        quantity: 1
    }

    const overlayWrapper = document.getElementById('shorts-overlay-wrapper')

    shortsOverlay.src = shorts.image;
    overlayWrapper.classList.remove('hidden');
    shortsOverlay.classList.remove('hidden');

    selectedShorts = shorts;

    document.getElementById('dress-overlay').classList.add('hidden');
    hideAllOptions();
}

function openModal() {
  const container = document.getElementById('checkboxContainer');
  listOfOps = []
  options = []

  // Clear any previous checkboxes
  container.innerHTML = '';

  // Define your checkbox options
  if (selectedDress) {
    listOfOps.push(selectedDress);
  }
  if (selectedTop) {
    listOfOps.push(selectedTop);
  }
  if (selectedShorts) {
    listOfOps.push(selectedShorts)
  }

  for (let i = 0; i < listOfOps.length; i++) {
    options.push({id: 'chk[i]', label: listOfOps[i].name, value: i})
  }

  // Add checkboxes to container
  options.forEach(opt => {
    // Create checkbox input
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = opt.id;
    checkbox.value = opt.value;

    // Create label for checkbox
    const label = document.createElement('label');
    label.htmlFor = opt.id;
    label.textContent = opt.label;

    // Append checkbox and label to container with a line break
    container.appendChild(checkbox);
    container.appendChild(label);
    container.appendChild(document.createElement('br'));
  });

  // Show the modal
  document.getElementById('myModal').style.display = 'block';
}


function addToCart() {
    let itemToAdd = [];

    if (selectedDress) {
        itemToAdd.push(selectedDress);
    }
    if (selectedTop) {
        itemToAdd.push(selectedTop);
    } 
    if (selectedShorts) {
        itemToAdd.push(selectedShorts);
    }

    if (itemToAdd.length == 0) {
        alert('Nothing selected');
        return;
    }

    for (let i = 0; i < itemToAdd.length; i++) {
        const existingItem = cartList.find(cartItem => cartItem.name === itemToAdd[i].name);

        if (existingItem) {
            existingItem.quantity = (existingItem.quantity || 1) + 1;
        } else {
            // Make sure quantity is initialized to 1
            cartList.push({ ...itemToAdd[i], quantity: 1 });
        }
    }
    saveCartToLocalStorage();
    
}


function renderCart() {
  console.log("rendering cart")
  loadCartFromLocalStorage(); 
  const container = document.getElementById('cart-items');
  const subtotalElem = document.getElementById('subtotal');

  if (!container || !subtotalElem) {
    // Not on the cart page — exit silently
    return;
  }

  if (!cartList || cartList.length === 0) {
    container.innerHTML = "<p>Your cart is empty.</p>";
    subtotalElem.textContent = "";
    return;
  }

  let subtotal = 0;
  container.innerHTML = ""; // Clear previous content

  cartList.forEach(item => {
    subtotal += item.price * item.quantity;

    const itemDiv = document.createElement('div');
    itemDiv.classList.add('cart-item');
    itemDiv.style.display = "flex";
    itemDiv.style.alignItems = "center";
    itemDiv.style.marginBottom = "20px";
    itemDiv.style.borderBottom = "1px solid #ccc";
    itemDiv.style.paddingBottom = "15px";

    itemDiv.innerHTML = `
      <img src="${item.image}" alt="${item.name}" style="width: 120px; height: 120px; object-fit: contain; margin-right: 20px;">
      <div>
        <div style="font-weight: bold; font-size: 1.2em;">${item.name}</div>
        <div>Quantity: ${item.quantity}</div>
        <div style="font-weight: bold; font-size: 1.1em;">$${(item.price * item.quantity).toFixed(2)}</div>
      </div>
    `;

    container.appendChild(itemDiv);
  });

  subtotalElem.textContent = `Subtotal: $${subtotal.toFixed(2)}`;
}

// Run this function when page loads
document.addEventListener('DOMContentLoaded', renderCart);