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

function selectDress(dressId) {
    const dressOverlay = document.getElementById('dress-overlay');

    const dressImages = {
        'dress1': '/static/images/black_knotted_h&m_fitted.png'
        // add more dress options here
    };

    dressOverlay.src = dressImages[dressId];
    dressOverlay.classList.remove('hidden');
    document.getElementById('top-overlay').classList.add('hidden');
    document.getElementById('shorts-overlay').classList.add('hidden');
}

function selectTop(topId) {
    const topOverlay = document.getElementById('top-overlay');

    const topImages = {
        'top1': '/static/images/crochet_vest_h&m_fitted.png'
        // add more top options here
    };

    topOverlay.src = topImages[topId];
    topOverlay.classList.remove('hidden');
    document.getElementById('dress-overlay').classList.add('hidden');
}

function selectShorts(shortsId) {
    const shortsOverlay = document.getElementById('shorts-overlay');

    const shortsImages = {
        'shorts1': '/static/images/black_skort_h&m_fitted.png'
        // add more shorts options here
    };

    shortsOverlay.src = shortsImages[shortsId];
    shortsOverlay.classList.remove('hidden');
    document.getElementById('dress-overlay').classList.add('hidden');
}

