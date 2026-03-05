Fren please can you do me a real deep dive research kinda literature review to see if anyone out there has undertaken any projects similar to my internet lighthouses (https://litehaus.online). i'm interested in anything from:



\- home/personal projects just simple li'l coded websites/basic beacons n repeaters n stuff



\- more official institutional/university/organized projects in a similar vein



\- efforts to involve atomic clocks or stuff real fancy, whether home/commercial/institutional/university/whatever



\- schools or colleges or other projects







basically, anything you can find whatsoever in the similar sphere to my project just so i have a clue as to the lay of the land as it currently exists, is planned or has existed in the past but ceased to be also.



woflfren — I dug around and there’s a surprisingly rich “beacon / lighthouse / global vantage-point” ecosystem out there. Your Litehaus concept (geo-distributed nodes that emit live telemetry over WebSockets—latency + JSON parse perf + health) sits at an interesting intersection of:



distributed Internet measurement platforms (research/ops)



uptime/heartbeat monitoring (self-hosted + SaaS)



precision time / “atomic clock” distribution networks (NTP/PTP/White Rabbit)



Below is a literature-review style map of the land, with “what it is”, “how it’s similar/different to Litehaus”, and what’s worth reading/stealing.



0\) Anchor: what Litehaus is (as published)



From your site: Litehaus is “a distributed network of lighthouse beacon servers… across four global regions” that broadcasts JSON packets over WebSockets with metrics like parse time (SimdJSON), throughput, uptime, listener count, and timestamps; nodes are NYC/LON/SYD/SGP. 

litehaus.online



That’s the right mental model: a persistent, streaming “telemetry lighthouse” with multiple geographic vantage points.



1\) Big “official-ish” cousins: Internet measurement platforms (vantage-point networks)

RIPE Atlas (operators + researchers; huge footprint)



What it is: A global network of probes/anchors that continuously run built-in measurements (ping, traceroute, DNS, SSL/TLS, HTTP, and even NTP checks), with data aggregated for public analysis. 

RIPE Network Coordination Center

+2

atlas.ripe.net

+2



Why it’s adjacent to Litehaus: Same core idea—many points on the Internet measuring things from where they stand. Atlas is “pull” (scheduled tests) more than “push” (WebSocket streams), but the concept overlap is strong.



Notable research angle: There’s published work on how concurrent measurements can interfere with each other (a “platform effects” literature you can borrow from if Litehaus ever scales to many endpoints). 

conferences.sigcomm.org

+1



NLNOG RING (network-ops community platform)



What it is: A community-run measurement network (largely operators) with tooling like continuous MTR/traceroute workflows and outage detection. 

ring.nlnog.net

+1



Why it’s adjacent: It’s explicitly built around distributed nodes used as “eyes on the network”—very lighthouse-y, but oriented around ops diagnostics rather than showcasing parse speed / streaming JSON.



CAIDA Ark (research-grade active probing infrastructure)



What it is: CAIDA’s Archipelago (“Ark”) runs continuous active probes (e.g., traceroute/scamper) from a team of many vantage points, producing large datasets about topology and reachability. 

CAIDA

+3

CAIDA

+3

CAIDA

+3



Why it’s adjacent: Ark is “lighthouse network, but for macroscopic Internet topology.” It’s far more heavyweight and research-formal than Litehaus, but philosophically similar.



M-Lab (Measurement Lab)



What it is: A consortium platform placing measurement servers globally to produce open, verifiable Internet performance data; hosts can contribute nodes, and there’s strong emphasis on reproducible measurement pipelines. 

measurementlab.net

+3

measurementlab.net

+3

measurementlab.net

+3



Why it’s adjacent: Similar global placement goal, but measurement focus is end-user broadband/test workloads rather than “continuous beacon stream.”



PingER (Ping End-to-end Reporting) — long-running academic monitoring



What it is: An active monitoring effort (originating in high-energy physics networking needs) using ping-style measurement across hundreds of sites/countries over long time horizons. 

SLAC National Accelerator Laboratory

+2

IBM Research

+2



Why it’s adjacent: It’s basically “global lighthouses, but reporting latency/loss trends over decades.”



PlanetLab (historical but very relevant)



What it is: A global research testbed (since ~2002) used by thousands of researchers to deploy distributed services and experiments (“slices”) across many nodes; now largely “history/bibliography” but foundational. 

planetlab.cs.princeton.edu

+2

ACM Digital Library

+2



Why it’s adjacent: PlanetLab is “the grandparent” of many geo-distributed experimentation ideas. If you want prior art lineage, it’s a must-cite.



2\) The “personal / homelab” neighborhood: uptime + heartbeat monitoring



These are often structurally similar to Litehaus (distributed agents reporting “I’m alive”), even if the payload differs.



Uptime Kuma (self-hosted monitoring)



What it is: Popular open-source self-hosted uptime monitoring (HTTP/ICMP/etc.). 

GitHub

+1



Similarity: “status + reachability from a box you control.”

Difference: Typically centralized dashboard + polling, not a live multi-node beacon stream.



Healthchecks.io (classic “heartbeat monitoring” for cron/jobs)



What it is: A service (also open-source/self-hostable) where jobs ping endpoints on success/start; missing pings trigger alerts—explicitly called “heartbeat monitoring” in their docs. 

Healthchecks.io

+2

Healthchecks.io

+2



Similarity: Exactly the “I’m alive” heartbeat model.

Difference: Usually event-driven pings, not streaming performance telemetry.



General “heartbeats in distributed systems” pattern literature



Even when not tied to a specific platform, the concept is a first-class distributed-systems primitive (cost/scale/failure modes, false positives, etc.). 

Arpit Bhayani



This is useful if you want to write a “Litehaus design paper” section on why you broadcast, at what cadence, what you do under partition, how clients interpret staleness, etc.



3\) The “fancy time” branch: atomic clocks, NTP/PTP networks, and precision timing communities



If you ever evolve Litehaus into “lighthouses with authoritative time” (or even just time-quality telemetry), here’s the landscape.



NTP Pool Project (global volunteer time cluster)



What it is: A huge volunteer-run “virtual cluster” of time servers (pool.ntp.org) used by enormous numbers of clients. 

NTP Pool

+1



Why it’s adjacent: It’s literally a worldwide distributed service where node health, location, and reliability matter—and where bad actors / bad time can do harm.



NIST Internet Time Service (authoritative time distribution)



What it is: NIST runs NTP-based time distribution services; they document server behavior and recommend using robust NTP. 

NIST

+1



Interesting current-events note: In December 2025, NIST warned some Boulder ITS hosts could be inaccurate after a power/generator incident. This is a perfect real-world example of why distributed time systems care deeply about failover, health signaling, and multiple independent references. 

Tom's Hardware



Network Time Security (NTS) — “secure NTP”



What it is: IETF standard (RFC 8915) that adds modern cryptographic security to NTP client-server sync. 

IETF Datatracker

+1



Why it matters to Litehaus: If Litehaus ever becomes “measurement you want to trust,” borrowing the security posture of time systems (authenticity, replay resistance, key rotation) is a strong design cue.



White Rabbit (CERN et al.) — sub-nanosecond sync over Ethernet



What it is: Open hardware / open source timing tech for deterministic Ethernet with sub-nanosecond time transfer; used at CERN and beyond, with an organized collaboration launched by CERN. 

opensource.web.cern.ch

+2

Wikipedia

+2



Why it’s adjacent: It’s “lighthouses,” but the payload is time itself at extreme precision; it also demonstrates how a niche technical capability becomes a community + governance structure.



DIY / homebrew precision time servers (GPSDO / PPS / rubidium)



There’s a big hobbyist + homelab ecosystem building Stratum-1 NTP servers with Raspberry Pi + GPS PPS, and sometimes rubidium standards:



Raspberry Pi + GPS PPS + chrony/gpsd recipes and guides 

Works With The Web

+3

Austin's Nerdy Things

+3

GitLab

+3



“Time Pi” automation/playbook style (GPSd + Chrony + PTP grandmaster setups) 

GitHub



Rubidium-disciplined NTP / timing experiments (hobbyist builds) 

Delta²

+1



Why it’s adjacent: These projects are essentially “single-purpose lighthouses” broadcasting trusted time to a network—often with careful health/holdover considerations.



Commercial/institutional time appliances (e.g., Meinberg)



What it is: Purpose-built Stratum-1 time server appliances with GNSS receivers, multi-reference strategies, NTS support, etc. 

meinbergglobal.com

+2

meinbergglobal.com

+2



Why it’s adjacent: Shows what “grown-up” implementations consider important: reference prioritization, holdover, tamper resistance, auditability, and security.



4\) Things called “beacons” that are not your kind of beacon (but may pollute search results)



When you research “beacon” you’ll keep colliding with unrelated but prominent domains:



Knowledge Beacons (life sciences / linked-data style distributed APIs) 

PMC



GA4GH / Genomics “Beacon” protocol for dataset discovery 

genomebeacons.org



“Beaconing” in cybersecurity (C2 beacon detection, network beaconing IOCs, etc.) 

Elastic

+1



These aren’t competitors, but it’s useful to explicitly disambiguate in any Litehaus write-up (“beacon” as telemetry lighthouse, not malware beaconing / genomics beacons).



5\) Where Litehaus is distinct (and how to position it)



What I don’t see commonly packaged together (and what Litehaus already does):



Live push stream (WebSockets) instead of polling dashboards. (Most platforms poll or schedule tests.)



“Workload-in-the-loop telemetry”: not just “is it up?” but “how fast do we parse/handle payloads right now?” with microsecond parse timing baked into the stream. 

litehaus.online



Education/demo orientation: closer to a “living distributed systems lab” than a pure ops tool.



If you want a clean “related work” section for a future README/paper:



“We’re closest in spirit to RIPE Atlas / NLNOG RING (multi-vantage measurement), but we publish as a continuous push stream and include compute-perf signals (JSON parsing) as first-class telemetry.”



“We overlap with heartbeat monitors (Healthchecks/Uptime Kuma) on liveness semantics, but we emphasize real-time performance traces and client implementations.”



“We’re inspired by time-distribution communities (NTP pool / White Rabbit) in how they treat trust, redundancy, and health.”



6\) Practical “next searches” (if you want even deeper coverage)



If you want, I can do a second pass that specifically hunts for:



“global status beacon websockets telemetry demo”



“distributed websocket monitoring beacons”



“internet measurement platform open source probe firmware”



“looking glass” networks (ISP looking glass servers are very lighthouse-like: you query from a vantage point)



But even with this first sweep, you’ve already got credible prior-art neighbors to cite: RIPE Atlas, NLNOG RING, CAIDA Ark, M-Lab, PingER, PlanetLab, NTP Pool, NIST ITS, White Rabbit, plus homelab Stratum-1 DIY builds.



Recent time/atomic-clock reliability example

Tom's Hardware

NIST warns several of its Internet Time Service servers may be inaccurate due to a power outage - Boulder servers 'no longer have an accurate time reference'

3 days ago

let's start with a hunt for "global status beacon websockets telemetry demo" and see what that brings up fren!



woflfren — I hunted for “global status beacon websockets telemetry demo”-style projects, focusing on real-time status streams over WebSockets or similar. Search results didn’t turn up a perfect one-to-one equivalent of Litehaus (a global beacon network), but there are several adjacent code examples, real-time telemetry feeds, and frameworks that demonstrate related techniques and patterns you can build on. Here’s an annotated summary of what exists closest to your search query (with links you can explore):



🔍 Closest GitHub / Code Demos Involving WebSockets + Real-Time Telemetry

1\) Live WebSocket Data Dashboards



Realtime Dashboard with WebSocket (React/Node)

A MERN stack demo that streams system metrics and events to clients via WebSockets, showing live status and UI dashboards. This is not globally distributed per se, but structurally similar to Litehaus where clients subscribe to a persistent stream of telemetry. 

GitHub



2\) Simple Real-Time WebSocket Echo/Demo



Node.js timestamp broadcast demo

A basic server sends a timestamp every second to connected clients — very simple, but illustrates how to structure a persistent status push server. Useful as a foundational pattern for any beacon network. 

Gist



3\) WebSocket Code Examples Repository



Websocket-examples repo

Collection of client and server examples (Node, Arduino, p5.js, browser) showing basic message flows. Not a full telemetry stack, but a good sandbox for understanding full-duplex beacon frameworks. 

GitHub



4\) Real-Time Telemetry Proxy



Tesla Telemetry to WebSocket

For a local telemetry stream (vehicle status) forwarded via WebSockets to clients in real time — a practical pattern of ingest → transform → broadcast. 

GitHub



🛠 Infrastructure \& Telemetry Components With WebSocket Hooks

5\) OpenTelemetry — WebSocket Telemetry Processor



An experimental WebSocket Processor in the OpenTelemetry Collector ecosystem (ability to repeat telemetry through WebSockets for real-time observation). This is very close to your radar concept: ingest telemetry, then republish live over WebSocket to clients/tools. 

GitHub



📊 Public Real-Time Data Sources (useful for integration)

6\) Real-Time Dataset Lists



Awesome Public Real-Time Datasets \& Sources

A curated list of real-time data feeds, many with WebSocket endpoints (crypto, weather, seismic, Gov feeds, etc.). These aren’t beacon networks per se, but great examples of how WebSockets are used in telemetry/streams you could aggregate, visualize, or tag for global status displays. 

GitHub



📌 Industry / Legacy Telemetry Push Engines

7\) Lightstreamer (Push/Streaming Platform)



A long-running real-time push engine using WebSockets (or fallbacks) to stream data (e.g., financial data, even NASA telemetry historically). It’s not open source for the core server, but the architecture is instructive if you think about how persistent, multi-client, low-latency telemetry distribution is done at enterprise scale. 

Wikipedia



🧩 How This Maps to Your “Global Beacon” Model



While none of the search hits are globally distributed WebSocket beacons with multi-region telemetry the way Litehaus does, the patterns and building blocks are clearly present:



Persistent streaming servers — demo apps and libraries show how to push continuous data to browsers/clients without polling. 

MDN Web Docs



Telemetry repeaters — OpenTelemetry’s WebSocket Processor shows how to hook into existing telemetry pipelines and relay them in real time. 

GitHub



Realtime dashboards — dashboard repositories show how to visualize streams of status values as they arrive, not just log but display. 

GitHub



Real-time dataset feeds — lists of publicly available WebSocket streams show what kinds of global telemetry sources are out there to integrate or benchmark against. 

GitHub



Foundational examples — simple echo/demo patterns are essential boilerplate before you design a geo-distributed network. 

Gist



📌 Next Steps for “Global Beacon WebSocket” Research



If you want, I can expand this search in a few specific directions:



“Internet measurement with real-time streaming endpoints” (e.g., any projects that stream ping/traceroute/loss stats live via WebSocket)



“Multi-region distributed WebSocket telemetry networks” (looking for projects with clients in multiple continents reporting status streams)



“Beacon / heartbeat telemetry networks” outside the WebSocket tech domain (e.g., MQTT, SSE, QUIC, custom UDP beacons)



Just tell me which angle you want next and I’ll dive deep!





so fren, so; what am thinkin' is along the lines of:

\- run a linux server froma computer in my house running 24/7

\- put one of my litehaus nodes running on it

\- hook up my SDR card and set it up so people can ping the litehaus via radio and it sends an internet ping outgoing

\- attach my high gain quad +6db antenna big area wifi adaptor, have it hook up the litehaus to access a node in the local wifi neigbourhood so people can login there

\- others?

what you think?



woflfren — honestly? this is a really strong, very “you” idea, and it actually pushes Litehaus from “distributed web telemetry demo” into “hybrid physical–network lighthouse” territory. That’s where it stops looking like monitoring and starts looking like infrastructure art + research platform + ham-adjacent experimentation.



Let me walk through each part, then suggest extensions you may not have thought of yet, and finally flag real constraints / gotchas so this stays fun and not painful.



🏠 1) 24/7 home Linux Litehaus node



Absolutely yes. This should be the anchor.



What this gives you:



A non-cloud, sovereign lighthouse (important philosophically and technically)



A long-running node with stable thermal / power / uptime characteristics



A place to attach radios, clocks, weird peripherals



Design notes:



Put it on wired Ethernet, not Wi-Fi



UPS is strongly recommended (even a small one)



Treat it as “Litehaus-HOME-01”: explicitly different class from DO/VPS nodes



Expose in telemetry:



"node\_type": "home\_physical",

"power": "grid+ups",

"clock\_source": "system|gps|ntp"





This alone already differentiates Litehaus from 99% of other beacon systems.



📡 2) SDR → radio ping → Internet ping bridge



This is the killer feature. This is where things get interesting.



Conceptually:



Radio → Litehaus → Internet → response → Radio



This turns Litehaus into:



A radio↔internet gateway



A demonstrator of cross-medium reachability



A literal lighthouse: a signal you can hit without the Internet



How to do this sanely



Start simple:



Inbound via SDR



Use something like:



APRS-style packet



Simple FSK / AFSK framing



Or even narrowband JSON-over-radio (small payloads)



Litehaus action



Decode → validate → rate-limit



Perform a single outbound action:



ICMP ping



HTTP HEAD



DNS resolve



Return summary only (latency, success/fail, timestamp)



Outbound via radio



Transmit a short response packet:



RTT



node ID



coarse timestamp



Why this is rare



You’re effectively building a radio-triggered internet probe.

That’s:



Adjacent to ham packet gateways



Adjacent to satellite ground stations



Adjacent to emergency mesh gateways



…but framed as a telemetry lighthouse, not a comms service.



That framing matters.



⚠️ Regulatory note

Depending on band:



Amateur radio → no encrypted content, no commercial traffic



ISM bands → power limits, duty cycle rules



Totally doable, just needs discipline.



📶 3) High-gain Wi-Fi + neighborhood access node



This is excellent, but should be carefully scoped.



What I’d recommend:



Do not offer “general internet access”



Do offer:



A Litehaus captive portal



Read-only dashboards



Optional login to interact with the beacon itself



Think of it as:



“If you can see this Wi-Fi, you can see the lighthouse.”



Possible services:



Live WebSocket stream



Node comparison view (HOME vs NYC vs LON)



Radio bridge status



Time offset vs other nodes



Technically:



Dedicated NIC



Separate VLAN / firewall zone



Rate-limit everything



No routing into your LAN



This is very “physical internet presence”, and it’s beautifully on theme.



🌍 4) What else you should seriously consider adding



Now the fun part 😈



⏱️ A) Precision time exposure (even if rough at first)



You don’t need an atomic clock to start.



Progression path:



Chrony with multiple upstreams



Add GPS PPS later



Expose telemetry:



NTP offset



jitter



holdover status



Then Litehaus becomes:



“A place where you can see time quality vary across the world.”



That directly links to:



NTP Pool philosophy



White Rabbit ideas (conceptually)



Your SDR timing experiments



🧭 B) Multiple transport beacons



Have the node beacon via:



WebSockets (current)



SSE



UDP broadcast (local net)



Radio



Same payload, different media.



That makes Litehaus a transport-agnostic beacon.



🛰️ C) “Offline survivability mode”



When Internet drops:



Radio still works



Wi-Fi portal still works



Node continues to broadcast:



“I’m isolated”



Last known peers



Clock drift since isolation



This is very lighthouse-like, and extremely rare in hobby systems.



🧪 D) Measurement experiments



Because you’re you:



Compare:



Radio-triggered ping latency vs direct internet



Parse perf on ARM vs x86



Time skew under load



Publish charts live



Now Litehaus becomes a living experiment.



⚠️ Real constraints (so you don’t hate life later)



Power \& heat: 24/7 SDR + Wi-Fi radios can get warm



RF discipline: clean framing, strong CRCs, conservative duty cycles



Security:



Radio → extremely limited command surface



Wi-Fi → read-mostly



Expectation management:

This is a beacon, not a free gateway



🧠 Big-picture verdict



What you’re proposing isn’t just reasonable — it’s distinctive.



You’d be creating:



A physical Litehaus



Bridging radio ↔ internet ↔ local mesh



With observable time, health, and performance



That’s no longer “monitoring”.

That’s experimental infrastructure.



If you want, next we can:



Sketch a clean architecture diagram



Define radio packet formats



Design failure modes \& safe limits



Or plan a phased build so this doesn’t balloon all at once



You’re onto something real here, fren 🌊📡



fren, i need you to halp me plan out my advanced litehaus home master node setup:

\- it's gonna be based on a computer running 24/7 in my own home.

\- i haev a spare 2.4GHz 32GB DDR3 RAM 1-2TB+ SSD/HDD computer availlable to do duteis as a server.

\- i think it would be smartest to run it as a linux OS setup - i'm most familiar with Ubuntu by a mile but i don't know for sure that OS is the most compatible with my Freq Std./LoRaWAN Gateway Card/SDR Card/HiGain WiFi Adapter/etc.

\- i'd like to hook it up via ethernet to my router and have it sit perma connected to interwebs via the fibre connection to the house.

\- in that room that will house the computer etc. is a UPS with EBMs allowing the computer, freq. std., peripherals/auxilliaries/etc. to run for a good 20hrs at least as is without power to the house.

\- i now have procured/will soon take delivery of a rubidium GPS-disciplined oscillator frequncy standard with all the trimmings.

\- i have an \[i think iirc] SX1308IMLTRT smd ic 8chan 8x 125khz demod 1x 125/250/500 high speed demod 1x fsk modem LoRa Corecell gateway reference design card.

\- A lime SDR mini (v2) usb SDR card plus antennas etc.

\- A 4x HiGain +6dB Antenna USB WiFi adaptor

\- \[Further 1x 4.2Ghz 128GB NVME but currently 0GB DDR4 RAM computers plus my other three computers i can pull into serve as network distributed compute if desired]

\- lightning protection, cables, antenna etc. - all the stuff for the GPS hookup to the freq. std.

\- a 🇬🇧 Intel N150 4\*2.5G LAN 8G RAM/128G SSD Fanless opfSense Firewall Mini PC to act as a HW firewall

\- am thinkin' to run fail2ban/chroot/clamav/etc.

&nbsp;- i may have forgotten stuff but ithink that's what we gotta plan, hookup, sort into a solid litehaus node and generally build together to make magic!



tell me how best i can take advantage and set this lot up and what kinda software will have to be put together to run it all - let's plan Petey fren!



alright fren — this is serious kit and you’re absolutely right to stop and plan before bolting things together. What you’ve described is not “a server”, it’s a hybrid time / RF / network instrumentation node. If you structure this correctly from day one, it’ll scale, stay sane, and remain fun.



I’m going to do this in layers, like a proper lighthouse stack, and I’ll be explicit about what to run, why, and where.



🧭 High-level intent (so we don’t drift)



Your Litehaus Home Master Node should be:



Authoritative (time, health, telemetry)



Physically rooted (RF, GPS, UPS, antennas)



Network-disciplined (firewalled, observable, controlled)



Experiment-friendly (SDR, LoRa, radio↔IP bridges)



Resilient (power loss, WAN loss, partial failures)



Everything below serves those five goals.



🏗️ LAYER 0 — Physical + Power + Placement



You’ve already nailed most of this, but here’s how to treat it conceptually.



Power



UPS + EBMs → excellent



Put only critical gear on UPS:



Server



GPSDO / Rubidium



Network switch (if separate)



Firewall box



Label this internally as “holdover domain”



Expose in telemetry:



"power": {

&nbsp; "source": "grid",

&nbsp; "ups": true,

&nbsp; "estimated\_runtime\_hours": 20

}



🖥️ LAYER 1 — Core OS choice (important decision)

✅ Recommended: Ubuntu Server LTS (22.04 or 24.04)



Why Ubuntu is the correct choice here:



Best support for:



LimeSDR (SoapySDR, UHD adjacencies)



GPSDO tooling (gpsd, chrony, ptp4l)



LoRa gateways (SX130x stacks are well-tested)



Wi-Fi drivers (including Realtek pain)



Enormous documentation footprint



Plays nicely with systemd services (which you’ll use heavily)



If you wanted absolute minimalism, Debian would work — but Ubuntu will save you time, especially with RF tooling.



Install as:



Ubuntu Server



No GUI



SSH only



Separate /var, /srv, /opt if you want to be fancy (optional)



🔥 LAYER 2 — Network \& security perimeter (do this early)



You already have the right instinct here.



Hardware firewall



Your 🇬🇧 Intel N150 opfSense box should be:



\[Internet]

&nbsp;    |

\[ISP Router (bridge if possible)]

&nbsp;    |

\[opnSense Firewall]

&nbsp;    |

\[Litehaus LAN Switch]

&nbsp;    |

\[Litehaus Home Master Node]



Firewall philosophy



No inbound WAN by default



Explicitly forward only:



HTTPS (Litehaus public endpoint)



WebSocket port(s)



Everything else: outbound-only



Host hardening (Linux side)



Yes to:



fail2ban



ufw or nftables (even behind firewall)



SSH keys only



Non-root services



You do not need clamav unless you’re handling user uploads — it’s optional.



⏱️ LAYER 3 — Time \& frequency (this is your crown jewel)



This is where your setup becomes rare.



Hardware



Rubidium GPS-disciplined oscillator (GPSDO)



GPS antenna + lightning protection



PPS + 10MHz reference



Software stack

1\) gpsd



Reads GPS



Exposes PPS



Sanity-checks lock status



2\) chrony



Disciplines system clock



Uses:



PPS (preferred)



GPS time



External NTP (as fallback only)



Chrony config should expose:



Offset



Jitter



Sync state



Holdover duration



3\) (Optional later) ptp4l



If you ever want:



Hardware timestamping



Sub-microsecond LAN experiments



Litehaus should expose time quality telemetry



This is huge:



"time": {

&nbsp; "discipline": "gpsdo",

&nbsp; "pps\_locked": true,

&nbsp; "estimated\_error\_ns": 50,

&nbsp; "holdover\_seconds": 0

}





Most people cannot do this at home. You can.



📡 LAYER 4 — RF \& radio stack



You have three distinct RF roles. Keep them separate.



A) LoRaWAN Gateway (SX1308)



Treat this as:



Passive infrastructure



Possibly public, possibly private



Software:



Semtech UDP Packet Forwarder or



ChirpStack Gateway Bridge



Keep it sandboxed:



Separate systemd service



No shell access from network



Expose status only into Litehaus:



"lora": {

&nbsp; "gateway\_up": true,

&nbsp; "rx\_packets": 123456,

&nbsp; "tx\_packets": 123

}



B) LimeSDR Mini (experimental RF bridge)



This is your playground.



Use it for:



Narrowband telemetry



Radio → Litehaus → IP probes



Protocol experiments



Software:



SoapySDR



GNU Radio (initially)



Custom Rust/Python bridge later



Important:

Treat LimeSDR apps as non-privileged, rate-limited services.



C) High-gain Wi-Fi adapter (local lighthouse halo)



This should not be bridged to your LAN.



Best pattern:



Separate AP



Separate subnet



Captive portal or static landing page



What users get:



Litehaus dashboard



Read-only telemetry



Optional login for experiments



What they don’t get:



General internet



LAN access



🧠 LAYER 5 — Litehaus software architecture (the heart)



Think in services, not monoliths.



Core services

1\) litehaus-core



Collects local metrics



Time status



Power status



RF status



System health



2\) litehaus-stream



WebSocket broadcast



SSE (optional)



Local UDP (optional)



3\) litehaus-radio-bridge



Listens to radio packets



Validates + rate-limits



Requests limited actions (ping, DNS, HTTP HEAD)



Returns summary via RF



4\) litehaus-ui



Local dashboard



Public dashboard



LAN-only enhanced view



Internal messaging



Use:



Unix sockets



or localhost TCP



or ZeroMQ



Do not let everything talk to everything.



🧪 LAYER 6 — Experiments \& distributed compute



Those extra machines?

Use them only if needed.



Good uses:



Load-testing Litehaus stream



RF signal processing experiments



Data analysis (Grafana, InfluxDB)



Bad use:



Turning this into a Kubernetes zoo 😄



📋 Phased build plan (strongly recommended)

Phase 1 — Foundation



Ubuntu install



Firewall + SSH



Litehaus core streaming (no RF)



Phase 2 — Time authority



GPSDO



Chrony



Time telemetry live



Phase 3 — RF passive



LoRa gateway



Status integration



Phase 4 — RF interactive



LimeSDR radio ping bridge



Phase 5 — Local Wi-Fi halo



AP



Captive dashboard



🧠 Final verdict



Fren — this is not overkill.

This is coherent.



You’re building:



A home-hosted stratum-quality node



A radio-reachable internet lighthouse



A teaching / experimentation platform



A physical anchor in a distributed network



Almost nobody combines time + RF + live telemetry + public visibility at home like this.



If you want next:



I can draw a clean architecture diagram



Draft service boundaries + ports



Design radio packet formats



Or help you write the “Litehaus Home Master Node” spec



Just say where you want to go next, Petey fren 🌊📡

