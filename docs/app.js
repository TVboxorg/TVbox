(() => {
  const root = document.documentElement;
  const toast = document.getElementById("toast");
  const themeToggle = document.getElementById("themeToggle");
  const storageKey = "tvbox-theme";

  const applyTheme = (theme) => {
    if (theme === "dark") {
      root.setAttribute("data-theme", "dark");
    } else {
      root.removeAttribute("data-theme");
    }
  };

  const saved = localStorage.getItem(storageKey);
  if (saved === "dark" || saved === "light") {
    applyTheme(saved);
  }

  themeToggle?.addEventListener("click", () => {
    const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    applyTheme(next);
    localStorage.setItem(storageKey, next);
  });

  let toastTimer = 0;
  const showToast = (message) => {
    if (!toast) return;
    toast.textContent = message;
    toast.hidden = false;
    toast.classList.add("is-on");
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => {
      toast.classList.remove("is-on");
    }, 1400);
  };

  document.querySelectorAll("[data-copy]").forEach((button) => {
    button.addEventListener("click", async () => {
      const target = document.querySelector(button.getAttribute("data-copy"));
      const text = target?.textContent?.trim();
      if (!text) return;
      const original = button.textContent;

      try {
        await navigator.clipboard.writeText(text);
        button.textContent = "已复制";
        showToast("已复制订阅地址");
      } catch {
        const range = document.createRange();
        range.selectNodeContents(target);
        const selection = window.getSelection();
        selection?.removeAllRanges();
        selection?.addRange(range);
        button.textContent = "请手动复制";
        showToast("请手动复制选中内容");
      }

      window.setTimeout(() => {
        button.textContent = original;
      }, 1600);
    });
  });
})();
