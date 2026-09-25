# Haiku + Fast Mode Setup

Force Claude CLI & Codex to use the cheapest, fastest configuration for maximum cost savings.

**Cost Reduction:** ~50-80% cheaper than default models  
**Speed Improvement:** Fast mode reduces output tokens  
**Setup Time:** ~2 minutes for both tools

## Quick Start

### Claude CLI (30 seconds)

Edit or create `~/.claude/settings.json`:

```json
{
  "theme": "dark",
  "model": "haiku",
  "fastMode": true
}
```

### Codex (2 minutes)

Edit `claude_subscription_mcp.py` in your Codex MCP integration directory (typically `~/Documents/Codex/.integrations/smart-model-router/`):

```python
# Around line 10, change this:
SETTINGS = json.dumps({"env": {"ANTHROPIC_API_KEY": "", ...}})

# To this:
SETTINGS = json.dumps({"model": "haiku", "fastMode": True, "env": {"ANTHROPIC_API_KEY": "", ...}})
```

Restart Codex. Done! ✅

## Why Haiku + Fast Mode?

| Model | Cost/1M tokens | Speed | Best For |
|-------|----------------|-------|----------|
| **Haiku** ⭐ | $0.80 | Fastest | Code, summaries, high-volume |
| Sonnet | $3.00 | Fast | Balanced capability |
| Opus | $15.00 | Slower | Complex reasoning |

### Cost Savings Example
- **100 questions/month on Sonnet:** $0.30
- **100 questions/month on Haiku:** $0.08
- **Monthly savings:** $0.22 (73% reduction)

At scale (1,000 queries/month), you save **$2.20+** with Haiku + Fast Mode.

## Detailed Setup

### Claude CLI Setup

**File:** `~/.claude/settings.json`

```json
{
  "theme": "dark",
  "model": "haiku",
  "fastMode": true,
  "verbose": false
}
```

**Verify:**
```bash
claude "What model are you using?"
# Response: "I'm Claude, using Haiku model..."
```

**Override per session:**
```bash
claude --model opus "Complex reasoning task"  # Use Opus this once
claude "Normal task"  # Back to Haiku
```

### Codex Setup

**File path:** Typically `~/Documents/Codex/.integrations/smart-model-router/claude_subscription_mcp.py`

**Before:**
```python
CLAUDE = os.environ.get("CLAUDE_BIN", "claude")
SETTINGS = json.dumps({"env": {"ANTHROPIC_API_KEY": "", "ANTHROPIC_AUTH_TOKEN": "", "ANTHROPIC_BASE_URL": ""}})
```

**After:**
```python
CLAUDE = os.environ.get("CLAUDE_BIN", "claude")
SETTINGS = json.dumps({"model": "haiku", "fastMode": True, "env": {"ANTHROPIC_API_KEY": "", "ANTHROPIC_AUTH_TOKEN": "", "ANTHROPIC_BASE_URL": ""}})
```

**Restart Codex** (quit and reopen). All Claude routing now uses Haiku + fast mode.

## Configuration Reference

| Tool | File | Setting |
|------|------|---------|
| **Claude CLI** | `~/.claude/settings.json` | `"model": "haiku"` + `"fastMode": true` |
| **Codex** | `claude_subscription_mcp.py` | `"model": "haiku"` + `"fastMode": True` |

## FAQ

### Can I override this per session?
Yes! Claude CLI respects `--model` flag:
```bash
claude --model opus "complex task"  # Override to Opus
claude "normal task"                # Back to Haiku (default)
```

### What if I need more capability?
Haiku is excellent for code tasks, summaries, and focused work. For complex reasoning, use `--model opus` on demand. Fast mode is ideal for high-volume work.

### Does fast mode affect output quality?
Fast mode reduces output tokens (more concise), not quality. Responses are shorter but still complete. Perfect for code, summaries, and structured output.

### Will this break my workflows?
No. Haiku + fast mode is backward compatible. All Claude CLI and Codex features work identically. The only difference you'll notice is in your billing.

### How do I check what's configured?
```bash
# Claude CLI
cat ~/.claude/settings.json

# Codex
grep "SETTINGS = " ~/Documents/Codex/.integrations/smart-model-router/claude_subscription_mcp.py
```

### Can I use different settings for different projects?
Yes! Create `.claude/settings.json` in your project directory. Claude Code reads project settings first:
```bash
# Project-specific Haiku config
mkdir my-project/.claude
echo '{"model": "haiku", "fastMode": true}' > my-project/.claude/settings.json
```

## Performance Notes

### Latency
- Haiku: ~200-300ms average response time
- Sonnet: ~300-400ms average response time
- **Fast mode adds 0-50ms savings** by reducing output generation

### Quality
- Haiku excels at code, structured output, and focused tasks
- Use Opus for open-ended reasoning, creative work, or complex analysis
- Fast mode produces more concise (not lower quality) responses

### Recommendations
- **Use Haiku + Fast Mode for:**
  - Code generation and refactoring
  - API interactions and tool use
  - Summaries and structured output
  - High-volume querying
  - Trading/finance calculations (like OMLX analysis)

- **Use Sonnet/Opus for:**
  - Complex reasoning tasks
  - Open-ended creative work
  - Long-form analysis
  - When you need maximum capability

## Advanced: Custom Model Routing

For Codex, if you want different models for different routing modes, edit `smart_model_router_mcp.py`:

```python
# Default model for Claude routing
DEFAULT_MODEL = "haiku"
FAST_MODE = True

# Override as needed:
SETTINGS = json.dumps({
    "model": DEFAULT_MODEL,
    "fastMode": FAST_MODE,
    "env": {...}
})
```

## Troubleshooting

### Claude CLI not using Haiku
Check your settings:
```bash
cat ~/.claude/settings.json
```

If empty or missing `model` field, add it and save.

### Codex still using expensive model
1. Verify the file path to `claude_subscription_mcp.py`
2. Check the SETTINGS variable was updated (around line 10)
3. Restart Codex completely (quit from menu, not just close window)
4. Check logs: `~/Applications/ChatGPT.app/Contents/Logs/` (varies by OS)

### Settings not applying
- **Claude CLI:** Clear cache: `rm -rf ~/.claude/cache`
- **Codex:** Restart the app
- Both should apply within seconds

## Contributing

Found a better setup? Have improvements? Open an issue or PR!

## License

MIT — Use freely, modify, share.

## Resources

- [Claude API Docs](https://docs.anthropic.com)
- [Claude Code Guide](https://claude.com/claude-code)
- [Haiku Model Card](https://docs.anthropic.com/claude/docs/models-overview#claude-haiku)

---

**Questions?** Open an issue on GitHub.

**Setup complete?** You're now saving 50-80% on Claude usage. 🎉
