# GUI Testing Guide

This guide will help you test the complete GUI application end-to-end.

## Prerequisites

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set API key:
   ```bash
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```

## Test Procedure

### Test 1: First Launch

1. **Launch the application:**
   ```bash
   python novel_gui.py
   ```

2. **Expected behavior:**
   - Application window opens with dark theme
   - Welcome message appears with instructions
   - Shows "No project loaded" in menu bar
   - All tabs are visible: Configure, Generate, Review, Export

3. **Verify:**
   - [ ] Welcome message displayed
   - [ ] Window size is 1400x900
   - [ ] Dark theme is active
   - [ ] All UI elements are visible

### Test 2: Create New Project

1. **Click "New Project" button**

2. **Expected behavior:**
   - New Project dialog appears
   - Shows fields for: Project Name, Author Name, Directory
   - Shows default directory location

3. **Fill in the form:**
   - Project Name: "Test Novel"
   - Author Name: "Test Author"
   - Directory: Leave blank (use default)

4. **Click "Create Project"**

5. **Expected behavior:**
   - Success message appears showing project path
   - Message includes next steps
   - Automatically switches to Configure tab
   - Project name appears in menu bar: "Project: Test Novel"
   - Getting Started guide is visible in Configure tab

6. **Verify:**
   - [ ] Project created in ~/NovelProjects/test-novel
   - [ ] .novel-config.json file exists
   - [ ] Directory structure created (planning, manuscript, etc.)
   - [ ] Configure tab is active
   - [ ] Getting Started guide is visible

### Test 3: Configure Story

1. **In Configure tab (Simple Mode):**
   - Fill in Story Idea: "A mystery novel about a detective investigating a cold case"
   - Select Genre: "Mystery"
   - Target Word Count: "80000"
   - Themes: "justice, redemption, truth"
   - Tone: "dark, suspenseful"

2. **Click "Save Project" in menu (or press Ctrl+S)**

3. **Expected behavior:**
   - Success message appears
   - No errors

4. **Switch to Advanced Mode:**
   - Click "Advanced" in the mode selector
   - All fields from Simple mode should be populated
   - Additional fields available (POV, Chronology, etc.)

5. **Verify:**
   - [ ] All simple mode fields transferred to advanced mode
   - [ ] Save succeeded
   - [ ] Ctrl+S shortcut works

### Test 4: Advanced Configuration

1. **In Configure tab (Advanced Mode):**
   - Change POV to "first_person"
   - Change Chronology to "non_linear"
   - Estimated Chapters: "25"
   - Uncheck some agents (e.g., uncheck Agent 5: Research Agent)

2. **Save the project**

3. **Verify:**
   - [ ] All settings saved correctly
   - [ ] Selected agents remembered

### Test 5: Generate Content (Without Configuration)

1. **Switch to Generate tab WITHOUT configuring story (create a new project for this test)**

2. **Click "Start Conversation"**

3. **Expected behavior:**
   - Warning dialog appears: "Story Not Configured"
   - Asks if you want to continue anyway
   - Clicking "No" returns to Generate tab
   - Clicking "Yes" starts conversation with limited context

4. **Verify:**
   - [ ] Validation works when story_idea is empty
   - [ ] User can choose to continue or go back

### Test 6: Generate Content (With Configuration)

1. **Use a configured project**

2. **In Generate tab:**
   - Getting Started guide is visible at top
   - Select Agent: "8. Story Advocate Agent"
   - Click "Start Conversation"

3. **Expected behavior:**
   - If API key not set: Error message with instructions
   - If API key set: Conversation starts
   - System message appears in chat: "[SYSTEM] Started conversation with..."
   - Real-time log shows conversation started
   - Status shows: "Status: Connected to Story Advocate Agent"

4. **Type a message:**
   - Enter: "Help me develop my mystery novel idea"
   - Press Enter or click "Send"

5. **Expected behavior:**
   - Message appears in chat
   - Agent response streams in real-time
   - Log shows activity
   - Can see text being generated character by character

6. **Test controls:**
   - Try "Stop Generation" button during generation
   - Try "Clear Conversation" button
   - Try "Save Agent Output" button

7. **Verify:**
   - [ ] Conversation starts successfully
   - [ ] Real-time streaming works
   - [ ] Logs update in real-time
   - [ ] All buttons work

### Test 7: Save Agent Output

1. **After having a conversation:**
   - Click "Save Agent Output"

2. **Expected behavior:**
   - Success message appears
   - Output saved to agent-outputs directory

3. **Verify:**
   - [ ] File created: agent-outputs/agent_8_story-advocate-agent.md
   - [ ] File contains the conversation
   - [ ] Timestamp included

### Test 8: Review Tab

1. **Switch to Review tab**

2. **Select "Final Story" from dropdown**
   - Click "Load"

3. **Expected behavior:**
   - Shows placeholder text (no content yet for new project)
   - Word count shows: "Words: 0"

4. **Select "Agent 8: Story Advocate Agent"**
   - Click "Load"

5. **Expected behavior:**
   - Shows saved agent output
   - Word count updates
   - Can edit the text

6. **Edit the text:**
   - Make some changes
   - Notice "Unsaved changes" indicator appears

7. **Click "Save Changes"**

8. **Expected behavior:**
   - Success message
   - Unsaved indicator clears

9. **Verify:**
   - [ ] Can view different outputs
   - [ ] Can edit content
   - [ ] Unsaved changes tracked
   - [ ] Save works

### Test 9: Export Tab

1. **Switch to Export tab**

2. **Create a version:**
   - Enter version name: "First Draft"
   - Click "Create"

3. **Expected behavior:**
   - Success message
   - Version appears in list

4. **Create another version:**
   - Name: "Second Draft"
   - Click "Create"

5. **Compare versions:**
   - Select both versions (checkboxes)
   - Click "Compare Selected Versions"

6. **Expected behavior:**
   - Comparison window opens
   - Shows side-by-side view

7. **Export to Word:**
   - Fill in Document Title: "My Test Novel"
   - Fill in Author Name: "Test Author"
   - Check "Include all agent outputs as appendix"
   - Click "Export to Word Document"

8. **Expected behavior:**
   - File dialog appears
   - Save the file
   - Success message appears

9. **Verify:**
   - [ ] Versions created successfully
   - [ ] Comparison works
   - [ ] Word document exports correctly
   - [ ] Document contains story + agent outputs

### Test 10: Open Existing Project

1. **Close the application (or create a new instance)**

2. **Click "Open Project"**

3. **Expected behavior:**
   - Info dialog appears explaining what to select
   - Shows default location
   - File dialog opens to ~/NovelProjects

4. **Select your test project directory**

5. **Expected behavior:**
   - Project loads successfully
   - All tabs show correct data
   - Project name in menu bar

6. **Verify:**
   - [ ] Project loads correctly
   - [ ] All configuration preserved
   - [ ] Agent outputs still there
   - [ ] Versions preserved

### Test 11: Error Handling

1. **Try to open invalid directory:**
   - Click "Open Project"
   - Select a directory without .novel-config.json

2. **Expected behavior:**
   - Error message with helpful information

3. **Try to generate without API key:**
   - Unset ANTHROPIC_API_KEY
   - Try to start conversation

4. **Expected behavior:**
   - Error message with instructions

5. **Verify:**
   - [ ] Errors handled gracefully
   - [ ] Helpful error messages

### Test 12: Keyboard Shortcuts

1. **Make changes in Configure tab**

2. **Press Ctrl+S (or Cmd+S on Mac)**

3. **Expected behavior:**
   - Project saves

4. **Verify:**
   - [ ] Ctrl+S works
   - [ ] Cmd+S works on Mac

## All Tests Complete!

If all tests pass, the GUI is working correctly and ready for use.

## Common Issues and Solutions

### Issue: CustomTkinter not found
**Solution:** `pip install customtkinter`

### Issue: Anthropic not found
**Solution:** `pip install anthropic`

### Issue: python-docx not found
**Solution:** `pip install python-docx`

### Issue: API key not configured
**Solution:** `export ANTHROPIC_API_KEY='your-key'`

### Issue: Project directory not found when opening
**Solution:** Make sure you're selecting the project root directory (the one containing .novel-config.json)

## Success Criteria

The GUI is working properly if:
- ✅ Can create new projects
- ✅ Can open existing projects
- ✅ Can configure story in both Simple and Advanced modes
- ✅ Can chat with agents and see real-time streaming
- ✅ Can save and load agent outputs
- ✅ Can edit outputs in Review tab
- ✅ Can create versions and compare them
- ✅ Can export to Word document
- ✅ All error messages are helpful and clear
- ✅ Keyboard shortcuts work
- ✅ Welcome message guides new users
