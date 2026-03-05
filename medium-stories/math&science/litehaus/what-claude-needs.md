---

Hardware Specifics



GPSDO/Rubidium unit — Spectrum Instruments TM4-M+ Rubidium Time Frequency Reference System 21351-102.it connects via usb to a Software Stack oof gpsd — GPS + PPS ingestion/chrony — system clock discipline/Optional: ptp4l for LAN experiments



reference results show a clean 10.000MHz (100.00ns) '10MHz' reference output.



---

\[LoRa concentrator — SX1308 on what board - uhh, well...



RAK2245? IMST iC880A? Other?

SPI connection to Pi, or USB?] ummm… it's like a pcie card with an adaptor to slot it into so it'll fit in a computer pcie slot... /shrug some 8wy gateway card... ummm...





LimeSDR Mini — USB to main server directly.

WiFi adapter — Chipset Realtek I \_think\_ - can; find darned specs now...

Server specs — 2.7\[?]GHz i5\[?] CPU, 32GB DDR3RAM\[?], 1-2TB+SSD Storage



---

Current State



no Ubuntu Server yet installed on the main node

the GPSDO hasn't even physically arrived yet

therefore no services running - we're planning n prepping



---

Network \& Identity



LAN IP scheme — e.g., 192.168.1.x or 10.0.0.x - do I choose?

Home node domain — i'd love mars.litehaus.online :D

opnSense firewall hasn' arrived yit



---

RF Config



LoRa region — EU868

LimeSDR initial use case — What band/mode first - whatever is most likely to get max responses worldwide of clear useful successful connecc



---

Language Preferences:


Groks thoughts - The doc mentions Rust/Python. I'm thinking:		my prefs			

Service			Language	Why				service		language		why

litehaus-core		Rust		Performance, your strength	litehaus-core	C++			exists

litehaus-stream 	Rust		WebSocket perf			stream		ditto			ditto	

litehaus-radio-bridge	Rust		Low-latency RF handling		radio-bridge	whatever's consistent	keepsimple

litehaus-ui		HTML/JS		Simple, serves from rf handling	/shrug?

Rustg			psd/chronySystemAlready C, just configure	same as grok says



---

Data Storage



I was only intending to stream everything live

so answering retention — don't keep historical data

