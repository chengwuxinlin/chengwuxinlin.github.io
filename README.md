# Wuxinlin Cheng — personal website

A static, no-build website for GitHub Pages, served from the repository root.

## Preview locally

From this folder, run:

```powershell
python scripts/preview.py
```

Open <http://127.0.0.1:8765>. Stop the server with `Ctrl+C`. The preview server binds only to this computer and supplies consistent image types so WebP covers open correctly on Windows.

## Validate

Run `python scripts/check_site.py` for local reference, content, accessibility-markup, and document-exclusion checks. Review layout and interactions in a browser at desktop and mobile widths.

## Maintain the site

- `index.html`: biography, selected work, publications, experience, and contact information. Core content and navigation remain available without JavaScript.
- `assets/css/site.css`: layout, typography, colors, and responsive styles.
- `assets/js/site.js`: optional project search, topic filters, reading-position navigation, and a keyboard-accessible cover viewer. Cover links remain ordinary image links without JavaScript.
- `assets/images/`: current site artwork and optimized assets. The hero manifold can be regenerated with `python scripts/build_manifold.py`.
- `assets/js/ambient-field.js` and `assets/css/ambient-field.css`: a full-viewport manifold point field with irregular surface samples, slow drift, and local mouse deformation. Includes pause/resume, reduced-motion support, and hidden-tab suspension; opaque cards preserve reading clarity.
- `images/`: retained original image assets.
- `assets/images/covers/`: twelve project covers; `ATTRIBUTION.md` records source material and the SGM cover license. Each cover is framed consistently and labeled as a source example, published result, demo frame, or illustration.
- `scripts/covers/`: optional rebuild scripts (Pillow; FFmpeg for the avatar cover). Original download/generation inputs stay in ignored `.local/cover-sources/` and are not included in the public site.

Use the CV as a private editorial reference. Do not upload or link the CV, its source files, or extracted copies in this repository. Keep public descriptions accurate and distinguish research papers, demonstrations, and industry work.

This revision is for local review. No build or deployment workflow is included, and nothing should be pushed or published until the owner has reviewed and approved it.

## Historical attribution

The previous site used **Editorial by HTML5 UP**, by [AJ](https://html5up.net), under Creative Commons Attribution 3.0. Its runtime, stylesheet, Sass, and bundled font files have been retired. The original `LICENSE.txt` is retained as historical license documentation; it does not assert ownership or grant new rights over third-party images, research figures, or publications.

`_config.yml` excludes repository documentation, local tools, and preview artifacts from a GitHub Pages Jekyll publication.
