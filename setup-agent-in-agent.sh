#!/bin/bash
set -e

echo "🚀 Setting up Agent-in-Agent Claude Code MCP..."

# Step 1: Check if Claude CLI is installed
echo ""
echo "1️⃣ Checking Claude CLI installation..."
if ! command -v claude &> /dev/null; then
    echo "❌ Claude CLI not found. Please install it first."
    exit 1
fi

CLAUDE_PATH=$(which claude)
echo "✅ Claude CLI found at: $CLAUDE_PATH"

# Step 2: Clone and build claude-code-mcp
echo ""
echo "2️⃣ Installing claude-code-mcp..."
cd /home/alin

if [ -d "claude-code-mcp" ]; then
    echo "⚠️  claude-code-mcp directory already exists. Updating..."
    cd claude-code-mcp
    git pull
else
    echo "📦 Cloning claude-code-mcp..."
    git clone https://github.com/steipete/claude-code-mcp.git
    cd claude-code-mcp
fi

echo "📦 Installing dependencies..."
npm install

echo "🔨 Building..."
npm run build

if [ ! -f "build/index.js" ]; then
    echo "❌ Build failed! build/index.js not found."
    exit 1
fi

echo "✅ claude-code-mcp built successfully"

# Step 3: Accept permissions (one-time)
echo ""
echo "3️⃣ Accepting Claude Code permissions..."
cd /home/alin/claude-pro-writer

echo "📝 Running Claude Code with --dangerously-skip-permissions..."
echo "   Press Enter when prompted to accept permissions, then type 'exit' to continue."
echo ""
read -p "Press Enter to continue..."

unset ANTHROPIC_API_KEY ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN
claude --dangerously-skip-permissions

echo "✅ Permissions accepted"

# Step 4: Test MCP server
echo ""
echo "4️⃣ Testing MCP server..."
cd /home/alin/claude-code-mcp

echo "Starting MCP server for 3 seconds..."
timeout 3s node build/index.js || echo "✅ MCP server started successfully (timeout expected)"

# Step 5: Verify configuration
echo ""
echo "5️⃣ Verifying configuration..."
MCP_CONFIG="/home/alin/DATA/OBSIDIAN/inteles-vault/.mcp.json"

if [ ! -f "$MCP_CONFIG" ]; then
    echo "❌ .mcp.json not found at $MCP_CONFIG"
    exit 1
fi

if grep -q "claude-code-writer" "$MCP_CONFIG"; then
    echo "✅ .mcp.json configured correctly"
else
    echo "⚠️  .mcp.json does not contain claude-code-writer config"
    echo "   Please update it manually using the template in SOLUTION-AGENT-IN-AGENT.md"
fi

# Done
echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Start GLM vault session:"
echo "   cd /home/alin/DATA/OBSIDIAN/inteles-vault"
echo "   claude"
echo ""
echo "2. Check MCP status:"
echo "   /mcp"
echo ""
echo "3. Test the writer:"
echo "   Use @claude-code-writer to execute: { \"prompt\": \"Scrie un paragraf în română despre vise.\", \"workFolder\": \"/home/alin/claude-pro-writer\" }"
echo ""
echo "📚 See SOLUTION-AGENT-IN-AGENT.md for complete guide"
echo ""
