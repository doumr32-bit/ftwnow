---
description: Activate FTWNOW development environment for a project
argument-hint: [project-name] [optional-task-description]
---

Activate the FTWNOW full-stack development methodology for project "$1".

Execute the following startup sequence:

1. **Load FTWNOW Skill** — Read `${CLAUDE_PLUGIN_ROOT}/skills/ftwnow/SKILL.md` to load the full methodology
2. **Tool Chain Check** — Verify all required MCP tools are connected (~~docs, ~~project tracker, Supabase, GitHub). Report any missing tools
3. **Project Context** — Search ~~docs for any existing project documents (PRD, architecture, sprint reports) related to "$1"
4. **Code Status** — If a GitHub repo exists for the project, check the latest commits and branch status
5. **Output Summary** — Present a project status report:
   - Current phase (if previously started) or "New project"
   - Recent documents and decisions
   - Pending tasks from ~~project tracker
   - Recommended next action

If a task description is provided as $2, enter PLAN mode to analyze the task within the FTWNOW framework. Wait for user to say "FTW" before executing.

If no arguments are provided, list recent FTWNOW projects found in ~~docs and ask which one to activate.
