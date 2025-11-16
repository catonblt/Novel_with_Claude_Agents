# Novel Writing Agent System - Clean Rebuild Specification

## 🎯 Project Vision

A streamlined, modern desktop application for collaborative novel writing with AI agents. The system features a beautiful dark-mode web UI, intelligent agents that autonomously manage project files, built-in version control, and a friction-free workflow from concept to completed manuscript.

---

## 🏗️ Technical Architecture

### Stack
- **Desktop Framework**: Tauri (Rust + Web) or Electron
  - Tauri preferred: smaller bundle size, better security, native performance
  - Fallback to Electron if Tauri proves complex
- **Frontend**: React with TypeScript
  - **UI Framework**: shadcn/ui or Radix UI (modern, accessible components)
  - **Styling**: Tailwind CSS with custom dark theme
  - **State Management**: Zustand or React Context
  - **Markdown Editor**: Monaco Editor or CodeMirror 6
- **Backend/API Layer**:
  - Python FastAPI embedded in the desktop app
  - Anthropic Claude API integration
  - File system management
- **Version Control**: libgit2 (Git operations under the hood)
- **Database**: SQLite for project metadata, conversation history

### Application Structure
```
novel-writer/
├── src-tauri/           # Rust backend (if using Tauri)
│   ├── src/
│   │   ├── main.rs
│   │   ├── file_ops.rs
│   │   └── git_ops.rs
│   └── Cargo.toml
├── src/                 # React frontend
│   ├── components/
│   │   ├── SetupWizard/
│   │   ├── Workspace/
│   │   ├── AgentChat/
│   │   └── ui/         # Reusable UI components
│   ├── lib/
│   │   ├── api.ts      # Backend API calls
│   │   ├── agents.ts   # Agent definitions
│   │   └── types.ts
│   ├── App.tsx
│   └── main.tsx
├── python-backend/      # Python API server
│   ├── main.py         # FastAPI server
│   ├── agents/         # Agent system
│   ├── claude_client.py
│   └── requirements.txt
└── package.json
```

---

## 🤖 Agent System Design

### Streamlined Agent Roster (5 Core Agents)

**1. Story Architect** (merged from Architect + Story Advocate)
- Overall narrative structure, acts, chapters, scenes
- Thematic architecture and story arcs
- Facilitates initial story development dialogue
- **Output**: `planning/story-outline.md`, `planning/chapter-breakdown.md`

**2. Character & Dialogue Specialist** (merged from Character Psychologist + some Prose Stylist)
- Character creation, psychology, development
- Authentic dialogue with subtext
- Character voice consistency
- **Output**: `characters/*.md` (one file per character)

**3. Prose & Atmosphere Writer** (merged from Prose Stylist + Atmosphere Agent)
- Scene writing with beautiful prose
- Sensory detail and atmospheric description
- Narrative voice consistency
- **Output**: `manuscript/chapters/*.md`, `manuscript/scenes/*.md`

**4. Research & Continuity Guardian** (merged from Research + Continuity Editor)
- Fact-checking and research
- Story bible maintenance
- Timeline and detail tracking
- Contradiction detection
- **Output**: `story-bible/continuity.md`, `story-bible/timeline.md`, `research/*.md`

**5. Editorial Reviewer** (merged from Beta Reader + Redundancy Editor)
- Critical reading and feedback
- Redundancy detection and variation suggestions
- Pacing and engagement analysis
- **Output**: `feedback/editorial-notes.md`, `feedback/revision-suggestions.md`

### Agent Capabilities

Each agent has:
- **Read Access**: Full project folder access
- **Write Access**: Can create/modify/delete any file in project
- **Version Awareness**: Can view file history and previous versions
- **Autonomous Action**: Can propose AND execute changes (with user approval settings)
- **Collaboration**: Can reference other agents' work and coordinate

### Agent System Prompts

Each agent gets a comprehensive system prompt including:
```python
{
  "role": "Story Architect",
  "expertise": [...],
  "responsibilities": [...],
  "file_access": {
    "primary_outputs": ["planning/", "outlines/"],
    "can_edit": "*",  # All project files
    "version_control": true
  },
  "capabilities": [
    "read_file",
    "write_file",
    "list_directory",
    "search_content",
    "view_history",
    "create_version_tag"
  ],
  "collaboration_style": "...",
  "quality_standards": "..."
}
```

---

## 🎨 UI/UX Design

### Design System

**Color Palette (Dark Mode Primary)**
```css
--background: #0a0a0a (deep black)
--surface: #141414 (card backgrounds)
--surface-elevated: #1e1e1e (hover states)
--border: #2a2a2a (subtle dividers)
--accent: #8b5cf6 (purple - primary actions)
--accent-hover: #7c3aed
--text-primary: #ffffff
--text-secondary: #a3a3a3
--text-muted: #737373
--success: #10b981
--warning: #f59e0b
--error: #ef4444
```

**Typography**
- Headers: Inter or Geist Sans (clean, modern)
- Body: Same as headers for consistency
- Code/Mono: JetBrains Mono or Fira Code (for markdown editing)

**Spacing**: 8px base unit system (8, 16, 24, 32, 48, 64px)

### Application Screens

#### 1. Welcome Screen (First Launch)
- Centered card with app logo/title
- "Create New Project" button (large, prominent)
- API key configuration link (bottom corner)
- Recent projects list (if any exist)

#### 2. Setup Wizard (New Project)

**Step 1: Project Basics**
```
┌─────────────────────────────────────┐
│  Create Your Novel Project          │
│                                     │
│  Novel Title: [_______________]     │
│  Author Name: [_______________]     │
│  Genre: [Dropdown ▼]               │
│  Target Word Count: [___________]   │
│                                     │
│  Project Location:                  │
│  ~/NovelProjects/my-novel  [Browse] │
│                                     │
│           [Cancel]  [Next →]        │
└─────────────────────────────────────┘
```

**Step 2: Story Foundation**
```
┌─────────────────────────────────────┐
│  Tell Me About Your Story           │
│                                     │
│  Core Premise:                      │
│  [Multi-line text area]             │
│                                     │
│  Themes (optional):                 │
│  [Multi-line text area]             │
│                                     │
│  Setting (optional):                │
│  [Multi-line text area]             │
│                                     │
│  Key Characters (optional):         │
│  [Multi-line text area]             │
│                                     │
│        [← Back]  [Create Project]   │
└─────────────────────────────────────┘
```

**Post-Creation**
- Show success message with project location
- Auto-initialize Git repository
- Create folder structure
- Transition to Workspace

#### 3. Main Workspace

**Layout: Single-Page Application**

```
┌────────────────────────────────────────────────────────────┐
│ 📚 My Novel Title                      [⚙️] [📊] [💾]      │ Header
├──────────────────────────────────────┬─────────────────────┤
│                                      │                     │
│  Agent Chat Interface                │  Project Explorer   │
│  ┌────────────────────────────────┐  │  ┌───────────────┐ │
│  │                                │  │  │ 📁 planning   │ │
│  │  [Agent Messages & Responses]  │  │  │ 📁 characters │ │
│  │                                │  │  │ 📁 manuscript │ │
│  │  User: "Let's develop the      │  │  │ 📁 story-bible│ │
│  │        main character..."       │  │  │ 📁 research   │ │
│  │                                │  │  │ 📁 feedback   │ │
│  │  Story Architect: "I'll help..." │  │  └───────────────┘ │
│  │                                │  │                     │
│  │  [File updates shown inline]   │  │  Active Files:      │
│  │  ✓ Updated character/alice.md  │  │  - chapter-1.md    │
│  │                                │  │  - story-outline.md│
│  │                                │  │                     │
│  └────────────────────────────────┘  │  [Preview pane]     │
│  ┌────────────────────────────────┐  │  Shows selected     │
│  │ Message: @architect            │  │  file content with  │
│  │                                │  │  syntax highlighting│
│  └────────────────────────────────┘  │                     │
│  Active Agents:                      │                     │
│  [Architect] [Character] [Prose]...  │                     │
│                                      │                     │
│  Left: Chat (60%)                    │  Right: Files (40%) │
└──────────────────────────────────────┴─────────────────────┘
```

**Key Features:**

1. **Agent Chat Panel (Left - 60%)**
   - Scrollable conversation history
   - Agent avatars/icons with different colors
   - Inline file change indicators
   - Message timestamp
   - Streaming response support (words appear as typed)
   - @mention support to invoke specific agents
   - Rich text for agent responses (formatted markdown)

2. **Project Explorer (Right - 40%)**
   - Collapsible folder tree
   - File click opens preview pane below
   - File badges (modified indicator, word count)
   - Quick actions: Edit in external editor, View history
   - Search across all files

3. **Header Bar**
   - Project title (click to open project settings)
   - Settings icon (API key, preferences)
   - Stats icon (word count, progress)
   - Save icon with auto-save indicator

4. **Agent Selector Bar (Bottom of Chat)**
   - Toggle which agents are active
   - Visual indicator when agent is "thinking"
   - Click agent to see their specialized capabilities

#### 4. Settings Panel (Modal/Drawer)
```
┌─────────────────────────────────┐
│  Settings                       │
├─────────────────────────────────┤
│  API Configuration              │
│    Anthropic API Key: [*****]   │
│    Model: claude-3-5-sonnet ▼   │
│                                 │
│  Project Settings               │
│    Auto-save: [✓] Enabled       │
│    Auto-commit: [✓] On change   │
│                                 │
│  Agent Behavior                 │
│    Autonomy Level:              │
│    [○────────●─] High           │
│    (Low = Always ask)           │
│    (High = Auto-execute changes)│
│                                 │
│  [Export Project] [Close]       │
└─────────────────────────────────┘
```

#### 5. Version History Viewer (Modal)
```
┌─────────────────────────────────────────────┐
│  Version History                            │
├─────────────────────────────────────────────┤
│  Timeline                    File: chapter-1.md │
│  ┌─────────────────────────┐                │
│  │ ● Now                   │  [View] [Restore]│
│  │ │ 1,247 words           │                │
│  │ ↓                       │                │
│  │ ● 10 minutes ago        │  [View] [Restore]│
│  │ │ Added dialogue scene  │                │
│  │ ↓                       │                │
│  │ ● 2 hours ago           │  [View] [Restore]│
│  │   Initial draft         │                │
│  └─────────────────────────┘                │
│                                             │
│  Diff View:                                 │
│  [Show side-by-side comparison]            │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 📁 Project Folder Structure

When a project is created, generate this clean structure:

```
~/NovelProjects/my-novel-title/
├── .git/                      # Git repository (auto-initialized)
├── .novel-project.json        # Project metadata
│
├── planning/
│   ├── story-outline.md       # High-level story structure
│   ├── chapter-breakdown.md   # Detailed chapter plan
│   └── themes.md              # Thematic notes
│
├── characters/
│   ├── alice.md               # One file per character
│   ├── bob.md
│   └── _character-template.md # Template for new characters
│
├── manuscript/
│   ├── final-manuscript.md    # Compiled full manuscript
│   ├── chapters/
│   │   ├── chapter-01.md
│   │   ├── chapter-02.md
│   │   └── ...
│   └── scenes/                # Optional: scene-level drafts
│       ├── ch01-scene01.md
│       └── ...
│
├── story-bible/
│   ├── continuity.md          # Facts, details, established info
│   ├── timeline.md            # Story chronology
│   └── world-notes.md         # Setting, world-building
│
├── research/
│   └── [agent-generated research files]
│
├── feedback/
│   ├── editorial-notes.md     # Beta reader feedback
│   └── revision-log.md        # Changes made
│
└── exports/                   # Generated output files
    ├── manuscript.docx
    ├── manuscript.pdf
    └── manuscript-epub/
```

### File Format Standards

**Chapter Files** (`manuscript/chapters/chapter-01.md`):
```markdown
# Chapter 1: The Beginning

_1,247 words | Last updated: 2024-01-15_

---

The prose content here, beautifully formatted with proper paragraph breaks.

Dialogue is clean and well-attributed.

Sensory details immerse the reader.

---

## Notes
- Key events: Alice meets Bob
- Character development: Alice's fear of commitment
- Themes: isolation, connection
```

**Character Files** (`characters/alice.md`):
```markdown
# Alice Mercer

## Core Identity
- **Age**: 32
- **Occupation**: Marine biologist
- **Key Trait**: Intellectually curious but emotionally guarded

## Psychology
Deep dive into motivations, fears, desires...

## Voice & Dialogue
Examples of how this character speaks...

## Arc
Where they start → transformation → where they end

## Relationships
- **Bob**: Initially antagonistic, develops into...

## Appearance
Brief but vivid description...

## Notes
- Established facts to maintain continuity
```

---

## 🔄 Workflow & User Experience

### Typical User Session

1. **Launch App** → Opens to Workspace (last project auto-loads)
2. **Start Conversation**: "Let's outline the first three chapters"
3. **Story Architect Responds**:
   - Generates outline
   - **Automatically writes** `planning/chapter-breakdown.md`
   - Shows inline notification: "✓ Created chapter-breakdown.md"
   - User can click notification to view file
4. **Continue Dialogue**: "Now write chapter 1"
5. **Prose & Atmosphere Writer**:
   - Writes chapter
   - **Automatically creates** `manuscript/chapters/chapter-01.md`
   - Git commit created automatically
6. **User Reviews** file in Project Explorer
7. **Request Revision**: "Make Alice more assertive in the opening"
8. **Writer Edits** the file directly
   - Shows diff in chat: `± Modified chapter-01.md (127 words changed)`
   - New commit created
9. **Version Control**: User can click "View History" to see all versions

### Agent Autonomy Settings

**Low Autonomy (Default for new users)**
- Agent proposes changes
- User clicks "Approve" before file is written
- Good for learning the system

**High Autonomy (Power users)**
- Agents write/edit files immediately
- User can undo via version history
- Faster workflow

### Auto-Save & Git Integration

- **Every agent file operation** triggers:
  1. File write
  2. Git commit with message: `[Agent Name]: Brief description`
  3. Update UI to show change
- User can also manually save with Ctrl+S
- Git history viewable in Version History panel
- Can restore any previous version with one click

---

## 🚀 Technical Implementation Priorities

### Phase 1: Foundation (MVP)
1. **Project Setup**
   - Tauri/Electron boilerplate
   - React app with Tailwind + shadcn/ui
   - Python FastAPI backend
   - SQLite database schema

2. **Core UI**
   - Setup Wizard (2-step)
   - Main Workspace layout (chat + file explorer)
   - Settings panel
   - Dark theme implementation

3. **Agent System**
   - Claude API integration
   - 5 agent system prompts
   - Basic agent routing (user messages → correct agent)
   - File read/write capabilities for agents

4. **File Management**
   - Project folder initialization
   - File CRUD operations via agents
   - Project Explorer UI with file preview

### Phase 2: Intelligence
1. **Agent Collaboration**
   - Agents can reference each other's work
   - Cross-file awareness (e.g., Continuity agent reads manuscript)

2. **Version Control**
   - Git integration (libgit2)
   - Auto-commit on agent changes
   - Version history UI
   - Diff viewer

3. **Advanced Chat**
   - Streaming responses
   - @mentions to invoke specific agents
   - File change notifications inline
   - Conversation history persistence

### Phase 3: Polish
1. **Export System**
   - Generate formatted DOCX
   - PDF export
   - EPUB compilation
   - Print-ready formatting

2. **Quality of Life**
   - Search across project files
   - Word count tracking & goals
   - Keyboard shortcuts
   - Agent "thinking" indicators
   - Undo/redo for user edits

3. **Performance**
   - Large file handling (novels can be 100k+ words)
   - Caching for file operations
   - Optimized rendering

---

## 🛠️ Development Guidelines

### Code Quality Standards
- **TypeScript**: Strict mode, comprehensive types
- **Python**: Type hints with mypy, Black formatting
- **Testing**: Unit tests for agent logic, E2E tests for critical flows
- **Documentation**: JSDoc for components, docstrings for Python

### Agent Development Principles
1. **Clarity**: Each agent has ONE clear purpose
2. **Autonomy**: Agents should take action, not just suggest
3. **Collaboration**: Agents reference each other's work
4. **Quality**: Output should be publication-ready
5. **Traceability**: Every change logged and reversible

### File System Safety
- **Never delete without asking** (except temp files)
- **Always commit before major changes**
- **Validate file paths** before operations
- **Handle errors gracefully** (disk full, permissions, etc.)

---

## 🎯 Success Metrics

A successful rebuild means:
- ✅ User can create a project in under 30 seconds
- ✅ Agents can autonomously update any project file
- ✅ Every change is reversible via version history
- ✅ Chat interface is responsive (< 100ms to show streaming start)
- ✅ UI is beautiful and feels modern (not "programmer art")
- ✅ System handles a 100k word novel smoothly
- ✅ Zero configuration after API key setup
- ✅ No bloat: every feature has a clear purpose

---

## 📦 Deliverables

### Repository Structure
```
novel-writer/
├── README.md                    # Clear setup instructions
├── docs/
│   ├── ARCHITECTURE.md
│   ├── AGENT_GUIDE.md
│   └── USER_GUIDE.md
├── src/                         # Frontend
├── src-tauri/ or electron/      # Desktop wrapper
├── python-backend/              # Agent system
├── package.json
└── .github/workflows/           # CI/CD
    └── build.yml                # Auto-build releases
```

### Documentation Requirements
1. **README.md**: One-command setup, clear feature list
2. **ARCHITECTURE.md**: Technical deep-dive for developers
3. **AGENT_GUIDE.md**: How agents work, how to customize
4. **USER_GUIDE.md**: Walkthrough for writers

### First Release (v1.0.0)
- Installers for Windows, macOS, Linux
- All Phase 1 & Phase 2 features
- Comprehensive error handling
- Basic user documentation
- Example project included

---

## 🎨 Design Assets Needed

1. **App Icon**: 1024x1024, works at small sizes
2. **Agent Avatars**: 5 distinct icons for each agent
3. **Splash Screen**: For app launch
4. **Empty States**: Illustrations for empty project, no files yet, etc.

Suggestion: Use a consistent illustration style, perhaps:
- Purple/violet accent color theme
- Minimalist line-art style
- Dark-mode first design

---

## 🔐 Security & Privacy

- **API keys**: Stored securely in system keychain (not plaintext)
- **Local-first**: All project data stays on user's machine
- **No telemetry**: Respect user privacy, no tracking
- **Open source**: Code auditable by users

---

## 📝 Next Steps to Build

1. **Create new repository**: `novel-writer` or similar
2. **Choose stack**: Finalize Tauri vs Electron decision
3. **Setup boilerplate**:
   - Frontend: `npm create vite@latest -- --template react-ts`
   - Add Tailwind + shadcn/ui
   - Backend: FastAPI project structure
4. **Implement Phase 1** following priorities above
5. **Iterate** based on testing

---

## 💡 Future Enhancements (Post-v1.0)

- **Templates**: Genre-specific project templates
- **Cloud Sync**: Optional backup to user's cloud storage
- **Collaboration**: Multiple writers on same project (advanced)
- **Audio**: Text-to-speech for reading manuscript aloud
- **Analytics**: Story structure visualization (plot diagrams, pacing graphs)
- **Plugins**: Allow community to create custom agents

---

**End of Specification**

This document is the complete blueprint for rebuilding the Novel Writing Agent System. The goal is a clean, powerful, beautiful application that makes collaborative AI writing effortless.
