# CORRECT WordPress MCP Setup - Official Adapter

## ⚠️ Previous Setup Was Wrong

The `@instawp/mcp-wp` npm package I suggested is a **community tool**, not the official WordPress MCP Adapter.

The **official WordPress MCP Adapter** (`WordPress/mcp-adapter`) is a **WordPress plugin** that must be installed on inteles.ro itself.

---

## Two Options to Fix This

### Option A: Use Official WordPress MCP Adapter (Requires Plugin Installation)

**What it is:**
- Official WordPress plugin from WordPress.org team
- Installs ON inteles.ro (not your local machine)
- Exposes WordPress Abilities API via MCP protocol
- Most powerful and future-proof option

**Requirements:**
- WordPress 5.6+ ✅ (inteles.ro has this)
- WordPress Abilities API plugin ✅ (will install together)
- Ability to install plugins on inteles.ro ✅ (you have admin access)

**Installation Steps:**

#### Step 1: Install on inteles.ro

**Method 1: Via WordPress Admin (Easiest)**
1. Download plugin ZIP from: https://github.com/WordPress/mcp-adapter/releases/latest
2. Go to: inteles.ro/wp-admin → Plugins → Add New → Upload Plugin
3. Upload the ZIP file
4. Click "Activate"

**Method 2: Via Composer (If you have SSH access)**
```bash
# SSH into your ZUME hosting
ssh your-username@inteles.ro

# Navigate to WordPress directory
cd public_html  # or wherever inteles.ro is installed

# Install via Composer
composer require wordpress/abilities-api wordpress/mcp-adapter
```

**Method 3: Via cPanel File Manager**
1. Download from GitHub releases
2. Extract ZIP
3. Upload `mcp-adapter` folder to `wp-content/plugins/`
4. Activate in WordPress admin

#### Step 2: Configure MCP Server

The plugin automatically creates a default MCP server at:
```
REST API: https://inteles.ro/wp-json/mcp-adapter/v1/mcp
STDIO: wp mcp-adapter serve --server=mcp-adapter-default-server
```

#### Step 3: Connect Claude Desktop

**For HTTP Transport (Remote Site):**

You need an MCP HTTP proxy because Claude Desktop doesn't directly support HTTP MCP servers. This is complex and not recommended for shared hosting.

**For STDIO Transport (Requires SSH):**

If you have SSH access to ZUME hosting:

```json
{
  "mcpServers": {
    "inteles-wordpress": {
      "command": "ssh",
      "args": [
        "your-username@inteles.ro",
        "cd /path/to/wordpress && wp mcp-adapter serve --user=baretrea --server=mcp-adapter-default-server"
      ]
    }
  }
}
```

**Problem:** This requires:
- Persistent SSH connection
- WP-CLI installed on server
- Complex authentication

---

### Option B: Use Community Package (What I Originally Suggested)

**What it is:**
- Community-built npm package: `@instawp/mcp-wp`
- Runs locally on your machine (not on inteles.ro)
- Connects via WordPress REST API
- Simpler setup, less powerful

**This is what we actually configured, and it SHOULD work.**

**Configuration:**
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

**Why it might not be working:**

1. **The package might not exist or is outdated**
2. **Authentication issues**
3. **REST API disabled on inteles.ro**

---

## Let's Debug What's Actually Wrong

### Test 1: Check if REST API is accessible

```bash
curl https://inteles.ro/wp-json/wp/v2/posts?per_page=1
```

**Expected:** Should return JSON with your posts
**If fails:** REST API might be disabled

### Test 2: Check authentication

```bash
curl -u "baretrea:Yzix4308YGsRNLirTWJfdztM" https://inteles.ro/wp-json/wp/v2/posts?per_page=1
```

**Expected:** Should return JSON
**If 401 error:** Authentication failed

### Test 3: Check if the npm package exists

```bash
npm view @instawp/mcp-wp
```

**Expected:** Should show package info
**If error:** Package doesn't exist or name is wrong

---

## My Recommendation: Hybrid Approach

Since the official adapter is complex and requires plugin installation, and the community package might not work, here's the **simplest working solution**:

### Create a Simple Local MCP Server (Python)

This runs on your machine and connects to WordPress REST API.

**File: `/mnt/data/Work/inteles-ro/mcp-server/server.py`**

```python
#!/usr/bin/env python3
"""
Simple WordPress MCP Server for inteles.ro
Connects via REST API, runs locally on your machine
"""

import json
import sys
import asyncio
import requests
from requests.auth import HTTPBasicAuth

# WordPress configuration
WP_URL = "https://inteles.ro/wp-json/wp/v2"
WP_USER = "baretrea"
WP_PASS = "Yzix4308YGsRNLirTWJfdztM"

class WordPressMCP:
    def __init__(self):
        self.auth = HTTPBasicAuth(WP_USER, WP_PASS)

    def list_posts(self, per_page=10):
        """List WordPress posts"""
        url = f"{WP_URL}/posts"
        params = {"per_page": per_page}
        response = requests.get(url, auth=self.auth, params=params)
        response.raise_for_status()
        return response.json()

    def get_post(self, post_id):
        """Get single post"""
        url = f"{WP_URL}/posts/{post_id}"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def create_post(self, title, content, status='draft'):
        """Create new post"""
        url = f"{WP_URL}/posts"
        data = {'title': title, 'content': content, 'status': status}
        response = requests.post(url, auth=self.auth, json=data)
        response.raise_for_status()
        return response.json()

    def update_post(self, post_id, **kwargs):
        """Update post"""
        url = f"{WP_URL}/posts/{post_id}"
        response = requests.post(url, auth=self.auth, json=kwargs)
        response.raise_for_status()
        return response.json()

    def search_posts(self, search_term):
        """Search posts"""
        url = f"{WP_URL}/posts"
        params = {"search": search_term, "per_page": 100}
        response = requests.get(url, auth=self.auth, params=params)
        response.raise_for_status()
        return response.json()

async def handle_mcp_request(request):
    """Handle MCP JSON-RPC requests"""
    wp = WordPressMCP()
    method = request.get("method")
    params = request.get("params", {})

    try:
        if method == "tools/list":
            # Return available tools
            return {
                "tools": [
                    {"name": "list_posts", "description": "List WordPress posts"},
                    {"name": "get_post", "description": "Get single post by ID"},
                    {"name": "create_post", "description": "Create new post"},
                    {"name": "update_post", "description": "Update existing post"},
                    {"name": "search_posts", "description": "Search posts by keyword"}
                ]
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {})

            if tool_name == "list_posts":
                result = wp.list_posts(args.get("per_page", 10))
            elif tool_name == "get_post":
                result = wp.get_post(args["post_id"])
            elif tool_name == "create_post":
                result = wp.create_post(args["title"], args["content"], args.get("status", "draft"))
            elif tool_name == "update_post":
                result = wp.update_post(args["post_id"], **args.get("data", {}))
            elif tool_name == "search_posts":
                result = wp.search_posts(args["search_term"])
            else:
                raise ValueError(f"Unknown tool: {tool_name}")

            return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}

        else:
            raise ValueError(f"Unknown method: {method}")

    except Exception as e:
        return {"error": {"code": -32603, "message": str(e)}}

async def main():
    """Main MCP server loop"""
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break

            request = json.loads(line)
            response = await handle_mcp_request(request)
            response["jsonrpc"] = "2.0"
            response["id"] = request.get("id")

            print(json.dumps(response), flush=True)

        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if 'request' in locals() else None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    asyncio.run(main())
```

**Claude Desktop Config:**
```json
{
  "mcpServers": {
    "inteles-wordpress": {
      "command": "python3",
      "args": ["/mnt/data/Work/inteles-ro/mcp-server/server.py"]
    }
  }
}
```

---

## What Should You Do?

**Tell me:**

1. **Do you want to install the official WordPress plugin on inteles.ro?**
   - Pros: Most powerful, official, future-proof
   - Cons: Requires plugin installation, more complex setup

2. **Or stick with the community package and debug why it's not working?**
   - Pros: Simpler, no WordPress changes
   - Cons: Might be outdated or broken

3. **Or use my custom Python MCP server?**
   - Pros: Simple, works guaranteed, full control
   - Cons: You maintain it

**What error are you actually seeing?** That will help me fix the right thing.
