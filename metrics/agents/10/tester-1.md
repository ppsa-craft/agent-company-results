# tester-1 — cycle 10 lane log

```
 message="loading config from /home/node/.opencode/opencode.jsonc"
timestamp=2026-07-16T01:22:22.372Z level=INFO run=ae8bbc42 message=loading path=/home/node/.opencode/opencode.jsonc
[pixel-office:instance] stub at /data/.opencode/plugins (real events fire from /data/.opencode/plugin)
[pixel-office:instance] LIVE at /data/.opencode/plugin
[pixel-office:instance] stub at /home/node/.config/opencode/plugins (real events fire from /data/.opencode/plugin)
[pixel-office:instance] stub at /home/node/.config/opencode/plugin (real events fire from /data/.opencode/plugin)
[pixel-office:instance] stub at /home/node/.opencode/plugins (real events fire from /data/.opencode/plugin)
timestamp=2026-07-16T01:22:22.996Z level=INFO run=ae8bbc42 message="all LSPs are disabled"
timestamp=2026-07-16T01:22:23.001Z level=INFO run=ae8bbc42 message="all formatters are disabled"
timestamp=2026-07-16T01:22:23.002Z level=INFO run=ae8bbc42 message=init
[93m[1m! [0m agent "tester-1" is a subagent, not a primary agent. Falling back to default agent
timestamp=2026-07-16T01:22:24.881Z level=INFO run=ae8bbc42 message="event connected"
timestamp=2026-07-16T01:22:28.470Z level=INFO run=ae8bbc42 message=loop session.id=ses_09c315210ffeHyHyoGq8QmDGPT step=0
[0m
> build · deepseek-v4-flash-free
[0m
timestamp=2026-07-16T01:22:28.976Z level=WARN run=ae8bbc42 message="failed to add snapshot files" exitCode=128 stderr="fatal: pathspec ':(top,literal).orchestrator/agent-pids/71978' did not match any files\n"
timestamp=2026-07-16T01:22:29.048Z level=INFO run=ae8bbc42 message=tracking hash=a6ff908d7031126a2f32e0b6c93f1310d01ecffd cwd=/data git=/home/node/.local/share/opencode/snapshot/8ac707f92920840a2e9a3889a8239df82cc1d3ae/9112fb2807d43dd27fe08840179971e4632a7f2b
timestamp=2026-07-16T01:22:29.085Z level=INFO run=ae8bbc42 message="shell tool using shell" shell=/usr/bin/bash
timestamp=2026-07-16T01:22:29.279Z level=INFO run=ae8bbc42 message=init count=27
timestamp=2026-07-16T01:22:30.450Z level=INFO run=ae8bbc42 message="watcher backend" directory=/data platform=linux backend=inotify
timestamp=2026-07-16T01:22:30.672Z level=INFO run=ae8bbc42 message="project copy refresh started" projectID=8ac707f92920840a2e9a3889a8239df82cc1d3ae
timestamp=2026-07-16T01:22:33.795Z level=INFO run=ae8bbc42 message="project copy refresh done" projectID=8ac707f92920840a2e9a3889a8239df82cc1d3ae updated=[] removed=[]
timestamp=2026-07-16T01:22:33.872Z level=INFO run=ae8bbc42 message="booting location services" directory=/data workspaceID=undefined
timestamp=2026-07-16T01:22:33.916Z level=INFO run=ae8bbc42 message=process session.id=ses_09c315210ffeHyHyoGq8QmDGPT messageID=msg_f68849a4c001a07wWdhMJOr7Zl
timestamp=2026-07-16T01:22:33.947Z level=INFO run=ae8bbc42 message=stream providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_09c315210ffeHyHyoGq8QmDGPT small=false agent=build mode=primary
timestamp=2026-07-16T01:22:33.971Z level=INFO run=ae8bbc42 message="llm runtime selected" llm.runtime=ai-sdk llm.provider=ppsa llm.model=deepseek-v4-flash-free
timestamp=2026-07-16T01:22:52.014Z level=ERROR run=ae8bbc42 message="stream error" providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_09c315210ffeHyHyoGq8QmDGPT small=false agent=build mode=primary error.error="AI_APICallError: Error from provider (Console): Upstream request failed"
timestamp=2026-07-16T01:22:52.023Z level=ERROR run=ae8bbc42 message=process session.id=ses_09c315210ffeHyHyoGq8QmDGPT messageID=msg_f68849a4c001a07wWdhMJOr7Zl error="Error from provider (Console): Upstream request failed" stack="AI_APICallError: Error from provider (Console): Upstream request failed\n    at <anonymous> (/$bunfs/root/chunk-kr06e4aj.js:6:14582)\n    at async <anonymous> (/$bunfs/root/chunk-kr06e4aj.js:6:12790)\n    at processTicksAndRejections (native:7:39)"
[91m[1mError: [0mError from provider (Console): Upstream request failed
timestamp=2026-07-16T01:22:52.351Z level=INFO run=ae8bbc42 message="disposing instance" directory=/data

```
