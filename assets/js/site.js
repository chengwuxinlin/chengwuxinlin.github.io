(function () {
	const projects = Array.isArray(window.PROJECTS_DATA) ? window.PROJECTS_DATA : [];
	const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
	const themeStorageKey = "wc-theme-v2";
	let refreshFieldPalette = null;

	const state = {
		track: "All",
		query: ""
	};

	function slugify(value) {
		return String(value)
			.trim()
			.toLowerCase()
			.replace(/[^a-z0-9]+/g, "-")
			.replace(/^-+|-+$/g, "");
	}

	function safeDate(value) {
		const date = new Date(value);
		return Number.isNaN(date.getTime()) ? null : date;
	}

	function formatDate(date) {
		return new Intl.DateTimeFormat("en-US", {
			year: "numeric",
			month: "long",
			day: "numeric"
		}).format(date);
	}

	function getStoredTheme() {
		try {
			const stored = window.localStorage.getItem(themeStorageKey);
			return stored === "light" || stored === "dark" ? stored : null;
		} catch (error) {
			return null;
		}
	}

	function resolveTheme() {
		const stored = getStoredTheme();
		if (stored) {
			return stored;
		}

		return "light";
	}

	function updateThemeToggle(theme) {
		const toggle = document.getElementById("themeToggle");
		if (!toggle) {
			return;
		}

		const nextLabel = theme === "dark" ? "Light mode" : "Dark mode";
		toggle.textContent = nextLabel;
		toggle.setAttribute("aria-label", `Switch to ${nextLabel.toLowerCase()}`);
	}

	function applyTheme(theme) {
		document.body.classList.remove("theme-dark", "theme-light");
		document.body.classList.add(`theme-${theme}`);
		updateThemeToggle(theme);

		if (typeof refreshFieldPalette === "function") {
			refreshFieldPalette();
		}
	}

	function initTheme() {
		applyTheme(resolveTheme());

		const toggle = document.getElementById("themeToggle");
		if (toggle) {
			toggle.addEventListener("click", () => {
				const nextTheme = document.body.classList.contains("theme-dark") ? "light" : "dark";

				try {
					window.localStorage.setItem(themeStorageKey, nextTheme);
				} catch (error) {
					// Ignore storage failures and still apply the theme for the session.
				}

				applyTheme(nextTheme);
			});
		}

		const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
		const handleSystemThemeChange = () => {
			if (!getStoredTheme()) {
				applyTheme(resolveTheme());
			}
		};

		if (typeof mediaQuery.addEventListener === "function") {
			mediaQuery.addEventListener("change", handleSystemThemeChange);
		} else if (typeof mediaQuery.addListener === "function") {
			mediaQuery.addListener(handleSystemThemeChange);
		}
	}

	async function readLastModified(path, fallbackDate) {
		const requests = [
			() => fetch(path, { method: "HEAD", cache: "no-store" }),
			() => fetch(path, { cache: "no-store" })
		];

		for (const runRequest of requests) {
			try {
				const response = await runRequest();
				if (!response.ok) {
					continue;
				}

				const header = response.headers.get("last-modified");
				const parsed = safeDate(header);
				if (parsed) {
					return parsed;
				}
			} catch (error) {
				continue;
			}
		}

		return fallbackDate;
	}

	async function syncUpdatedDates() {
		const pageDate = safeDate(document.lastModified);
		const [cvDate, projectDate] = await Promise.all([
			readLastModified("chengwuCVgithub.pdf", pageDate),
			readLastModified("assets/js/projects-data.js", pageDate)
		]);

		const cvNode = document.getElementById("cvLastUpdated");
		const projectNode = document.getElementById("projectsLastUpdated");

		if (cvNode) {
			cvNode.textContent = cvDate ? formatDate(cvDate) : "Latest deployment";
		}

		if (projectNode) {
			projectNode.textContent = projectDate ? formatDate(projectDate) : "Latest deployment";
		}
	}

	function createProjectArt(project) {
		const art = document.createElement("div");
		art.className = "project-art";

		if (project.image) {
			const image = document.createElement("img");
			image.src = project.image;
			image.alt = `${project.title} preview`;
			art.appendChild(image);
			return art;
		}

		art.classList.add("project-art--placeholder");

		const label = document.createElement("span");
		label.className = "project-art-label";
		label.textContent = project.artLabel || project.track;
		art.appendChild(label);
		return art;
	}

	function createProjectLinks(project) {
		if (!Array.isArray(project.links) || project.links.length === 0) {
			return null;
		}

		const links = document.createElement("div");
		links.className = "project-links";

		project.links.forEach((link) => {
			const anchor = document.createElement("a");
			anchor.className = "project-link";
			anchor.href = link.url;
			anchor.textContent = link.label;
			anchor.target = "_blank";
			anchor.rel = "noreferrer";
			links.appendChild(anchor);
		});

		return links;
	}

	function createProjectCard(project) {
		const card = document.createElement("article");
		const trackSlug = slugify(project.track);
		card.className = "project-card";
		card.dataset.track = trackSlug;

		if (project.featured) {
			card.classList.add("is-featured");
		}

		card.appendChild(createProjectArt(project));

		const body = document.createElement("div");
		body.className = "project-body";

		const meta = document.createElement("div");
		meta.className = "project-meta";

		const track = document.createElement("span");
		track.className = `project-pill project-pill--track-${trackSlug}`;
		track.textContent = project.track;
		meta.appendChild(track);

		const venue = document.createElement("span");
		venue.className = "project-pill";
		venue.textContent = project.venue;
		meta.appendChild(venue);

		const title = document.createElement("h3");
		title.className = "project-title";
		title.textContent = project.title;

		const impact = document.createElement("p");
		impact.className = "project-impact";
		impact.textContent = project.impact;

		const summary = document.createElement("p");
		summary.className = "project-summary";
		summary.textContent = project.summary;

		const tags = document.createElement("div");
		tags.className = "project-tags";

		(project.tags || []).forEach((item) => {
			const tag = document.createElement("span");
			tag.className = "tag";
			tag.textContent = item;
			tags.appendChild(tag);
		});

		body.append(meta, title, impact, summary, tags);

		const links = createProjectLinks(project);
		if (links) {
			body.appendChild(links);
		}

		card.appendChild(body);
		return card;
	}

	function matchesProject(project) {
		const trackMatch = state.track === "All" || project.track === state.track;
		if (!trackMatch) {
			return false;
		}

		const query = state.query.trim().toLowerCase();
		if (!query) {
			return true;
		}

		const haystack = [
			project.title,
			project.track,
			project.venue,
			project.impact,
			project.summary,
			...(project.tags || [])
		]
			.join(" ")
			.toLowerCase();

		return haystack.includes(query);
	}

	function renderProjectCount(count) {
		const projectCount = document.getElementById("projectCount");
		if (!projectCount) {
			return;
		}

		projectCount.textContent = `${count} selected project${count === 1 ? "" : "s"}`;
	}

	function renderProjects() {
		const grid = document.getElementById("projectGrid");
		const emptyState = document.getElementById("projectEmptyState");
		if (!grid || !emptyState) {
			return;
		}

		grid.innerHTML = "";
		const filteredProjects = projects.filter(matchesProject);
		renderProjectCount(filteredProjects.length);

		if (filteredProjects.length === 0) {
			emptyState.hidden = false;
			return;
		}

		emptyState.hidden = true;
		filteredProjects.forEach((project) => {
			grid.appendChild(createProjectCard(project));
		});
	}

	function renderFilters() {
		const filters = document.getElementById("projectFilters");
		if (!filters) {
			return;
		}

		const tracks = ["All", ...new Set(projects.map((project) => project.track))];
		filters.innerHTML = "";

		tracks.forEach((trackName) => {
			const button = document.createElement("button");
			button.type = "button";
			button.className = "filter-button";
			if (trackName === state.track) {
				button.classList.add("is-active");
			}
			button.textContent = trackName;
			button.addEventListener("click", () => {
				state.track = trackName;
				renderFilters();
				renderProjects();
			});
			filters.appendChild(button);
		});
	}

	function initProjectSearch() {
		const search = document.getElementById("projectSearch");
		if (!search) {
			return;
		}

		search.addEventListener("input", (event) => {
			state.query = event.target.value || "";
			renderProjects();
		});
	}

	function initProjectSection() {
		renderFilters();
		initProjectSearch();
		renderProjects();
	}

	function initReveal() {
		const nodes = document.querySelectorAll(".reveal");
		if (prefersReducedMotion || !("IntersectionObserver" in window)) {
			nodes.forEach((node) => node.classList.add("is-visible"));
			return;
		}

		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (!entry.isIntersecting) {
						return;
					}

					entry.target.classList.add("is-visible");
					observer.unobserve(entry.target);
				});
			},
			{ threshold: 0.16 }
		);

		nodes.forEach((node) => observer.observe(node));
	}

	function initNeuralField() {
		const canvas = document.getElementById("neuralField");
		if (!canvas) {
			return;
		}

		const context = canvas.getContext("2d");
		if (!context) {
			return;
		}

		function getThemeValue(name, fallback) {
			const value = getComputedStyle(document.body).getPropertyValue(name).trim();
			return value || fallback;
		}

		const pointer = { x: 0, y: 0, active: false };
		let width = 0;
		let height = 0;
		let dpr = 1;
		let points = [];
		let animationFrame = null;
		let fieldPalette = {
			line: "rgba(110, 165, 242, 0.2)",
			node: "rgba(239, 247, 252, 0.9)",
			glow: "rgba(88, 205, 182, 0.08)",
			contours: []
		};

		function makePoints() {
			const count = Math.max(22, Math.min(48, Math.round(width / 34)));
			points = Array.from({ length: count }, () => ({
				originX: Math.random() * width,
				originY: Math.random() * height,
				orbit: 16 + Math.random() * 72,
				phase: Math.random() * Math.PI * 2,
				speed: 0.15 + Math.random() * 0.5,
				radius: 1.1 + Math.random() * 2,
				tilt: 0.7 + Math.random() * 0.6
			}));
		}

		function resize() {
			width = window.innerWidth;
			height = window.innerHeight;
			dpr = Math.min(window.devicePixelRatio || 1, 2);
			canvas.width = Math.floor(width * dpr);
			canvas.height = Math.floor(height * dpr);
			canvas.style.width = `${width}px`;
			canvas.style.height = `${height}px`;
			context.setTransform(dpr, 0, 0, dpr, 0, 0);
			makePoints();
		}

		function readFieldPalette() {
			fieldPalette = {
				line: getThemeValue("--field-line", "rgba(110, 165, 242, 0.2)"),
				node: getThemeValue("--field-node", "rgba(239, 247, 252, 0.9)"),
				glow: getThemeValue("--field-glow", "rgba(88, 205, 182, 0.08)"),
				contours: [
					getThemeValue("--field-contour-1", "rgba(88, 205, 182, 0.12)"),
					getThemeValue("--field-contour-2", "rgba(110, 165, 242, 0.1)"),
					getThemeValue("--field-contour-3", "rgba(217, 164, 93, 0.08)")
				]
			};

			if (prefersReducedMotion) {
				drawStaticFrame(0);
			}
		}

		refreshFieldPalette = readFieldPalette;

		function withAlpha(color, alpha) {
			if (!color.startsWith("rgba(")) {
				return color;
			}

			const channels = color.slice(5, -1).split(",").slice(0, 3).map((item) => item.trim());
			return `rgba(${channels.join(", ")}, ${alpha})`;
		}

		function drawContours(time) {
			fieldPalette.contours.forEach((color, index) => {
				context.beginPath();
				const baseY = height * (0.22 + index * 0.2);

				for (let x = -30; x <= width + 30; x += 18) {
					const wave =
						Math.sin(x * 0.006 + time * 0.00055 + index * 1.1) * (22 + index * 10) +
						Math.cos(x * 0.0028 + time * 0.00042 + index) * 12;
					const y = baseY + wave;

					if (x === -30) {
						context.moveTo(x, y);
					} else {
						context.lineTo(x, y);
					}
				}

				context.lineWidth = 1;
				context.strokeStyle = color;
				context.stroke();
			});
		}

		function getAnimatedPoints(time) {
			return points.map((point) => {
				const x =
					point.originX +
					Math.cos(time * 0.00018 * point.speed + point.phase) * point.orbit;
				const y =
					point.originY +
					Math.sin(time * 0.00015 * point.speed + point.phase) * point.orbit * point.tilt;

				if (!pointer.active) {
					return { ...point, x, y };
				}

				const dx = x - pointer.x;
				const dy = y - pointer.y;
				const distance = Math.hypot(dx, dy);
				if (distance === 0 || distance > 160) {
					return { ...point, x, y };
				}

				const force = (160 - distance) / 160;
				return {
					...point,
					x: x + (dx / distance) * force * 18,
					y: y + (dy / distance) * force * 18
				};
			});
		}

		function drawNetwork(animatedPoints) {
			const threshold = Math.min(180, width * 0.16);

			for (let i = 0; i < animatedPoints.length; i += 1) {
				for (let j = i + 1; j < animatedPoints.length; j += 1) {
					const a = animatedPoints[i];
					const b = animatedPoints[j];
					const distance = Math.hypot(a.x - b.x, a.y - b.y);

					if (distance > threshold) {
						continue;
					}

					const alpha = (1 - distance / threshold) * 0.26;
					context.beginPath();
					context.moveTo(a.x, a.y);
					context.lineTo(b.x, b.y);
					context.strokeStyle = withAlpha(fieldPalette.line, alpha.toFixed(3));
					context.lineWidth = 1;
					context.stroke();
				}
			}

			animatedPoints.forEach((point) => {
				context.beginPath();
				context.arc(point.x, point.y, point.radius, 0, Math.PI * 2);
				context.fillStyle = fieldPalette.node;
				context.fill();

				context.beginPath();
				context.arc(point.x, point.y, point.radius * 3.2, 0, Math.PI * 2);
				context.fillStyle = fieldPalette.glow;
				context.fill();
			});
		}

		function drawStaticFrame(time) {
			context.clearRect(0, 0, width, height);
			drawContours(time);
			drawNetwork(getAnimatedPoints(time));
		}

		function frame(time) {
			drawStaticFrame(time);
			animationFrame = window.requestAnimationFrame(frame);
		}

		window.addEventListener("resize", resize);
		window.addEventListener("pointermove", (event) => {
			pointer.x = event.clientX;
			pointer.y = event.clientY;
			pointer.active = true;
		});
		window.addEventListener("mouseout", (event) => {
			if (!event.relatedTarget) {
				pointer.active = false;
			}
		});

		resize();
		readFieldPalette();

		if (prefersReducedMotion) {
			drawStaticFrame(0);
			return;
		}

		if (animationFrame) {
			window.cancelAnimationFrame(animationFrame);
		}

		animationFrame = window.requestAnimationFrame(frame);
	}

	document.addEventListener("DOMContentLoaded", () => {
		initTheme();
		initReveal();
		initProjectSection();
		syncUpdatedDates();
		initNeuralField();
	});
})();
