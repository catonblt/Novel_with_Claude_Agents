# Getting Started - Novel Writing with 9 AI Agents

This is a **reusable framework** for writing literary fiction novels with collaborative AI agents. You can use it to write as many different novels as you want.

## What This System Does

This framework provides 9 specialized AI agents that help you write novels:
- **Architect** - Story structure and plotting
- **Prose Stylist** - Beautiful, polished writing
- **Character Psychologist** - Deep, complex characters
- **Atmosphere & Setting** - Vivid, immersive worlds
- **Research Agent** - Factual accuracy
- **Continuity Editor** - Consistency tracking
- **Beta Reader** - Reader feedback
- **Story Advocate** - Human-AI collaboration facilitator
- **Redundancy Editor** - Eliminate unnecessary repetition

## Quick Start (5 Minutes)

### Step 1: Create a New Novel Project

```bash
# Navigate to where you want your novels
cd ~/writing  # or wherever you keep your writing

# Create a new project (replace with your novel's name)
python /path/to/Novel_with_Claude_Agents/novel.py init "My Novel Title" --author "Your Name"

# Go into the project directory
cd my-novel-title
```

This creates a complete project structure with folders for planning, manuscript, research, and more.

### Step 2: Check Your Project

```bash
python /path/to/Novel_with_Claude_Agents/novel.py status
```

This shows your project information, current phase, and settings.

### Step 3: Start with the Story Advocate

```bash
python /path/to/Novel_with_Claude_Agents/novel.py agent 8
```

This displays the Story Advocate agent's instructions. Copy these instructions and paste them into your Claude conversation.

### Step 4: Discuss Your Vision

In your Claude conversation (with the Story Advocate instructions pasted), tell the agent about your novel:
- What kind of novel are you writing?
- What themes interest you?
- What's the emotional core of the story?
- Any character or plot ideas?

The agent will help you develop and document your vision.

### Step 5: Save Your Work

Save the vision document the agent helps you create:
```bash
# Save to planning/vision.md in your project directory
```

## What Happens Next?

After establishing your vision, you'll work through phases:

1. **Planning** - Work with the Architect to structure your novel
2. **Development** - Develop characters, settings, and research
3. **Drafting** - Write scenes and chapters with the Prose Stylist
4. **Revision** - Get feedback and improve with Beta Reader
5. **Polish** - Final refinements

Each phase involves working with different agents.

## How to Work with Agents

### View an Agent's Instructions

```bash
python novel.py agent <number>

# Examples:
python novel.py agent 1   # Architect
python novel.py agent 2   # Prose Stylist
python novel.py agent 8   # Story Advocate
```

### Use the Agent

1. Run the command above to see the agent's instructions
2. Copy the instructions
3. Paste them into a Claude conversation
4. Provide any relevant files or context
5. Ask the agent for help with your specific need

### Save the Agent's Output

Save what the agent creates to your project directories:
- Planning docs → `planning/`
- Character work → `story-bible/characters/`
- Scene drafts → `manuscript/`
- Feedback → `feedback/`

## Quick Command Reference

```bash
# Create new project
python novel.py init "Project Name" --author "Your Name"

# Check project status
python novel.py status

# List all agents
python novel.py agents

# View agent instructions
python novel.py agent <number>

# Update project phase
python novel.py phase <vision|planning|development|drafting|revision|polish>

# View templates
python novel.py templates

# View/edit configuration
python novel.py config
```

## Creating an Alias (Optional but Recommended)

To make the command shorter, add this to your `~/.bashrc` or `~/.zshrc`:

```bash
alias novel='python /full/path/to/Novel_with_Claude_Agents/novel.py'
```

Then restart your terminal, and you can just use:
```bash
novel init "My Novel"
novel status
novel agent 8
```

## Working on Multiple Novels

Each novel project is completely independent. Just create a new project for each novel:

```bash
cd ~/writing

# First novel
novel init "Mystery Novel" --author "Your Name"

# Second novel
novel init "Literary Fiction" --author "Your Name"

# Third novel
novel init "Thriller" --author "Your Name"
```

Switch between them by changing directories:

```bash
cd ~/writing/mystery-novel
novel status   # Shows mystery novel info

cd ~/writing/literary-fiction
novel status   # Shows literary fiction info
```

## Project Structure

When you initialize a project, you get:

```
my-novel-title/
├── .novel-config.json      # Project settings
├── planning/               # Outlines, vision docs, plans
├── manuscript/            # Your actual novel chapters
├── story-bible/           # Characters, world, continuity
├── feedback/              # Beta reader reports
├── research/              # Research notes
└── templates/             # Character, chapter, scene templates
```

## Typical Workflow

1. **Create project** - `novel init "Title"`
2. **Vision phase** - Work with Story Advocate (Agent 8)
3. **Planning phase** - Work with Architect (Agent 1)
4. **Development** - Work with Character Psychologist (3), Research (5), Atmosphere (4)
5. **Set up tracking** - Work with Continuity Editor (Agent 6)
6. **Draft scenes** - Work with Prose Stylist (Agent 2), supported by others
7. **Get feedback** - Work with Beta Reader (Agent 7)
8. **Revise** - Work with Redundancy Editor (9), Architect (1), Prose Stylist (2)
9. **Polish** - Final pass with Prose Stylist (2) and Continuity Editor (6)

## Common Questions

**Q: Do I need to use all 9 agents?**
A: Use the ones you need. Some novels need extensive research (Agent 5), others don't. Some need complex character work (Agent 3), others are more plot-driven. Pick what serves your novel.

**Q: Can I skip the planning phase?**
A: Yes! If you prefer discovery writing, you can draft first and structure later. The agents adapt to your process.

**Q: How do I handle revisions?**
A: Save different versions (chapter-01-v1.md, chapter-01-v2.md) or use Git for version control.

**Q: Can I customize the project structure?**
A: Absolutely! The directories are suggestions. Organize however works for you. Just update the paths in `.novel-config.json`.

## Need More Help?

- **USAGE.md** - Comprehensive guide with complete examples
- **WORKFLOW.md** - Detailed phase-by-phase process
- **README.md** - System overview and philosophy
- **example-novel-config.json** - Sample configuration file
- **agents/** directory - Each agent's complete instructions

## Example First Session

```bash
# 1. Create your project
cd ~/writing
novel init "The Echo Chamber" --author "Jane Smith"
cd the-echo-chamber

# 2. View project
novel status

# 3. Edit configuration with your vision
nano .novel-config.json
# Add themes, comp titles, basic ideas

# 4. Start with Story Advocate
novel agent 8
# Copy instructions to Claude
# Discuss your vision for 30-60 minutes
# Save vision document to planning/vision.md

# 5. Move to planning phase
novel phase planning

# 6. Work with Architect
novel agent 1
# Provide vision document
# Develop structure for 1-2 hours
# Save outline to planning/outline.md
```

## Tips for Success

1. **Save your work** - Always save agent outputs to your project directories
2. **Version your config** - Update `.novel-config.json` as your vision evolves
3. **Use phases** - Update your phase with `novel phase <name>` to track progress
4. **Stay organized** - Use consistent file naming (chapter-01.md, chapter-02.md)
5. **Backup** - Keep backups of your project (use Git, Dropbox, etc.)
6. **Be flexible** - Return to earlier phases when needed
7. **Trust the process** - Iteration creates quality

## Ready to Begin?

Run this now:

```bash
novel init "Your Novel Title" --author "Your Name"
```

Then follow the on-screen instructions. Your collaborative novel-writing journey begins!

---

**Happy Writing!** 📚✨
