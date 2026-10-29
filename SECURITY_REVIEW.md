# Portfolio security and quality review

Review date: 28 October 2026. Scope: the generated static portfolio, included assets and PDFs, source-side content handling, and browser interactions. This is a bounded development review, not an independent penetration test or a guarantee of zero vulnerabilities.

## Application controls

- No runtime npm dependencies, CDN scripts, remote fonts, tracking libraries, forms, uploads, API endpoints, database writes, or custom authentication.
- All untrusted content is HTML-escaped during page generation. Search input is only compared to existing text and is never inserted as HTML, evaluated, or sent over the network.
- Browser code uses `textContent` for messages and does not use `innerHTML`, `eval`, `Function`, `document.write`, cookies, or persistent browser storage.
- Restrictive CSP is present in every document's metadata: same-origin scripts/styles/assets, no connections, objects, workers, frames, form submissions, or base-URL overrides. JSON-LD is authorized with an exact SHA-256 hash.
- `_headers` configures CSP response headers (including restricted frame ancestors), `nosniff`, no-referrer, Permissions-Policy, HSTS, and cross-origin isolation-related headers. Actual delivery of these response headers is a hosting responsibility and must be verified separately; metadata cannot enforce frame-ancestors or HSTS.
- External new-tab links carry `noopener noreferrer`. The contact link does not submit a server-side form. Copy-email only writes on an explicit click.
- `.well-known/security.txt` and a security-reporting page provide a contact and scope. No active testing authorization or bounty promise is implied.
- The static output excludes private source archives, ID documents, signatures, student numbers, credentials, and debug fixtures.

## Checks completed

- Static checks passed across 22 HTML files (20 content routes and two 404 representations): local files/anchors resolve, IDs are unique, one H1 per page, language/description metadata exists, meaningful images have text alternatives, and external tabs use safe attributes.
- JavaScript syntax check passed. Source scan found no dangerous DOM insertion/evaluation APIs, network-fetch APIs, persistent storage, known secret patterns, or government-ID patterns in the deployable text files.
- CSP structure and JSON-LD hash checks passed. Hosting-header configuration is present; this is distinct from proof of live header enforcement.
- Both included PDFs were checked for document/page/annotation actions and JavaScript; no active actions were found. The one-page résumé was rendered and visually inspected.
- Desktop homepage and project-card visuals were reviewed. Responsive browser frames at nominal 320, 390, and 768 pixels showed no horizontal document overflow (content widths 305, 375, and 753 pixels with scrollbars).
- Mobile project collection, a case-study page, and credential directory showed no horizontal document overflow at 375 CSS pixels of content width.
- Mobile navigation opens, Escape closes it, and focus is returned to the toggle. Light/dark mode changes the visible theme and accessible control state.
- Project category filtering, combined text search, empty-state reset, and credential search were exercised. A string containing an image tag and event handler was treated as text and triggered no dialog or inserted element.
- Copy-email reported success after the user-initiated click. No application console errors were observed in the final mobile checks. Browser-extension messages were excluded from application findings.
- Core content and links are server-rendered static HTML. No-JavaScript navigation and reduced-motion rules were source-reviewed; these are not represented as full assistive-technology or WCAG conformance audits.

## Remaining boundaries

No exhaustive security guarantee is possible. Hosting, TLS policy, authentication, provider logs, account security, and third-party destinations are outside this code review. No scans, intrusion attempts, or stress tests were run against the hosting provider or external repositories. Live GitHub code and every external certificate destination could not be independently fetched in this environment. Supplied certificate URLs were checked for appropriate schemes and exact local provenance, not for continuing provider availability.

No server-side mutation surface exists in the application, so application-level SQL injection, CSRF on writes, file-upload execution, and password storage are avoided by architecture. This does not imply the infrastructure is free of vulnerabilities. Re-review changes before adding forms, analytics, authentication, uploads, payment features, or external integrations.

Public release, legal adequacy for a particular jurisdiction, full screen-reader testing, and testing on physical mobile devices remain separate decisions or activities. The original preview was owner-private. This downloadable GitHub export is independent; GitHub Pages is normally public when the owner enables deployment.

## Technical references

- MDN, Content Security Policy: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
- MDN, frame-ancestors (header only): https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors
- MDN, Strict-Transport-Security: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security

## GitHub export review — 29 October 2026

The standalone export removes private hosting identity, Git metadata, and preview-domain dependencies. The résumé no longer points to the private preview. Build configuration validates the HTTPS site URL and supports both root domains and repository subpaths. The application remains static.

The workflow builds and checks the site before publishing only `dist/`; source, content JSON, and tools are not uploaded to the Pages artifact. Build permissions are `contents: read` and `pages: read`; deployment alone receives `pages: write` and `id-token: write`. Checkout does not persist credentials. No personal access token, app secret, or repository-write permission is required. Automatic publication is limited to `main`. Dependabot configuration is included for workflow action updates.

The artifact action includes hidden public files so `.well-known/security.txt` is retained. No private dotfiles or source metadata are present under `dist/`. For compatible hosts, the response-header template uses `frame-ancestors 'none'`. GitHub Pages does not apply `_headers` as a custom-header configuration. CSP in HTML metadata remains in the output, but it cannot enforce header-only controls such as `frame-ancestors`, `nosniff`, or HSTS. Do not infer delivery of these headers from their presence in a file.

No actual GitHub repository was created and no GitHub workflow was executed during export. Successful local validation is not a claim of a successful live deployment or exhaustive security testing. The owner must enable Pages and run the supplied workflow in their repository.

Export validation passed for the GitHub user-site URL, a `/portfolio` project path, and a custom-domain URL. All 22 HTML files passed structural/link/CSP checks in each build. Ten representative project-path routes and assets returned HTTP 200 in a local server check. Five malformed site URL configurations were rejected. The exported résumé remains one page, was visually reviewed, and both included PDFs passed the action scan. The final archive was checked for integrity and excluded Git history, hosting identity, caches, and private source archives. Workflow YAML was parsed and its permissions, artifact directory, and URL configuration were checked locally; the workflow has not run on GitHub.
