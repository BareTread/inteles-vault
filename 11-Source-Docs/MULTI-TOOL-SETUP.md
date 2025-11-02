# Setting Up WordPress MCP Across Multiple AI Tools

## Overview

You want to use inteles.ro WordPress MCP with:
1. ✅ **Claude Desktop** (already configured)
2. **Windsurf** (Codeium's AI IDE)
3. **Codex CLI** (OpenAI Codex terminal tool)

Each tool has different configuration methods.

---

## 1. Claude Desktop (✅ DONE)

**Config Location:**
```
~/.config/Claude/claude_desktop_config.json
```

**Status:** ✅ Already configured and tested

**Config:**
```json
{
  "mcpServers": {
    "inteles-wordpress": {
      "command": "npx",
      "args": [
        "-y",
        "@instawp/mcp-wp",
        "--url=https://inteles.ro",
        "--username=baretrea",
        "--appPassword=Yzix4308YGsRNLirTWJfdztM"
      ]
    }
  }
}
```

---

## 2. Windsurf (Codeium AI IDE)

### Where is Windsurf MCP Config?

**Linux:**
```
~/.codeium/windsurf/mcp_settings.json
```

OR

```
~/.config/Windsurf/User/globalStorage/mcp_settings.json
```

**To find yours:**
```bash
find ~ -name "mcp_settings.json" 2>/dev/null
```

### Updated Config for Windsurf

I created `windsurf-mcp-config.json` with the WordPress MCP added:

```json
{
  "mcpServers": {
    "perplexity-ask": { ... },
    "memory": { ... },
    "sequential-thinking": { ... },
    "claude-code": { ... },
    "chrome-devtools": { ... },
    "inteles-wordpress": {
      "command": "npx",
      "args": [
        "-y",
        "@instawp/mcp-wp",
        "--url=https://inteles.ro",
        "--username=baretrea",
        "--appPassword=Yzix4308YGsRNLirTWJfdztM"
      ],
      "disabled": false
    }
  }
}
```

### How to Apply

**Option A: Manual Copy-Paste**
1. Find your Windsurf config:
   ```bash
   find ~ -name "mcp_settings.json" 2>/dev/null
   ```

2. Open it:
   ```bash
   nano /path/to/mcp_settings.json
   ```

3. Add the `inteles-wordpress` block to the `mcpServers` section

4. Save and restart Windsurf

**Option B: Replace Entire File**
```bash
# Find your Windsurf config location first
WINDSURF_CONFIG=$(find ~ -name "mcp_settings.json" 2>/dev/null | head -1)

# Backup current config
cp "$WINDSURF_CONFIG" "${WINDSURF_CONFIG}.backup"

# Copy new config
cp /mnt/data/Work/inteles-ro/windsurf-mcp-config.json "$WINDSURF_CONFIG"

# Restart Windsurf
```

### Testing in Windsurf

1. Open Windsurf
2. Open AI chat panel
3. Type: `"List my inteles.ro WordPress posts"`
4. Should return your posts

---

## 3. Codex CLI (OpenAI)

### Important: Codex CLI ≠ MCP

**Codex CLI** is OpenAI's code interpreter - it does NOT natively support MCP protocol.

### Workarounds for Codex

You have 3 options:

#### Option A: Use REST API Directly (Simplest)

Create a helper script for Codex to call:

**File: `~/bin/wp-inteles`**
```bash
#!/bin/bash
# WordPress API helper for inteles.ro

BASE_URL="https://inteles.ro/wp-json/wp/v2"
AUTH="baretrea:Yzix4308YGsRNLirTWJfdztM"

case "$1" in
  list)
    curl -s -u "$AUTH" "$BASE_URL/posts?per_page=${2:-10}" | jq .
    ;;
  get)
    curl -s -u "$AUTH" "$BASE_URL/posts/$2" | jq .
    ;;
  create)
    curl -s -u "$AUTH" -X POST "$BASE_URL/posts" \
      -H "Content-Type: application/json" \
      -d "{\"title\":\"$2\",\"content\":\"$3\",\"status\":\"draft\"}" | jq .
    ;;
  update)
    curl -s -u "$AUTH" -X POST "$BASE_URL/posts/$2" \
      -H "Content-Type: application/json" \
      -d "$3" | jq .
    ;;
  *)
    echo "Usage: wp-inteles {list|get|create|update} [args]"
    exit 1
    ;;
esac
```

**Setup:**
```bash
# Create the script
cat > ~/bin/wp-inteles << 'EOF'
[paste script above]
EOF

# Make executable
chmod +x ~/bin/wp-inteles

# Test it
wp-inteles list 5
```

**Then in Codex CLI:**
```
codex: "Use the wp-inteles command to list my posts"
codex: "Create a new draft post with wp-inteles create 'Title' 'Content'"
```

---

#### Option B: Python Wrapper (More Powerful)

Create a Python script Codex can import:

**File: `~/bin/wp_inteles.py`**
```python
#!/usr/bin/env python3
"""WordPress API wrapper for inteles.ro"""

import requests
from requests.auth import HTTPBasicAuth
import json
import sys

class IntelesWP:
    def __init__(self):
        self.base_url = "https://inteles.ro/wp-json/wp/v2"
        self.auth = HTTPBasicAuth("baretrea", "Yzix4308YGsRNLirTWJfdztM")

    def list_posts(self, per_page=10, page=1):
        """List posts"""
        url = f"{self.base_url}/posts"
        params = {"per_page": per_page, "page": page}
        response = requests.get(url, auth=self.auth, params=params)
        response.raise_for_status()
        return response.json()

    def get_post(self, post_id):
        """Get single post"""
        url = f"{self.base_url}/posts/{post_id}"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def create_post(self, title, content, status='draft'):
        """Create new post"""
        url = f"{self.base_url}/posts"
        data = {
            'title': title,
            'content': content,
            'status': status
        }
        response = requests.post(url, auth=self.auth, json=data)
        response.raise_for_status()
        return response.json()

    def update_post(self, post_id, **kwargs):
        """Update post fields"""
        url = f"{self.base_url}/posts/{post_id}"
        response = requests.post(url, auth=self.auth, json=kwargs)
        response.raise_for_status()
        return response.json()

    def search_posts(self, search_term):
        """Search posts by keyword"""
        url = f"{self.base_url}/posts"
        params = {"search": search_term, "per_page": 100}
        response = requests.get(url, auth=self.auth, params=params)
        response.raise_for_status()
        return response.json()

# CLI interface
if __name__ == "__main__":
    wp = IntelesWP()

    if len(sys.argv) < 2:
        print("Usage: wp_inteles.py {list|get|create|update|search} [args]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "list":
        posts = wp.list_posts(per_page=int(sys.argv[2]) if len(sys.argv) > 2 else 10)
        for post in posts:
            print(f"{post['id']}: {post['title']['rendered']}")

    elif cmd == "get" and len(sys.argv) > 2:
        post = wp.get_post(int(sys.argv[2]))
        print(json.dumps(post, indent=2))

    elif cmd == "create" and len(sys.argv) > 3:
        result = wp.create_post(sys.argv[2], sys.argv[3])
        print(f"Created post ID {result['id']}: {result['link']}")

    elif cmd == "search" and len(sys.argv) > 2:
        posts = wp.search_posts(sys.argv[2])
        print(f"Found {len(posts)} posts:")
        for post in posts:
            print(f"{post['id']}: {post['title']['rendered']}")

    else:
        print("Invalid command or missing arguments")
```

**Setup:**
```bash
# Create the script
cat > ~/bin/wp_inteles.py << 'EOF'
[paste script above]
EOF

# Make executable
chmod +x ~/bin/wp_inteles.py

# Install requests if needed
pip install requests

# Test it
python ~/bin/wp_inteles.py list 5
```

**Then in Codex CLI:**
```python
# Import the module
import sys
sys.path.append('/home/alin/bin')
from wp_inteles import IntelesWP

# Use it
wp = IntelesWP()
posts = wp.list_posts()
print(f"Found {len(posts)} posts")

# Create new post
wp.create_post("Test from Codex", "<p>This is a test</p>", status='draft')
```

---

#### Option C: Codex Config File (If Supported)

Some versions of Codex CLI support config files. Check documentation:

**Typical location:**
```
~/.codex/config.json
```

**Try adding:**
```json
{
  "tools": {
    "wordpress": {
      "type": "rest-api",
      "url": "https://inteles.ro/wp-json/wp/v2",
      "auth": {
        "username": "baretrea",
        "password": "Yzix4308YGsRNLirTWJfdztM"
      }
    }
  }
}
```

**Check if Codex supports this:**
```bash
codex --help | grep -i config
codex config --list
```

---

## Recommended Setup Summary

| Tool | Method | Complexity | Power |
|------|--------|-----------|-------|
| **Claude Desktop** | Native MCP | ✅ Easy | ⭐⭐⭐⭐⭐ |
| **Windsurf** | Native MCP | ⭐ Medium | ⭐⭐⭐⭐⭐ |
| **Codex CLI** | Python wrapper | ⭐⭐ Medium | ⭐⭐⭐⭐ |

### My Recommendation:

1. **Claude Desktop:** Use MCP (already done) ✅
2. **Windsurf:** Use MCP (copy config from `windsurf-mcp-config.json`)
3. **Codex CLI:** Use Python wrapper (Option B above)

This gives you consistent WordPress access across all tools.

---

## Testing Each Tool

### Claude Desktop
```
"List my inteles.ro posts"
```

### Windsurf
```
"Using the inteles-wordpress MCP, list my posts"
```

### Codex CLI
```python
from wp_inteles import IntelesWP
wp = IntelesWP()
posts = wp.list_posts()
```

---

## Unified Workflow Example

**Scenario:** Add affiliate links to death-related posts

### In Claude Desktop:
```
"Find all inteles.ro posts about death and list them"
```

### In Windsurf (writing code):
```
"Generate Python code that adds affiliate links to these posts using the MCP"
```

### In Codex CLI (automation):
```python
from wp_inteles import IntelesWP
wp = IntelesWP()

# Search for posts
posts = wp.search_posts("moarte")

# Update each one
for post in posts:
    content = post['content']['rendered']
    content += '<div>AFFILIATE LINK HTML</div>'
    wp.update_post(post['id'], content=content)
    print(f"Updated post {post['id']}")
```

---

## File Locations Reference

### Claude Desktop
```
~/.config/Claude/claude_desktop_config.json
```

### Windsurf
```
~/.codeium/windsurf/mcp_settings.json
OR
~/.config/Windsurf/User/globalStorage/mcp_settings.json
```

### Codex CLI
```
~/bin/wp_inteles.py  (custom script)
```

### Your Project
```
/mnt/data/Work/inteles-ro/
├── windsurf-mcp-config.json    ← Config for Windsurf
├── MULTI-TOOL-SETUP.md         ← This file
└── [other docs]
```

---

## Next Steps

1. **Claude Desktop:** ✅ Already working

2. **Windsurf:**
   ```bash
   # Find config location
   find ~ -name "mcp_settings.json" 2>/dev/null

   # Add inteles-wordpress block from windsurf-mcp-config.json
   # Restart Windsurf
   ```

3. **Codex CLI:**
   ```bash
   # Create Python wrapper
   cat > ~/bin/wp_inteles.py << 'EOF'
   [paste Python script from Option B]
   EOF

   chmod +x ~/bin/wp_inteles.py
   pip install requests

   # Test it
   python ~/bin/wp_inteles.py list 5
   ```

---

## Security Note

**All three tools share the same WordPress credentials:**
- Username: `baretrea`
- App Password: `Yzix4308YGsRNLirTWJfdztM`

**If compromised:**
1. Go to: https://inteles.ro/wp-admin → Users → Your Profile
2. Find "Application Passwords" section
3. Revoke the "mcp" password
4. Generate new one
5. Update all three configs

---

## Troubleshooting

### "Command not found" in Codex
Make sure `~/bin` is in your PATH:
```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### "Module not found" in Codex Python
```bash
pip install requests
# Or add to system path:
export PYTHONPATH="$HOME/bin:$PYTHONPATH"
```

### Windsurf MCP not working
1. Check file location is correct
2. Verify JSON syntax: `cat config.json | jq .`
3. Restart Windsurf completely
4. Check logs: Windsurf → Help → Toggle Developer Tools → Console

---

## Questions?

**Q: Can I use different passwords for each tool?**
A: Yes! Create separate Application Passwords in WordPress for each tool. Good for security.

**Q: Which tool should I use for what?**
A:
- **Claude Desktop:** Quick content edits, conversational interface
- **Windsurf:** Writing automation code, complex logic
- **Codex CLI:** Scripting, batch operations, terminal workflows

**Q: Can these run simultaneously?**
A: Yes! WordPress REST API handles concurrent connections.

**Q: What if I want to add BareTread too?**
A: Create another Application Password, add another MCP server block with BareTread's URL.

---

**Ready?** Pick one tool to set up first, test it, then move to the next.
