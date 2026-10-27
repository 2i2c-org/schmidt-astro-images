"""Claude Code status line: today's LiteLLM spend against the $20 daily budget.

Adapted from https://docs.litellm.ai/docs/tutorials/claude_code_budget_statusline
in Python, since the image has no curl or jq. "Today" is the UTC date, as
LiteLLM buckets daily spend in UTC. Prints nothing on any failure so a slow or
unreachable proxy never holds up Claude Code.
"""

import datetime
import json
import os
import urllib.parse
import urllib.request

DAILY_BUDGET = 20.0

base = os.environ.get("LITELLM_BASE_URL") or os.environ.get("ANTHROPIC_BASE_URL")
key = os.environ.get("LITELLM_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")
if not (base and key):
    raise SystemExit

base = base.rstrip("/").removesuffix("/anthropic").removesuffix("/v1")
today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
query = urllib.parse.urlencode({"start_date": today, "end_date": today})
request = urllib.request.Request(
    f"{base}/user/daily/activity?{query}",
    headers={"Authorization": f"Bearer {key}"},
)
try:
    with urllib.request.urlopen(request, timeout=2) as response:
        spend = json.load(response)["metadata"]["total_spend"]
except Exception:
    raise SystemExit

remaining = max(DAILY_BUDGET - spend, 0)
print(f"Daily budget: ${spend:.2f} spent, ${remaining:.2f} remaining of ${DAILY_BUDGET:.2f}")
