# dev — cycle 25 lane log

```
node/.opencode/opencode.json
timestamp=2026-08-02T04:52:56.300Z level=DEBUG run=8263e381 message="loading config from /home/node/.opencode/opencode.jsonc"
timestamp=2026-08-02T04:52:56.300Z level=INFO run=8263e381 message=loading path=/home/node/.opencode/opencode.jsonc
[pixel-office:instance] stub at /home/node/.config/opencode/plugin (real events fire from /data/.opencode/plugin)
[pixel-office:instance] LIVE at /data/.opencode/plugin
[pixel-office:instance] stub at /home/node/.config/opencode/plugins (real events fire from /data/.opencode/plugin)
[pixel-office:instance] stub at /home/node/.opencode/plugins (real events fire from /data/.opencode/plugin)
[pixel-office:instance] stub at /data/.opencode/plugins (real events fire from /data/.opencode/plugin)
timestamp=2026-08-02T04:52:56.783Z level=INFO run=8263e381 message="all LSPs are disabled"
timestamp=2026-08-02T04:52:56.847Z level=INFO run=8263e381 message="all formatters are disabled"
timestamp=2026-08-02T04:52:56.848Z level=INFO run=8263e381 message=init
[93m[1m! [0m agent "dev" is a subagent, not a primary agent. Falling back to default agent
timestamp=2026-08-02T04:52:58.767Z level=INFO run=8263e381 message="event connected"
timestamp=2026-08-02T04:53:02.293Z level=INFO run=8263e381 message=loop session.id=ses_03f99234cffe91CS6p3O9hODz7 step=0
timestamp=2026-08-02T04:53:02.455Z level=INFO run=8263e381 message="shell tool using shell" shell=/usr/bin/bash
timestamp=2026-08-02T04:53:02.594Z level=INFO run=8263e381 message=init count=48
[0m
> build · deepseek-v4-flash-free
[0m
timestamp=2026-08-02T04:53:03.663Z level=INFO run=8263e381 message="watcher backend" directory=/data platform=linux backend=inotify
timestamp=2026-08-02T04:53:03.683Z level=INFO run=8263e381 message="project copy refresh started" projectID=global
timestamp=2026-08-02T04:53:03.754Z level=INFO run=8263e381 message="project copy refresh done" projectID=global updated=[] removed=[]
timestamp=2026-08-02T04:53:08.748Z level=INFO run=8263e381 message="booting location services" directory=/data workspaceID=undefined
timestamp=2026-08-02T04:53:09.768Z level=INFO run=8263e381 message=process session.id=ses_03f99234cffe91CS6p3O9hODz7 messageID=msg_fc0d17d14001SUY6uvjvJtuUVc
timestamp=2026-08-02T04:53:09.774Z level=INFO run=8263e381 message=stream providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_03f99234cffe91CS6p3O9hODz7 small=false agent=build mode=primary
timestamp=2026-08-02T04:53:09.847Z level=INFO run=8263e381 message="llm runtime selected" llm.runtime=ai-sdk llm.provider=ppsa llm.model=deepseek-v4-flash-free
timestamp=2026-08-02T04:53:17.077Z level=ERROR run=8263e381 message="stream error" providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_03f99234cffe91CS6p3O9hODz7 small=false agent=build mode=primary error.error="AI_APICallError: Error from provider (Console): Upstream request failed: [400] Provider returned error"
timestamp=2026-08-02T04:53:17.089Z level=ERROR run=8263e381 message=process session.id=ses_03f99234cffe91CS6p3O9hODz7 messageID=msg_fc0d17d14001SUY6uvjvJtuUVc error="Error from provider (Console): Upstream request failed: [400] Provider returned error" stack="AI_APICallError: Error from provider (Console): Upstream request failed: [400] Provider returned error\n    at <anonymous> (/$bunfs/root/chunk-kr06e4aj.js:6:14582)\n    at async <anonymous> (/$bunfs/root/chunk-kr06e4aj.js:6:12790)\n    at processTicksAndRejections (native:7:39)"
[91m[1mError: [0mError from provider (Console): Upstream request failed: [400] Provider returned error
timestamp=2026-08-02T04:53:17.132Z level=INFO run=8263e381 message="disposing instance" directory=/data
timestamp=2026-08-02T04:53:17.173Z level=INFO run=8263e381 message=loading path=/data/opencode.json
timestamp=2026-08-02T04:53:17.183Z level=DEBUG run=8263e381 message="loading config from /data/.opencode/opencode.json"
timestamp=2026-08-02T04:53:17.184Z level=INFO run=8263e381 message=loading path=/data/.opencode/opencode.json

```
