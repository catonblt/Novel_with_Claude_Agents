# Quick Start Guide - Novel Writer Desktop Application

Welcome! This guide will walk you through everything from installation to exporting your first novel draft. No command line required!

## Table of Contents
- [Installation](#installation)
- [First Launch & API Key Setup](#first-launch--api-key-setup)
- [Creating Your First Project](#creating-your-first-project)
- [Configuring Your Story](#configuring-your-story)
- [Working with AI Agents](#working-with-ai-agents)
- [Reviewing & Editing Outputs](#reviewing--editing-outputs)
- [Saving & Exporting](#saving--exporting)
- [Tips for Success](#tips-for-success)

---

## Installation

### Windows

1. **Download** the Novel Writer application folder
2. **Locate** the file named `Novel Writer.bat`
3. **Double-click** `Novel Writer.bat`
4. **Wait** for the installation wizard to appear
5. Click **"Install Dependencies"** and wait for completion
6. When you see **"Installation Complete!"**, close the installer

**That's it!** From now on, just double-click `Novel Writer.bat` to launch the application.

### Mac

1. **Download** the Novel Writer application folder
2. **Locate** the file named `Novel Writer.command`
3. **Right-click** → **Open** (required for first-time security approval)
4. Click **"Open"** in the security dialog
5. **Wait** for the installation wizard to appear
6. Click **"Install Dependencies"** and wait for completion
7. When you see **"Installation Complete!"**, close the installer

**That's it!** From now on, just double-click `Novel Writer.command` to launch the application.

### Linux

**Option 1: Desktop Shortcut**
1. Double-click `Novel Writer.desktop`
2. If prompted, click "Trust and Launch" or "Execute"
3. Wait for automatic installation
4. Close installer when complete

**Option 2: Shell Script**
1. Double-click `novel-writer.sh` (or run `./novel-writer.sh` in terminal)
2. Wait for automatic installation
3. Close installer when complete

**Note:** If you don't have Python 3 installed:
- Ubuntu/Debian: `sudo apt install python3 python3-pip python3-tk`
- Fedora: `sudo dnf install python3 python3-pip python3-tkinter`
- Arch: `sudo pacman -S python python-pip tk`

---

## First Launch & API Key Setup

### Launch the Application

**Just double-click the same file you used for installation:**
- Windows: `Novel Writer.bat`
- Mac: `Novel Writer.command`
- Linux: `Novel Writer.desktop` or `novel-writer.sh`

The application will open in a beautiful dark mode interface.

### Set Up Your API Key (One-Time Only)

When you first launch, you'll see the **"API Key Setup"** dialog:

**Step 1: Get Your API Key**
1. Click the **"Get API Key from Anthropic"** button
2. Your web browser opens to https://console.anthropic.com/settings/keys
3. **Sign in** to your Anthropic account (or create one - it's free)
4. Click **"Create Key"** and give it a name like "Novel Writer"
5. **Copy** the API key (it starts with `sk-ant-`)

**Step 2: Save Your API Key**
1. Go back to the Novel Writer dialog
2. **Paste** your API key into the text field
3. Click **"Save and Continue"**

**Done!** Your API key is saved securely in `~/.novel_writer/.env` and you'll never need to enter it again.

### Verify Setup

Look at the top-right corner of the application. You should see:
- **✓ API Key Configured** (green text)

If you see **⚠ No API Key** (orange), click **Settings** and set up your key.

---

## Creating Your First Project

### Start a New Project

1. Click the **"New Project"** button in the top menu
2. A dialog appears with three fields:

**Fill in the form:**
- **Project Name**: Give your novel a working title (e.g., "My First Novel", "The Hidden Garden")
- **Author Name**: Your name (e.g., "Jane Smith")
- **Project Directory** (optional): Leave blank to use the default location `~/NovelProjects/`

3. Click **"Create Project"**

**Success!** You'll see a confirmation message with next steps, and the Configure tab will automatically open.

### Where Are My Files?

Your project is stored in a complete folder structure:

```
~/NovelProjects/your-novel-title/
├── .novel-config.json      # Project settings (auto-managed)
├── planning/               # Planning documents
├── manuscript/             # Your novel manuscript
│   └── final_story.md
├── story-bible/            # Continuity tracking
├── feedback/               # Beta reader notes
├── agent-outputs/          # Individual agent contributions
│   ├── agent_1_architect-agent.md
│   ├── agent_2_prose-stylist-agent.md
│   └── ... (all 9 agents)
└── versions/               # Version snapshots
```

**You can browse these files anytime**, but the GUI makes it easy to work with everything.

---

## Configuring Your Story

After creating a project, you're automatically taken to the **Configure** tab. This is where you describe your novel to the AI agents.

### Simple Mode (Recommended for Beginners)

**Simple Mode** shows just the essential fields:

1. **Story Idea** (required)
   - Describe your novel concept
   - Example: "A psychological thriller about a therapist who begins to suspect her patient is manipulating her, blurring the lines between helper and victim."

2. **Themes** (optional but helpful)
   - What ideas does your story explore?
   - Example: "Power dynamics, manipulation, truth vs. perception, professional boundaries"

3. **Target Length** (optional)
   - Short Novel: 40,000-60,000 words
   - Standard Novel: 60,000-90,000 words
   - Long Novel: 90,000-120,000 words
   - Epic: 120,000+ words

4. **Tone** (optional)
   - Example: "Dark, suspenseful, psychologically intense"

### Advanced Mode (For Detailed Planning)

Click **"Switch to Advanced Mode"** to see all configuration options:

- **Additional Story Details**: Genre, setting, time period, POV
- **Character Information**: Protagonists, relationships, arcs
- **Structural Preferences**: Plot outline, pacing notes
- **Style Guidelines**: Narrative voice, prose style preferences
- **Research Needs**: Historical details, technical accuracy requirements

**You don't need to fill everything out!** Add what you know, skip what you don't.

### Save Your Configuration

After filling in your story details:

1. Click the **"💾 Save Configuration"** button (top-right of Configure tab)
2. Or press **Ctrl+S** (Windows/Linux) or **Cmd+S** (Mac)

You'll see a success message: **"Project configuration saved successfully!"**

**You can always come back and update your configuration as your story evolves.**

---

## Working with AI Agents

Now the fun part! Go to the **Generate** tab to chat with your 9 specialized AI agents.

### Meet Your Agent Team

1. **Architect Agent** - Overall story structure, plot, pacing
2. **Prose Stylist Agent** - Beautiful writing, narrative voice, sentence craft
3. **Character Psychologist Agent** - Deep character development, dialogue, psychology
4. **Atmosphere & Setting Agent** - Vivid settings, sensory details, mood
5. **Research Agent** - Historical accuracy, fact-checking, cultural context
6. **Continuity Editor Agent** - Tracking details, catching contradictions, story bible
7. **Beta Reader Agent** - Reader perspective, emotional impact, pacing feedback
8. **Story Advocate Agent** - Helps develop your vision, coordinates the team ⭐ **Start here!**
9. **Redundancy Editor Agent** - Eliminates repetition, ensures variety

### Your First Conversation

**Start with Agent 8: Story Advocate**

1. In the Generate tab, select **"Agent 8: Story Advocate"** from the dropdown
2. Click **"Start New Conversation"**
3. Type your first message in the text box at the bottom
4. Click **"Send"** or press **Enter**

**Example first message:**
```
Hi! I'm starting a new novel about a therapist and her patient
where the power dynamics become twisted. I've filled in the basic
concept, but I'd love your help developing the vision and planning
the structure. Can we talk through this?
```

**What happens next:**
- The agent responds in real-time (you'll see the text stream in)
- They'll ask clarifying questions about your vision
- They'll help you articulate themes, tone, and structure
- They'll suggest which other agents to work with next

### Chatting with Agents

**The interface is simple:**

- **Agent Selector** (top): Choose which agent you're talking to
- **Conversation Area** (middle): See the full chat history with timestamps
- **Message Box** (bottom): Type your messages here
- **Send Button**: Send your message (or press Enter)

**Useful buttons:**
- **"Start New Conversation"**: Begin fresh (previous chat is saved)
- **"Clear Conversation"**: Erase current chat (careful!)
- **"Save to Agent File"**: Save the current conversation to that agent's output file

### Workflow Example

Here's a typical workflow for your first novel:

**Session 1: Vision & Planning**
1. **Agent 8 (Story Advocate)**: Discuss your vision, themes, goals (30-60 min)
2. **Agent 1 (Architect)**: Develop story structure and outline (1-2 hours)
3. Save both conversations to agent files

**Session 2: Character Development**
1. **Agent 3 (Character Psychologist)**: Develop main characters (1-2 hours)
2. **Agent 4 (Atmosphere & Setting)**: Design key settings (30-60 min)
3. Save conversations

**Session 3: Begin Drafting**
1. Review your planning materials in the Review tab
2. **Agent 2 (Prose Stylist)**: Draft your first scene or chapter (1-3 hours)
3. **Agent 7 (Beta Reader)**: Get feedback on the draft (30 min)
4. Save outputs

**Continue iterating!**

### Tips for Agent Conversations

✅ **Do:**
- Be conversational - they're designed for dialogue
- Ask questions when you're unsure
- Say "I don't like that" if something doesn't resonate
- Request multiple options to compare
- Save conversations regularly

❌ **Don't:**
- Expect perfection on the first try - it's iterative
- Be afraid to change direction
- Fill in every detail immediately - discover as you go
- Worry about using the "wrong" agent - they collaborate

---

## Reviewing & Editing Outputs

The **Review** tab shows all content generated by your agents.

### What You'll See

**Left Panel: File List**
- All agent output files
- Planning documents
- Manuscript files
- Story bible
- Feedback notes

**Right Panel: Content Viewer**
- Full text of the selected file
- Editable text area
- Save changes button

### Editing Outputs

1. Click any file in the left panel to view it
2. Edit directly in the text area on the right
3. Click **"Save Changes"** when done
4. Or press **Ctrl+S** (Cmd+S on Mac)

**All your edits are saved immediately to the file.**

### Organizing Your Work

Files are organized by type:
- `agent-outputs/` - Individual agent contributions
- `manuscript/` - Your actual novel manuscript
- `planning/` - Outlines, structural documents
- `story-bible/` - Continuity tracking
- `feedback/` - Beta reader notes and revisions

**You can also edit these files directly on your computer** - they're just markdown (.md) files in your project folder.

---

## Saving & Exporting

### Saving Your Project

**Automatic Saves:**
- Agent conversations are auto-saved as you chat
- File edits are saved when you click "Save Changes"

**Manual Save:**
- Click **"Save Project"** in the top menu anytime
- Or press **Ctrl+S** (Cmd+S on Mac)
- This saves your configuration and ensures all files are up-to-date

### Creating Version Snapshots

As your novel evolves, you'll want to save versions to compare later.

**In the Export tab:**

1. Enter a **Version Name** (e.g., "First Draft", "After Beta Feedback", "Final Edit")
2. Click **"Create Version Snapshot"**
3. A complete copy of your project is saved to `versions/your-version-name/`

**This lets you:**
- Compare different drafts side-by-side
- Roll back if you don't like changes
- Track your novel's evolution
- Submit different versions to beta readers

### Exporting to Word Document

Ready to share your manuscript?

**In the Export tab:**

1. Click **"Export to Word Document (.docx)"**
2. Choose what to include:
   - Full manuscript only
   - Manuscript + planning documents
   - Manuscript + agent notes
   - Everything
3. Choose where to save the file
4. Click **"Save"**

**You'll get a professionally formatted Word document** ready to share with beta readers, editors, or agents.

---

## Tips for Success

### 🎯 Getting Started
- **Start simple**: Don't fill out every field. Add what you know.
- **Begin with Story Advocate**: This agent helps you develop your vision.
- **Save often**: Use Ctrl+S (Cmd+S) regularly.

### 💡 Working with Agents
- **Be conversational**: Agents are designed for dialogue, not commands.
- **Ask for multiple options**: "Give me three different opening scenes."
- **Speak up**: If you don't like something, say so!
- **Iterate**: First drafts are starting points, not endpoints.

### 📝 Organization
- **Use version snapshots**: Before major revisions, create a snapshot.
- **Review the Review tab**: See all your materials in one place.
- **Keep notes**: Use the planning/ directory for your own notes.

### 🚀 Productivity
- **Work in sessions**: 1-3 hour focused sessions work better than marathons.
- **One agent at a time**: Focus on one conversation, save, then move to the next.
- **Regular exports**: Export to Word regularly to see your progress.

### 🎨 Creative Process
- **Trust the process**: Back-and-forth dialogue is how quality emerges.
- **Don't over-plan**: You can discover through writing.
- **Don't under-plan**: A little structure prevents major rewrites.
- **Your vision leads**: The agents serve your creative vision, not vice versa.

---

## Keyboard Shortcuts

- **Ctrl+S** (Cmd+S on Mac) - Save project
- **Enter** - Send message in Generate tab
- **Escape** - Clear message box without sending

---

## Troubleshooting

### "No API Key" Warning

**Solution:** Click **Settings** → **Change API Key** and enter your Anthropic API key.

### "No Project Loaded to Save"

**Solution:** Create a new project first (New Project button), or open an existing one (Open Project button).

### Can't Find My Project Files

**Default location:** `~/NovelProjects/` (or `C:\Users\YourName\NovelProjects` on Windows)

**To find it:**
1. Click **Open Project**
2. The dialog shows the default location
3. Browse to see your project folders

### Agent Response Seems Cut Off

The agents use streaming responses. If it stops mid-sentence:
- Wait a moment - it might be processing
- Check your internet connection
- If it truly failed, ask the agent to continue

### Application Won't Launch

**Make sure:**
- Python 3.8+ is installed
- You ran the installer wizard (double-click launcher, wait for install)
- On Mac: Right-click → Open (for security approval)
- On Linux: Made `.sh` files executable

---

## Next Steps

### You're Ready to Write!

1. ✅ Application installed
2. ✅ API key configured
3. ✅ First project created
4. ✅ Story configured
5. ✅ Know how to chat with agents
6. ✅ Can save and export

### Your First Session Plan

**Suggested 2-hour first session:**
- [ ] 30 min: Chat with Story Advocate about your vision
- [ ] 60 min: Work with Architect on structure/outline
- [ ] 30 min: Review what you've created, save everything

**Then take a break!** Let ideas percolate. Come back for your next session when you're fresh.

---

## Learning More

- **[README.md](README.md)** - System overview and agent descriptions
- **[WORKFLOW.md](WORKFLOW.md)** - Detailed writing workflow examples
- **[/agents/](agents/)** - Detailed specifications for each agent
- **[GUI_TESTING.md](GUI_TESTING.md)** - Feature testing guide

---

## You're All Set! 🎉

**The application is ready. Your agents are waiting. Your story is calling.**

Click **"New Project"** and begin your novel writing journey!

---

*Questions or issues? The Story Advocate agent is literally designed to help guide you. Just ask!*
