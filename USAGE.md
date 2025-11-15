# Usage Guide: Writing Multiple Novels with the 9-Agent System

This guide explains how to use the novel-writing framework to work on multiple novel projects. The system is now fully reusable with a CLI interface and project management.

## Table of Contents

1. [Quick Start](#quick-start)
2. [CLI Reference](#cli-reference)
3. [Working with Agents](#working-with-agents)
4. [Managing Multiple Projects](#managing-multiple-projects)
5. [Complete Workflow Example](#complete-workflow-example)
6. [Configuration Reference](#configuration-reference)
7. [Tips and Best Practices](#tips-and-best-practices)

---

## Quick Start

### Installation

No installation required! The system uses Python 3 (which is standard on most systems).

### Create Your First Novel Project

```bash
# Navigate to where you want to keep your novels
cd ~/writing

# Create a new novel project
python /path/to/Novel_with_Claude_Agents/novel.py init "My First Novel" --author "Your Name"

# Navigate into your project
cd my-first-novel

# Check project status
python /path/to/Novel_with_Claude_Agents/novel.py status
```

### Start Working with Agents

```bash
# Start with the Story Advocate (Agent 8)
python /path/to/Novel_with_Claude_Agents/novel.py agent 8
```

This will display the Story Advocate's instructions. Copy them and paste into your Claude conversation, then begin discussing your novel vision.

---

## CLI Reference

### Creating a New Project

```bash
python novel.py init <project-name> [options]

Options:
  --directory, -d PATH    Create project in specific directory
  --author, -a NAME       Set author name

Examples:
  python novel.py init "The Memory Keeper"
  python novel.py init "Dark Waters" --author "Jane Smith" -d ~/novels/
```

**What this does:**
- Creates project directory structure (planning/, manuscript/, story-bible/, feedback/, research/)
- Generates .novel-config.json with default settings
- Copies templates for characters, chapters, and scenes
- Creates README files in each directory

### Viewing Project Status

```bash
python novel.py status

# Shows:
# - Project name and metadata
# - Current phase
# - Vision and themes
# - Structure decisions
# - Project location
```

### Working with Agents

```bash
# Display specific agent instructions
python novel.py agent <number>

# Examples:
python novel.py agent 8   # Story Advocate
python novel.py agent 1   # Architect
python novel.py agent 2   # Prose Stylist

# List all agents
python novel.py agents
```

### Managing Project Phases

```bash
python novel.py phase <phase-name>

# Phases:
# - vision         (Initial concept and vision)
# - planning       (Structure and outline)
# - development    (Characters, research, world-building)
# - drafting       (Writing scenes and chapters)
# - revision       (Revising and improving)
# - polish         (Final refinements)

# Example:
python novel.py phase drafting
```

When you update the phase, the CLI recommends which agents to work with.

### Managing Configuration

```bash
# View configuration file location
python novel.py config

# Show current configuration
python novel.py config --show
```

### Viewing Templates

```bash
python novel.py templates

# Shows available templates:
# - character-dossier.md
# - chapter-outline.md
# - scene-template.md
```

---

## Working with Agents

### The Agent Workflow

Each agent has a specific role in the novel-writing process. Here's how to work with them:

#### 1. Display Agent Instructions

```bash
python novel.py agent <number>
```

This displays the agent's complete instructions and methodology.

#### 2. Copy Instructions to Claude

Copy the displayed agent instructions into your Claude conversation.

#### 3. Provide Context

Give the agent:
- Your current project vision (from .novel-config.json)
- Relevant project files (planning docs, character notes, etc.)
- What you need help with

#### 4. Collaborate

Work with the agent to:
- Develop ideas
- Create documents
- Write scenes
- Review work
- Make improvements

#### 5. Save Outputs

Save agent outputs to the appropriate project directory:
- Planning documents → `planning/`
- Character dossiers → `story-bible/characters/`
- Scene drafts → `manuscript/`
- Feedback → `feedback/`

### Agent Sequence Recommendations

**Starting a New Novel:**
1. Agent 8 (Story Advocate) - Vision discussion
2. Agent 1 (Architect) - Structure and outline
3. Agent 3 (Character Psychologist) - Character development
4. Agent 5 (Research) - Background research (if needed)
5. Agent 4 (Atmosphere & Setting) - World design
6. Agent 6 (Continuity Editor) - Story bible setup

**During Drafting:**
1. Agent 1 (Architect) - Review scene purpose
2. Agent 2 (Prose Stylist) - Draft the scene
3. Agent 3 (Character Psychologist) - Check character voices
4. Agent 4 (Atmosphere & Setting) - Add sensory detail
5. Agent 6 (Continuity Editor) - Track details
6. Agent 7 (Beta Reader) - Feedback

**During Revision:**
1. Agent 7 (Beta Reader) - Overall assessment
2. Agent 9 (Redundancy Editor) - Find repetition
3. Agent 6 (Continuity Editor) - Check consistency
4. Agent 1 (Architect) - Structural improvements
5. Agent 2 (Prose Stylist) - Language polish

---

## Managing Multiple Projects

### Project Organization

Each project lives in its own directory with its own `.novel-config.json` file:

```
~/writing/
├── mystery-novel/
│   ├── .novel-config.json
│   ├── planning/
│   ├── manuscript/
│   └── story-bible/
├── literary-fiction/
│   ├── .novel-config.json
│   ├── planning/
│   └── ...
└── sci-fi-project/
    ├── .novel-config.json
    └── ...
```

### Switching Between Projects

Simply navigate to the project directory:

```bash
cd ~/writing/mystery-novel
python /path/to/novel.py status

cd ~/writing/literary-fiction
python /path/to/novel.py status
```

The CLI automatically detects the project based on the current directory.

### Creating a Shortcut (Optional)

For convenience, create an alias:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias novel='python /full/path/to/Novel_with_Claude_Agents/novel.py'

# Then you can just use:
novel status
novel agent 8
novel phase drafting
```

---

## Complete Workflow Example

Let's write a novel from start to finish using the system.

### Phase 1: Vision (Day 1)

```bash
# Create the project
cd ~/writing
python novel.py init "The Silent Harbor" --author "Alex Chen"
cd the-silent-harbor

# Update configuration
# Edit .novel-config.json to add:
# - themes
# - comp titles
# - initial vision

# Work with Story Advocate
python novel.py agent 8
# Copy instructions to Claude
# Discuss: "I want to write a literary novel about a lighthouse
# keeper dealing with grief after losing her daughter at sea..."
```

**Outputs:**
- Vision document (save to `planning/vision.md`)
- Thematic framework
- Initial character ideas

### Phase 2: Planning (Week 1)

```bash
# Move to planning phase
python novel.py phase planning

# Work with Architect
python novel.py agent 1
# Provide vision document
# Request: "Help me structure this as a non-linear narrative..."

# Work with Character Psychologist
python novel.py agent 3
# Request: "Develop the protagonist: Elena, 47, lighthouse keeper..."
```

**Outputs:**
- Master outline (`planning/outline.md`)
- Character dossiers (`story-bible/characters/elena.md`, etc.)
- Chapter breakdown (`planning/chapter-outline.md`)

### Phase 3: Development (Week 2)

```bash
python novel.py phase development

# Research
python novel.py agent 5
# Request: "Research lighthouse keeper daily routines,
# marine biology, and grief psychology..."

# Settings
python novel.py agent 4
# Request: "Develop the lighthouse setting with full sensory detail..."

# Story Bible
python novel.py agent 6
# Request: "Set up tracking for timeline, locations, and character details..."
```

**Outputs:**
- Research briefing (`research/lighthouse-research.md`)
- Location guides (`story-bible/locations/`)
- Story bible structure (`story-bible/bible.md`)

### Phase 4: Drafting (Weeks 3-12)

```bash
python novel.py phase drafting

# For each scene/chapter:

# 1. Scene planning
python novel.py agent 1
# "Scene: Elena's first morning after the funeral..."

# 2. Draft scene
python novel.py agent 2
# "Draft this scene in intimate third person, contemplative tone..."

# 3. Character voice check
python novel.py agent 3
# "Review Elena's interiority in this scene..."

# 4. Atmosphere
python novel.py agent 4
# "Enhance the sensory detail of the foggy morning..."

# 5. Track details
python novel.py agent 6
# "Update story bible with details from this scene..."

# Save each chapter to manuscript/chapter-01.md, etc.
```

**Outputs:**
- Complete chapter drafts (`manuscript/chapter-01.md` through `chapter-24.md`)
- Updated story bible
- Scene-by-scene notes

### Phase 5: Revision (Weeks 13-16)

```bash
python novel.py phase revision

# Beta read
python novel.py agent 7
# Provide complete manuscript
# Request: "Read the full manuscript and provide comprehensive feedback..."

# Redundancy check
python novel.py agent 9
# Request: "Analyze the manuscript for unnecessary repetition..."

# Continuity audit
python novel.py agent 6
# Request: "Check for any contradictions or timeline issues..."

# Structural revision
python novel.py agent 1
# Provide beta feedback
# Request: "Address the pacing issues in Act 2..."
```

**Outputs:**
- Beta reader report (`feedback/beta-report-full.md`)
- Redundancy analysis (`feedback/redundancy-report.md`)
- Continuity audit (`feedback/continuity-check.md`)
- Revised chapters

### Phase 6: Polish (Weeks 17-18)

```bash
python novel.py phase polish

# Language polish
python novel.py agent 2
# Request: "Line-by-line polish of Chapter 1..."

# Final continuity pass
python novel.py agent 6
# Request: "Final verification pass..."

# Final beta read
python novel.py agent 7
# Request: "Final read of polished manuscript..."
```

**Outputs:**
- Polished manuscript (`manuscript/final/`)
- Completion documentation
- Final project archive

---

## Configuration Reference

### .novel-config.json Structure

```json
{
  "project_name": "Your Novel Title",
  "version": "1.0",
  "metadata": {
    "author": "Your Name",
    "genre": "Literary Fiction - Subgenre",
    "target_word_count": 85000,
    "created_date": "2025-11-15",
    "comp_titles": ["Similar Book 1", "Similar Book 2"]
  },
  "vision": {
    "themes": ["Theme 1", "Theme 2"],
    "tone": "Contemplative, lyrical, etc.",
    "style_notes": "Prose style description",
    "central_question": "The main question the novel explores",
    "emotional_core": "The emotional heart of the story"
  },
  "structure": {
    "pov": "third_person_limited",
    "chronology": "non_linear",
    "estimated_chapters": 24,
    "act_structure": "Three acts with dual timelines"
  },
  "workflow_preference": "iterative_spiraling",
  "active_phase": "drafting",
  "project_paths": {
    "project_root": "./projects/your-novel",
    "planning_dir": "./projects/your-novel/planning",
    "manuscript_dir": "./projects/your-novel/manuscript",
    "story_bible_dir": "./projects/your-novel/story-bible",
    "feedback_dir": "./projects/your-novel/feedback"
  },
  "custom_notes": {
    "research_needed": ["Topic 1", "Topic 2"],
    "key_locations": ["Location 1", "Location 2"]
  }
}
```

### Configuration Fields Explained

**POV Options:**
- `first_person` - "I" narration
- `third_person_limited` - He/she, one character's perspective
- `third_person_omniscient` - He/she, all-knowing narrator
- `multiple_pov` - Multiple character perspectives
- `second_person` - "You" narration (rare)

**Chronology Options:**
- `linear` - Events in order
- `non_linear` - Jumps in time
- `frame_narrative` - Story within a story
- `mixed` - Combination of approaches

**Workflow Preferences:**
- `detailed_planning` - Complete outline before drafting
- `discovery_writing` - Write to discover the story
- `key_scenes_first` - Draft pivotal scenes first
- `iterative_spiraling` - Draft and revise in waves (recommended)

**Phases:**
- `vision` - Developing initial concept
- `planning` - Creating structure and outline
- `development` - Building characters, research, world
- `drafting` - Writing the manuscript
- `revision` - Improving and refining
- `polish` - Final perfection

---

## Tips and Best Practices

### 1. Keep Configuration Updated

As your novel evolves, update `.novel-config.json`:
```bash
# Edit the file directly
nano .novel-config.json

# Or use your preferred editor
code .novel-config.json
```

### 2. Organize Your Files

Use consistent naming:
- `planning/outline-v1.md`, `outline-v2.md` (version iterations)
- `manuscript/chapter-01.md`, `chapter-02.md` (zero-padded numbers)
- `story-bible/characters/protagonist-name.md`
- `feedback/beta-read-YYYY-MM-DD.md` (dated feedback)

### 3. Version Control

Consider using Git for your project:
```bash
cd your-novel-project
git init
git add .
git commit -m "Initial novel setup"

# After each writing session
git add .
git commit -m "Drafted chapter 3"
```

### 4. Save Agent Conversations

When working with agents, save important conversations:
- Copy conversations to markdown files
- Store in appropriate project directories
- Include date and agent name in filename

Example: `planning/architect-discussion-2025-11-15.md`

### 5. Regular Status Checks

```bash
# Weekly
python novel.py status

# Update phase as you progress
python novel.py phase drafting
```

### 6. Backup Your Work

- Keep backups of your project directory
- Use cloud storage (Dropbox, Google Drive, etc.)
- Or use Git with GitHub/GitLab for version control

### 7. Multiple Sessions Per Phase

You don't do each phase once. You might:
- Draft chapters 1-5, then revise them
- Go back to planning when discovering new plot needs
- Return to character development mid-draft
- Get beta feedback on individual chapters, not just full manuscript

### 8. Customize for Your Process

The framework is flexible:
- Skip phases that don't serve you
- Combine agents in creative ways
- Adapt templates to your needs
- Add custom fields to configuration

### 9. Document Your Decisions

In `custom_notes` section of config, track:
- Major plot decisions
- Character backstory not in the text
- Symbolism and motif tracking
- Cut content (might use later)

### 10. Work at Your Own Pace

- Literary fiction takes time
- Some chapters need more revision than others
- Trust the process
- The agents are always available when you need them

---

## Troubleshooting

### CLI doesn't find my project

```bash
# Make sure you're in the project directory
cd /path/to/your-project
python novel.py status

# Or specify the config file
python novel.py status --config /path/to/.novel-config.json
```

### Want to move a project

Edit `.novel-config.json` and update all paths in `project_paths`.

### Need to start over on a chapter

Just create a new file: `chapter-05-v2.md`, `chapter-05-v3.md`, etc.

### Lost track of what phase you're in

```bash
python novel.py status
```

Shows current phase and project state.

---

## Next Steps

1. **Create your first project**: `python novel.py init "Your Novel Title"`
2. **Start with vision**: `python novel.py agent 8`
3. **Follow the workflow**: See WORKFLOW.md for detailed process
4. **Read agent files**: Each agent has comprehensive instructions

## Additional Resources

- `README.md` - System overview and philosophy
- `WORKFLOW.md` - Detailed phase-by-phase process
- `QUICK_START.md` - Condensed getting started guide
- `/agents/` - Individual agent specifications
- `/templates/` - Document templates
- `example-novel-config.json` - Sample configuration

---

**Remember**: This is your novel. The agents are expert collaborators, but you have creative authority. Use them to serve your vision, adapt the process to your needs, and create something remarkable.

Happy writing! 📚✨
