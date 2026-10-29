(() => {
  "use strict";

  function initWorkFilters() {
    const tools = document.getElementById("work-tools");
    const count = document.getElementById("work-count");
    const projects = Array.from(document.querySelectorAll("#work article[data-category]"));
    const buttons = tools ? Array.from(tools.querySelectorAll("button[data-filter]")) : [];
    const search = document.getElementById("project-search");
    const total = document.getElementById("project-total");
    const empty = document.getElementById("empty-results");
    const reset = document.getElementById("reset-projects");

    if (!tools || !projects.length || !buttons.length) return;

    let activeFilter = "all";
    const searchable = projects.map((project) =>
      project.querySelector(".work-body").textContent.toLocaleLowerCase());
    if (total) total.textContent = projects.length;

    function applyFilter(filter) {
      activeFilter = filter;
      let visibleCount = 0;
      const terms = (search ? search.value : "").trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);

      projects.forEach((project, index) => {
        const categories = (project.dataset.category || "").split(/\s+/);
        const matches = (filter === "all" || categories.includes(filter)) &&
          terms.every((term) => searchable[index].includes(term));
        project.hidden = !matches;
        if (matches) visibleCount += 1;
      });

      buttons.forEach((button) => {
        button.setAttribute("aria-pressed", String(button.dataset.filter === filter));
      });

      if (count) {
        count.textContent = `${visibleCount} of ${projects.length} projects`;
      }
      if (empty) empty.hidden = visibleCount !== 0;
    }

    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        applyFilter(button.dataset.filter || "all");
      });
    });
    if (search) search.addEventListener("input", () => applyFilter(activeFilter));
    if (reset) reset.addEventListener("click", () => {
      if (search) search.value = "";
      applyFilter("all");
      if (search) search.focus();
    });

    applyFilter("all");
    tools.hidden = false;
  }

  function initReadingPosition() {
    if (!("IntersectionObserver" in window)) return;

    const links = Array.from(document.querySelectorAll('.primary-nav a[href^="#"]'));
    const sections = links
      .map((link) => document.getElementById(link.getAttribute("href").slice(1)))
      .filter(Boolean);
    const hero = document.querySelector(".hero");
    if (!sections.length) return;

    let observer;
    let resizeFrame = 0;
    let currentId = null;

    function getReadingLine() {
      const height = Math.max(1, window.innerHeight);
      const scrollPadding = parseFloat(window.getComputedStyle(document.documentElement).scrollPaddingTop) || 0;
      const preferredLine = Math.min(180, Math.max(96, height * 0.22));
      return Math.min(height - 1, Math.max(preferredLine, scrollPadding + 1));
    }

    function setCurrent(id) {
      if (id === currentId) return;
      currentId = id;

      links.forEach((link) => {
        if (link.getAttribute("href") === `#${id}`) {
          link.setAttribute("aria-current", "location");
        } else {
          link.removeAttribute("aria-current");
        }
      });
    }

    function updateCurrent() {
      const readingLine = getReadingLine();
      const heroBounds = hero ? hero.getBoundingClientRect() : null;

      if (heroBounds && heroBounds.bottom > readingLine) {
        setCurrent("");
        return;
      }

      const atEnd = window.scrollY > 0 &&
        window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 3;
      if (atEnd) {
        setCurrent(sections[sections.length - 1].id);
        return;
      }

      let activeId = "";
      sections.forEach((section) => {
        if (section.getBoundingClientRect().top <= readingLine + 1) {
          activeId = section.id;
        }
      });
      setCurrent(activeId);
    }

    function observeSections() {
      if (observer) observer.disconnect();

      const height = window.innerHeight;
      const readingLine = getReadingLine();
      const bottomMargin = Math.max(0, height - readingLine - 1);

      observer = new IntersectionObserver(updateCurrent, {
        rootMargin: `-${readingLine}px 0px -${bottomMargin}px 0px`,
        threshold: 0
      });

      sections.forEach((section) => observer.observe(section));
      if (hero) observer.observe(hero);
      updateCurrent();
    }

    observeSections();

    window.addEventListener("resize", () => {
      if (resizeFrame) window.cancelAnimationFrame(resizeFrame);
      resizeFrame = window.requestAnimationFrame(() => {
        resizeFrame = 0;
        observeSections();
      });
    });

    // A short final section may never reach the reading line.
    // Keep its navigation state accurate when the page reaches its end.
    window.addEventListener("scroll", () => {
      const atEnd = window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 3;
      if (atEnd || currentId === sections[sections.length - 1].id) {
        updateCurrent();
      }
    }, { passive: true });
  }

  function initCoverViewer() {
    const viewer = document.getElementById("cover-viewer");
    if (!viewer || typeof viewer.showModal !== "function") return;
    const image = viewer.querySelector("img");
    const title = document.getElementById("cover-viewer-title");
    const caption = document.getElementById("cover-viewer-caption");
    const close = viewer.querySelector("button");
    let opener = null;

    document.querySelectorAll(".cover-link").forEach((link) => {
      link.setAttribute("aria-label", `Enlarge cover: ${link.closest("article").querySelector("h3").textContent}`);
      link.setAttribute("aria-haspopup", "dialog");
      link.addEventListener("click", (event) => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        opener = link;
        const source = link.querySelector("img");
        image.src = source.src;
        image.alt = source.alt;
        title.textContent = link.closest("article").querySelector("h3").textContent;
        caption.textContent = Array.from(link.closest("figure").querySelector("figcaption").children)
          .map((part) => part.textContent).join(" · ");
        viewer.showModal();
        close.focus();
      });
    });
    close.addEventListener("click", () => viewer.close());
    viewer.addEventListener("click", (event) => {
      if (event.target !== viewer) return;
      const box = viewer.getBoundingClientRect();
      if (event.clientX < box.left || event.clientX > box.right ||
          event.clientY < box.top || event.clientY > box.bottom) viewer.close();
    });
    viewer.addEventListener("close", () => {
      if (opener && opener.isConnected) opener.focus();
    });
  }

  function init() {
    initWorkFilters();
    initReadingPosition();
    initCoverViewer();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
