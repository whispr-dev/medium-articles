# The Dragon in the Welsh Countryside

### Or: How We Resurrected a Distributed Beacon Network by Refusing to Believe Anything Was Actually Broken

---

There is a particular kind of engineering satisfaction that comes from discovering that the problem you have been asked to solve is not the real problem. The real problem is usually three layers down, architecturally embarrassing, and has been running in production for fifty days while nobody noticed.

This is an account of how my collaborator wofl and I spent a day restoring the Litehaus — a distributed beacon network spanning four cloud relays and one physical node in Wales — to its intended architecture. We fixed three bugs in C++ source code that had been shipping for months. We evicted a ghost systemd service that had been respawning itself since March. We built two new JSON endpoints that now answer to the entire internet. And along the way, we learned something genuine about the difference between infrastructure that *runs* and infrastructure that *tells the truth*.

If you want to skip to the working system, it is here:

- **Dashboard**: [https://mars.litehaus.online](https://mars.litehaus.online)
- **Identity probe**: `curl https://mars.litehaus.online/ping`
- **Live beacon payload**: `curl https://mars.litehaus.online/beacon`

The dashboard shows five nodes — New York, London, Sydney, Singapore, and Mars — each beaconing once per second, their live feeds scrolling in a terminal aesthetic that would not look out of place in a 1990s cyberpunk film. Mars is the one with the dragon. It is also, as we shall see, the one with all the responsibility.

## What Litehaus Is, In Plain Terms

Litehaus is a federated beacon network. Five machines, geographically distributed, each continuously broadcasting their state — uptime, system load, time-source discipline, network reachability — to each other and to a public dashboard. Think of it as a distributed heartbeat monitor that happens to be built by someone who takes the *heart* part quite seriously.

The architecture, before we touched it, looked like this on paper:

- Four cloud nodes running on DigitalOcean droplets in NYC, London, Sydney, and Singapore, each running a compiled C++ process called `litehaus-core` that emits a beacon once per second as a UDP packet
- One physical node, Mars, running on an Intel NUC in a house in Wales, intended to be the *master* of the network — the authoritative source, not merely another relay
- A Node.js bridge that receives UDP beacons and forwards them to connected web browsers as WebSocket messages
- A public dashboard that renders the whole thing with the appropriate amount of dragons

What the architecture looked like *in practice*, however, was rather less coherent. Three different C++ codebases had been written over the preceding year. One, the "v1" architecture, had split the beacon emitter and the WebSocket stream into two clean binaries, with proper systemd units and configuration-file parsing. Another, "v2," had collapsed everything into a single monolith with a JavaScript bridge compensating for the parts the monolith didn't do. A third, "v3," was a Mars-specific rewrite that had been started and abandoned, leaving orphaned files scattered across the filesystem like archaeological strata.

The v1 architecture was what was meant to be running. The v2 monolith was what was actually running. And somewhere, quietly, unaccounted for in any process list we had bothered to check, a Node.js process from v3 had been listening on port 9875 for fifty days.

This is how things begin.

## The First Layer of Untruth

The Mars panel on the dashboard, before we started, displayed the node as *Offline*. This was puzzling, because the NUC was plainly running, serving HTTP through a reverse-SSH tunnel, and producing logs that indicated healthy activity. The node was clearly alive; the dashboard was clearly insisting otherwise.

The initial hypothesis — the one any reasonable person would form — was that the monolith was broken. Kill it, replace it with the proper v1 binary, and the dashboard would come to life.

We did replace the monolith. But it did not come to life. What came instead was a cascade of small revelations, each of which felt like it should be the last one but was not.

The first revelation concerned the configuration file. The v1 `litehaus-core` reads a standard INI-style config at `/etc/litehaus/core.conf`, specifying things like beacon targets (which cloud relays to send to), beacon intervals, and probe endpoints. We dutifully edited this file to include Mars's own loopback address so the node would beacon to itself and appear on its own dashboard.

It did not.

A careful `strace` of the running process revealed the awkward truth: the config file's `beacon_targets` directive was being read, parsed, and then completely ignored. The C++ parser had a clean hand-written branch for every configuration key it cared about — `fastping_url`, `beacon_interval_ms`, and so on — but the `beacon_targets` key was simply not in the list of keys it recognised. The `ConfigLoader::loadFromFile()` function reached the end of its `if/else if` chain without matching, shrugged, and fell through to the hardcoded defaults compiled into the binary.

This is not a bug one notices by reading logs. The program does not complain. It does not warn. It simply uses different values than the ones you asked for, and the discrepancy is invisible unless you happen to `strace` the network syscalls and compare destinations against your expectations. Past-someone had clearly intended to implement this parser, had written the infrastructure for it (the field existed on the `CoreConfig` struct, correctly typed as a vector of host/port pairs), and had then neglected to write the fifteen lines of parsing code that would have made it functional.

We wrote those fifteen lines.

```cpp
else if (key == "beacon_targets") {
    cfg.beacon_targets.clear();
    std::stringstream ss(value);
    std::string item;
    while (std::getline(ss, item, ',')) {
        size_t s = item.find_first_not_of(" \t");
        size_t e = item.find_last_not_of(" \t");
        if (s == std::string::npos) continue;
        item = item.substr(s, e - s + 1);
        size_t colon = item.rfind(':');
        if (colon == std::string::npos) continue;
        std::string host = item.substr(0, colon);
        uint16_t port;
        try {
            port = static_cast<uint16_t>(std::stoul(item.substr(colon + 1)));
        } catch (...) {
            continue;
        }
        cfg.beacon_targets.emplace_back(host, port);
    }
}
```

It is not beautiful code. It is, however, *present* code, which is a material improvement over what was there before.

## The Second Layer: The Kernel Has Opinions

With the parser fixed, rebuilt, and the new binary installed, we expected to watch five destinations receive beacons — four cloud relays and Mars's own loopback. What we saw instead was four successful UDP sends and one repeated `EACCES (Permission denied)` on a broadcast to `255.255.255.255:9877`.

The broadcast was intended, deliberately, by the original author. Litehaus has architectural ambitions that include a "WiFi halo" — a local wireless access point on Mars, eventually, for LAN-local emergency access to the dashboard when the broader internet is unavailable. The broadcast to `255.255.255.255` was meant to be picked up by clients on that hypothetical network.

The problem was that the author had created the UDP socket with `socket(AF_INET, SOCK_DGRAM, 0)` — correct — and had then used it to broadcast — incorrect. Linux requires a socket to be explicitly *given permission* to broadcast before it will allow you to address `255.255.255.255` from it. This is done with a single system call:

```cpp
int broadcast_enable = 1;
setsockopt(sock_, SOL_SOCKET, SO_BROADCAST,
           &broadcast_enable, sizeof(broadcast_enable));
```

Four lines, including the comment. This had been missing for the entire lifetime of the v1 codebase. Every beacon cycle, the process had attempted to broadcast, failed with `EACCES`, and carried on. The error went to stderr, stderr went to the systemd journal, and nobody had read the journal recently enough to notice.

We added the four lines. The broadcast began succeeding. This changed nothing about the dashboard — there is still no WiFi halo, and so nothing is listening for the broadcast — but the error messages stopped, which is a kind of progress all its own.

## The Third Layer: Hardware That Isn't There

With two source-level fixes landed, we started the service under systemd for the first time. It printed its banner — a pleasing ASCII-art castle — and then stopped. For twenty seconds. Thirty. A minute.

The process was not dead. It was alive, and it was holding a pipe open to a child process called `gpspipe`, which was attempting to read data from a GPS-disciplined rubidium oscillator that was not yet physically connected to the NUC. `gpspipe` was blocking indefinitely, waiting for data that would never arrive. Our main process was blocking on `gpspipe`. Nothing was happening at all.

This is the kind of bug that only manifests when you run code in an environment slightly different from the one where it was written. On the author's workstation, `gpspipe` probably behaved differently — timing out cleanly, perhaps, or simply being a harmless no-op because something on the path differed. Under systemd, with its privilege-dropped execution context and its lack of a controlling terminal, the same binary behaved differently: the signal-handling paths were subtly altered, and `gpspipe` became deaf to the usual termination signals.

The fix was to wrap every external hardware-probing command in a `timeout` invocation with aggressive kill semantics. Not just `timeout 2 gpspipe …`, which sends `SIGTERM` after two seconds — but `timeout --kill-after=1 2 gpspipe …`, which sends `SIGTERM` after two seconds and then `SIGKILL` one second later if the process has not complied. `SIGKILL` cannot be ignored by anything short of a zombie, and even zombies are somewhat well-behaved about it.

We applied this fix to eight separate `popen()` calls in the source: the GPS probe, the chrony time-daemon query, the UPS status readout, the APC battery interrogation, the sensor thermometry, and one or two others I have mercifully forgotten. None of the hardware they probe is currently attached to Mars; all of them would hang. After the fix, none of them did. Mars booted past its banner. The dashboard lit up. The dragon, finally, was Online.

## The Ghost in the Systemd Slice

Having achieved what we had set out to achieve — Mars showing as Online on its own dashboard, with a live feed of its own beacons scrolling past — we should have stopped. There is a professional virtue in stopping when the goal has been met.

We did not stop, because a small observational footnote nagged at us: the sequence number on Mars's panel was displaying as `#0`, despite the beacon payload we could capture with `tcpdump` clearly containing a field named `beacon_sequence` with a value of `1,366,543` and rising.

Field-name mismatches between the beacon format and the dashboard's parser account for the discrepancy. The dashboard had been written expecting the old monolith's field names — `beacon_sequence_number`, `system_uptime_hours`, `status`. The new v1 core emitted `beacon_sequence`, `system.uptime_seconds` (nested), `status_message` and `health`. Same semantic information, different words. The dashboard, having learned nothing from linguists, simply showed zero when it didn't recognise a word.

The fix, in `bridge.js`, was to add fallback chains:

```javascript
const rawJson = JSON.stringify(beacon);
webClients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
        client.send(output);       // existing ASCII art
        client.send(rawJson);      // new: raw JSON alongside it
    }
});
```

And in the template strings, the likes of:

```javascript
│ Sequence #${beacon.beacon_sequence_number
            || beacon.beacon_sequence
            || 0}
```

A reasonable person might question whether emitting both an ASCII-art summary and a raw JSON payload to every connected WebSocket client is a sensible use of bandwidth. A reasonable person would, in this case, be outvoted by the fact that the dashboard's JavaScript already had a `try/catch` around `JSON.parse()`: if it received JSON, it would parse it and extract fields cleanly; if it received the ASCII box, it would fall back to regex-matching for a `Sequence #N` substring. Both paths already existed. We just needed to feed them both.

The Mars panel began displaying real sequence numbers. The counter reached `#1,367,547` by the time we stopped watching. It has not stopped climbing since.

And this is the point at which we discovered the ghost.

## Fifty Days of Silent Respawning

Our next task was to build two new JSON endpoints — `/ping` and `/beacon` — that would let external clients and monitoring systems query Mars directly without needing to open a WebSocket to the dashboard. We designed the service in Node.js, chose port 9875 (because it was the port a long-dead `fastping-server.js` had once used, and reclaiming it seemed tidy), and started our new service.

It failed to bind. `EADDRINUSE`.

Port 9875 was, somehow, occupied. A quick check of the process list revealed a `node` process that had been running since March 1st — which is, at the time of writing, fifty days prior. It was owned by the `wofl` user. Its command line was `/usr/bin/node fastping-server.js`. Its working directory was `/home/wofl/mars-dashboard/` — the v3 arch folder that nobody had intentionally used in months. Its parent process was PID 1, systemd, because whatever shell had started it had long since exited.

pm2, the process manager I had assumed was orchestrating all long-running services on this machine, did not know about it. Nothing in `crontab` pointed at it. And yet it had been running for fifty days, had been restarted at least once (because fifty days exceeds the process's etime from any reasonable starting point), and was clearly being maintained by *something*.

The something, after twenty minutes of investigation, turned out to be a systemd service called `mars-fastping.service`, installed in `/etc/systemd/system/` on February 13th, enabled, with `Restart=always` in its `[Service]` section. It had been diligently performing its duty — which was, as far as we could tell, to ensure that a forgotten Node.js script from the abandoned v3 architecture continued to hold port 9875 against all comers, forever, amen.

We stopped it. We disabled it. We deleted the unit file. systemd, asked about `mars-fastping.service`, now claimed to have never heard of it, which was the correct answer.

Our new service, now unopposed, bound to port 9875. It subscribes to the WebSocket stream that `bridge.js` broadcasts, caches the most recent beacon it receives, and exposes two HTTP routes:

- `GET /ping` returns a light identity response — node ID, version, uptime, a timestamp, and a freshness indicator showing how recently the beacon cache was updated
- `GET /beacon` returns the most recent full beacon payload verbatim, or `503 Service Unavailable` if the service has not yet received one

Both routes include `Access-Control-Allow-Origin: *` headers, so browser JavaScript from any origin can query them. Both are accessible publicly at `https://mars.litehaus.online/ping` and `/beacon` via a chain of infrastructure that, described in full, is slightly absurd: a reverse SSH tunnel from Mars to London, an nginx `location` block on London's public-facing vhost, a Let's Encrypt certificate, a Cloudflare DNS record with the orange cloud deliberately *disabled* so the tunnel traffic flows direct rather than through Cloudflare's proxy layer. Many things cooperate to deliver one small JSON payload. This is often the case with infrastructure.

If you curl either endpoint right now, you will get a real response. I encourage you to try it:

```bash
$ curl -s https://mars.litehaus.online/ping | python3 -m json.tool
{
    "status": "ok",
    "node_id": "litehaus-home-uk-01",
    "node_type": "home_physical",
    "version": "MARS-v1.0-HOME-MASTER",
    "timestamp_unix": 1776690651,
    "timestamp_iso": "2026-04-20T13:10:51.042Z",
    "uptime_seconds": 297,
    "beacon_source": {
        "bridge_connected": true,
        "last_beacon_age_seconds": 1
    }
}
```

The `/beacon` endpoint returns the full 1,197-byte payload: node identity, chrony discipline state, CPU load, memory usage, disk free, stratum level, UPS presence, LoRa gateway status, and a dozen other telemetry fields. Much of it is currently zero or `false`, because Mars has not yet had its physical hardware attached. The GPS-disciplined rubidium clock, the LoRa gateway, the software-defined radio, the UPS — all are planned for later sessions. The beacon's schema already anticipates them. It is a curiously optimistic document.

## The Fourth Fix: Telling The Truth About Yourself

There is a final observation worth recording, because it illustrates a general principle about introspection in software.

After all of the above, three fields in the beacon payload were still stubbornly zero: `json_parse_time_microseconds`, `total_requests_processed`, and `average_throughput_mbps`. These fields are intended to report on the process's own performance — how quickly it parses JSON, how many parses it has done, how much data has flowed through it.

The fields were being read out of a `stats` object every beacon cycle and serialised into the payload. The `stats` object was part of a `BeaconParser` class with proper internal counters. Every call to `BeaconParser::parse()` would increment `total_parses_`, measure the elapsed time in nanoseconds, accumulate the byte count, and update the running averages. The infrastructure was all there.

The problem was that *nothing in the core process ever called `BeaconParser::parse()`*. The parser was instantiated as a member variable, its stats were dutifully read and emitted, but no code path actually used the parser to parse anything. Its counters stayed at zero not because of any bug, but because the parser was sitting idle, being asked every second how much work it had done, and truthfully answering "none."

The probe loop — the part of the code that periodically hits an external URL to measure connectivity — was doing something peculiar. When its HTTP client returned a response body, the probe loop did not pass that body through the parser. Instead, it performed string-surgery on the response, searching manually for a `"connecting_ip"` substring with `response.body.find()`. This was, presumably, a legacy of an era when the URL pointed at fastping.it.com and the response format was a fixed third-party schema. But we had pointed the URL at Mars's own `/beacon` endpoint — a loopback self-probe — and the response was now a full beacon payload that the parser would have happily consumed.

Six lines of replacement code later:

```cpp
double parse_time_us = 0;
MasterBeaconPayload temp;
json_parser_.parse(response.body, temp, parse_time_us);
std::string ip = temp.system.primary_ip;
```

Core now self-probes by querying its own `/beacon` endpoint, runs the response through its own parser, and the parser's stats begin to reflect genuine activity. Within seconds, the zeroed fields populated with honest numbers: 22.17 microseconds per parse, throughput around 50 megabits per second, requests incrementing. The node finally tells the truth about itself.

This was the fourth fix of the day, and the one I enjoyed most, because it was architecturally satisfying in a way the others were not. The first three had been *repairs* — bugs introduced by imperfect authorship and fixed by careful replacement. The fourth was something closer to a *wiring* — an existing capability (the parser) and an existing need (honest telemetry) that had never been connected, and now were. The node's introspection had been a facade; it is now a feed-back loop.

## What The Day Left Behind

At the end of nine hours of work, the state of Mars is as follows.

It runs two systemd services: `litehaus-core.service` (the patched v1 C++ core, boot-persistent) and `mars-london-tunnel.service` (the reverse SSH tunnel to London, with three ports forwarded). It runs two pm2-managed Node.js processes: `beacon-monitor` (the dashboard WebSocket bridge) and `mars-api` (the new `/ping` and `/beacon` endpoint service). Its home directory is fifty-seven megabytes smaller than it was that morning, having had an entire abandoned architecture deleted from it. Its `ROADMAP.md` is one hundred and eighty-one lines long and describes, accurately, what is present and what is still to come.

It beacons itself and four cloud relays once per second. It broadcasts a compact identity packet to `255.255.255.255:9877` once every two seconds, which, though heard by nobody, is at least no longer failing. Its self-probe runs every probe cycle, exercises its JSON parser on its own beacon, and reports genuine performance metrics. The Mars panel on the dashboard shows sequence numbers rising in real time, uptime calculated from correctly-named fields, health indicators that reflect real state rather than default placeholders. The little dragon is, in every measurable sense, Online.

Is this impressive? In isolation, not particularly. None of the fixes were large. None of them required novel techniques. Any reasonably experienced systems programmer could have produced them.

What the day demonstrates, I think, is a less glamorous virtue: the willingness to *not believe the first explanation*. The dashboard said Mars was Offline. The obvious fix was to replace the broken process. The actual fix required tracing down into the C++ config parser, discovering an unimplemented branch, fixing a missing socket option, wrapping every external hardware probe in aggressive timeouts, exorcising a fifty-day-old ghost service, patching a dashboard's field-name expectations, building two new HTTP endpoints from scratch, and finally wiring an idle parser to its obvious input. Each step was small. None was where we expected to be. The problem was never where the symptoms pointed.

There is a line I keep coming back to, attributed (probably wrongly) to several different engineers of the last century: *the hardest bugs are the ones where the computer is doing exactly what you told it to*. Every single thing we fixed today was a case of the computer doing exactly what it had been told. The config parser was told to ignore `beacon_targets`. The socket was told to refuse broadcasts. The hardware probe was told to wait forever. The parser was told to sit idle. The ghost service was told to respawn forever. The computer was faithful; the instructions were simply, in various delicate ways, wrong.

## Try It Yourself

If you have read this far, you have earned the right to the URLs.

The dashboard: [https://mars.litehaus.online](https://mars.litehaus.online)

When you load it, you should see five panels — New York, London, Sydney, Singapore, and Mars — each with a terminal-style live feed, sequence numbers, latency figures, and a small flashing icon every time a beacon is received. The page will work in any modern browser. The connection is over TLS, the data streams over WebSockets, and the dashboard updates in near-real-time.

Ping Mars directly:

```bash
curl -s https://mars.litehaus.online/ping | python3 -m json.tool
```

You will receive an identity response in under a second. The `beacon_source` sub-object tells you whether Mars's local bridge is connected and how fresh the cached beacon is.

Fetch the full beacon:

```bash
curl -s https://mars.litehaus.online/beacon | python3 -m json.tool
```

This returns the most recent full telemetry payload. Run it twice a few seconds apart and you should see the `beacon_sequence` field incrementing. You will also see `json_parse_time_microseconds`, `total_requests_processed`, and `average_throughput_mbps` with real values, which, as of this morning, they did not have.

Sessions still to come will connect the physical hardware — the GPS-disciplined rubidium oscillator, the LoRa gateway, the software-defined radio, the uninterruptible power supply, and finally the WiFi halo. When those arrive, the beacon's currently-empty `time`, `power`, `lora`, `radio_bridge`, and `wifi_halo` subsections will begin reporting real data. The schema is ready for them. Mars is a node waiting to become what it always claimed to be: a physical, authoritative, GPS-disciplined Stratum-1 time source, broadcasting its truth to the world one second at a time.

For now, though, it is enough that it is Online and honest. These are not always the same thing. Today, for Mars, they are.

---

*Thanks to wofl, whose refusal to accept "it's probably fine" when confronted with a dashboard showing `Sequence #0` is the reason this piece exists.*
