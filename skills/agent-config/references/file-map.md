# OpenClaw Context File Map

## Overview

OpenClaw agents load several core context files at startup. Each file has a specific purpose, loading order, and size limit. Understanding which file to modify is critical for effective agent configuration.

## File Loading Order

1. **IDENTITY.md** - Core identity (name, emoji, vibe)
2. **SOUL.md** - Personality, tone, boundaries
3. **USER.md** - User profile, preferences
4. **AGENTS.md** - Operational procedures, workflows
5. **TOOLS.md** - Tool-specific notes, conventions
6. **MEMORY.md** - Long-term curated facts (main session only)
7. **HEARTBEAT.md** - Periodic check checklist

## File Purposes & Guidelines

### IDENTITY.md
**Purpose:** Core agent identity
**Content:**
- Agent name
- Creature/type
- Core vibe/energy
- Emoji symbol
- Role/mission statement
**Style:** Minimal, punchy bullets
**Size target:** < 500 chars
**Who sees it:** All sessions (main + subagents)

### SOUL.md
**Purpose:** Personality, tone, ethical boundaries
**Content:**
- First-person identity statements
- Tone guidelines (what to sound like)
- Ethical boundaries (what never to do)
- Anti-patterns (forbidden phrases)
- Before/after examples
**Style:** Narrative, first-person OK, examples
**Size target:** < 5,000 chars
**Who sees it:** Main session only (subagents skip)

### USER.md
**Purpose:** User profile and preferences
**Content:**
- User name, pronouns
- Timezone, location
- Preferences (language, formatting)
- Work focus areas
- Task rhythm preferences
**Style:** Factual, third-person, bullet lists
**Size target:** < 2,000 chars
**Who sees it:** All sessions

### AGENTS.md
**Purpose:** Operational procedures and workflows
**Content:**
- Startup sequence
- Memory management rules
- Delegation thresholds
- Safety protocols
- Group chat behavior
- Heartbeat procedures
- Tool usage guidelines
**Style:** Structured, imperative, numbered processes
**Size target:** < 15,000 chars
**Who sees it:** All sessions (critical for subagents)

### TOOLS.md
**Purpose:** Tool-specific notes and conventions
**Content:**
- Local tool configurations
- Command examples
- API endpoints
- Device names/locations
- Environment-specific notes
**Style:** Reference guide, tables, code blocks
**Size target:** < 3,000 chars
**Who sees it:** All sessions

### MEMORY.md
**Purpose:** Long-term curated facts and learnings
**Content:**
- User preferences history
- Successful strategies
- Failure cases and lessons
- Authorization history
- Reasoning patterns
**Style:** Wiki-style, topic-based, dated entries
**Size target:** < 10,000 chars
**Who sees it:** Main session only (privacy-sensitive)

### HEARTBEAT.md
**Purpose:** Periodic check checklist
**Content:**
- Items to check on each heartbeat
- No explanations, just actions
**Style:** Extremely concise bullet list
**Size target:** < 500 chars
**Who sees it:** All sessions

## Size Limits & Truncation

**Hard limit:** 20,000 characters per file
**Warning threshold:** 18,000 characters
**Truncation behavior:** Files > 20K chars are truncated at startup context load
**Workaround:** Agent can still read full file with `read` tool

### When Files Approach Limits

1. **Audit for duplication** - Consolidate similar rules
2. **Move examples to reference files** - Link instead of embed
3. **Convert procedures to templates** - Store in separate files
4. **Split into base + advanced** - Load advanced on-demand
5. **Archive historical content** - Move to vault/archive

## Decision Tree: Which File to Modify?

```
Is this about agent personality or tone?
├─ Yes → SOUL.md
└─ No → Is this about operational procedures?
   ├─ Yes → AGENTS.md
   └─ No → Is this about user preferences?
      ├─ Yes → USER.md
      └─ No → Is this about tool usage or local config?
         ├─ Yes → TOOLS.md
         └─ No → Is this long-term memory/learning?
            ├─ Yes → MEMORY.md (main session only)
            └─ No → Is this core identity?
               ├─ Yes → IDENTITY.md
               └─ No → Is this heartbeat checklist?
                  ├─ Yes → HEARTBEAT.md
                  └─ No → Create new reference file
```

## Subagent Visibility

**Subagents see:**
- AGENTS.md (operational rules)
- TOOLS.md (tool conventions)
- USER.md (user preferences)
- IDENTITY.md (core identity)
- HEARTBEAT.md (checklist)

**Subagents DO NOT see:**
- SOUL.md (personality - irrelevant for task execution)
- MEMORY.md (privacy-sensitive long-term memory)

**Critical implication:** Any operational rule that subagents need to follow MUST be in AGENTS.md or TOOLS.md, not SOUL.md.

## Cross-Referencing Best Practices

**When content relates to multiple files:**
1. **Primary location** - Where the rule "lives"
2. **Cross-reference** - Other files point to primary location
3. **Avoid duplication** - Don't copy full content

**Example:**
- Delegation rules live in AGENTS.md
- SOUL.md mentions: "See AGENTS.md for delegation thresholds"
- TOOLS.md mentions: "For complex tasks, see delegation rules in AGENTS.md"

## File Maintenance Schedule

**Daily:**
- Update MEMORY.md with new learnings
- Check HEARTBEAT.md relevance

**Weekly:**
- Review AGENTS.md for outdated procedures
- Update USER.md with new preferences

**Monthly:**
- Full audit of all files
- Check file sizes, consolidate if needed
- Archive old content to vault

## Common Mistakes to Avoid

1. **Personality in AGENTS.md** - Tone rules belong in SOUL.md
2. **Operations in SOUL.md** - Subagents won't see them
3. **Long examples embedded** - Move to reference files
4. **Duplication across files** - Pick one primary location
5. **Vague instructions** - Be specific with examples
6. **No motivation** - Explain WHY rules exist
7. **Ignoring size limits** - Check before adding content
8. **Privacy leaks** - Sensitive info in MEMORY.md only

## Emergency Procedures

**If a file becomes corrupted:**
1. Check git history for last good version
2. Restore from backup if available
3. Recreate from memory/vault references
4. Document what was lost

**If changes break agent behavior:**
1. Identify which file change caused issue
2. Revert to previous version
3. Analyze why change failed
4. Document in config-failures log
5. Try refined approach

## Version Control Integration

**Recommended git practices:**
- Commit before making config changes
- Use descriptive commit messages
- Tag significant configuration versions
- Maintain changelog in vault/decisions/

**Example commit message:**
```
feat(config): Update delegation thresholds in AGENTS.md

- Changed from 2+ to 3+ tool calls for subagent spawn
- Added cost rationale section
- Updated examples for clarity

Reason: Reduce subagent overhead for simple tasks
```