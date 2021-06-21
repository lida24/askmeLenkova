const btns = document.querySelectorAll('.vote-btn');
btns.forEach(btn => {
  btn.addEventListener('click', function() {
    const direction = this.dataset.direction;
    const inp = this.parentElement
      .querySelector('.vote-count');
    const currentValue = +inp.value;
    let newValue;

    if (direction === 'plus') {
      newValue = currentValue + 1;
    } else {
      newValue = currentValue - 1;
    }
    inp.value = newValue;
  })
})
