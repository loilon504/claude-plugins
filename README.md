# claude-plugins

Personal Claude Code plugins, as one marketplace (`loi-plugins`).

| Plugin | What |
|---|---|
| [tech-explainer](plugins/tech-explainer) | explains a technical system as an artifact page in one house style |

## Install on a machine

One step (it adds the marketplace too):

```sh
claude plugin install tech-explainer --marketplace loilon504/claude-plugins
```

Or in two, the same from inside a session with `/plugin`:

```sh
claude plugin marketplace add loilon504/claude-plugins
claude plugin install tech-explainer@loi-plugins
```

Then start a new session (or run `/reload-plugins`). Update later with
`claude plugin marketplace update loi-plugins && claude plugin update tech-explainer@loi-plugins`.

## Work on a plugin

Link the plugin folder into the skills folder; Claude Code loads it as `<name>@skills-dir`, and edits apply
on the next session without reinstalling:

```sh
ln -s "$PWD/plugins/tech-explainer" ~/.claude/skills/tech-explainer
```

Do not also install the same plugin from the marketplace on that machine, or the skill loads twice.
Check before committing: `claude plugin validate .` and `claude plugin validate plugins/<name>`.
