export async function initSearch() {
  const dialog = document.querySelector<HTMLDialogElement>("[data-search-dialog]");
  const openButton = document.querySelector<HTMLButtonElement>("[data-search-open]");
  const closeButton = document.querySelector<HTMLButtonElement>("[data-search-close]");
  const input = document.querySelector<HTMLInputElement>("#site-search");
  const results = document.querySelector<HTMLElement>("[data-search-results]");
  if (!dialog || !openButton || !closeButton || !input || !results) return;

  let topics: Array<{ type: string; label: string; title: string; description: string; href: string; search: string }> = [];

  const render = (query = "") => {
    const normalized = query.trim().toLowerCase();
    const matches = topics
      .filter((topic) => !normalized || topic.search.toLowerCase().includes(normalized))
      .slice(0, 8);

    results.innerHTML = matches.length
      ? matches
          .map(
            (topic) => `
              <a href="${topic.href}">
                <span>${topic.label}</span>
                <div><strong>${topic.title}</strong><small>${topic.description}</small></div>
                <b>↗</b>
              </a>`
          )
          .join("")
      : `<p class="search-empty">일치하는 전략 질문이 없습니다.</p>`;
  };

  const open = async () => {
    dialog.showModal();
    if (!topics.length) topics = await fetch("/api/search.json").then((response) => response.json());
    render(input.value);
    requestAnimationFrame(() => input.focus());
  };

  openButton.addEventListener("click", open);
  closeButton.addEventListener("click", () => dialog.close());
  input.addEventListener("input", () => render(input.value));
  dialog.addEventListener("click", (event) => event.target === dialog && dialog.close());
  document.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      open();
    }
  });
}
