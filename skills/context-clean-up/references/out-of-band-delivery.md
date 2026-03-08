# Out-of-Band Delivery for Silent Automation

## Problem

Automated jobs (cron, heartbeat) that report "OK" or status updates inject noise into the main session transcript, causing context bloat.

## Solution

Send notifications **out-of-band** (to external channels) while keeping the automation output silent in the main session.

## Patterns

### Pattern 1: Telegram/Slack/Discord Notifications

```yaml
# Cron job configuration
delivery:
  mode: "announce"
  channel: "telegram"
  to: "@username"
```

**Result:**
- Job runs silently in background
- Success/failure notifications go to Telegram
- Main session transcript stays clean

### Pattern 2: Webhook Delivery

```yaml
# For integration with monitoring systems
delivery:
  mode: "webhook"
  to: "https://hooks.slack.com/services/..."
```

### Pattern 3: Conditional Silence

Only speak when there's something important:

```python
# Pseudo-code logic
if has_important_update():
    send_notification(channel="telegram", message="Update: ...")
else:
    # Stay silent
    output = "NO_REPLY"
```

## Implementation Examples

### OpenClaw Cron Job with Silent Success

```json
{
  "name": "Daily backup check",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Taipei"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Check if daily backups completed successfully. If any failures, send alert to Telegram. Otherwise, output NO_REPLY."
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "@your_username"
  },
  "sessionTarget": "isolated",
  "enabled": true
}
```

### Heartbeat with Minimal Output

In `HEARTBEAT.md`:
```markdown
# HEARTBEAT.md

- Check email (only alert if urgent)
- Check calendar (only alert if event <2h)
- Check weather (only alert if severe)
- Otherwise: HEARTBEAT_OK
```

## Benefits

1. **Reduced context bloat** - Main session stays lean
2. **Better notifications** - Alerts go where you'll see them
3. **Clean transcripts** - Easier to read conversation history
4. **Lower token usage** - Less noise means cheaper operation

## When to Use Out-of-Band

✅ **Use out-of-band when:**
- Regular status updates (daily, hourly)
- Success/failure notifications
- Monitoring alerts
- Scheduled reports

❌ **Keep in-session when:**
- Interactive debugging
- User-requested status
- One-time manual checks
- Development/testing

## Migration Strategy

1. **Identify noisy jobs** - Look for frequent "OK" messages
2. **Add delivery config** - Route to external channel
3. **Make job silent** - Output `NO_REPLY` on success
4. **Test** - Verify notifications work
5. **Monitor** - Watch context size decrease

## Tools Integration

### Telegram
```bash
# Send message via OpenClaw
openclaw message send --channel telegram --to "@username" --message "Backup completed"
```

### Slack Webhook
```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Backup completed"}' \
  https://hooks.slack.com/services/...
```

### Discord
```bash
openclaw message send --channel discord --to "channel-name" --message "✅ Backup completed"
```

## Silent Success Pattern

The key pattern:
```python
try:
    result = perform_task()
    if result["status"] == "success":
        # Silent success
        return "NO_REPLY"
    else:
        # Alert on failure
        send_alert(f"Task failed: {result['error']}")
        return f"Task failed - alert sent"
except Exception as e:
    send_alert(f"Task error: {str(e)}")
    return f"Error - alert sent"
```

## Monitoring

After implementing out-of-band delivery:

1. **Check context size** - Should stabilize or decrease
2. **Verify notifications** - Ensure alerts arrive
3. **Review cron logs** - Confirm silent operation
4. **Measure token usage** - Should show reduction

## Troubleshooting

**Problem:** Notifications not arriving
**Solution:** Check channel configuration, permissions, and network connectivity

**Problem:** Job still outputs to session
**Solution:** Ensure `NO_REPLY` is the exact output on success

**Problem:** Missing important alerts
**Solution:** Review alert logic, add more conditions

## Best Practices

1. **Fail loud, succeed silent** - Only notify on problems
2. **Use appropriate channels** - Urgent → Telegram, Logs → Discord channel
3. **Include context** - Notifications should have enough info to act
4. **Test thoroughly** - Verify both success and failure paths
5. **Document** - Note which jobs use out-of-band delivery

## Example: Complete Migration

**Before:**
```
[System] Daily backup: OK
[System] Email check: OK
[System] Calendar check: OK
```

**After:**
- All OK messages go to Telegram
- Main session shows nothing (or `NO_REPLY`)
- Only failures appear in main session

**Result:** Cleaner transcripts, better notifications, reduced bloat.