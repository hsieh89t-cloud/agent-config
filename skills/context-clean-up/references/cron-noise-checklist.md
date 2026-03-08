# Cron Noise Checklist

## Purpose

Identify and fix noisy cron jobs that contribute to context bloat by injecting unnecessary status messages into session transcripts.

## Quick Assessment

Run this check on your cron jobs:

```bash
# List all cron jobs
openclaw cron list

# Check recent runs
openclaw cron runs <jobId>
```

## Noise Indicators

### High Noise (Fix Immediately)

✅ **Job outputs "OK" or status on every successful run**
✅ **Frequent runs (more than hourly) with verbose output**
✅ **Large output payloads (JSON dumps, logs)**
✅ **No conditional logic (always speaks)**

### Medium Noise (Consider Fixing)

⚠️ **Daily jobs with brief status**
⚠️ **Jobs that could be silent but include timestamps**
⚠️ **Redundant information in output**

### Low Noise (Probably OK)

✅ **Jobs that only output on failure**
✅ **Infrequent jobs (weekly/monthly)**
✅ **Minimal, essential output only**

## Fix Patterns

### Pattern 1: Silent Success

**Before:**
```yaml
payload:
  kind: agentTurn
  message: "Check system status and report"
# Outputs: "System status: OK" every time
```

**After:**
```yaml
payload:
  kind: agentTurn
  message: "Check system status. If all OK, output NO_REPLY. If issues, describe them."
delivery:
  mode: announce
  channel: telegram
  to: "@username"
# Outputs: NO_REPLY (silent) on success, Telegram alert on failure
```

### Pattern 2: Out-of-Band Delivery

**Before:** Status in main session
**After:** Status sent to external channel

```yaml
# Add delivery configuration
delivery:
  mode: announce
  channel: telegram  # or discord, slack, etc.
  to: "@username"
```

### Pattern 3: Conditional Output

Only output when something changes:

```python
# Pseudo-code
last_status = read_last_status()
current_status = check_system()

if current_status != last_status:
    output = f"Status changed: {current_status}"
    send_to_telegram(output)
else:
    output = "NO_REPLY"
```

## Step-by-Step Fix Guide

### Step 1: Identify Noisy Jobs

```bash
# Get job list
openclaw cron list --includeDisabled

# For each job, check recent output
openclaw cron runs <jobId> --limit 5
```

### Step 2: Analyze Output Pattern

Ask:
- Does this job need to run this frequently?
- Is the output always the same?
- Could failures be detected without success messages?
- Would out-of-band delivery work better?

### Step 3: Choose Fix Strategy

| Noise Level | Recommended Fix |
|-------------|-----------------|
| High | Out-of-band delivery + silent success |
| Medium | Conditional output or reduce frequency |
| Low | Probably OK as-is |

### Step 4: Implement Fix

**For OpenClaw cron jobs:**
```bash
# Update job configuration
openclaw cron update <jobId> --patch '{
  "payload": {
    "kind": "agentTurn",
    "message": "Check X. If OK: NO_REPLY. If not OK: describe issue."
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "@username"
  }
}'
```

### Step 5: Test

1. Run job manually: `openclaw cron run <jobId>`
2. Verify output is minimal/`NO_REPLY`
3. Check external channel for notifications
4. Monitor next scheduled run

### Step 6: Monitor Impact

- Check context size reduction
- Verify notifications work
- Ensure no important alerts are missed

## Common Job Types & Fixes

### 1. Health Checks

**Before:** "Service X: OK" every 5 minutes
**Fix:** Only alert on failure via Telegram

### 2. Backup Jobs

**Before:** "Backup completed: 1.2GB" daily
**Fix:** Weekly summary via email, silent daily runs

### 3. Data Sync

**Before:** "Synced 15 items" hourly
**Fix:** Only report errors, success is silent

### 4. Maintenance Tasks

**Before:** "Cleaned 45MB cache" daily
**Fix:** Monthly report, daily silent

### 5. Monitoring

**Before:** "All systems normal" hourly
**Fix:** Alert on anomalies only

## Configuration Examples

### Minimal Cron Job

```json
{
  "name": "Silent health check",
  "schedule": {
    "kind": "every",
    "everyMs": 300000  # 5 minutes
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Check API health. If status != 200, send Telegram alert with details. Otherwise NO_REPLY.",
    "timeoutSeconds": 30
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "@username"
  },
  "sessionTarget": "isolated",
  "enabled": true
}
```

### Conditional Notification Job

```json
{
  "name": "Smart backup monitor",
  "schedule": {
    "kind": "cron",
    "expr": "0 2 * * *",  # 2 AM daily
    "tz": "Asia/Taipei"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Check backup status. If failed or size changed >10%, send summary to Telegram. Otherwise NO_REPLY."
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "@username"
  },
  "sessionTarget": "isolated",
  "enabled": true
}
```

## Testing Your Fixes

### Test Script

```bash
#!/bin/bash
# test-cron-silence.sh

JOB_ID="$1"

echo "Testing job: $JOB_ID"
echo "Running job manually..."

# Run job
openclaw cron run "$JOB_ID"

echo ""
echo "Checking output..."
echo "If you see 'NO_REPLY' or minimal output, the fix works."
echo "Check Telegram for any notifications."
```

### Verification Steps

1. **Run job manually** - Verify output
2. **Check external channels** - Verify notifications
3. **Wait for scheduled run** - Verify automation
4. **Monitor context size** - Verify reduction

## Troubleshooting

### Problem: Job still outputs to session
**Solution:** Check the exact output string. `NO_REPLY` must be exact.

### Problem: Notifications not arriving
**Solution:** Verify channel configuration and permissions.

### Problem: Missing important status
**Solution:** Review conditional logic, add more checks.

### Problem: Job fails silently
**Solution:** Add failure detection and alerting.

## Maintenance Schedule

### Weekly
- Review cron job outputs
- Check for new noisy jobs
- Verify notification channels

### Monthly
- Full cron job audit
- Update job configurations as needed
- Review and archive old jobs

### Quarterly
- Evaluate job necessity
- Optimize schedules
- Update contact information for alerts

## Metrics to Track

1. **Context size** - Should decrease after fixes
2. **Notification volume** - Appropriate level for importance
3. **Job success rate** - Maintain reliability
4. **Alert response time** - Ensure timely notifications

## Final Checklist

- [ ] All frequent jobs use silent success pattern
- [ ] Important alerts go to appropriate channels
- [ ] No "OK" messages in main session
- [ ] Conditional logic prevents unnecessary output
- [ ] Notifications include enough context to act
- [ ] Failure scenarios are properly alerted
- [ ] Context size is stable or decreasing
- [ ] Regular maintenance scheduled

## Remember

**Good cron jobs are like good butlers:**
- They work quietly in the background
- They only bother you when necessary
- They handle problems before you notice
- They keep your space (context) clean