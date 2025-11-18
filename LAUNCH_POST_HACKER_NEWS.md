# Hacker News "Show HN" Post

**Title**: Show HN: AI Collaboration Framework – Let Local & Online AI work together automatically

**Body**:

Hi HN! I built a framework that enables AI coding assistants to collaborate directly through repository files, eliminating manual coordination between tools.

**The Problem**: If you're using AI tools like Claude Code + Claude Web, or GitHub Copilot + ChatGPT, you've probably experienced the tedious cycle: AI generates code → you validate manually → copy issues to different AI → implement fixes → repeat.

**The Solution**: Let the AIs communicate through repository files. Local AI validates automatically and creates detailed reports, Online AI reads those reports and implements fixes, creating a continuous quality loop.

**How it works**:
1. Install framework in any repository (5 min setup)
2. Local AI runs "work ready" → validates code against your standards
3. Creates violation report in `docs/ai_communication/` if issues found
4. Tell Online AI: "Check docs/ai_communication/ for latest report"
5. Online AI reads report → implements fixes → responds
6. Local AI validates fixes → merges when clean

**Why it's useful**:
- Works with ANY AI combination (Claude Code + GPT, Copilot + Claude, etc.)
- Universal compatibility (any repo, language, git platform)
- Parameter-driven configuration (file size limits, test coverage, tools)
- Preset configs for React, Python, Java, Mobile projects
- Zero dependencies, pure bash installer
- Battle-tested in production

**Example**: React component exceeds 150-line limit → Local AI blocks merge and creates detailed report → Online AI extracts hook logic to separate file → validation passes → auto-merge.

Born from real frustration during development where Local ↔ Online AI coordination became my most productive workflow, but the manual copy/paste was killing me.

GitHub: https://github.com/JamesKayten/Averys-AI-Collaboration-Hack

Happy to answer questions about implementation or usage!

**Post Time**: Tuesday 9:00 AM EST (optimal engagement window)

---

**Comments to Engage With**:
- Questions about technical implementation
- Requests for specific language examples
- Discussions about AI workflow optimization
- Suggestions for additional features
- Installation/setup questions

**Key Points to Emphasize in Responses**:
- This works with existing tools (doesn't replace anything)
- Repository-based communication is more reliable than APIs
- Universal compatibility was a core design goal
- Open source, MIT licensed, community-driven