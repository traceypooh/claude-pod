# Claude Code in a throwaway container, one per repo session.
# Built and launched by claude-pod -- see there for mounts.
#
# No COPY and no context: build from stdin (`claude-pod --build`).

# Same base + distro hugo as politicaladarchive's Dockerfile, so a `hugo`
# run in here matches what the real build does.
FROM alpine:3.24

# libgcc/libstdc++ + system ripgrep: what Claude Code needs on musl.
# GNU coreutils/grep/sed/findutils so shell one-liners behave like the ones
# written for Linux boxes, not busybox.
RUN apk add --no-cache \
      bash zsh git less curl jq file procps coreutils findutils grep sed diffutils \
      libgcc libstdc++ ripgrep \
      deno nodejs npm \
      python3 \
      caddy hugo \
      brotli gzip \
      nftables

RUN npm install -g @anthropic-ai/claude-code && npm cache clean --force

# The global npm dir is root-owned and the container runs as you, so the
# self-updater can't work anyway. Update by rebuilding: `claude-pod --build`.
ENV DISABLE_AUTOUPDATER=1 \
    USE_BUILTIN_RIPGREP=0

# Throwaway HOME for caches etc. Anything worth keeping lives in
# CLAUDE_CONFIG_DIR, which the wrapper mounts from ~/.claude-pod.
RUN mkdir -m 1777 /home/claude
ENV HOME=/home/claude \
    SHELL=/bin/zsh

ENTRYPOINT ["claude"]
