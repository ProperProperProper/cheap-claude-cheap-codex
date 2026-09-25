#!/usr/bin/env python3
"""
Read-only Claude Code MCP bridge that requires subscription OAuth.

SETUP: Copy this file over your existing claude_subscription_mcp.py
Location: ~/Documents/Codex/.integrations/smart-model-router/claude_subscription_mcp.py

Key changes:
- Line 10: Added "model": "haiku" and "fastMode": True to SETTINGS
"""

import json
import os
import subprocess
import sys

CLAUDE = os.environ.get("CLAUDE_BIN", "claude")

# ⭐ KEY CHANGE: Added model and fastMode settings
SETTINGS = json.dumps({
    "model": "haiku",
    "fastMode": True,
    "env": {
        "ANTHROPIC_API_KEY": "",
        "ANTHROPIC_AUTH_TOKEN": "",
        "ANTHROPIC_BASE_URL": ""
    }
})


def clean_env():
    env = os.environ.copy()
    for key in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL"):
        env.pop(key, None)
    return env


def ask(prompt):
    env = clean_env()
    status = subprocess.run(
        [CLAUDE, "--settings", SETTINGS, "auth", "status", "--json"],
        env=env, capture_output=True, text=True, timeout=15,
    )
    try:
        auth = json.loads(status.stdout)
    except ValueError:
        raise RuntimeError("Could not check Claude Code authentication.")
    if not auth.get("loggedIn") or auth.get("authMethod") != "claude.ai" or auth.get("apiKeySource"):
        raise RuntimeError("Claude subscription login is not active. Sign in to Claude Code with your Claude account first.")
    result = subprocess.run(
        [CLAUDE, "--settings", SETTINGS, "--print", "--output-format", "json",
         "--tools", "", "--permission-mode", "dontAsk", "--no-session-persistence", prompt],
        env=env, capture_output=True, text=True, timeout=180,
    )
    try:
        data = json.loads(result.stdout)
    except ValueError:
        raise RuntimeError((result.stderr or "Claude Code failed")[-500:])
    if data.get("is_error"):
        raise RuntimeError(str(data.get("result") or "Claude Code returned an error"))
    if result.returncode:
        raise RuntimeError((result.stderr or "Claude Code failed")[-500:])
    return str(data.get("result") or "")


TOOL = {
    "name": "ask_claude_subscription",
    "description": (
        "Ask Claude via subscription auth. Responses are streamed to stdout "
        "and also returned as a JSON/text response."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "The prompt to ask Claude."
            }
        },
        "required": ["prompt"]
    }
}
