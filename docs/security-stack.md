# Security stack

Monthly Dependabot updates cover GitHub Actions only. Minor and patch releases
are grouped; major releases remain separate, with three open update PRs allowed.
No package ecosystem is configured because this repository has no package
manifests. CODEOWNERS requests owner review for every path.

The SHA-pinned Gitleaks v2 action scans pull requests and pushes to main. Git
history is fetched completely, credentials are not persisted by checkout, and
the job explicitly selects the supported Node 24 runtime. Findings fail the
check. Comments, finding uploads and summaries are disabled; the redacted local
report is removed even on failure. The existing packaging workflow is unchanged.

Weekly scans fail on findings or scanner errors.

The weekly workflow runs from main only, with manual dispatch and cron
`0 15 * * 6`: Sunday 02:00 Sydney during daylight saving, 01:00 in standard
time. Gitleaks scans the entire history. OSV scans the whole working tree,
accepts the current empty package inventory and still fails on vulnerability,
download, checksum, report or scanner errors. There is no PR dependency scan
or severity gate for this repository without package manifests.

This public repository uses hosted Linux. Leave `CI_RUNNER` unset so
`vars.CI_RUNNER || 'ubuntu-latest'` falls back to the hosted runner. A small
hosted policy job fails if that variable is set; both weekly scanner jobs depend
on it, so a changed setting cannot schedule them on a self-hosted machine.
No workflow modifies repository variables or settings.

The OSV CLI release and platform checksums are pinned. Its download is capped
at 128 MiB; the binary and JSON report live in a temporary directory removed on
normal completion or failure. No result artifact is uploaded by these new
workflows. Logs stay in the hosted Actions service under repository retention.

All new checks are advisory, not required merge checks. No deploy or repository
security setting is added. Dependency alerts, secret scanning, push protection
and CodeQL settings remain separate owner actions.

Sources: [OSV release](https://github.com/google/osv-scanner/releases/tag/v2.7.1),
[Gitleaks](https://github.com/gitleaks/gitleaks-action),
[Node 24 runner migration](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/).
