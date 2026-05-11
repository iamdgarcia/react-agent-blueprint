# ReAct Agent Blueprint

A deployable template for a ReAct (Reasoning + Acting) Agent based on the Agentic AI for Beginners course. This template includes a working ReAct agent implementation with a simple web interface.

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://join.netlify.com/bxmfy8pxswau-w6zrwt)

## What is a ReAct Agent?

ReAct (Reasoning + Acting) Agents combine reasoning and acting in a loop:
1. **Reason** - Think about what to do next
2. **Act** - Execute an action
3. **Observe** - See the result
4. Repeat until the task is complete

This pattern is covered in Module 1.3 of the Agentic AI for Beginners course.

## Features

- 🤖 **Working ReAct Agent** - Implementation based on course teachings
- 💬 **Simple Chat Interface** - Interact with the agent through a web UI
- 🔧 **Visible Reasoning** - See the agent's thought process
- ⚡ **Netlify Functions** - Serverless backend for the agent logic
- 🎨 **Clean Interface** - Responsive design that works on mobile and desktop
- 📚 **Course-Aligned** - Directly implements concepts from Module 1.3
- 🚀 **One-Click Deploy** - Ready to deploy to Netlify with affiliate tracking

## How It Works

The ReAct agent follows this loop:
1. Given a user query, the agent **reasons** about what actions to take
2. It **acts** by executing available tools (like search, calculator, etc.)
3. It **observes** the results
4. It repeats until it has enough information to answer

## Included Implementation

- Python-based ReAct agent logic
- Simple REST API endpoint (`/.netlify/functions/react-agent`)
- HTML/JavaScript frontend for interaction
- Example tools: search, calculator, and weather (mock implementations)
- Conversation history tracking

## Local Development

To run this blueprint locally:

```bash
# Clone the repository
git clone https://github.com/your-username/react-agent-blueprint.git
cd react-agent-blueprint

# Install dependencies
pip install -r requirements.txt

# Start the server (for local testing)
python server.py

# Visit http://localhost:8000 to test
```

## Deployment Details

This blueprint uses:
- **Netlify Functions** for the agent logic (Python runtime)
- **Static frontend** served from the `public/` directory
- **Build command**: None (static site + functions)
- **Publish directory**: `public/`
- **Functions directory**: `netlify/functions/`

## Customization

After deployment, you can:
1. Modify the agent's system prompt in `netlify/functions/react-agent.py`
2. Add or modify tools in the `tools/` directory
3. Update the frontend in `public/` directory
4. Change the styling in `public/style.css`
5. Add more sophisticated tools (real APIs, etc.)

## Course Connection

This blueprint directly implements the ReAct pattern taught in:
- **Module 1.3: The ReAct Pattern**
- Shows how to combine LLMs with tool use
- Demonstrates the reasoning-acting-observing loop
- Provides a foundation for more complex agents

## Extending This Blueprint

You can extend this to:
- Add real API integrations (weather, search, etc.)
- Implement memory for conversation context
- Add more sophisticated reasoning patterns
- Create specialized ReAct agents for specific domains
- Build upon it to create Planning, Reflective, or Router agents

## Support

For issues or questions:
- Refer to the course materials in tlc_agents_training and tlc_course
- Check Netlify Functions documentation: https://docs.netlify.com/functions/
- Review the original ReAct agent implementation concepts

---
*Built with ❤️ for The Learning Curve community. Deploy using your affiliate link to support continued development of free AI education resources.*