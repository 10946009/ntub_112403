document.addEventListener("DOMContentLoaded", function() {
  const deleteIcons = document.querySelectorAll(".delete-icon");

  deleteIcons.forEach(icon => {
    icon.addEventListener("click", function() {
      const card = this.closest(".card");
      card.classList.add("shake");

      // 移除抖動效果以重置動畫
      setTimeout(() => {
        card.classList.remove("shake");
      }, 500); // 等待抖動動畫完成
    });
  });
});