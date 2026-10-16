FROM base_image

COPY environment.yml /tmp/environment.yml

RUN mamba env update --prefix ${NB_PYTHON_PREFIX} --file /tmp/environment.yml

# Claude Code (terminal) and the ACP bridge behind JupyterAI's @Claude persona.
# See https://jupyter-ai.readthedocs.io/en/stable/getting-started.html
# Check release dates with `npm view @agentclientprotocol/claude-agent-acp time`
ARG CLAUDE_CODE_VERSION=2.1.292
ARG CLAUDE_AGENT_ACP_VERSION=0.91.0
RUN npm install -g --prefix ${NB_PYTHON_PREFIX} \
      @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION} \
      @agentclientprotocol/claude-agent-acp@${CLAUDE_AGENT_ACP_VERSION} \
      npm cache clean --force

# Default models for Claude Code. Users can override these in ~/.claude/settings.json ("env" block),
# with `claude --model`, or with /model in a session.
ENV ANTHROPIC_MODEL=sonnet \
    ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-6 \
    ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5 \
    DISABLE_AUTOUPDATER=1
