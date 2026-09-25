# Claude CLI Setup Guide

Quick setup to force Claude CLI to always use Haiku + Fast Mode.

## File Location

Create or edit: `~/.claude/settings.json`

**macOS/Linux:**
```bash
nano ~/.claude/settings.json
```

**Windows (PowerShell):**
```powershell
notepad $env:USERPROFILE\.claude\settings.json
```

## Configuration

Add these two settings:

```json
{
  "theme": "dark",
  "model": "haiku",
  "fastMode": true
}
```

**Save and close.**

## Verify Setup

Test with:

```bash
claude "What model are you using?"
```

Expected: Response from Haiku model, faster than usual.

## How It Works

When you run `claude`, these settings are automatically applied:
- `model: "haiku"` → Uses Haiku (cheapest, fastest)
- `fastMode: true` → Enables fast mode (reduces output tokens)

No additional flags needed. Every command automatically uses this config.

## Override for Single Query

Need Opus for a complex task? Use `--model`:

```bash
# Use Opus once
claude --model opus "Complex reasoning task"

# Back to Haiku (your default)
claude "Normal task"
```

**Available models:**
- `claude-opus-5` (or `--model opus`)
- `claude-sonnet-5` (or `--model sonnet`)
- `claude-haiku-4-5-20251001` (or `--model haiku`) — your default

## Per-Project Settings

For a specific project, create `.claude/settings.json` in that directory:

```bash
cd my-project
mkdir -p .claude
cat > .claude/settings.json << 'EOF'
{
  "model": "haiku",
  "fastMode": true,
  "verbose": false
}
EOF
```

Claude CLI reads project settings first, then user settings.

## Configuration Priority

Claude CLI loads settings in this order (highest → lowest priority):
1. **Flag:** `claude --model sonnet "prompt"`
2. **Project:** `.claude/settings.json` in current directory
3. **User:** `~/.claude/settings.json`
4. **Default:** Current default model + settings

## Full Configuration Example

For a complete setup:

```json
{
  "theme": "dark",
  "model": "haiku",
  "fastMode": true,
  "verbose": false,
  "permissions": {
    "defaultMode": "auto"
  },
  "editor": "vim",
  "sandbox": {
    "enabled": true
  }
}
```

**Common options:**
- `theme` — "dark", "light", "auto" (default)
- `model` — "haiku", "sonnet", "opus", or full ID
- `fastMode` — true/false
- `verbose` — true/false (verbose output)
- `editorMode` — "normal" or "vim"
- `effortLevel` — "low", "medium", "high", "xhigh"

## Cost Breakdown

**100 questions/month:**

| Config | Cost | Time/Query | Total/Month |
|--------|------|-----------|------------|
| **Haiku + Fast** ✅ | $0.80/1M | 200-300ms | $0.08 |
| Sonnet + Fast | $3.00/1M | 300-400ms | $0.30 |
| Opus | $15.00/1M | 400-600ms | $1.50 |

**Monthly savings with Haiku + Fast Mode:** $0.22 (73% reduction)

## Troubleshooting

### Settings not applying

**Check file syntax:**
```bash
# Validate JSON
python3 -m json.tool ~/.claude/settings.json
```

If error, fix the JSON and save.

**Clear cache:**
```bash
rm -rf ~/.claude/cache
```

Then retry: `claude "test"`

### "model: haiku not found"

Make sure you're using Claude Code CLI (not the web version):
```bash
which claude
claude --version
```

Should show: `Claude Code 0.x.x` or higher.

### Still using expensive model

1. Check settings file:
   ```bash
   cat ~/.claude/settings.json
   ```

2. Verify model field:
   ```bash
   grep '"model"' ~/.claude/settings.json
   # Should output: "model": "haiku"
   ```

3. Clear cache and try again:
   ```bash
   rm -rf ~/.claude/cache
   claude "test"
   ```

## Advanced: Custom Settings Per Shell

You can also set defaults via environment:

```bash
# Add to ~/.zshrc or ~/.bashrc
export CLAUDE_CODE_MODEL=haiku
export CLAUDE_CODE_FAST_MODE=1
```

But using `~/.claude/settings.json` is cleaner and more reliable.

## Monitor Your Usage

Check spending:

```bash
# Via Claude Code (when logged in)
claude auth status
```

This shows your account tier and usage.

## Performance Tips

### For Speed
- Use Haiku + Fast Mode (your current config)
- Fast mode produces more concise output
- Perfect for code, summaries, structured tasks

### For Quality
- Use `claude --model opus` for complex reasoning
- Good for creative work, deep analysis, novel problems
- ~15x more expensive, worth it for important queries

### For Development
```bash
# Quick syntax check (Haiku)
claude "Check this code: $(cat myfile.py)"

# Deep analysis (Opus, once)
claude --model opus "Deep review: $(cat myfile.py)"
```

## Reset to Defaults

Remove your settings to use Claude Code defaults:

```bash
rm ~/.claude/settings.json
```

Or just delete these lines:
```json
"model": "haiku",
"fastMode": true
```

## Next Steps

- **Codex Setup:** See [SETUP_CODEX.md](SETUP_CODEX.md)
- **Cost Calculator:** See [README.md](README.md#cost-savings-example)
- **More Settings:** `claude help settings` or check Claude Code documentation

---

**Saving money?** You're now running Haiku + Fast Mode. 🎉
