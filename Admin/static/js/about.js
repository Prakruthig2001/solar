document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#passwordForm");
    if (form) {
      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const response = await fetch("/change_password", {
          method: "POST",
          body: formData,
        });
  
        const text = await response.text();
        document.querySelector("#feedback").innerHTML = text;
      });
    }
  });
  