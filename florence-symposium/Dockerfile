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
      @agentclientprotocol/claude-agent-acp@${CLAUDE_AGENT_ACP_VERSION} && \
    npm cache clean --force

# Default models for Claude Code. Users can override these in ~/.claude/settings.json ("env" block),
# with `claude --model`, or with /model in a session.
ENV ANTHROPIC_MODEL=sonnet \
    ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-6 \
    ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5 \
    DISABLE_AUTOUPDATER=1

# Hub-wide Claude Code managed settings: apply to every user and can't be overridden.
#   availableModels         only Sonnet and Haiku can be picked in /model or user settings
#   permissions.defaultMode sessions start in manual mode, not auto; users can still Shift+Tab to auto
#   statusLine              shows today's (UTC) LiteLLM spend against the $20 daily budget
#   extraKnownMarketplaces  registers the uw-ssec/rse-plugins marketplace from GitHub
#   enabledPlugins          installs these three plugins at each user's first session
# See https://code.claude.com/docs/en/managed-settings
COPY managed-settings.json budget-statusline.py /etc/claude-code/

# Open Markdown files in the rendered preview by default instead of the text editor.
# We assume the base image does not provide its own overrides.json, so we can just copy in our version.
COPY overrides.json ${NB_PYTHON_PREFIX}/share/jupyter/lab/settings/overrides.json
