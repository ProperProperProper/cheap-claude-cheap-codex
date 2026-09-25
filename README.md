# 💰 Cheap Claude + Cheap Codex

**Force BOTH Claude CLI AND Codex to use Haiku + Fast Mode for maximum cost savings.**

Save **50-80% on Claude costs** while keeping full capability. Works with both tools.

---

## 📋 Quick Navigation

| Tool | Time | File | Goal |
|------|------|------|------|
| **Claude CLI** | 30 sec | `~/.claude/settings.json` | Add 2 settings → Use Haiku + fast mode always |
| **Codex** | 2 min | `claude_subscription_mcp.py` | Edit 1 line → Route to Haiku + fast mode |

---

## ⚡ Quick Start

### Claude CLI (30 seconds)

Edit or create **`~/.claude/settings.json`:**

```json
{
  "theme": "dark",
  "model": "haiku",
  "fastMode": true
}
```

**Test:** `claude "What model are you using?"` → Should say Haiku ✅

---

### Codex (2 minutes)

**Find:** `~/Documents/Codex/.integrations/smart-model-router/claude_subscription_mcp.py`

**Edit line ~10** from:
```python
SETTINGS = json.dumps({"env": {"ANTHROPIC_API_KEY": "", ...}})
```

**To:**
```python
SETTINGS = json.dumps({"model": "haiku", "fastMode": True, "env": {"ANTHROPIC_API_KEY": "", ...}})
```

**Restart Codex.** Done! ✅

---

## 💡 Why? Cost Breakdown

### Per 1 Million Tokens
| Model | Cost | Speed |
|-------|------|-------|
| **Haiku** 🏆 | $0.80 | Fastest |
| Sonnet | $3.00 | Fast |
| Opus | $15.00 | Slower |

### Real-World Savings (100 queries/month)

| Scenario | Default | Cheap Claude + Codex | Savings |
|----------|---------|----------------------|---------|
| Claude CLI only | $0.30 | $0.08 | $0.22 (73%) |
| Codex only | $0.30 | $0.08 | $0.22 (73%) |
| **Both tools** | $0.60 | $0.16 | **$0.44 (73%)** |

**At scale (1,000 queries/month):** Save **$4.40/month** with both tools.

---

## 📚 Complete Guides

### Claude CLI Setup (Full)
See **[SETUP_CLI.md](SETUP_CLI.md)** for:
- Detailed file location and syntax
- How to verify settings work
- Per-session overrides
- Project-specific settings
- Troubleshooting

### Codex Setup (Full)
See **[SETUP_CODEX.md](SETUP_CODEX.md)** for:
- Finding your integration file (multiple locations)
- Exact line-by-line edit instructions
- How to verify Codex is using Haiku
- MCP routing explanation
- Detailed troubleshooting

---

## 🔧 Troubleshooting

### Claude CLI Not Using Haiku?

```bash
# Check settings exist and are valid
cat ~/.claude/settings.json | python3 -m json.tool

# Clear cache
rm -rf ~/.claude/cache

# Restart and test
claude "test"
```

**See [SETUP_CLI.md](SETUP_CLI.md) for full CLI troubleshooting.**

---

### Codex Still Expensive?

```bash
# Find the file
FILE=$(find ~/Documents/Codex -name "claude_subscription_mcp.py" 2>/dev/null | head -1)

# Check it was edited
grep "haiku" "$FILE"
# Should show: {"model": "haiku", "fastMode": True, ...}

# Kill Codex processes
pkill -9 -f Codex

# Verify killed (should be empty)
ps aux | grep -i codex | grep -v grep

# Restart Codex from Applications
```

**See [SETUP_CODEX.md](SETUP_CODEX.md) for detailed Codex troubleshooting.**

---

## 🎓 Advanced

### Override Per Session (Claude CLI Only)

```bash
# Use expensive model once
claude --model opus "Complex analysis"

# Back to Haiku (your default)
claude "Normal task"
```

### Switch Model Permanently (Codex)

Edit `SETTINGS` in `claude_subscription_mcp.py`:

```python
# Use Sonnet instead (3x more expensive, better reasoning)
SETTINGS = json.dumps({"model": "sonnet", "fastMode": True, "env": {...}})

# Or use Opus (expensive but best)
SETTINGS = json.dumps({"model": "opus", "fastMode": False, "env": {...}})
```

Then restart Codex.

### Custom Routing (Codex)

Route different questions to different models:

```python
def get_model(prompt):
    if "complex" in prompt.lower():
        return "opus"  # Expensive, powerful
    elif "code" in prompt.lower():
        return "haiku"  # Cheap, fast
    else:
        return "sonnet"  # Balanced

# Use: model = get_model(prompt)
```

---

## ❓ FAQ

### Does fast mode affect output quality?
No. Fast mode reduces output tokens (more concise), not quality. Perfect for:
- Code generation
- Summaries  
- Structured output
- High-volume work

### Can I use different settings for different projects?
**Claude CLI:** Yes! Create `.claude/settings.json` in your project directory.

**Codex:** Edit the file to change for all queries.

### What if I need more capability?
- **Claude CLI:** Use `--model opus` on demand
- **Codex:** Temporarily edit settings to use Sonnet or Opus, then change back

### Will this break anything?
No. Haiku + fast mode is fully compatible. All Claude CLI and Codex features work identically. Only your billing changes.

### How do I disable it?
**Claude CLI:**
```bash
rm ~/.claude/settings.json
```

**Codex:**
Revert the `SETTINGS` line to original, restart Codex.

---

## 📁 Files in This Repo

| File | Purpose |
|------|---------|
| **README.md** | This overview |
| **SETUP_CLI.md** | Claude CLI detailed guide |
| **SETUP_CODEX.md** | Codex detailed guide + troubleshooting |
| **examples/claude-settings.json** | Example Claude settings (copy to `~/.claude/settings.json`) |
| **examples/codex-claude_subscription_mcp.py** | Example Codex MCP bridge (reference) |
| **CONTRIBUTING.md** | How to contribute improvements |
| **LICENSE** | MIT license |

---

## 🚀 Real-World Examples

### Example 1: Code Review
```bash
claude --model opus "Review this architecture" < myfile.py
# Uses expensive Opus (better reasoning)
# Cost: $0.015
```

### Example 2: Quick Fix
```bash
claude "Fix this syntax error" < myfile.py
# Uses cheap Haiku + fast mode (default)
# Cost: $0.0008
```

### Example 3: Codex Analysis
```
You (Codex): "Why is my momentum dimension at 95.2%?"
→ Smart router detects trading keywords
→ Routes to Claude Haiku + Fast Mode
→ Returns analysis with live calibration data
Cost: $0.0008 per query (vs $0.003 default)
```

### Example 4: High-Volume Work
```
You (Codex): 10 backtest questions in a session
→ Each routes to Haiku + Fast Mode
→ Total cost: $0.008
→ Vs $0.030 with default Sonnet
→ Savings: $0.022
```

---

## 🔄 Hybrid Approach (Recommended)

**Claude CLI:**
```bash
claude "quick task"                    # Haiku + Fast (cheap)
claude --model opus "deep analysis"    # Opus (expensive, once)
claude "back to normal"                # Haiku + Fast (default)
```

**Codex:**
```python
# Keep settings at Haiku + Fast (default)
SETTINGS = json.dumps({"model": "haiku", "fastMode": True, ...})

# Use Opus for important analysis by temporarily changing settings
# Then change back
```

---

## 🎯 Performance Tips

### For Speed
- Use Haiku + Fast Mode (default)
- Fast mode produces concise output
- Perfect for code, summaries, structured tasks
- **Latency:** 200-300ms avg

### For Quality
- Use Sonnet/Opus for complex reasoning
- Turn off fast mode for longer responses
- Better for creative work, deep analysis
- **Latency:** 300-600ms avg

### Cost vs Quality Trade-Off
```
High Volume, Good Speed    → Haiku + Fast ✅
Balanced Work              → Sonnet + Fast
Complex Reasoning          → Opus (no fast mode)
Important Decisions        → Opus (full reasoning)
```

---

## 📊 Token Efficiency

### Claude CLI
With Haiku + Fast Mode default:
- Save ~$0.22 per 100 queries (73% reduction)
- ~200-300ms response time
- Perfect for high-volume work

### Codex
With Haiku + Fast Mode routing:
- Every Claude routing uses cheap model
- Save ~$0.22 per 100 queries (73% reduction)
- Transparent to you—just use Codex normally

### Both Tools Combined
- **100 queries:** Save $0.44/month
- **1,000 queries:** Save $4.40/month
- **10,000 queries:** Save $44.00/month

---

## 🔗 Related Links

- [Claude API Docs](https://docs.anthropic.com)
- [Claude Code Guide](https://claude.com/claude-code)
- [Anthropic Models](https://docs.anthropic.com/claude/docs/models-overview)
- [Haiku Model Specs](https://docs.anthropic.com/claude/docs/models-overview#claude-haiku)

---

## 🤝 Contributing

Found an issue or improvement? Open a PR or issue!

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License

MIT — Use freely, modify, share.

---

## 🎉 You're Set!

Both **Cheap Claude** and **Cheap Codex** are now running Haiku + Fast Mode.

**Save 50-80% on Claude costs while keeping full capability.** ✅

Questions? Check [SETUP_CLI.md](SETUP_CLI.md) or [SETUP_CODEX.md](SETUP_CODEX.md).
