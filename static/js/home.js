// Js for flip cards in feature engineering section

    document.querySelectorAll('.flip-card').forEach(card => {
        card.addEventListener('click', () => {
            card.querySelector('.flip-card-inner').classList.toggle('flipped');
        });
    });

