# Codex Setup Guide

Complete guide to forcing Codex to use Haiku + Fast Mode.

## Prerequisites

- Codex installed on macOS/Windows/Linux
- Codex MCP integration with Claude routing enabled
- Claude Code CLI installed

## Step 1: Locate Your Integration File

Find `claude_subscription_mcp.py` in your Codex directory:

**Typical locations:**
- macOS: `~/Documents/Codex/.integrations/smart-model-router/claude_subscription_mcp.py`
- Windows: `%USERPROFILE%\Documents\Codex\.integrations\smart-model-router\claude_subscription_mcp.py`
- Linux: `~/Documents/Codex/.integrations/smart-model-router/claude_subscription_mcp.py`

**Can't find it?**
```bash
# Search for the file
find ~/Documents -name "claude_subscription_mcp.py" 2>/dev/null
```

## Step 2: Edit the Settings

Open `claude_subscription_mcp.py` in your text editor. Around **line 10**, you'll see:

```python
CLAUDE = os.environ.get("CLAUDE_BIN", "claude")
SETTINGS = json.dumps({"env": {"ANTHROPIC_API_KEY": "", "ANTHROPIC_AUTH_TOKEN": "", "ANTHROPIC_BASE_URL": ""}})
```

**Replace with:**

```python
CLAUDE = os.environ.get("CLAUDE_BIN", "claude")
SETTINGS = json.dumps({"model": "haiku", "fastMode": True, "env": {"ANTHROPIC_API_KEY": "", "ANTHROPIC_AUTH_TOKEN": "", "ANTHROPIC_BASE_URL": ""}})
```

**Save the file.**

## Step 3: Restart Codex

Completely exit Codex (don't just close the window):

**macOS:**
```bash
# Via menu: Codex → Quit Codex
# Or terminal:
pkill -f "Codex"
```

**Then reopen Codex** and ask a question that routes to Claude. It will now use Haiku + Fast Mode.

## Step 4: Verify

Ask Codex a routing question:

```
"What model are you using for Claude routing?"
```

**Expected response:**
```
I'm using Haiku model with fast mode enabled.
```

Or check logs:

```bash
# macOS
tail -f ~/Library/Logs/Codex.log | grep -i "haiku\|model"

# Windows
Get-Content "$env:APPDATA\Codex\logs\*.log" | Select-String -Pattern "haiku|model"

# Linux
tail -f ~/.local/share/Codex/logs/*.log | grep -i "haiku\|model"
```

## Understanding the Change

### What Changed
- `"model": "haiku"` — Forces Claude routing to use Haiku (cheapest)
- `"fastMode": True` — Enables fast mode (faster output generation)

### How It Works
When you ask Codex a question that triggers Claude routing:
1. The smart router detects a question needs Claude
2. It calls `ask()` function with your prompt
3. `ask()` uses the updated SETTINGS
4. Your prompt is sent to Claude via CLI with `--model haiku --fast`
5. Haiku + Fast Mode responds
6. Response is returned to Codex

### What Stays the Same
- All Codex features work identically
- No breaking changes
- You can still override per-query if needed

## Advanced: Per-Query Overrides

If you need a more powerful model for a specific query, you can edit `ask()` function to accept model overrides. Example:

```python
def ask(prompt, model="haiku"):
    env = clean_env()
    status = subprocess.run(
        [CLAUDE, "--settings", SETTINGS, "--model", model, "auth", "status", "--json"],
        # ... rest of function
    )
```

Then calls can specify: `ask(prompt, model="opus")` for one-off powerful queries.

## Troubleshooting

### Codex still using expensive models

**Check 1: File was edited correctly**
```bash
grep "haiku" ~/Documents/Codex/.integrations/smart-model-router/claude_subscription_mcp.py
# Should output: {"model": "haiku", "fastMode": True, ...}
```

**Check 2: Codex fully restarted**
```bash
# Verify Codex process is not running
ps aux | grep -i codex | grep -v grep
# Should return nothing

# Restart Codex
open /Applications/Codex.app  # or your Codex path
```

**Check 3: MCP server reloaded**
In Codex settings, disable and re-enable the smart_models MCP server.

### Permission denied when editing file

If you get a permission error:
```bash
chmod +w ~/Documents/Codex/.integrations/smart-model-router/claude_subscription_mcp.py
# Then edit the file again
```

### Changes not applying

1. Clear Codex cache:
   ```bash
   rm -rf ~/.codex/cache
   rm -rf ~/Library/Caches/Codex  # macOS
   ```

2. Restart Codex completely

3. Check that `fastMode` is `True` (capital T, not `true`)

### "Claude subscription login not active" error

Your Claude Code CLI needs to be authenticated:
```bash
claude auth login
# or
claude auth status
```

Verify you're logged in with your Claude subscription.

## Monitoring & Optimization

### Monitor API usage
```bash
# Via Claude Code
claude --help
# Look for --max-budget-usd to set spending limits
```

### Check actual model being used
In Codex, ask:
```
"Show me your model information and settings."
```

### Track cost savings
- **Before:** ~$0.003 per query (Sonnet average)
- **After:** ~$0.0008 per query (Haiku average)
- **100 queries:** $0.30 → $0.08 (save $0.22)

## Performance Tuning

### If responses are too brief
Fast mode reduces output tokens. If you need longer responses:

```python
SETTINGS = json.dumps({
    "model": "haiku",
    "fastMode": False,  # Disable fast mode
    "env": {...}
})
```

Then restart Codex.

### If Codex routing is slow
Haiku is already fast. Fast mode speeds it up further. If you need more capability:

```python
SETTINGS = json.dumps({
    "model": "sonnet",  # Use Sonnet instead
    "fastMode": True,
    "env": {...}
})
```

Cost will be ~3x higher but reasoning capability increases.

## Rollback

To revert to default settings:

```python
SETTINGS = json.dumps({"env": {"ANTHROPIC_API_KEY": "", "ANTHROPIC_AUTH_TOKEN": "", "ANTHROPIC_BASE_URL": ""}})
```

Then restart Codex.

## Next Steps

- **Claude CLI Setup:** See [Setup Guide](README.md#claude-cli-setup) for CLI configuration
- **Advanced Routing:** Edit `smart_model_router_mcp.py` for custom detection logic
- **Cost Tracking:** Monitor spending in your Claude account dashboard

---

**Questions?** Open an issue on GitHub or check [README.md](README.md).
