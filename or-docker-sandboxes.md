# claude-pod or Docker Sandboxes?

Both keep a coding agent from running arbitrary commands directly on your machine.
The main difference is **where your main Claude runs**:

- **[Docker Sandboxes](https://www.docker.com/products/docker-sandboxes/) (`sbx`)** put the agent itself in the box.
  Claude runs inside a microVM, typically with `--dangerously-skip-permissions`, and the VM is the security boundary.
- **claude-pod** keeps your normal Claude in VSCode or your terminal, in `acceptEdits` mode, and sends only
  its *commands* to the box.  Running Claude inside the pod is optional.

| | Docker Sandboxes (`sbx`) | claude-pod |
|---|---|---|
| Isolation | microVM per sandbox: its own kernel and its own Docker daemon, with sudo inside | Containers sharing one podman VM kernel (on Mac). Lighter, but a weaker boundary |
| Network | Host-side proxy with **per-domain** policy (Open / Balanced / Locked Down, plus per-domain allows). A blocked request gets a 403 naming the domain. Raw TCP, UDP and ICMP are blocked | **Port-level**: only 443 goes out, to any host. Domain blocking is on our "Future?" list |
| Credentials | The proxy **injects** API keys into outbound requests, so the key never enters the VM | Nothing from the host is visible. In-pod Claude's login lives in `~/.claude-pod` (see [Known gaps](#known-gaps)) |
| Filesystem | The working dir, in direct mode or clone mode. Anything in the tree (a `.env`, untracked files) is readable | The repo r/w with `.git`, `.claude` and `.vscode` read-only, **plus every `$CLAUDE_PODS` dir read-only** for browsing other repos |
| Docker inside the box | Yes | No |
| Dev servers | (not compared) | Same port numbers on `localhost`, claimed automatically |
| Platforms | Apple silicon macOS 14+, Windows 11, Ubuntu 24.04+ with KVM | Anything podman runs on |
| What it is | A Docker product: `sbx login`, and org policy can override your local rules | About 350 lines of bash you can read in one sitting |


## Where Docker Sandboxes are stronger
- A kernel boundary per sandbox.
- Domain allowlists.
- Credential injection.
- Docker inside the box.

For running an agent unattended with every permission skipped, it's the more serious sandbox.


## Where claude-pod is stronger
- **Your IDE workflow doesn't change.** Claude in VSCode still sees your editor, diffs and selections,
  and only the riskier work moves out.
- **Read-only access to all your other repos.** Very useful when you have lots of related clones.
- **`.git` is read-only**, so commits, pushes and other history changes stay with the human.
- It's tiny, auditable and needs no vendor account.


## Known gaps
`~/.claude-pod` (in-pod Claude's login, sessions and memory) is mounted **r/w into every pod**,
even ones that only ever get `exec`.  So any command in any pod can read that login token,
or plant a memory file that another repo's in-pod Claude would later load.
If you don't run Claude inside pods, nothing sensitive is in that dir.
A future fix: mount it only when running Claude in the pod, or read-only for `exec`.


## Which one?
They're complementary rather than competitors.
Use **Docker Sandboxes** if you want a fully unattended agent in a microVM.
Use **claude-pod** if you want to keep your normal Claude and just stop approving every command.

---

*The Docker Sandboxes details were gathered in October 2026 from Docker's docs and third-party write-ups
(one checked against `sbx` v0.43.0, September 2026).  `sbx` is changing fast, so check Docker's docs for current specifics.*

Sources:
- [Docker Sandboxes (product page)](https://www.docker.com/products/docker-sandboxes/)
- [Docker blog: Run Claude Code and more safely](https://www.docker.com/blog/docker-sandboxes-run-claude-code-and-other-coding-agents-unsupervised-but-safely/)
- [Docker docs: Sandboxes architecture](https://docs.docker.com/ai/sandboxes/architecture)
- [Docker docs: Sandboxes integrations](https://docs.docker.com/ai/sandboxes/integrations/)
- [Docker docs: Upstream proxy](https://docs.docker.com/ai/sandboxes/configuration/upstream-proxy/)
- [Docker docs: Claude Code sandbox with Model Runner](https://docs.docker.com/guides/claude-code-sandbox-model-runner/)
- [Collabnix: What an agent can and can't do](https://collabnix.com/sandboxing-claude-code-with-docker-sandboxes-what-an-agent-can-and-cant-do-with-full-access/)
- [rdiachenko: Sandboxing Claude Code in a microVM with sbx](https://rdiachenko.com/til/docker/sbx/)
- [Sandboxing Claude and MCP: a dive into Docker sbx](https://hrittikhere.com/posts/sandbox-claude-code-mcp-docker-sbx)
- [Ry Walker: Docker Sandboxes research](https://rywalker.com/research/docker-sandboxes)
- [Arrange Act Assert: when Claude Code needs Docker](https://arrangeactassert.com/posts/docker-sandboxes-when-claude-code-needs-docker/)
- [Florian Bruniaux: Docker Sandboxes isolation evaluation](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/docs/resource-evaluations/docker-sandboxes-isolation.md)
