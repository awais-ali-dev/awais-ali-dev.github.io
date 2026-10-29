# Awais Ali — professional portfolio

A responsive personal website for Awais Ali Lashari: cybersecurity, software development, and applied AI. This repository is the complete editable source, with a ready-to-serve `dist/` directory.

**Start with [DEPLOY_TO_GITHUB.md](DEPLOY_TO_GITHUB.md)** for uploading this package and publishing it through GitHub Pages.

## Included

- Responsive homepage with portrait, selected work, experience, education, and contact links.
- Thirteen project profiles and a searchable project collection.
- Forty-two course and program credential records, with supplied verification links and selected local certificate copies.
- Three completed internships and clearly labelled learning in progress.
- Light/dark views, accessible mobile navigation, filters, copy-email, and a downloadable public résumé.
- Privacy, terms, security reporting, accessibility, custom 404, sitemap, and social metadata.
- GitHub Pages deployment workflow with separate build/deploy permissions and automatic URL-prefix handling.

## Files to edit

| File | Purpose |
| --- | --- |
| `content/projects.json` | Project descriptions and repository links |
| `content/credentials.json` | Credential records and certificate links |
| `tools/build.py` | Page templates, biography, experience, and policy text |
| `dist/assets/site.css` | Responsive styles and themes |
| `dist/assets/site.js` | Browser interactions |
| `dist/downloads/Awais-Ali-Resume.pdf` | Public résumé |
| `site.json` | Default base URL for local builds or other hosts |
| `.github/workflows/deploy.yml` | Automatic deployment on pushes to `main` |
| `tools/check_site.py` | Local link, CSP, and structural checks |

The assets under `dist/assets/` and the PDF under `dist/downloads/` are source assets as well as deployment files. Do not delete the entire `dist/` folder before a build. The generator rewrites the HTML and metadata while retaining those assets.

## Build and preview

Python 3.9+ is sufficient for website generation; there are no Python or npm packages to install for this step.

```bash
python3 tools/build.py
python3 tools/check_site.py
node --check dist/assets/site.js
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Open `http://localhost:8000/`. On Windows, use `py` if `python3` is unavailable. Node is only needed for the optional JavaScript syntax check, not serving or building the site. The included GitHub workflow runs all three checks before publishing.

For a different hostname or repository path, set the full HTTPS URL in `site.json` or the `SITE_URL` environment variable. On GitHub Actions the workflow sets `SITE_URL` from the repository's actual Pages configuration, including custom domains and project paths. Core content remains available without JavaScript.

## Optional résumé generation

The finished PDF is already included and the website workflow does not regenerate it. To regenerate it, install ReportLab, provide `DejaVuSans.ttf` and `DejaVuSans-Bold.ttf`, then run `python3 tools/make_resume.py`. The default font folder is `/usr/share/fonts/truetype/dejavu`; set `RESUME_FONT_DIR` to another font folder on Windows or macOS. Review the rendered PDF after changing its contents. You can instead replace the PDF with an updated one-page résumé.

## Content and privacy

Content was prepared from the owner's supplied archives, CV, certificate evidence, repository listing, and learning records. BSCS is completed. Three internship completions are supported by supplied documents. The 42 credential entries distinguish individual course completions from professional programs and specializations. Google Cybersecurity and Microsoft Cybersecurity Analyst remain in progress, using the supplied October 2026 snapshot.

The project descriptions are documentation-based summaries. They do not claim a fresh audit of the linked GitHub code. Security exercises use authorized or local lab contexts; medical-imaging and emergency-communication projects are prototypes. No clinical-performance, production-traffic, or independent-security-certification claims are made.

Original private source archives, identity documents, domicile scans, signatures, student numbers, transcript, phone number, and full street address are excluded. The included public contact email, portrait, professional résumé, and selected credential copies are intentional portfolio content. No authentication token or hosting-account configuration is required or included.

## Hosting and security

Publish only `dist/`. The application has no backend, database, authentication service, upload endpoint, analytics, contact-form service, remote font, or runtime package dependency. Contact links open the visitor's email client. Search and theme preferences are not persisted.

GitHub Pages publication is normally public; this standalone export does not inherit a private preview's access controls. `_headers` is a configuration for compatible hosts, not a custom-header mechanism for GitHub Pages. The HTML meta CSP is included independently. Read [SECURITY_REVIEW.md](SECURITY_REVIEW.md) for completed checks and remaining hosting limits. No website can be guaranteed vulnerability-free.

Keep learning progress, résumé details, certificate links, and security contact expiry current. Review Dependabot pull requests for the GitHub Actions workflow. Project repositories and third-party certificate materials retain their own licensing terms; this package does not impose a new licence on them.
