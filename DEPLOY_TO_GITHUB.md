# Put your portfolio on GitHub Pages

This is the complete editable source, including the finished website, your portrait, selected certificate copies, a public résumé, project and credential data, and an automated deployment workflow. No ChatGPT login or API key is required for the exported website.

## Recommended first deployment

1. Extract the ZIP. Open the `awais-ali-portfolio` folder inside it.
2. Sign in to GitHub as `awais-ali-dev`. Create a repository named **`awais-ali-dev.github.io`**, with `main` as its default branch. A public repository works with GitHub Free. If that repository already exists, use a new repository such as `portfolio` instead of overwriting an existing site.
3. Upload **the contents inside** `awais-ali-portfolio` to the repository root. Do not upload the ZIP itself or nest everything inside an extra folder. Include `.github/workflows/deploy.yml`, `.github/dependabot.yml`, `.gitignore`, `content`, `dist`, `tools`, and `site.json`. GitHub Desktop or Git preserves dotfolders reliably. If using the browser uploader, verify that `.github/workflows/deploy.yml` is visible in the repository afterward.
4. In the repository, open **Settings → Pages → Build and deployment → Source**, and select **GitHub Actions**. The workflow is already included; you do not need to create a second workflow.
5. Open **Actions → Deploy portfolio to GitHub Pages → Run workflow**, choose `main`, and run it. If an earlier run failed because Pages was not enabled yet, rerun it after step 4.
6. Wait for both `build` and `deploy` to turn green. Open the published URL shown in the deployment or Pages settings.

For the recommended repository name, your expected address is **https://awais-ali-dev.github.io/**. A repository called `portfolio` uses **https://awais-ali-dev.github.io/portfolio/**. These are expected destinations, not claims that this package has already been deployed there. The workflow reads the actual Pages URL and adapts all internal links, metadata, and sitemap paths automatically.

GitHub Pages normally publishes a public website, even when a plan permits the source repository to remain private. This export includes only the intended public portfolio material. Your previous private preview is separate and is not changed by this package.

## Upload using Git (alternative)

Run these commands inside the extracted `awais-ali-portfolio` folder after creating an empty repository. If you chose another name, replace the remote URL below with your new repository's HTTPS URL. Authenticate through GitHub's normal sign-in flow; do not put a password or token into these files.

```bash
git init
git add .
git commit -m "Add professional portfolio"
git branch -M main
git remote add origin https://github.com/awais-ali-dev/awais-ali-dev.github.io.git
git push -u origin main
```

Then complete steps 4–6 above. Future pushes to `main` rebuild and deploy the website automatically. This workflow does not deploy pull requests.

## Edit and preview

- Project content: `content/projects.json`.
- Credential content: `content/credentials.json`.
- Homepage, experience, education, and policy text: `tools/build.py`.
- Visual design: `dist/assets/site.css`.
- Menus, filters, theme, and clipboard interaction: `dist/assets/site.js`.
- Public résumé: replace `dist/downloads/Awais-Ali-Resume.pdf` with your updated PDF.
- Default local-build URL: `site.json`. GitHub Actions overrides it with the configured Pages URL.

Python 3.9+ is enough to rebuild the website. There are no packages to install for the website build. From the project folder, run:

```bash
python3 tools/build.py
python3 tools/check_site.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

On Windows, use `py` instead of `python3` if needed. Open **http://localhost:8000/**. Keep `site.json` at the root-domain default for this simple local preview. Opening `index.html` by double-clicking is not a supported preview because the site uses server paths.

To preview a project-path build, first set `site_url` in `site.json` to its full URL (for example `https://awais-ali-dev.github.io/portfolio`), rebuild, and serve `dist` mounted under that same path. The GitHub workflow handles this automatically when deploying, so this is optional.

## Other hosts and custom domains

For any static host, publish **only `dist/`**. Set `site_url` in `site.json` to your intended full HTTPS URL and run the build before uploading. Use directory indexes and `404.html`. There is no backend, database, or runtime dependency.

For a custom domain on GitHub Pages, configure the domain in the repository's Pages settings and rerun the workflow. Its URL metadata then comes from GitHub's updated configuration. Follow GitHub's DNS and HTTPS instructions before switching traffic.

`dist/_headers` is provided for hosts that explicitly support that format. GitHub Pages does not apply it as your custom response-header policy. The restrictive HTML meta CSP and referrer policy still travel with the pages; header-only controls depend on your host. See `SECURITY_REVIEW.md` for the limits of the checks.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| No workflow in Actions | Ensure `.github/workflows/deploy.yml` is uploaded at the repository root, not inside an extra folder. |
| Configure Pages fails | Enable GitHub Actions as the Pages source, then rerun. Check whether your repository plan supports Pages. |
| No run after a push | Push to `main`; the workflow intentionally deploys only that branch. |
| Styling or links missing | Use the included workflow. Do not publish the repository root or an old `dist` built for another base URL. |
| Site requires a ChatGPT login | You are opening the previous private preview. Use the URL from GitHub Pages settings. |
| Unexpected 404 | Check that both workflow jobs succeeded and use their deployment URL. |

## Official references

- [Configure a GitHub Pages publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [Custom GitHub Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [Configure Pages action and URL outputs](https://github.com/actions/configure-pages)
- [Upload Pages artifact, including hidden files](https://github.com/actions/upload-pages-artifact)

Prepared 29 October 2026. Local builds and archive checks can validate this package; the first actual GitHub deployment must still run in your repository.
