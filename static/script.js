// static/script.js

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("answer-form");
  const textarea = document.getElementById("user_output");

  form.addEventListener("submit", (event) => {
    if (textarea.value.trim() === "") {
      event.preventDefault();
      alert("출력 결과를 입력해주세요!");
      textarea.focus();
    }
  });
});
