# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod

### 記憶中樞 (Memory Hub)

- 記憶中樞路徑: /home/ysga/文件/Obsidian Vault/智研法律AI系統/98_記憶中樞
- 用途: 集中存放可回滾的會話重點、每日摘要與後續向量化檢索素材
- 結構: 日誌/、摘要/、索引/
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

### Installed Skills Reference

#### Design & Planning
- `brainstorming` - Design workflow before implementation
- `adaptive-reasoning` - Automatic reasoning level adjustment

#### Configuration Management
- `agent-config` - Core context file modifications
- `openclaw-config` - Gateway configuration editing

#### Context Management
- `context-clean-up` - Context bloat audit and fix planning
- `context-hygiene` - Context maintenance protocol

#### Browser Automation
- `agent-browser` - Headless browser automation CLI

#### Skill Installation
- Use `clawhub search <skill-name>` to find skills
- Use `clawhub install <skill-name>` to install
- Check `SKILLS_INDEX.md` for installed skills

---

Add whatever helps you do your job. This is your cheat sheet.
