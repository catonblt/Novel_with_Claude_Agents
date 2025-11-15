# Novel Writer GUI

A user-friendly desktop application for collaborative novel writing with AI agents. This GUI provides an intuitive interface to the multi-agent novel writing system, making it easy to create, manage, and export your literary works.

## Features

### 🎨 Dark Mode Interface
- Modern, easy-on-the-eyes dark theme
- Clean, professional design
- Responsive layout

### 📝 Four Main Sections

#### 1. Configure Tab
- **Simple Mode**: Quick setup with story idea, genre, and basic settings
- **Advanced Mode**: Full control over narrative structure, agents, and detailed configuration
- Real-time project configuration
- Agent selection and customization

#### 2. Generate Tab
- **Interactive Chat**: Direct conversation with any of the 9 specialized agents
- **Real-time Logs**: Monitor generation progress and agent activities
- **Streaming Responses**: See agent output as it's being generated
- **Save Agent Outputs**: Preserve individual agent contributions
- Start/Stop controls for generation

#### 3. Review Tab
- View and edit final story
- Access all individual agent outputs
- Real-time word and character counts
- Edit any output directly in the GUI
- Unsaved changes tracking

#### 4. Export Tab
- **Export to Word**: Professional .docx export with formatting
- **Version Management**: Create snapshots of your work
- **Version Comparison**: Side-by-side comparison of different versions
- Optional inclusion of agent outputs as appendix

## Installation

### Prerequisites

1. **Python 3.8 or higher**
2. **Anthropic API Key** (for Claude AI)

### Step 1: Install Dependencies

```bash
cd Novel_with_Claude_Agents
pip install -r requirements.txt
```

The required packages are:
- `customtkinter` - Modern UI framework
- `anthropic` - Claude AI API
- `python-docx` - Word document export
- `pillow` - Image support
- `python-dateutil` - Date utilities

### Step 2: Set Up API Key

Set your Anthropic API key as an environment variable:

**On Linux/Mac:**
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

**On Windows:**
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

Or add it to your system's environment variables permanently.

### Step 3: Launch the Application

```bash
python novel_gui.py
```

Or make it executable and run directly:

```bash
chmod +x novel_gui.py
./novel_gui.py
```

## Quick Start Guide

### 1. Create a New Project

1. Click **"New Project"** in the menu bar
2. Enter your novel's name and your author name
3. Optionally choose a custom directory
4. Click **"Create Project"**

### 2. Configure Your Story

**Simple Mode** (recommended for beginners):
1. Go to the **Configure** tab
2. Describe your story idea in the text box
3. Select genre and target word count
4. Optionally add themes and tone
5. Click **"Save Project"** in the menu

**Advanced Mode** (for full control):
1. Toggle to **Advanced** mode
2. Configure all story details, structure, and agents
3. Select which agents to use
4. Save your configuration

### 3. Generate Your Story

1. Go to the **Generate** tab
2. Select an agent to work with (start with **Agent 8: Story Advocate**)
3. Click **"Start Conversation"**
4. Chat with the agent about your story
5. Watch real-time logs on the right panel
6. Save agent outputs using **"Save Agent Output"**

**Recommended workflow:**
- **Agent 8** (Story Advocate): Discuss vision and plan
- **Agent 1** (Architect): Create story structure
- **Agent 3** (Character Psychologist): Develop characters
- **Agent 2** (Prose Stylist): Write polished prose
- **Agent 7** (Beta Reader): Get feedback
- **Agent 9** (Redundancy Editor): Polish final draft

### 4. Review and Edit

1. Go to the **Review** tab
2. Select what to view (Final Story or individual agent outputs)
3. Click **"Load"** to load the content
4. Edit directly in the text editor
5. Click **"Save Changes"** when done

### 5. Export Your Novel

1. Go to the **Export** tab
2. Enter document title and author (optional)
3. Check "Include agent outputs" if desired
4. Click **"Export to Word Document"**
5. Choose save location

**Create Versions:**
- Enter a version name (e.g., "First Draft", "After Edits")
- Click **"Create"** to snapshot current state
- Select 2 versions and click **"Compare"** to see differences

## Project Structure

When you create a project, the following structure is created:

```
your-novel-title/
├── .novel-config.json        # Project configuration
├── planning/                 # Planning documents
├── manuscript/               # Final story
│   └── final_story.md
├── story-bible/             # Continuity tracking
├── feedback/                # Beta reader notes
├── research/                # Research materials
├── agent-outputs/           # Individual agent outputs
│   ├── agent_1_architect-agent.md
│   ├── agent_2_prose-stylist-agent.md
│   └── ...
└── versions/                # Version snapshots
    ├── version_20250115_143022/
    └── first-draft/
```

## Using the Chat Interface

### Tips for Effective Agent Conversations

1. **Be specific**: Give detailed context and clear requests
2. **Iterative approach**: Work in small chunks, refine as you go
3. **Ask questions**: Agents can explain their reasoning
4. **Request revisions**: Don't hesitate to ask for changes
5. **Save regularly**: Use "Save Agent Output" to preserve work

### Example Conversation Starters

**With Story Advocate (Agent 8):**
> "I want to write a literary novel about identity and belonging, set in a small coastal town. The main character is dealing with the loss of a parent. Can you help me develop this idea?"

**With Architect (Agent 1):**
> "Based on my story idea, can you create a three-act structure with chapter breakdown? I want the pacing to be contemplative and character-driven."

**With Character Psychologist (Agent 3):**
> "Develop a complex protagonist who is a 35-year-old photographer returning to her hometown. She should have unresolved family issues and a guarded personality."

**With Prose Stylist (Agent 2):**
> "Write the opening scene of Chapter 1 where the protagonist arrives at the coastal town. Use lyrical, descriptive prose with a melancholic tone."

## Keyboard Shortcuts

- **Enter** in chat input: Send message
- **Ctrl+S** (when editing): Save changes (use Save Changes button)

## Troubleshooting

### "Claude API not configured" Error

**Solution:** Set your ANTHROPIC_API_KEY environment variable:
```bash
export ANTHROPIC_API_KEY='your-key'
```

### Import Errors

**Solution:** Install all required packages:
```bash
pip install -r requirements.txt
```

### "python-docx not installed" Warning

**Solution:** Install the python-docx package:
```bash
pip install python-docx
```

### GUI Won't Start

**Solution:** Ensure you have CustomTkinter installed:
```bash
pip install customtkinter
```

### Application Freezes During Generation

This is normal - the agent is thinking. Watch the real-time log for activity. If truly frozen, use the "Stop Generation" button.

## Tips for Best Results

### Story Development

1. **Start with Agent 8** (Story Advocate) to refine your vision
2. **Use Agent 1** (Architect) to create structure before writing
3. **Develop characters** with Agent 3 before drafting scenes
4. **Get feedback early** from Agent 7 (Beta Reader)
5. **Save versions** at major milestones

### Managing Complexity

- Use **Simple Mode** for straightforward projects
- Switch to **Advanced Mode** when you need fine control
- Create **versions** before major revisions
- Review **agent outputs** regularly to maintain consistency

### Collaboration Workflow

1. **Vision Phase**: Configure tab + Agent 8
2. **Planning Phase**: Agent 1 (structure) + Agent 3 (characters)
3. **Drafting Phase**: Agent 2 (prose) + Agent 4 (atmosphere)
4. **Review Phase**: Agent 7 (feedback) + Agent 9 (redundancy)
5. **Polish Phase**: Agent 2 (final prose) + Agent 6 (continuity)

## Advanced Features

### Version Comparison

1. Create version snapshots at key stages
2. Select exactly 2 versions
3. Click "Compare Selected Versions"
4. View side-by-side differences

### Multiple Projects

- Create as many projects as you want
- Each project is completely independent
- Switch between projects using "Open Project"

### Custom Agent Instructions

In **Advanced Mode**, you can customize which agents to use. This is useful for:
- Genre-specific workflows
- Focusing on particular aspects (e.g., only character and prose)
- Experimenting with different agent combinations

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 100MB for application + space for projects
- **Internet**: Required for Claude API access

## Support and Documentation

- **Main Documentation**: See README.md in the project root
- **CLI Documentation**: See USAGE.md for CLI interface
- **Workflow Guide**: See WORKFLOW.md for detailed writing process
- **Agent Specs**: See individual agent files in `agents/` directory

## Privacy and Data

- All project files are stored **locally** on your computer
- API calls to Claude are made via Anthropic's official API
- No data is collected or stored by this application
- Your API key is never saved or transmitted except to Anthropic

## License

This application is part of the Novel_with_Claude_Agents framework and is provided for creative use. Adapt it freely for your literary projects.

---

## Ready to Write Your Novel?

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Set API key**: `export ANTHROPIC_API_KEY='your-key'`
3. **Launch**: `python novel_gui.py`
4. **Create project** and start writing!

Happy writing! 📚✍️
