# Choose participants / 选择参与者

[Workflow](GUIDE.md) · [Client compatibility](COMPATIBILITY.md)

Each node has its own roster in `node.json`. Invite the assistants or sessions you want for that task. Every selected ID gets a separate branch and status file. Different IDs can use the same client, and a client name can be written in any language. The checker uses the IDs from the node.

每个节点都单独选名单。参与者可以来自不同工具，也可以是同一个工具里的两个独立会话。只把这次需要交付的参与者填进名单。

## Examples of tools and access modes

| Mode | Example labels |
|---|---|
| Terminal or local coding workflow | Codex, Claude Code, Gemini CLI, GitHub Copilot CLI, OpenCode, Aider, Amp, goose |
| Editor or IDE workflow | Qoder, Cursor, Cline, Roo Code, Junie, Kiro, Continue, Windsurf |
| Browser, remote, or self-hosted workflow | ChatGPT in a browser, Claude on the web, Gemini on the web, or a team-hosted assistant |

These are examples for the `label` field. If a client can access the workspace, use its own branch directory. For a browser chat or other client with manual transfer, provide the same brief and fixed inputs, then save its actual response, evidence, and available transcript into its branch. See [client compatibility](COMPATIBILITY.md) for the clients with specific setup guidance.

## Copyable roster examples

### Three tools for one code task

```json
{
  "id": "N03",
  "participants": [
    { "id": "claude", "label": "Claude Code" },
    { "id": "cursor", "label": "Cursor" },
    { "id": "opencode", "label": "OpenCode" }
  ]
}
```

### Two independent sessions in the same tool

```json
{
  "id": "N07",
  "participants": [
    { "id": "gemini-session-a", "label": "Gemini CLI" },
    { "id": "gemini-session-b", "label": "Gemini CLI" }
  ]
}
```

### A local assistant and a manually transferred answer

```json
{
  "id": "N11",
  "participants": [
    { "id": "local-aider", "label": "Aider" },
    { "id": "browser-reviewer", "label": "浏览器助手（手动归档）" }
  ]
}
```

Use a different roster for the next node whenever it suits the work. If a participant withdraws during an independent round, ask the user whether to restart with a revised roster. Preserve earlier outputs under their original round.
