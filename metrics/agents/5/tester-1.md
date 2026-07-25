# tester-1 — cycle 5 lane log

```
ce] stub at /home/node/.opencode/plugins (real events fire from /data/.opencode/plugin)
timestamp=2026-07-15T03:54:40.780Z level=INFO run=d5e91d3e message="all LSPs are disabled"
timestamp=2026-07-15T03:54:40.785Z level=INFO run=d5e91d3e message="all formatters are disabled"
timestamp=2026-07-15T03:54:40.786Z level=INFO run=d5e91d3e message=init
[93m[1m! [0m agent "tester-1" is a subagent, not a primary agent. Falling back to default agent
timestamp=2026-07-15T03:54:43.271Z level=INFO run=d5e91d3e message="event connected"
timestamp=2026-07-15T03:54:46.282Z level=INFO run=d5e91d3e message=loop session.id=ses_09c315210ffeHyHyoGq8QmDGPT step=0
[0m
> build · deepseek-v4-flash-free
[0m
timestamp=2026-07-15T03:54:47.051Z level=INFO run=d5e91d3e message=tracking hash=9425f1914d913c64875293a9a8036c773d64733a cwd=/data git=/home/node/.local/share/opencode/snapshot/8ac707f92920840a2e9a3889a8239df82cc1d3ae/9112fb2807d43dd27fe08840179971e4632a7f2b
timestamp=2026-07-15T03:54:47.071Z level=INFO run=d5e91d3e message="shell tool using shell" shell=/usr/bin/bash
timestamp=2026-07-15T03:54:47.164Z level=INFO run=d5e91d3e message=init count=27
timestamp=2026-07-15T03:54:48.152Z level=INFO run=d5e91d3e message="watcher backend" directory=/data platform=linux backend=inotify
timestamp=2026-07-15T03:54:48.179Z level=INFO run=d5e91d3e message="project copy refresh started" projectID=8ac707f92920840a2e9a3889a8239df82cc1d3ae
timestamp=2026-07-15T03:54:51.758Z level=INFO run=d5e91d3e message="project copy refresh done" projectID=8ac707f92920840a2e9a3889a8239df82cc1d3ae updated=[] removed=[]
timestamp=2026-07-15T03:54:51.802Z level=INFO run=d5e91d3e message="booting location services" directory=/data workspaceID=undefined
timestamp=2026-07-15T03:54:51.975Z level=INFO run=d5e91d3e message=process session.id=ses_09c315210ffeHyHyoGq8QmDGPT messageID=msg_f63e9acd9001n5PsDz3uea2TO7
timestamp=2026-07-15T03:54:51.982Z level=INFO run=d5e91d3e message=stream providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_09c315210ffeHyHyoGq8QmDGPT small=false agent=build mode=primary
timestamp=2026-07-15T03:54:52.052Z level=INFO run=d5e91d3e message="llm runtime selected" llm.runtime=ai-sdk llm.provider=ppsa llm.model=deepseek-v4-flash-free
timestamp=2026-07-15T03:55:03.632Z level=ERROR run=d5e91d3e message="stream error" providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_09c315210ffeHyHyoGq8QmDGPT small=false agent=build mode=primary error.error="AI_APICallError: No available API keys across all providers — soonest key recovers in ~94s"
timestamp=2026-07-15T03:55:41.477Z level=INFO run=d5e91d3e message=cleanup prune=7.days
timestamp=2026-07-15T03:56:37.652Z level=INFO run=d5e91d3e message=stream providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_09c315210ffeHyHyoGq8QmDGPT small=false agent=build mode=primary
timestamp=2026-07-15T03:56:37.661Z level=INFO run=d5e91d3e message="llm runtime selected" llm.runtime=ai-sdk llm.provider=ppsa llm.model=deepseek-v4-flash-free
timestamp=2026-07-15T03:56:42.432Z level=ERROR run=d5e91d3e message="stream error" providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_09c315210ffeHyHyoGq8QmDGPT small=false agent=build mode=primary error.error="AI_APICallError: No available API keys across all providers — soonest key recovers in ~91s"
timestamp=2026-07-15T03:58:13.441Z level=INFO run=d5e91d3e message=stream providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_09c315210ffeHyHyoGq8QmDGPT small=false agent=build mode=primary
timestamp=2026-07-15T03:58:13.450Z level=INFO run=d5e91d3e message="llm runtime selected" llm.runtime=ai-sdk llm.provider=ppsa llm.model=deepseek-v4-flash-free
timestamp=2026-07-15T03:58:18.501Z level=ERROR run=d5e91d3e message="stream error" providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_09c315210ffeHyHyoGq8QmDGPT small=false agent=build mode=primary error.error="AI_APICallError: No available API keys across all providers — soonest key recovers in ~396s"

```
