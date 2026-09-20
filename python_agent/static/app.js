document.addEventListener('DOMContentLoaded', () => {
  const tabButtons = document.querySelectorAll('.tab-button');
  const panels = document.querySelectorAll('.tab-panel');

  tabButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const target = button.dataset.target;

      tabButtons.forEach((btn) => btn.classList.toggle('active', btn === button));
      panels.forEach((panel) => {
        panel.classList.toggle('active', panel.id === target);
      });
    });
  });
});
