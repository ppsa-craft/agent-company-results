# tester-2 — cycle 5 lane log

```
nstance] stub at /data/.opencode/plugins (real events fire from /data/.opencode/plugin)
timestamp=2026-07-15T03:54:40.548Z level=INFO run=799a9d62 message="all LSPs are disabled"
timestamp=2026-07-15T03:54:40.554Z level=INFO run=799a9d62 message="all formatters are disabled"
timestamp=2026-07-15T03:54:40.554Z level=INFO run=799a9d62 message=init
[93m[1m! [0m agent "tester-2" is a subagent, not a primary agent. Falling back to default agent
timestamp=2026-07-15T03:54:42.446Z level=INFO run=799a9d62 message="event connected"
timestamp=2026-07-15T03:54:45.847Z level=INFO run=799a9d62 message=loop session.id=ses_09c315270ffeMg5IHQlGQ23X4i step=0
[0m
> build · deepseek-v4-flash-free
[0m
timestamp=2026-07-15T03:54:46.660Z level=INFO run=799a9d62 message=tracking hash=9425f1914d913c64875293a9a8036c773d64733a cwd=/data git=/home/node/.local/share/opencode/snapshot/8ac707f92920840a2e9a3889a8239df82cc1d3ae/9112fb2807d43dd27fe08840179971e4632a7f2b
timestamp=2026-07-15T03:54:46.689Z level=INFO run=799a9d62 message="shell tool using shell" shell=/usr/bin/bash
timestamp=2026-07-15T03:54:46.901Z level=INFO run=799a9d62 message=init count=27
timestamp=2026-07-15T03:54:47.692Z level=INFO run=799a9d62 message="watcher backend" directory=/data platform=linux backend=inotify
timestamp=2026-07-15T03:54:47.751Z level=INFO run=799a9d62 message="project copy refresh started" projectID=8ac707f92920840a2e9a3889a8239df82cc1d3ae
timestamp=2026-07-15T03:54:51.550Z level=INFO run=799a9d62 message="project copy refresh done" projectID=8ac707f92920840a2e9a3889a8239df82cc1d3ae updated=[] removed=[]
timestamp=2026-07-15T03:54:51.673Z level=INFO run=799a9d62 message="booting location services" directory=/data workspaceID=undefined
timestamp=2026-07-15T03:54:51.763Z level=INFO run=799a9d62 message=process session.id=ses_09c315270ffeMg5IHQlGQ23X4i messageID=msg_f63e9aaf1001A26FWTvf2u0JNd
timestamp=2026-07-15T03:54:51.773Z level=INFO run=799a9d62 message=stream providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_09c315270ffeMg5IHQlGQ23X4i small=false agent=build mode=primary
timestamp=2026-07-15T03:54:51.800Z level=INFO run=799a9d62 message="llm runtime selected" llm.runtime=ai-sdk llm.provider=ppsa llm.model=deepseek-v4-flash-free
timestamp=2026-07-15T03:55:03.202Z level=ERROR run=799a9d62 message="stream error" providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_09c315270ffeMg5IHQlGQ23X4i small=false agent=build mode=primary error.error="AI_APICallError: No available API keys across all providers — soonest key recovers in ~94s"
timestamp=2026-07-15T03:55:40.731Z level=INFO run=799a9d62 message=cleanup prune=7.days
timestamp=2026-07-15T03:56:37.223Z level=INFO run=799a9d62 message=stream providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_09c315270ffeMg5IHQlGQ23X4i small=false agent=build mode=primary
timestamp=2026-07-15T03:56:37.229Z level=INFO run=799a9d62 message="llm runtime selected" llm.runtime=ai-sdk llm.provider=ppsa llm.model=deepseek-v4-flash-free
timestamp=2026-07-15T03:56:43.082Z level=ERROR run=799a9d62 message="stream error" providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_09c315270ffeMg5IHQlGQ23X4i small=false agent=build mode=primary error.error="AI_APICallError: No available API keys across all providers — soonest key recovers in ~90s"
timestamp=2026-07-15T03:58:13.103Z level=INFO run=799a9d62 message=stream providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_09c315270ffeMg5IHQlGQ23X4i small=false agent=build mode=primary
timestamp=2026-07-15T03:58:13.156Z level=INFO run=799a9d62 message="llm runtime selected" llm.runtime=ai-sdk llm.provider=ppsa llm.model=deepseek-v4-flash-free
timestamp=2026-07-15T03:58:18.497Z level=ERROR run=799a9d62 message="stream error" providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_09c315270ffeMg5IHQlGQ23X4i small=false agent=build mode=primary error.error="AI_APICallError: No available API keys across all providers — soonest key recovers in ~396s"

```
