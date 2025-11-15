# Manuscript Directory

This directory contains the actual drafted prose of your novel.

## Structure

Organize your manuscript files as follows:

### By Chapter
```
chapter-01.md
chapter-02.md
chapter-03.md
[etc.]
```

### Scenes (if drafting scene-by-scene)
```
scenes/
  ch01-scene01.md
  ch01-scene02.md
  ch02-scene01.md
  [etc.]
```

### Drafts
```
drafts/
  draft-1/
  draft-2/
  [etc.]
```

## File Naming

Use consistent naming conventions:
- Chapters: `chapter-##.md` (e.g., `chapter-01.md`, `chapter-23.md`)
- Scenes: `ch##-scene##-[title].md` (e.g., `ch03-scene02-confrontation.md`)

## Front Matter

Each chapter file should include:
```markdown
# Chapter [Number]: [Title]

**POV:** [Character]
**Setting:** [Location]
**Time:** [When]
**Status:** [Draft/Revised/Polished/Final]

---

[Chapter text begins here]
```

## Version Control

- Keep previous drafts in `drafts/` directory
- Date your draft folders: `draft-1-2024-01-15/`
- Never delete old drafts—they may contain useful material

## Word Count Tracking

Maintain a word count log:
```
word-count-log.md
```

Track:
- Per chapter word counts
- Total manuscript word count
- Target vs. actual
- Progress over time

## Assembly

When ready to compile:
- Create `compiled/` directory
- Assemble full manuscript in single file
- Generate different formats as needed

## Usage

This directory contains the prose output of the Prose Stylist Agent, with input from all other agents. Keep organized by chapter or scene as suits your process.
