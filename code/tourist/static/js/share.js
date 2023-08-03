
  const toggleHeartCheckboxes = document.querySelectorAll('.toggle-heart-checkbox');

  toggleHeartCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
      const isChecked = checkbox.checked;
      if (isChecked) {
        checkbox.parentElement.classList.add('active');
      } else {
        checkbox.parentElement.classList.remove('active');
      }
    });
  });





