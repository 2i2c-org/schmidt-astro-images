# Inherit from an upstream image
FROM pangeo/pangeo-notebook:2026.06.04

# We copy the `environment.yml` file in this repo, only adding in extra
# packages that aren't in our base image.
COPY environment.yml /tmp/environment.yml

RUN mamba env update --prefix ${NB_PYTHON_PREFIX} --file /tmp/environment.yml

# Claude Code (terminal) and the ACP bridge behind JupyterAI's @Claude persona.
# Pinned so an upstream release mid-event cannot change what attendees get. Bump deliberately.
ARG CLAUDE_CODE_VERSION=2.1.220
ARG CLAUDE_AGENT_ACP_VERSION=0.91.0
RUN npm install -g --prefix ${NB_PYTHON_PREFIX} \
      @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION} \
      @agentclientprotocol/claude-agent-acp@${CLAUDE_AGENT_ACP_VERSION}

# Jupyter AI 3.2 pre-release (PyPI only; conda-forge has only ~=3.0). This MUST stay after the
# conda step above, which would otherwise be free to replace what uv installs. uv resolves the
# whole pre-release family in one pass.
RUN ${NB_PYTHON_PREFIX}/bin/uv pip install \
      --python ${NB_PYTHON_PREFIX}/bin/python \
      --prerelease=allow \
      "jupyter-ai==3.2.0a1"

# System-wide Claude Code settings. Lives in /etc, not $HOME, because the hub mounts a
# persistent home over /home/jovyan and would hide anything written there at build time.
# Symbolic mode: files 644, directories 755. A plain --chmod=644 also strips the execute bit from the
# /etc/claude-code directory BuildKit creates, which makes the file unreadable for the notebook user.
COPY --chmod=u=rwX,go=rX managed-settings.json /etc/claude-code/managed-settings.json

# Fail the build if the AI layer is incomplete.
RUN node --version | grep -E '^v(2[2-9]|[3-9][0-9])\.' \
 && claude --version | grep -F "2.1.220" \
 && command -v claude-agent-acp \
 && ${NB_PYTHON_PREFIX}/bin/python -c "import importlib.metadata as m; assert m.version('jupyter-ai') == '3.2.0a1', m.version('jupyter-ai'); eps = [e.name.lower() for e in m.distribution('jupyter-ai-acp-client').entry_points]; print('acp-client entry points:', eps); assert any('claude' in n for n in eps), eps" \
 && jupyter lab --version

# The stock pangeo-notebook image already reports 4 `uv pip check` problems (xmip/xgcm,
# lonboard/anywidget, and pygobject/pycairo, which conda ships without WHEEL files). Fail only
# on problems outside that baseline, so the jupyter-ai pre-release cannot silently break anything new.
RUN ! ${NB_PYTHON_PREFIX}/bin/uv pip check --python ${NB_PYTHON_PREFIX}/bin/python 2>&1 \
      | grep '^The package' \
      | grep -vE '`(xmip|lonboard|pygobject|pycairo)`'

# The image, not the hub, decides the model names; nothing relaxes the permission mode.
RUN ${NB_PYTHON_PREFIX}/bin/python -c "import json; s = json.load(open('/etc/claude-code/managed-settings.json')); e = s['env']; assert e['ANTHROPIC_MODEL'] == 'claude-sonnet-4-6'; assert e['ANTHROPIC_DEFAULT_SONNET_MODEL'] == 'claude-sonnet-4-6'; assert e['ANTHROPIC_DEFAULT_HAIKU_MODEL'] == 'claude-haiku-4-5'; assert e['ANTHROPIC_SMALL_FAST_MODEL'] == 'claude-haiku-4-5'; assert 'permissions' not in s, 'must not change permission mode'"