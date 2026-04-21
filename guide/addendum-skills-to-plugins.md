# From Skills to Plugins

## The BOUCH Skills Foundations Addendum

> © 2026 Paul Boucherat / BOUCH. Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
> See [LICENSE.txt](LICENSE.txt) for full terms.

A practical walkthrough for turning your first skill into an installable Claude Code plugin. This addendum extends the main BOUCH Skills Foundations guide and assumes you have read Parts 1 to 4 first.

---

## Why plugins exist

You can do a lot with standalone skills. Drop a SKILL.md into `~/.claude/skills/` and Claude picks it up automatically. For personal use and rapid iteration, that is the right answer.

The friction starts when you want to share.

If you write a great skill that your team would benefit from, the standalone path becomes a list of chores: copy the file, tell them where to put it, walk them through `~/.claude/skills` vs `.claude/skills`, explain why it did not trigger, re-send the file when you update it. Every new teammate is another manual install. Every skill version is a fresh round of messages.

Plugins fix that. A plugin is a directory that bundles one or more skills, plus optional extras (hooks, slash commands, MCP configuration, custom subagents), into a single installable unit. Users install with one command, namespacing prevents conflicts, versioning handles updates, and a marketplace lets them discover new plugins without knowing you by name.

For BOUCH, plugins are how non-developers get access to production-grade Claude workflows without having to understand file paths or copy-paste configs. That is the whole thesis.

## When to use a plugin vs a standalone skill

The Claude Code docs lay out the split clearly:

- **Standalone** (`.claude/` directory) — personal workflows, project-specific customisation, experiments. Skills get short names like `/hello` or `/deploy`.
- **Plugins** (directories with `.claude-plugin/plugin.json`) — sharing with teammates, distributing to a community, versioned releases, reuse across projects. Skills are namespaced as `/plugin-name:hello`.

Rule of thumb: **start standalone, graduate to plugin when you want to share.**

If you are writing a skill only you will use, do not add the plugin wrapper. The overhead is not worth it. The moment you catch yourself explaining the file layout to someone else for the second time, convert to a plugin.

## The plugin manifest

Every plugin lives in its own directory with a manifest file at `.claude-plugin/plugin.json`. This is the minimum viable manifest:

```json
{
  "name": "my-first-plugin",
  "description": "A greeting plugin to learn the basics",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

Four fields matter:

- **`name`** — the unique identifier and the slash-command namespace. Claude prefixes all your plugin's skills with this. If `name` is `my-first-plugin` and you have a skill called `hello`, users invoke it with `/my-first-plugin:hello`.
- **`description`** — shown in the plugin manager when users are browsing the marketplace. Keep it specific and action-oriented, not marketing fluff.
- **`version`** — semantic versioning (`1.0.0`, `1.2.3`). Bump this when you publish updates so Claude Code knows to refresh the install.
- **`author`** — optional but useful. Gives users someone to credit or contact.

Plugin names must be kebab-case (lowercase letters, digits, hyphens). No spaces, no camelCase, no underscores. The Claude.ai marketplace sync rejects anything else.

## Plugin directory layout

A plugin is a directory. The layout the docs expect:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # the manifest
├── skills/
│   └── hello/
│       └── SKILL.md         # your skill
├── commands/                # optional: slash commands as .md files
├── agents/                  # optional: custom subagents
├── hooks/
│   └── hooks.json           # optional: event handlers
├── .mcp.json                # optional: MCP server config
└── settings.json            # optional: default settings
```

One common mistake: **do not put `skills/`, `commands/`, `agents/`, or `hooks/` inside `.claude-plugin/`**. Only `plugin.json` goes in `.claude-plugin/`. Everything else lives at the plugin root.

## Skills inside a plugin

A plugin's skills directory looks exactly like a standalone skills directory. Each skill is a folder named after the skill, containing a `SKILL.md` file. The frontmatter format is identical to Part 2 of the main Skills Foundations guide.

The only behavioural difference is namespacing. A standalone skill named `hello` becomes `/hello`. The same skill in a plugin named `my-plugin` becomes `/my-plugin:hello`. The namespace prevents two plugins from colliding when both define a `hello` skill.

If you already have standalone skills, converting them to a plugin is a file move plus a manifest. The skills themselves do not change.

## Beyond skills: the full plugin toolkit

This is where plugins earn their keep. A plugin can bundle five things beyond skills, and they compose to replace what would otherwise be manual setup for every user.

### Slash commands

`commands/` holds flat markdown files that become slash commands. Where skills are triggered by description matching (Claude decides when to apply them), slash commands are triggered by the user typing `/plugin-name:command-name`.

A slash command is useful when the user needs explicit control. For a property analysis plugin, you might have:

- `/property:screen <rightmove-url>` — run the deal screener
- `/property:comps <postcode>` — fetch comparables
- `/property:yield <postcode>` — estimate rental yield

Each command is a `.md` file in `commands/`. The frontmatter uses the same description field, and the body is the instructions Claude follows when the command fires. You can reference `$ARGUMENTS` to pick up whatever the user typed after the command.

### Hooks

`hooks/hooks.json` defines event handlers that fire automatically when Claude does certain things. The format mirrors the `hooks` section in `.claude/settings.json`, and the supported events include:

- **`PreToolUse`** — before a tool runs (useful for guardrails)
- **`PostToolUse`** — after a tool runs (useful for auto-save, logging, validation)
- **`UserPromptSubmit`** — when the user hits enter (useful for auto-routing)

A practical example for a property plugin: a `PostToolUse` hook that fires on `property_report` and writes the output to `./analysis/[postcode].md` so the user builds a local library of reports without having to ask.

Hooks run as shell commands. They receive JSON input on stdin describing the tool call, and they can write output that Claude sees. They are powerful and easy to misuse, so start simple.

### MCP server configuration

`.mcp.json` at the plugin root lets you pre-configure MCP server connections. When the plugin is enabled, Claude automatically has access to whatever servers you declare.

For a BOUCH property plugin, the `.mcp.json` would include the property-shared server URL so buyers do not have to copy-paste the config themselves. One-command install gives them both the skills and the live UK data access.

The schema is identical to the user-level `.mcp.json`. Use `${CLAUDE_PLUGIN_ROOT}` to reference files inside the plugin directory.

### Custom subagents

`agents/` holds custom subagent definitions. A subagent runs in an isolated context, so you can delegate long-running analysis without polluting the main conversation. For a property plugin, you might define a `property-analyst` subagent that handles deep multi-property comparisons in its own thread.

Subagents are defined as markdown files with frontmatter declaring `name`, `description`, `tools`, `model`, and an optional `skills` list (since subagents do not inherit the main conversation's skills automatically).

### Default settings

`settings.json` at the plugin root applies defaults when the plugin is enabled. Currently the two supported keys are `agent` (activate one of the plugin's subagents as the main thread) and `subagentStatusLine` (customise the status line).

Most plugins do not need this. If your plugin shifts how Claude fundamentally behaves, it is useful.

## Marketplaces: how plugins get distributed

A marketplace is a catalog of plugins hosted in a git repository (or local path). Users add your marketplace once, then install individual plugins from it with a single command.

The marketplace itself is defined by a `.claude-plugin/marketplace.json` file at the repo root:

```json
{
  "name": "bouch-plugins",
  "owner": {
    "name": "Paul Boucherat",
    "email": "paul@bouch.dev"
  },
  "metadata": {
    "description": "UK-specific Claude Code plugins for property investors, solicitors, and small business owners.",
    "version": "0.1.0"
  },
  "plugins": [
    {
      "name": "foundations",
      "source": "./plugins/foundations",
      "description": "10 curated skills demonstrating distinct patterns.",
      "version": "1.0.0"
    }
  ]
}
```

Required fields: `name` (kebab-case, not on the reserved list), `owner.name`, and `plugins`. Each plugin entry needs at minimum a `name` and `source`. Relative sources (`./plugins/foundations`) resolve from the marketplace root, so you can host multiple plugins in subdirectories of the same repo.

Once your marketplace repo exists, users install your plugins in three commands:

```
/plugin marketplace add your-org/plugin-repo
/plugin install foundations@your-marketplace-name
/reload-plugins
```

The marketplace name in the install command is the `name` field from `marketplace.json`, not the GitHub repo name. Worth double-checking before telling users how to install.

## Worked example: building the BOUCH foundations plugin

This is the plugin that ships alongside Skills Foundations. It is also the one you are looking at right now if you installed the marketplace. The build process:

1. **Create the marketplace directory.** One git repo, one marketplace, one or more plugins inside it.

```
mkdir -p bouch-plugins/.claude-plugin
mkdir -p bouch-plugins/plugins/foundations/.claude-plugin
mkdir -p bouch-plugins/plugins/foundations/skills
```

2. **Write the marketplace manifest** at `bouch-plugins/.claude-plugin/marketplace.json`. Use the example above as a template. List the foundations plugin with `"source": "./plugins/foundations"`.

3. **Write the plugin manifest** at `bouch-plugins/plugins/foundations/.claude-plugin/plugin.json`. Set `name: foundations`, `version: 1.0.0`, add a description.

4. **Copy your skills in.** For the foundations plugin, these are ten curated SKILL.md files, each demonstrating a distinct pattern (property-report, humaniser, bouch-voice, ai-policy, sop-writer, client-prep, workflow-auditor, meeting-actions, thread-reply, signal-to-post). Each goes in its own subdirectory under `skills/` with the filename `SKILL.md`.

5. **Validate before publishing.** Run `claude plugin validate .` from inside the marketplace directory. This catches structural problems early: missing required fields, bad JSON syntax, invalid relative paths. Fix anything red before you push.

6. **Test locally.** Before putting the repo on GitHub, test the install flow locally:

```
claude plugin marketplace add /path/to/bouch-plugins
claude plugin install foundations@bouch-plugins
claude
```

Inside the Claude Code session, run `/plugin` and verify the foundations plugin appears under the Installed tab with all ten skills loaded. Try invoking one with a matching prompt. If it works, you are ready to publish.

7. **Publish to GitHub.** Create a new repo, push the marketplace directory, and share the install command with users.

```
cd bouch-plugins
git init
git add .
git commit -m "feat: initial bouch-plugins marketplace"
gh repo create paulieb89/bouch-plugins --public
git remote add origin git@github.com:paulieb89/bouch-plugins.git
git push -u origin main
```

From now on, users install with `/plugin marketplace add paulieb89/bouch-plugins` then `/plugin install foundations@bouch-plugins`. When you update a skill, bump the version in `plugin.json`, push the commit, and users get the update on their next marketplace refresh.

## What is next after foundations

Once you have a working marketplace with one plugin, adding more is mechanical. The BOUCH roadmap has four more plugins planned, each following the same pattern:

- **property** — 7 property skills, `.mcp.json` for property-shared, `/property:*` slash commands, a PostToolUse hook that auto-saves reports, a property-analyst subagent
- **legal** — 4 legal skills, `.mcp.json` for uk-legal-mcp and bailii-mcp, `/legal:*` slash commands
- **due-diligence** — 5 to 6 DD skills, `.mcp.json` for uk-due-diligence-mcp, `/dd:*` slash commands
- **p6** — 3 P6 scheduling skills, `.mcp.json` for pyp6xer-mcp

Each plugin is independent. Users install only the verticals they need. Pricing follows the vertical: the paid BOUCH Gumroad products sell the walkthroughs, playbooks, worked examples, and support for each vertical. The plugins themselves stay free on GitHub.

## When to convert a skill to a plugin

You will know it is time when one of these starts happening:

- **You are sharing the same skill with more than two people.** Plugin beats email-attaching a markdown file.
- **Your skill depends on an MCP server.** Bundling the `.mcp.json` into the plugin means users do not have to configure it themselves.
- **You have slash commands that should always be available alongside the skill.** `commands/` in the plugin lets you ship them together.
- **You want hooks to run automatically after the skill fires.** `hooks/hooks.json` lets you wire them up once and forget.
- **You want to version your work.** Plugins update via semver; standalone skills do not have a built-in update mechanism.

Conversely, do not convert a skill to a plugin just because you can. A skill you use alone for debugging a specific codebase is a standalone skill. Keep it simple.

## Gotchas

A few things that will bite you if you are new to the plugin format:

- **Plugin files are copied to a cache on install.** Anything your skill references with a relative path like `../shared/` will not be copied and will break. Keep all references inside the plugin directory, or use `${CLAUDE_PLUGIN_ROOT}` in hook commands.
- **Subagents do not inherit skills automatically.** If you build a custom subagent that should use one of your plugin's skills, you must explicitly list it in the subagent's `skills` frontmatter field.
- **Skill names inside plugins are namespaced.** Remember to say `/plugin-name:skill` when pointing users at a specific skill. If you forget the namespace the skill will not be found.
- **Always restart Claude Code (or run `/reload-plugins`) after changes.** Plugin metadata is cached at startup.
- **Some marketplace names are reserved.** `claude-plugins-official`, `anthropic-plugins`, `agent-skills` and a few others are blocked by Anthropic to prevent impersonation. Stick to your own brand.
- **Private repos work, but background auto-updates need a git token in your environment.** If you want to distribute to paying customers via a private repo, set `GITHUB_TOKEN` in your shell config.

## Summary

A plugin is a directory with a manifest and some skills, optionally extended with hooks, commands, MCP config, and subagents. A marketplace is a git repo that catalogs plugins. Users install with one command and get a working environment without having to configure anything.

For BOUCH, plugins are how we bring Claude Code workflows to non-developers. For you, plugins are how you stop emailing markdown files and start shipping real software. Start with a single skill. Convert to a plugin when you want to share. Add a marketplace when you have two or more plugins worth hosting.

The foundations plugin is the starting point. Build from there.

---

## Appendix: install commands reference

From inside a Claude Code session:

- Add a marketplace from GitHub: `/plugin marketplace add owner/repo`
- Add a marketplace from a local path: `/plugin marketplace add ./path/to/marketplace`
- Install a plugin: `/plugin install plugin-name@marketplace-name`
- Reload after changes: `/reload-plugins`
- Browse plugins interactively: `/plugin` then navigate to Discover / Installed / Marketplaces / Errors tabs
- Validate a marketplace or plugin: `claude plugin validate .` (from inside the directory)

From the CLI (non-interactive):

- `claude plugin marketplace add <source>`
- `claude plugin install <plugin-name>@<marketplace-name>`
- `claude plugin marketplace update <marketplace-name>`
- `claude plugin uninstall <plugin-name>@<marketplace-name>`
- `claude plugin validate <directory>`

## Further reading

- Anthropic's free Introduction to Agent Skills course (skilljar.com) — the definitive source on SKILL.md format
- Claude Code plugin docs at code.claude.com/docs/en/plugins and /discover-plugins
- The BOUCH Learning Path (free on Gumroad) — curated order through Anthropic's 17 free courses with UK context
- bouch.dev for UK-specific MCP servers that pair with these plugins

bouch.dev | paul@bouch.dev | Nottingham, UK
