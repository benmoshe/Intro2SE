# 09 — Git and code review

**Goal:** collaborate on code without stepping on each other, and give and
receive reviews that make the code better.

This module has no pytest exercise. The work is done in your terminal and
with your eyes.

## A workflow that scales from one person to a team

```bash
git switch -c add-due-dates        # 1. branch from an up-to-date main
# ...edit, test...
git add -p                         # 2. stage deliberately, hunk by hunk
git commit                         # 3. commit a single logical change
git push -u origin add-due-dates   # 4. publish the branch
# 5. open a pull request, get review, let CI run
# 6. merge, delete the branch, pull main
```

`main` always works. All change arrives through short-lived branches —
ideally merged within a day or two. Long-lived branches drift and produce
painful merges.

## Commits

A commit is a unit of *reasoning*: one logical change that leaves the tests green.

```
Reject empty task titles

Titles consisting only of whitespace were stored as blank tasks,
which the list view rendered as empty rows. Strip the title in
TaskService.create and raise ValueError if nothing remains.
```

- **Subject:** imperative mood, about 50 characters, no trailing period.
  It should complete the sentence "If applied, this commit will…".
- **Body:** *why*, not what — the diff already shows what.
- Don't mix a refactor with a behaviour change in one commit (module 02).

`git add -p` is the habit that makes this possible: it shows each change and
asks whether to stage it, so stray debug prints never slip in.

## Commands worth knowing

| Command | Use |
|---------|-----|
| `git status`, `git diff`, `git diff --staged` | what have I changed? |
| `git log --oneline --graph` | what happened? |
| `git switch`, `git switch -c` | change / create branches |
| `git restore <file>` | discard uncommitted changes to a file |
| `git commit --amend` | fix the last commit (before pushing) |
| `git stash` | shelve work in progress |
| `git rebase main` | replay your branch on top of the latest main |
| `git revert <sha>` | undo a commit by adding its inverse — safe on shared branches |
| `git bisect` | binary-search history for the commit that broke something |
| `git reflog` | find commits you thought you'd lost |

**Never rewrite history others have pulled.** Amend and rebase freely on your
own unpushed branch; on shared branches, use `revert`.

## Pull requests

A good PR is **small** (a few hundred lines at most — review quality collapses
beyond that), does one thing, and has a description that answers: what
changed, why, and how to verify it. Review your own diff before asking anyone
else to.

## Reviewing code

Review in this order — there's no point polishing names in code that's wrong:

1. **Correctness** — does it do what it claims? Edge cases? Error paths?
2. **Tests** — is the new behaviour tested? Would the tests fail if the code broke?
3. **Design** — is it in the right place? Does it fit the existing structure?
4. **Security** — untrusted input, secrets, injection.
5. **Readability** — names, function size, comments explaining *why*.

Leave formatting and import order to ruff. Humans shouldn't spend review
time on anything a tool can check.

How to say it:

- Comment on the code, not the person: "this loop re-queries per item" rather
  than "you forgot to…".
- Ask when unsure: "what happens if `items` is empty here?"
- Mark severity: prefix optional remarks with **nit:** so the author knows
  what blocks the merge.
- Explain why, and suggest an alternative where you can.
- Say what's good, too.

As an author: the review is of the code, not of you. Reply to every comment,
and push fixes as new commits so reviewers can see what changed.

## Exercise 1 — practise the workflow

In a scratch directory:

1. `git init`, add a file, make a first commit.
2. Create a branch, make two unrelated edits to the file, and use
   `git add -p` to commit them as **two separate commits** with proper messages.
3. Switch back to `main`, change the same line differently, commit.
4. Merge your branch and resolve the conflict by hand.
5. Use `git revert` to undo one commit. Inspect the result with
   `git log --oneline --graph`.
6. Run `git reflog` and find the commit from before your merge.

## Exercise 2 — review a file

`review_me.py` is a small user-store module submitted for review. It runs.
It also has at least eight real problems, several of them serious.

Write your review in a new file, `my_review.md`: for each issue give the
line, the problem, its severity (blocking or nit), and a suggested fix. Order
your comments by severity.

Then compare with `REVIEW_NOTES.md`. Did you find the security issues first?

## Check yourself

- Why are small pull requests reviewed better than large ones?
- When is `git revert` the right tool and `git reset` the wrong one?
- What belongs in a commit body that isn't visible in the diff?
