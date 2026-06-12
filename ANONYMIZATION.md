# Anonymous Release Notes

This release is an anonymous artifact package for PromptSecurityEval. It
contains framework code, the anonymized JailbreakDB evaluation subtree, and
the leaderboard source. The interactive leaderboard is published from the
`gh-pages` branch of this repository.

The following artifacts are intentionally excluded:

- Git history, remotes, local Claude settings, local run commands, tmux logs, and internal planning files.
- Non-paper raw experiment outputs, exported dashboards, notebooks, and logs.
- API key files, local environment files, hard-coded credentials, and local absolute paths.
- Large prompt/result data files that are not required to inspect the released evaluation dataset or leaderboard.

Runtime credentials must be supplied through environment variables. See `.env.example` for the supported variable names.
