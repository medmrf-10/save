#!/bin/bash
export PATH="/opt/homebrew/bin:$PATH"

REPO="medmrf-10/claude-code-summary"

ISSUES=(
    "Task 1: Core Scaffolding & Setup|Initialize a React (Vite) application. Set up a global 'Claude Dark Theme' (dark mode only), RTL direction (dir=rtl), and React Router. Create a minimal, elegant wiki layout with a sidebar for navigation and a main content area. Make sure it supports Markdown rendering."
    "Task 2: Homepage Visualization & Setup|Create the interactive index.md homepage. Design an elegant, minimal visual map (or nodes/links) using CSS and React representing the 5 core sections (Query Engine, Memory System, Swarm, Tool System, Misc). Read the contents of index.md and integrate it."
    "Task 3: Query Engine - System Prompts Component|Read 01_QueryEngine/1_SystemPrompts_Secrets.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
    "Task 4: Query Engine - Context Secrets Component|Read 01_QueryEngine/2_Context_Secrets.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
    "Task 5: Query Engine - The Engine Loop Component|Read 01_QueryEngine/3_TheEngineLoop_Secrets.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
    "Task 6: Query Engine - Post Response Hooks Component|Read 01_QueryEngine/4_PostResponse_Hooks.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
    "Task 7: Memory System - Memdir Architecture Component|Read 02_MemorySystem/1_Memdir_Architecture_Secrets.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
    "Task 8: Memory System - Memory Taxonomy Component|Read 02_MemorySystem/2_Memory_Taxonomy_Secrets.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
    "Task 9: Memory System - Continuous Logs History Component|Read 02_MemorySystem/3_ContinuousLogs_History_Secrets.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
    "Task 10: Swarm - Coordinator Router Component|Read 03_Swarm/1_Coordinator_Router_Secrets.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
    "Task 11: Swarm - Prompt Synthesis Component|Read 03_Swarm/2_Prompt_Synthesis_Secrets.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
    "Task 12: Swarm - Task Types and Buddy Component|Read 03_Swarm/3_Task_Types_and_Buddy_Secrets.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
    "Task 13: Tool System - Tool Architecture Component|Read 04_ToolSystem/1_Tool_Architecture_Secrets.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
    "Task 14: Tool System - Permission Gating Component|Read 04_ToolSystem/2_Permission_Gating_Secrets.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
    "Task 15: Tool System - MCP and Caching Component|Read 04_ToolSystem/3_MCP_and_Caching_Secrets.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
    "Task 16: Misc - CLI DX and Ink React Component|Read 05_Misc/1_CLI_DX_and_Ink_React_Secrets.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
    "Task 17: Misc - Cost and Telemetry Component|Read 05_Misc/2_Cost_and_Telemetry_Secrets.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
    "Task 18: Misc - Voice and Vim Mode Component|Read 05_Misc/3_Voice_and_Vim_Mode_Secrets.md. Create a professional, minimal, RTL Wiki React component to display and explain this summary interactively."
)

echo "Starting deployment of 18 tasks to Jules..."

for ITEM in "${ISSUES[@]}"; do
    TITLE="${ITEM%%|*}"
    DESC="${ITEM##*|}"
    
    BODY="The goal is to build an interactive Wiki site in Arabic (RTL). Theme: Claude Dark Mode (minimal & elegant). Focus on visualizing complex things.

Required specific task:
$DESC

Please act as a professional frontend developer. Implement the requirements perfectly without errors."

    # Create the issue
    echo "Creating issue for: $TITLE"
    ISSUE_URL=$(gh issue create --repo $REPO --title "$TITLE" --body "$BODY")
    
    echo "Issue created: $ISSUE_URL. Dispatching to Jules..."
    # Dispatch to Jules
    jules new --repo $REPO "Fix Issue: $TITLE $ISSUE_URL. $BODY" > /dev/null 2>&1 &
    
    # Small delay to ensure API rate limits aren't hit aggressively
    sleep 2
done

echo "All 18 tasks successfully dispatched to Jules in parallel!"
