FROM base_image

COPY environment.yml /tmp/environment.yml

RUN mamba env update --prefix ${NB_PYTHON_PREFIX} --file /tmp/environment.yml

# Claude Code (terminal) and the ACP bridge behind JupyterAI's @Claude persona.
# Pinned so an upstream release mid-event cannot change what attendees get. Bump deliberately.
ARG CLAUDE_CODE_VERSION=2.1.220
ARG CLAUDE_AGENT_ACP_VERSION=0.91.0
RUN npm install -g --prefix ${NB_PYTHON_PREFIX} \
      @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION} \
      @agentclientprotocol/claude-agent-acp@${CLAUDE_AGENT_ACP_VERSION}
