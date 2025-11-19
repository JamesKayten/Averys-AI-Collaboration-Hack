#!/usr/bin/env python3
"""
AI Framework Command Manager - Web Interface
Access via browser: http://localhost:5555
"""

from flask import Flask, render_template_string, request, jsonify
from pathlib import Path
import json

app = Flask(__name__)

COMMANDS_DIR = Path.home() / "AI-Collaboration-Management" / ".claude" / "commands"
COMMANDS_DIR.mkdir(parents=True, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Command Manager</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 2em; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 1.1em; }
        .content { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; padding: 30px; }
        .panel {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .panel h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        input, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        input:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        textarea { resize: vertical; min-height: 120px; font-family: monospace; }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        button:active { transform: translateY(0); }
        .command-list {
            max-height: 400px;
            overflow-y: auto;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 10px;
        }
        .command-item {
            padding: 15px;
            margin-bottom: 10px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .command-item:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .command-item h3 { color: #667eea; margin-bottom: 5px; }
        .command-item p { color: #666; font-size: 0.9em; }
        .delete-btn {
            background: #ef4444;
            padding: 8px 15px;
            font-size: 0.9em;
            width: auto;
            margin-top: 10px;
        }
        .delete-btn:hover { background: #dc2626; }
        .success {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #10b981;
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            display: none;
            animation: slideIn 0.3s;
        }
        @keyframes slideIn {
            from { transform: translateX(400px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @media (max-width: 768px) {
            .content { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 AI Command Manager</h1>
            <p>Create voice commands - no code, no terminal required</p>
        </div>

        <div class="content">
            <div class="panel">
                <h2>Create New Command</h2>
                <form id="commandForm">
                    <div class="form-group">
                        <label>What phrase to say:</label>
                        <input type="text" id="phrase" placeholder="e.g., shit's ready" required>
                    </div>

                    <div class="form-group">
                        <label>What it should do:</label>
                        <textarea id="action" placeholder="e.g., ./verify_test.sh&#10;&#10;or&#10;&#10;Run all tests and report results" required></textarea>
                    </div>

                    <div class="form-group">
                        <label>Description (optional):</label>
                        <input type="text" id="description" placeholder="e.g., Verify framework test">
                    </div>

                    <div class="form-group">
                        <label>Additional phrases (comma separated):</label>
                        <input type="text" id="aliases" placeholder="e.g., check it, verify this, test ready">
                    </div>

                    <button type="submit">CREATE COMMAND</button>
                </form>
            </div>

            <div class="panel">
                <h2>Your Commands</h2>
                <div class="command-list" id="commandList">
                    <p style="text-align: center; color: #999;">Loading...</p>
                </div>
            </div>
        </div>
    </div>

    <div class="success" id="successMsg"></div>

    <script>
        function showSuccess(msg) {
            const el = document.getElementById('successMsg');
            el.textContent = msg;
            el.style.display = 'block';
            setTimeout(() => el.style.display = 'none', 3000);
        }

        function loadCommands() {
            fetch('/api/commands')
                .then(r => r.json())
                .then(commands => {
                    const list = document.getElementById('commandList');
                    if (commands.length === 0) {
                        list.innerHTML = '<p style="text-align: center; color: #999;">No commands yet. Create one!</p>';
                        return;
                    }
                    list.innerHTML = commands.map(cmd => `
                        <div class="command-item">
                            <h3>"${cmd.phrase}"</h3>
                            <p>${cmd.description}</p>
                            <button class="delete-btn" onclick="deleteCommand('${cmd.filename}')">Delete</button>
                        </div>
                    `).join('');
                });
        }

        document.getElementById('commandForm').addEventListener('submit', (e) => {
            e.preventDefault();

            const data = {
                phrase: document.getElementById('phrase').value,
                action: document.getElementById('action').value,
                description: document.getElementById('description').value,
                aliases: document.getElementById('aliases').value
            };

            fetch('/api/commands', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(r => r.json())
            .then(result => {
                showSuccess(`Command created! Say: "${data.phrase}"`);
                document.getElementById('commandForm').reset();
                loadCommands();
            })
            .catch(err => alert('Error creating command'));
        });

        function deleteCommand(filename) {
            if (!confirm('Delete this command?')) return;

            fetch(`/api/commands/${filename}`, {method: 'DELETE'})
                .then(() => {
                    showSuccess('Command deleted');
                    loadCommands();
                });
        }

        loadCommands();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/commands', methods=['GET'])
def get_commands():
    commands = []
    for filepath in COMMANDS_DIR.glob("*.md"):
        content = filepath.read_text()
        lines = content.split('\n')

        # Parse frontmatter
        desc = "Custom command"
        phrase = filepath.stem.replace('-', ' ')

        for line in lines:
            if line.startswith('description:'):
                desc = line.split(':', 1)[1].strip()
            elif line.startswith('aliases:'):
                try:
                    aliases = json.loads(line.split(':', 1)[1].strip())
                    if aliases:
                        phrase = aliases[0]
                except:
                    pass

        commands.append({
            'filename': filepath.stem,
            'phrase': phrase,
            'description': desc
        })

    return jsonify(commands)

@app.route('/api/commands', methods=['POST'])
def create_command():
    data = request.json
    phrase = data['phrase'].strip()
    action = data['action'].strip()
    desc = data.get('description', 'Custom command').strip()
    aliases = data.get('aliases', '').strip()

    # Parse aliases
    all_phrases = [phrase]
    if aliases:
        all_phrases.extend([a.strip() for a in aliases.split(',') if a.strip()])

    # Generate filename
    filename = phrase.lower().replace("'", "").replace(" ", "-")
    filename = ''.join(c for c in filename if c.isalnum() or c == '-')
    filepath = COMMANDS_DIR / f"{filename}.md"

    # Create command file
    content = f"""---
description: {desc}
aliases: {json.dumps(all_phrases)}
---

{action}
"""

    filepath.write_text(content)
    return jsonify({'success': True, 'filename': filename})

@app.route('/api/commands/<filename>', methods=['DELETE'])
def delete_command(filename):
    filepath = COMMANDS_DIR / f"{filename}.md"
    if filepath.exists():
        filepath.unlink()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

if __name__ == '__main__':
    print("\n🎯 AI Command Manager")
    print("=" * 50)
    print("Open your browser to: http://localhost:5555")
    print("=" * 50)
    print("\nPress Ctrl+C to stop\n")
    app.run(host='0.0.0.0', port=5555, debug=False)
