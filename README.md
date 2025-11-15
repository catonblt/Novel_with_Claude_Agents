# Novel Writing with Claude Agents

A sophisticated multi-agent system for collaborative literary fiction writing, where specialized AI agents work together with human authors to create psychologically rich, thematically deep novels.

## System Overview

This project implements a 9-agent collaborative writing system, where each agent has specialized expertise in different aspects of literary fiction craft. The agents work together under human creative direction to develop and write novels with professional-level attention to:

- Narrative structure and thematic architecture
- Prose style and linguistic artistry
- Character psychology and development
- Atmospheric world-building
- Historical and cultural accuracy
- Internal consistency
- Redundancy elimination and variation
- Reader experience
- Human-AI collaboration

## The Nine Agents

### 1. **Architect Agent** - Narrative Structure & Thematic Orchestrator
- Designs overall story structure (acts, chapters, scenes)
- Maps character arcs and transformation journeys
- Creates thematic architecture
- Plans pacing and information revelation
- Integrates subplots
- **Primary Output**: Story outlines, chapter breakdowns, structural frameworks

### 2. **Prose Stylist Agent** - Sentence-Level Craftsperson & Voice Keeper
- Crafts beautiful, precise prose
- Develops distinctive narrative voice
- Creates sensory-rich descriptions
- Writes compelling dialogue
- Ensures rhythm and musicality
- **Primary Output**: Polished prose passages, voice samples, style guides

### 3. **Character Psychologist Agent** - Interior Life Architect & Dialogue Specialist
- Creates psychologically complex characters
- Develops character voices and interiority
- Writes authentic dialogue with subtext
- Maps relationships and dynamics
- Designs character arcs
- **Primary Output**: Character dossiers, dialogue passages, relationship maps

### 4. **Atmosphere & Setting Agent** - Environmental Designer & Sensory World Builder
- Creates vivid, immersive settings
- Establishes atmospheric mood
- Provides sensory detail
- Designs spatial and temporal environments
- Uses setting thematically
- **Primary Output**: Location guides, atmospheric descriptions, sensory palettes

### 5. **Research Agent** - Accuracy Specialist & Cultural Reference Curator
- Ensures factual accuracy
- Researches historical periods
- Verifies professional/technical details
- Provides cultural context
- Fact-checks completed work
- **Primary Output**: Research briefings, fact-check reports, reference materials

### 6. **Continuity Editor Agent** - Internal Consistency Guardian & Detail Tracker
- Maintains story bible
- Tracks all established details
- Catches contradictions
- Manages timeline coherence
- Handles revision ripple effects
- **Primary Output**: Story bible, continuity error reports, tracking documents

### 7. **Beta Reader Agent** - Critical Reader & Narrative Effectiveness Analyst
- Reads as intelligent audience
- Assesses emotional resonance
- Evaluates pacing and engagement
- Identifies clarity issues
- Provides honest feedback
- **Primary Output**: Reader responses, scene feedback, effectiveness reports

### 8. **Story Advocate Agent** - Human Liaison & Narrative Plausibility Counselor
- Bridges human authors and AI team
- Presents proposals persuasively
- Listens actively to human vision
- Argues for narrative plausibility
- Facilitates collaborative refinement
- **Primary Output**: Narrative proposals, discussion summaries, synthesized guidance

### 9. **Redundancy Editor Agent** - Redundancy Detective & Variation Specialist
- Identifies unnecessary repetition throughout the novel
- Distinguishes intentional motifs from unintentional redundancy
- Tracks all established information, scenes, and language patterns
- Provides solutions for eliminating or varying redundant content
- Preserves meaningful repetition while cutting wheel-spinning
- **Primary Output**: Redundancy reports, revision recommendations, variation suggestions

## How It Works

### Collaborative Workflow

1. **Vision & Planning Phase**
   - Human author shares vision, themes, initial ideas
   - Story Advocate facilitates discussion
   - Architect creates structural options
   - Team develops comprehensive plan

2. **Development Phase**
   - Character Psychologist develops characters
   - Architect maps detailed outline
   - Research Agent provides necessary background
   - Atmosphere Agent designs settings
   - Continuity Editor establishes tracking systems

3. **Writing Phase**
   - Prose Stylist drafts scenes
   - Character Psychologist ensures voice consistency
   - Atmosphere Agent integrates sensory detail
   - Continuity Editor tracks all details

4. **Review & Revision Phase**
   - Beta Reader provides feedback
   - All agents refine their contributions
   - Story Advocate synthesizes and presents options
   - Human author makes final decisions

5. **Polish Phase**
   - Prose Stylist refines language
   - Continuity Editor final consistency check
   - Research Agent verifies all facts
   - Team prepares manuscript

### Agent Collaboration Principles

- **Human Authority**: Authors maintain creative control and final decision-making
- **Specialized Expertise**: Each agent contributes deep knowledge in their domain
- **Integrated Teamwork**: Agents coordinate to serve the unified vision
- **Iterative Refinement**: Work develops through dialogue and revision
- **Quality Standards**: Literary fiction excellence as the benchmark

## Getting Started

### 🖥️ Desktop GUI Application (Recommended for Beginners)

**NEW!** We now offer a user-friendly desktop application with a modern dark mode interface:

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Anthropic API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Launch the GUI
python novel_gui.py
```

**Features:**
- 📝 **Configure Tab**: Simple and Advanced modes for project setup
- 💬 **Generate Tab**: Interactive chat with agents + real-time logs
- 📖 **Review Tab**: View and edit all outputs in one place
- 📤 **Export Tab**: Export to .docx, manage versions, compare drafts

**See [GUI_README.md](GUI_README.md) for complete GUI documentation.**

### ⌨️ Command Line Interface (For Advanced Users)

This framework is **reusable** for writing multiple novels. Use the CLI to manage projects:

```bash
# Create a new novel project
python novel.py init "Your Novel Title" --author "Your Name"

# Navigate to your project
cd your-novel-title

# Check project status
python novel.py status

# Start working with agents
python novel.py agent 8  # Story Advocate (start here!)
```

**See [GETTING_STARTED.md](GETTING_STARTED.md) for a complete quick start guide.**

### For New Projects - Detailed Steps

1. Create a project using `novel.py init`
2. Review agent descriptions with `novel.py agents`
3. Read the workflow guide in `WORKFLOW.md`
4. Begin with Story Advocate (Agent 8): `novel.py agent 8`
5. Progress through phases: vision → planning → development → drafting → revision → polish

### Agent Files

Each agent has a comprehensive specification document:
- `/agents/01_ARCHITECT_AGENT.md`
- `/agents/02_PROSE_STYLIST_AGENT.md`
- `/agents/03_CHARACTER_PSYCHOLOGIST_AGENT.md`
- `/agents/04_ATMOSPHERE_SETTING_AGENT.md`
- `/agents/05_RESEARCH_AGENT.md`
- `/agents/06_CONTINUITY_EDITOR_AGENT.md`
- `/agents/07_BETA_READER_AGENT.md`
- `/agents/08_STORY_ADVOCATE_AGENT.md`
- `/agents/09_REDUNDANCY_EDITOR_AGENT.md`

## Key Features

### Literary Fiction Focus
This system is specifically designed for literary fiction that prioritizes:
- Psychological depth and character complexity
- Thematic richness and intellectual substance
- Prose artistry and linguistic beauty
- Moral ambiguity and nuanced exploration
- Slow-burning, contemplative narratives

### Comprehensive Craft Attention
Every aspect of novel craft receives expert attention:
- Structure and pacing
- Character development
- Prose quality
- Setting and atmosphere
- Research and accuracy
- Internal consistency
- Reader experience

### Collaborative Intelligence
The system balances:
- AI expertise in craft and execution
- Human vision and creative authority
- Genuine dialogue and refinement
- Respect for both perspectives

## Philosophy

This system operates on several core principles:

1. **Literary Fiction Demands Excellence**: Every aspect of craft matters and receives careful attention

2. **Humans Lead, AI Supports**: Creative vision comes from human authors; agents provide expertise and execution

3. **Collaboration Creates Quality**: Neither human nor AI alone could achieve what they create together

4. **Complexity Serves Story**: Sophisticated systems serve sophisticated storytelling

5. **Process Supports Product**: Careful development process enables excellent final work

## Project Structure

```
Novel_with_Claude_Agents/
├── README.md                 # This file
├── WORKFLOW.md              # Detailed workflow guide
├── agents/                  # Agent specification documents
│   ├── 01_ARCHITECT_AGENT.md
│   ├── 02_PROSE_STYLIST_AGENT.md
│   ├── 03_CHARACTER_PSYCHOLOGIST_AGENT.md
│   ├── 04_ATMOSPHERE_SETTING_AGENT.md
│   ├── 05_RESEARCH_AGENT.md
│   ├── 06_CONTINUITY_EDITOR_AGENT.md
│   ├── 07_BETA_READER_AGENT.md
│   ├── 08_STORY_ADVOCATE_AGENT.md
│   └── 09_REDUNDANCY_EDITOR_AGENT.md
├── project/                 # Your novel project files
│   ├── planning/           # Outlines, character docs, research
│   ├── manuscript/         # Draft chapters and scenes
│   ├── story-bible/        # Continuity tracking
│   └── feedback/           # Beta reader reports
└── templates/              # Reusable templates
    ├── character-dossier.md
    ├── chapter-outline.md
    └── scene-template.md
```

## CLI Interface & Multiple Projects

### The Novel CLI

The `novel.py` CLI makes it easy to create and manage multiple novel projects:

```bash
# Initialize new projects
python novel.py init "Mystery Novel"
python novel.py init "Literary Fiction"
python novel.py init "Thriller"

# Each project is independent with its own configuration and files
```

**Key Commands:**
- `init` - Create a new novel project
- `status` - View project information
- `agent <number>` - Display agent instructions
- `agents` - List all agents
- `phase <name>` - Update project phase
- `templates` - View available templates

### Managing Multiple Novels

Each novel project is self-contained:

```
~/writing/
├── mystery-novel/
│   ├── .novel-config.json    # Project configuration
│   ├── planning/
│   ├── manuscript/
│   └── story-bible/
├── literary-fiction/
│   ├── .novel-config.json
│   └── ...
└── thriller/
    ├── .novel-config.json
    └── ...
```

Switch between projects by changing directories:
```bash
cd ~/writing/mystery-novel
python novel.py status

cd ~/writing/literary-fiction
python novel.py status
```

### Configuration File

Each project has a `.novel-config.json` that stores:
- Project metadata (title, author, genre, word count target)
- Vision (themes, tone, central questions)
- Structure (POV, chronology, chapters)
- Current phase (vision, planning, drafting, etc.)
- Custom notes and settings

See `example-novel-config.json` for a complete example.

## Documentation

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Quick start guide (start here!)
- **[USAGE.md](USAGE.md)** - Comprehensive usage guide with examples
- **[WORKFLOW.md](WORKFLOW.md)** - Detailed phase-by-phase workflow
- **[QUICK_START.md](QUICK_START.md)** - Condensed workflow overview
- **example-novel-config.json** - Sample project configuration
- **novel-config.schema.json** - Configuration file schema

## Contributing

This is a framework for collaborative novel writing. You can adapt it by:
- Modifying agent roles for your specific needs
- Adding specialized sub-agents
- Adjusting workflows for your process
- Customizing output formats

## Credits

This multi-agent system draws on:
- Literary craft tradition and contemporary practice
- Psychological understanding of character and creativity
- Collaborative writing methodologies
- AI-human partnership principles

## License

This framework is provided for creative use. Adapt it freely for your literary projects.

---

## Ready to Begin?

**Using the GUI (Recommended):**

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY='your-api-key-here'
python novel_gui.py
```

**Then:**
1. Click "New Project" and enter your novel details
2. Configure your story in the Configure tab
3. Start chatting with agents in the Generate tab
4. Review and export your work!

**Using the CLI:**

```bash
python novel.py init "Your Novel Title" --author "Your Name"
cd your-novel-title
python novel.py agent 8  # Start with Story Advocate
```

**Resources:**
- 🖥️ **GUI Guide**: [GUI_README.md](GUI_README.md)
- 📖 **Getting Started**: [GETTING_STARTED.md](GETTING_STARTED.md)
- 📚 **Detailed Workflow**: [WORKFLOW.md](WORKFLOW.md)
- 💡 **Usage Examples**: [USAGE.md](USAGE.md)

Each agent stands ready to contribute their expertise to your novel. The system is fully reusable—create as many novel projects as you want.
