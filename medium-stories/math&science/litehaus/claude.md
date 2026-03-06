Alright fren, I've done a proper deep dive into the landscape around time synchronization projects and beacons. Based on what I couldn't access from your litehaus.online site but inferring from context, here's the lay of the land:



Hobbyist \& DIY Time Server Projects

The hobbyist GPS-based Stratum 1 NTP server scene is absolutely thriving. Jeff Geerling recently documented building a DIY PTP Grandmaster Clock with Raspberry Pi as part of the open source "Time Pi" project. Austin's Nerdy Things showed how to achieve microsecond-accurate NTP with a Raspberry Pi and PPS GPS for around $100. Jacob Deane built a GPS-based time server using Raspberry Pi with detailed guides, while JPaul documented a full Stratum 1 NTP server build for under $200. Gary Explains created an extensive YouTube tutorial on building Stratum 1 time servers using Raspberry Pi Pico W with GPS modules.

​

​



Gavin Andrews at AardvarkLabs pioneered using Com Pi/Serial Pi boards with VP Oncore GPS modules to transform Raspberry Pi units into precision NTP servers. These DIY projects consistently emphasize direct UTC time source connection via GPS satellites, achieving microsecond to millisecond accuracy.

​



Institutional \& University Projects

The University of Delaware hosts the Network Time Synchronization Research Project, the birthplace of NTP development, with ongoing research into planetary networks and deep space mission time synchronization. The University of Technology Sydney operates a Network Timing Lab developing methods to remotely detect errors in time servers that provide time to billions of computers. The University of British Columbia commissioned two dedicated Stratum 1 NTP servers in 2024, one at Point Grey campus and another at Okanagan campus, both using multi-constellation GNSS/GPS clocks as timekeeping sources. The University of Edinburgh provides Network Time Service allowing campus computers to synchronize to Universal Time.

​



Research institutions have published advanced work including a 2024 paper on dynamic NTP algorithms with FPGA implementations, comparing dynamic NTP (DNTP), static NTP (SNTP), and GPS-based NTP (GNTP) performance in varying network conditions.

​



Public \& Volunteer Time Services

The NTP Pool Project represents the largest volunteer-driven time infrastructure, providing Internet access to massive virtual clusters of NTP servers in most countries worldwide. Servers are volunteered by individuals and enterprises with internet-connected systems. Major vendors including Apple, Google, Cloudflare, Meta, Microsoft, and Ubuntu provide free public time services. Google notably implemented public NTP with load balancers and atomic clocks across their worldwide data centers, adopting unique leap-smearing technology for smooth leap second insertion. SIDN Labs provides free time service at time.nl. In the US, NIST has provided free time services via publicly accessible Stratum 1 servers for decades, alongside the US Naval Observatory (USNO).

​



Commercial \& Atomic Clock Systems

Galleon's ServerARC Atomic Clock Time Server uses radio time signals from atomic clocks in Colorado to provide sub-second accuracy for enterprise networks. Customers range from NASDAQ and Buckingham Palace to Daimler Chrysler, 3M, GlaxoSmithKline, Kellogg's, Sharp, and Shell. Bodet Time and Gorgy Time provide synchronized clock systems specifically for educational institutions, featuring class change systems, lockdown alerts, and automatic DST changeover. These systems aim to reduce lost learning time by ensuring all lessons begin and end simultaneously across multiple school buildings.

​



Artistic \& Experimental Beacon Projects

One fascinating Reddit side project uses synchronized visual beacons for finding friends in crowds, employing remote time server synchronization (timeapi) with network delay adjustment. All state information including beacon pattern, timing, and start timestamp embeds in URLs/QR codes for easy sharing. The "Connecting Light" installation at Hadrian's Wall for the London 2012 Olympics featured hundreds of 6-foot connected balloons using Programmable XBees, GSM mobile routers, and LED lights to transmit colors along 70+ miles, creating a communication network where visitors sent personalized messages displayed via the balloons. Revital Cohen's work explores GPS signal strength visualization through flickering lamps, providing tangible reminders of digital technology measurement accuracy. Heart Beacon in Portland, Oregon combines interactive light, color, and sound with pulse-activated sensors triggering synchronized lighting effects.

​



The landscape shows strong overlap between precision timekeeping infrastructure (NTP servers), educational/institutional clock synchronization, DIY hobbyist GPS time servers, and artistic interpretations of networked beacons and synchronization. Your internet lighthouses project sits at an interesting intersection of these domains.

