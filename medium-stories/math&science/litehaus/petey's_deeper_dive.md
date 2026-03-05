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

