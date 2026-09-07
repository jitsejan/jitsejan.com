Title: Obsidian, Claude, and agile-ai: my weekly workflow
Date: 2026-09-14 10:00
Modified: 2026-09-14 10:00
Category: posts
Tags: obsidian, claude, AI, productivity, note-taking, workflow, dbt, duckdb, dlt
Slug: obsidian-vs-claude-multi-project-context
Authors: Jitse-Jan
Summary: How I split responsibilities between Obsidian, Claude, and a small dlt + dbt + DuckDB pipeline so switching between projects doesn't mean re-explaining everything from scratch, and my weekly review is backed by real data instead of memory.

I usually have several projects going at once, each with its own codebase, its own people, and its own half-finished threads. The hard part was never doing the work, it was picking it back up after two days away and remembering exactly where I left it, and knowing what actually happened over a given week without relying on memory. Three tools ended up splitting that problem cleanly: Obsidian holds state, Claude does the work, and a small pipeline I built called [agile-ai](https://github.com/jitsejan/agile-ai) turns raw ticket activity into the numbers behind my weekly review.

## Three different jobs

Obsidian is where state lives. Claude is where work happens. agile-ai is where the facts come from. If I mix those up, either my vault turns into a code editor I fight with, or my AI sessions turn into something that forgets everything the moment the context window resets, or my weekly review turns into "I think I did a lot this week" instead of an actual number.

- **Obsidian** holds the things that are true independent of any single session: decisions made, who owns what, what's blocked on whom, what changed and why.
- **Claude** does the actual work inside that context: reading code, writing code, drafting messages, running commands.
- **agile-ai** answers the question neither of the above can: what actually shipped, and how does this week compare to the last one.

The vault doesn't replace my memory of a project. It replaces re-explaining the project to a fresh AI session every single time. And the pipeline doesn't replace the vault, it feeds it, so the weekly note isn't just prose, it's prose backed by a query.

## One handoff file per project, not per session

Early on I let Claude write a new summary file every time a session ended. That was a mistake. I'd end up with `handoff.md`, `handoff-v2.md`, `session-2026-07-14.md`, and no way to tell which one was current without reading all of them.

Now each active project gets exactly one rolling `AI-Handoff.md` in its vault folder, and the rule is explicit: update it in place, never create a dated duplicate. When something material happens, a PR merges, a decision gets made, a blocker clears, that file gets edited, not appended to as a new file.

The file itself has a small structure that repeats across projects:

- **Who and what this is** — the people involved and what the initiative actually is, so a cold read doesn't need me sitting next to it
- **Current state** — what's done, what's in review, what's blocked and on whom
- **Standing preferences** — the small stuff that isn't obvious from the code: how this person likes PRs split, what tone a message to that person should take, which shortcuts are explicitly not allowed
- **Known issues** — things that look like bugs but are actually already understood, so they don't get re-investigated from zero
- **Changelog** — a short line per update at the bottom, never deleted, so the history of the history is still there

That last point matters more than it sounds. A handoff document that silently rewrites itself loses the "why did we decide this" trail. Keeping old changelog entries costs nothing and saves a lot of "wait, didn't we already try that."

## What goes in the vault vs what stays ephemeral

Not everything needs to survive. A lot of what happens in a session is genuinely disposable, draft replies that got superseded by a real reply, a scratch file used mid-task, an in-progress investigation that resolved a different way than expected. Forcing all of that into permanent notes just adds noise to the next read.

The filter I use:

- If it's a fact that will still be true next week (a decision, an architecture choice, an owner, a deadline), it goes in the vault.
- If it's how I got there (an exploratory back-and-forth, a discarded draft, a false start), it doesn't need to survive the session.

Meeting notes and transcripts still get exported into per-project folders, but they're reference material, not the thing a new session reads first. The handoff file is the thing a new session reads first, because it's already been distilled.

## Where the weekly numbers actually come from

The vault is good at holding decisions and blockers, but it's a bad place to answer "how many tickets did I actually close this week" or "is this sprint slower than the last three." That's not a note-taking problem, it's a data problem, so I built [agile-ai](https://github.com/jitsejan/agile-ai) to solve it separately instead of trying to fake it in markdown.

It's a small [dlt](https://dlthub.com/) pipeline that pulls issues, sprints, comments, and issue history straight from the Jira API into [MotherDuck](https://motherduck.com/) (DuckDB in the cloud), then [dbt](https://www.getdbt.com/) reshapes it through a bronze/silver/gold layering:

- **Silver** cleans the raw Jira payloads into `issues` and `sprints` tables.
- **Gold** turns those into the models a weekly review actually needs: `sprint_velocity`, `sprint_carryover`, `team_member_performance`, `personal_activity`, `ticket_aging`.

The dashboards on top (Evidence.dev, with a Superset setup as an alternative) are almost an afterthought at that point. Once `sprint_velocity` and `personal_activity` exist as gold tables, the hard part is done, the visualization layer is just SQL against DuckDB.

Running it end to end is one command:

```bash
make refresh   # dlt fetch from Jira, then dbt run
```

The output feeds two things: a dashboard I glance at, and the actual weekly note in the vault. Instead of writing "had a productive sprint" from memory, the weekly note can say what the `sprint_velocity` and `ticket_aging` models actually show. Obsidian still holds the narrative, agile-ai just makes sure the narrative isn't guessing.

## Why this beats one giant context

The obvious alternative is to just paste everything into a session and let the model figure out what matters. That works until you're juggling more than one project, at which point every session either drowns in irrelevant history from other work, or starts from zero because you didn't want to paste all of it.

Splitting by project folder in the vault means each project's context is exactly as big as that project needs, no more. A fresh Claude session pointed at one project's `AI-Handoff.md` gets precisely the state it needs to be useful immediately, without inheriting noise from three other things I'm also working on.

## The result

Switching projects now looks like this: open the vault folder for the project, point a new session at its handoff file, and continue. No re-explaining who's who, no re-deriving decisions that were already made two weeks ago. Once a week, `make refresh` pulls the latest ticket activity so the weekly note is written against actual numbers instead of a vague sense of how the week went.

Three tools, three narrow jobs: the vault remembers so the AI session doesn't have to guess, the AI session does the work so the vault doesn't have to become a second codebase, and the pipeline measures so the weekly note doesn't have to rely on memory.

If you're running more than one AI-assisted project at a time, the biggest lever isn't a smarter prompt, it's separating where state lives, where work happens, and where the numbers come from, and not letting any one of them try to do the other two jobs.
