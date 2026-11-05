# Identity & Goal: Wexxy PC Bot

## 1. What is this project?
At its core, **Wexxy PC Bot** is an omnipresent, highly modular Remote Control interface for Windows, operated entirely through Telegram and secure zero-config tunnels (Cloudflared). It combines native system controls, a fully local Voice AI pipeline (Whisper + Gemma + Qwen), and a low-latency, absolute-touch screen stream.

## 2. What is it trying to be? (The Vision)
**Wexxy is the "Manual Heavy-Lifting Support System" for Agentic AI.**

As agentic AI frameworks like **ClawX** and **OpenClaw** become more capable of navigating codebases and operating systems, they still inevitably hit roadblocks: complex graphical GUIs, CAPTCHAs, unhandled exceptions, or tasks requiring nuanced human judgment.

Wexxy is designed to be the ultimate **hybrid bridge** between the Autonomous Agent and the Human Operator. 

### Why this matters for Agentic AI:
- **The "Unblocker":** When an agent like ClawX gets stuck on a visual task or requires an environment variable to be manually configured through a finicky UI, the human can instantly drop in via Wexxy's **Absolute Touch Stream** from their phone, complete the GUI task in seconds, and let the agent resume its work.
- **The Fallback Actuator:** While agents are great at scripts, humans are great at spatial reasoning. Wexxy provides the raw, manual "hands and eyes" (mouse, keyboard, screen) as a reliable fallback layer.
- **Voice-to-Agent Command:** With the local Whisper and Gemma pipeline, Wexxy allows the human to dictate complex, messy voice instructions while walking around the room, translating human intent into clean API commands or text strings that the Agentic AI can then execute.

## 3. Core Pillars
1. **Always-On, Invisible Infrastructure:** Deployed as a background Windows Service (NSSM) so it is always ready to assist without cluttering the desktop environment.
2. **Absolute Precision:** The unified Touch & Stream UI isn't just a gimmick—it's built for speed. Tapping the stream maps exactly to the PC pixel, ensuring human intervention is lightning-fast and frictionless.
3. **Strictly Local Ecosystem:** No subscriptions, no cloud dependencies. By relying on `faster-whisper`, `llama.cpp`, and native Windows libraries (`pycaw`, `mss`), it remains secure, private, and indefinitely sustainable alongside other local AI agents.

## 4. The End Goal
Wexxy is not trying to be a smart assistant that does everything autonomously. Instead, it is the **perfect co-pilot tool**—providing the manual, remote, and sensory heavy-lifting capabilities that empower both the human operator and the primary AI agents (like ClawX) to seamlessly collaborate on the same machine.
