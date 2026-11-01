# GitHub workflow for the 4-member team

## One person (the "owner", e.g. Member 1) - once
1. Create a repo on github.com: **New repository** -> name `satellite-knapsack` -> Private -> do NOT tick "Add README".
2. Unzip this project, then in its folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: shared core and all scripts"
   git branch -M main
   git remote add origin https://github.com/<owner>/satellite-knapsack.git
   git push -u origin main
   ```
3. Repo -> **Settings -> Collaborators -> Add people**: add the other three by username.
4. Repo -> **Settings -> Branches -> Add rule** for `main`: require a pull request before merging (1 approval).

## Every other member - once
```bash
git clone https://github.com/<owner>/satellite-knapsack.git
cd satellite-knapsack
```

## Each member - daily workflow
```bash
git checkout main && git pull                     # always start from the latest main
git checkout -b member2/trace-and-proof           # your own branch (member1/..., member3/..., member4/...)
# ... edit only your folder (+ docs/ for your slides) ...
python tests/test_all.py                          # must pass before pushing
git add member2_branch_and_bound docs
git commit -m "Add best-first trace and correctness proof"
git push -u origin member2/trace-and-proof
```
Then on GitHub click **Compare & pull request**, pick a teammate as reviewer, merge after approval.
Changing `src/core.py`? Tell the team first; everyone depends on it.

## Rules that avoid conflicts
* One member = one folder. Do not edit someone else's folder; ask them or comment on their pull request.
* Small commits with clear messages ("Add worst-case generator", not "update").
* Pull `main` before you start and before you push.
* If you get a merge conflict: `git pull origin main`, open the marked files, keep both sides' correct parts, `git add`, `git commit`.

## Suggested review pairs and final steps
Member1 reviews Member2, 2 reviews 3, 3 reviews 4, 4 reviews 1.
Final week: put slides PDF + one-page analysis sheet in `docs/`, run `benchmark.py` once on one machine, commit
`results/timing_plot.png`, then tag the submission:
```bash
git tag v1.0-submission && git push origin v1.0-submission
```
Submit: the slides PDF, the analysis sheet, and the repo (Code -> Download ZIP) with this README and the plot.
