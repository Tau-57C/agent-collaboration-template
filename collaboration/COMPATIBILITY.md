# Client compatibility

[Project mainline](../PROJECT.md) · [Workflow](GUIDE.md) · [Participant examples](PARTICIPANTS.md)

The same project files can be shared by any assistant that can follow the rules, read the common inputs, and write to its assigned directory. When a client has no project filesystem access, a person can transfer the brief and save the response for that participant.

| Client | Load the shared rules | Transfer visible dialogue | Verification |
|---|---|---|---|
| Codex | Use the project-root `AGENTS.md`. [OpenAI documentation](https://learn.chatgpt.com/docs/customization/overview#agents-guidance) | Supported Codex CLI sessions have `/export`. Copy visible dialogue when using a surface without that option. [Codex commands](https://learn.chatgpt.com/docs/developer-commands) | Documented; end-to-end in that client pending |
| Qoder | The Qoder IDE documents project-level `AGENTS.md`. Qoder CLI CN uses `AGENTS.md` as its default context filename. [IDE rules](https://docs.qoder.com/user-guide/rules) · [CLI CN memory](https://docs.qoder.cn/cli/memory) | Qoder CN task history offers export and Qoder CLI CN documents `/export`. [Task export](https://docs.qoder.cn/qoder/task-management) · [CLI sessions](https://docs.qoder.cn/cli/sessions) | Documented; end-to-end in that client pending |
| Gemini CLI | Add `@./AGENTS.md` to the project `GEMINI.md`, or configure Gemini CLI to load `AGENTS.md`. [Gemini CLI context guide](https://geminicli.com/docs/cli/gemini-md/) | Copy the visible dialogue into the assigned branch when needed. | Documented; end-to-end in that client pending |
| Claude Code | Check `AGENTS.md` support for your installation. Where needed, import it with `@./AGENTS.md` in the root `CLAUDE.md`. [Claude Code instructions](https://code.claude.com/docs/en/memory) | Save or copy visible messages into the assigned branch. | Documented; live client test pending |
| Cursor | Place `AGENTS.md` in the project root. [Cursor rules](https://cursor.com/docs/rules) | Save or copy visible messages into the assigned branch. | Documented; live client test pending |
| GitHub Copilot CLI | Use repository `AGENTS.md`. Check loaded instruction files with `/instructions`. [Copilot CLI instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions) | Save or copy visible messages into the assigned branch. | Documented; live client test pending |
| OpenCode | Use a project-level `AGENTS.md`. [OpenCode instructions](https://opencode.ai/docs/instructions) | Save or copy visible messages into the assigned branch. | Documented; live client test pending |
| Other tools | Use the native project rule mechanism to reference `AGENTS.md`, or supply it as instructions in the session. | Save or copy visible dialogue into the assigned branch and document the cutoff. | Check the tool and access mode before listing it as tested |

## Test record

The local file workflow was exercised with fictional two- and three-participant rounds, including cases where review or merge should be blocked. Tests invoke the Python checker against on-disk artifacts. The public six-participant example uses synthetic material and is checked by the same tool. Actual multi-client session export, live cross-reading, and strong directory isolation require separate tests in the chosen clients and workspaces.
