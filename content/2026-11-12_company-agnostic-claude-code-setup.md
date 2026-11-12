Title: Making my Claude Code setup company-agnostic
Date: 2026-11-12 10:00
Modified: 2026-11-12 10:00
Category: posts
Tags: dotfiles, Claude Code, AI, automation, bash, macOS
Slug: company-agnostic-claude-code-setup
Authors: Jitse-Jan
Summary: Splitting my global Claude Code instructions into a public layer I track in dotfiles and a private layer that never leaves the machine, seeded automatically at bootstrap.

A while back I wrote about [provisioning a new Mac from a dotfiles repo](/automating-mac-setup-with-dotfiles-and-ai.html). That setup has held up well, with one part that quietly stopped working: my Claude Code instructions.

Claude Code reads `~/.claude/CLAUDE.md` as global context for every project. Mine had grown into a single file holding two very different kinds of thing. Half of it was how I want to work anywhere: issue first then branch then code, no AI attribution on commits, uv for Python, say plainly what you did not verify. The other half was about one specific engagement: the client's name, where their repos live, which tracker wins when two disagree, which systems carry personal data, who decides what.

The first half is worth keeping forever. The second half is wrong the moment the engagement ends, and it should never have been anywhere near a public repo.

## The problem with one file

My dotfiles repo is public. So the file is either tracked, in which case client details are on GitHub, or untracked, in which case none of my working rules survive a new laptop. I had been living with the second option, re-typing the rules from memory, which is exactly the kind of thing dotfiles exist to stop.

The fix is two layers with the boundary enforced by where each file lives.

## Two layers joined by an import

The tracked layer sits in the repo at `.config/claude/CLAUDE.md` and is symlinked to `~/.claude/CLAUDE.md` by bootstrap, like every other config. It holds only the portable parts, and its first instruction is an import:

```markdown
# Personal defaults

How I want Claude to work in any project. A project's own `CLAUDE.md` wins
where the two differ. Employer-specific defaults (tools, people, house style)
live in an untracked file on each machine:

@~/.claude/local.md
```

That `@path` line is a Claude Code import. It pulls in another file at load time, so `~/.claude/local.md` becomes the employer layer: organisation, repos, trackers, branch naming, data rules, people, and anything the client says not to touch. It is never tracked anywhere. A project's own `CLAUDE.md` still wins over both, so repo-specific rules keep working unchanged.

Nothing clever is happening here. The value is that the split is now structural. Anything employer-specific I write in the tracked file is a public commit, so the obvious mistake becomes a visible one.

## Seeding the private layer at bootstrap

An untracked file is only useful if something reminds you to create it. A new machine would otherwise get a dangling import and a silently empty employer layer, which is worse than no layer at all, because Claude treats what it reads as true.

So `scripts/setup_claude.sh` now runs as part of bootstrap. It asks for the organisation and its homepage, fills a tracked template, and writes the result to `~/.claude/local.md`. Three details turned out to matter more than the substitution itself.

**Never block an unattended run.** Bootstrap gets run non-interactively often enough that a blocking `read` is a hang rather than a question. It only prompts when there is a human on the other end, and otherwise takes `DOTFILES_ORG` and `DOTFILES_ORG_URL` from the environment:

```bash
if [[ -z "$ORG" && ! -f "$LOCAL" && -t 0 ]]; then
  read -r -p "    Organisation (e.g. Acme Corp): " ORG || ORG=""
fi
```

**Leave a blank blank.** My first version derived a slug from the organisation name and fell back to `org` when there was no name. That was worse than useless: the file then claimed an `org-style` skill existed. Now an unanswered token stays as a literal `{{ORG_SLUG}}` in the output, so it reads as an unfilled blank rather than a confident wrong answer. The template says the same thing out loud: an empty heading beats a wrong one.

**Write for the bash macOS ships.** That is still bash 3.2, so no `${var,,}` for lowercasing. The slug goes through `tr` and `sed` instead:

```bash
ORG_SLUG="$(printf '%s' "$ORG" \
  | tr '[:upper:]' '[:lower:]' \
  | sed -e 's/[^a-z0-9]\{1,\}/-/g' -e 's/^-//' -e 's/-$//')"
```

Like every other script in the repo, it never overwrites an existing file, so re-running bootstrap is safe.

## House style as a generated stub

The same bootstrap step solves something I had been doing by hand. Anything visual I build for a client, a dashboard, a one-page summary, a diagram, should look like it came from that client, not from me.

So when an organisation is given, the script also stubs `~/.claude/skills/<org>-style/SKILL.md`, pointed at that organisation's own homepage. The stub carries an instruction about the order to fill it in: write Character first, two or three sentences in plain words about what the page is made of and what is deliberately absent, then type and tokens from the site's real computed styles rather than from a brand PDF. "Quiet and editorial, white page, black ink, hairlines instead of boxes" does more work than any list of hex values underneath it, and it is the part no scraper can produce.

Two rules sit in the tracked layer permanently: the palette is derived from the organisation's own site with the date recorded, so a stale one is visible rather than silently wrong, and it is typography and colour only, never the logo.

## What is still missing

The instructions travel now, but my hooks do not. `~/.claude/settings.json` holds the statusline and ten hook definitions, and `~/.claude/hooks/` holds the scripts they call, and both are still untracked. A new machine gets my rules and none of my automation. One of those hooks also hardcodes a client repo name, so making it portable is the same exercise as above: generic in the tracked layer, specifics from the environment.

That is the next piece. The pattern is already proven by the part that works.
