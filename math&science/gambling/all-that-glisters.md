# All That Glisters Is Not Gold

### A reply to the mathematics of slot machines — and a field guide to the sleight of hand the mathematics so politely declines to mention

---

*By Claudia G. Petersen*

---

Some weeks ago I read a genuinely lovely piece by Guilherme Ziegler titled ["To bet or not to bet, that is a math question."](https://medium.com) It is the rare gambling explainer that respects both its subject and its reader: it derives the house edge from first principles, builds a working slot machine in Python and Streamlit, and runs the Monte Carlo simulations that show — cleanly, irrefutably — that the house always wins. If you have not read it, do. I will be standing on its shoulders for the next several thousand words, and it would be unsporting of me not to send you to the source first.

But here is the thing, my darlings. Ziegler's article is *true*, and it is also — forgive me — the polite version. It describes a slot machine the way an architect describes a building: load-bearing walls, structural mathematics, the honest geometry of the thing. What it does not describe is the interior decorator who came in afterward and arranged every mirror, every light, every whisper of carpet underfoot to make absolutely certain you never find the exit.

A real modern slot machine is not merely a negative-expectation game. It is a negative-expectation game wrapped in roughly two dozen distinct psychological exploits, each one engineered with the same care that NASA brings to re-entry. The mathematics of the house edge is the skeleton. The skulduggery is the muscle, the skin, the perfume, and the smile.

So this is a companion piece. Where Ziegler did the heavy lifting on the foundational maths, I will gesture at it briefly and send you back to him for the full derivation. What I want to give you instead is everything that comes *after* the house edge: the self-adjusting return engine that decides, spin by spin, exactly how generous to be; the menagerie of bonus features that exist to disguise volatility as excitement; and — the main event — a complete accounting of the manipulation techniques themselves, with the mathematics laid bare wherever mathematics is what's doing the lying.

And because I cannot resist a worked example, all of it is real. My collaborator and I built the entire machine in Rust — a geospatial slot called *Around the World in 80 Days*, in which your spins generate coordinates and landing near a famous landmark sends you on a gamble around the globe. Every trick I describe, we implemented. In the final section, I'll show you the actual code. There is something clarifying about seeing a dark pattern reduced to forty lines of a systems programming language. It stops being psychology and starts being arithmetic.

Let us begin.

---

## Part the First: A Brief and Respectful Genuflection to the Maths Already Done

I promised brevity here, and I shall deliver it. If you want the full treatment, Ziegler is your man. But we need a shared vocabulary, so here is the skeleton in five sentences.

**Symbols have weights.** Each symbol on a reel is a ticket in a draw; a symbol with weight 5 is five times as likely to land as one with weight 1. Normalise the weights — divide each by the sum of all of them — and you have the probability of each symbol appearing. This is Ziegler's Equation 1, and it is the only probability you truly need.

**Wins require alignment.** A *winning position* is a rule about how many matching symbols must land, and where. Three-in-a-row is the classic. Add more lines — horizontals, verticals, diagonals — and you add more chances to win per spin, though crucially not in a way you can simply sum, because multiple lines can win simultaneously. The correct tool is the complement: compute the probability that *every* line loses, and subtract from one.

**Payouts scale with rarity.** Rarer symbols pay more. The multiplier for each symbol is a tunable parameter, set so that any single win returns more than the per-line stake — which is exactly why a win *feels* like a win even when, as we shall see at exhausting length, it frequently isn't one.

**RTP is the whole story, compressed.** Return to Player is the sum, over every symbol, of the probability of hitting that symbol times its payout multiplier. It is the average fraction of each wagered pound that comes back to you. Set it to 0.965 — a thoroughly typical figure — and you are telling the player: for every £100 you feed me, I shall return £96.50, on average, eventually. The missing £3.50 is the house edge, and it is not luck. It is design.

**Variance is the marketing department.** Here is the sentence Ziegler's simulations prove and that I want you to carry into the rest of this article: *an RTP below one guarantees the average player loses, but it says nothing whatsoever about any individual player.* In the short run, randomness reigns. Some players win. Some win enormously. The house does not need you specifically to lose — it needs the *average* to favour it, and then it needs enough players for the average to assert itself. The winners are not a bug. The winners are the advertisement.

Hold that last thought. We will return to it when we discuss how online casinos run thousands of machines at once, and why that is the most quietly sinister mathematics in the entire enterprise.

There. Five sentences, one debt of gratitude repaid. Now let us go somewhere Ziegler's article, for all its virtues, did not.

---

## Part the Second: The Maths the First Article Was Too Polite to Mention

A naïve slot machine has a fixed RTP. You set the weights, you set the multipliers, you compute the long-run return, and you walk away. The machine is honest in the limited sense that a guillotine is honest: it does exactly what its geometry dictates, every time, without favour.

Modern machines are not like this. Modern machines *watch you.* They maintain a running estimate of how much they have paid you, compare it against their target, and adjust — not the odds of any individual symbol, which would be illegal in most jurisdictions and is genuinely unnecessary, but *which set of reels they spin.* This is the single most important thing to understand about contemporary slot design, and Ziegler's article does not touch it. So we shall.

### The self-correcting return engine

Imagine three different reel strips. The **loose** strip is generous: more high-value symbols, more wilds, more bonus triggers. The **tight** strip is stingy: dominated by low-value filler. The **standard** strip sits between them. All three are perfectly legitimate reel sets. The machine doesn't cheat on any given spin — it simply *chooses which legitimate reel set to use*, and that choice is governed by a feedback loop of considerable elegance.

Here is the heart of it. The machine computes a *correction factor* using a sigmoid function:

$$\text{correction} = \left( \frac{1}{1 + e^{-k \cdot \delta}} - \frac{1}{2} \right) \times 2$$

where $\delta$ is the *deviation* — how far the machine's actual measured RTP has drifted from its target — and $k$ is a steepness constant, set to 15 in our implementation.

Let me unpack this for those who haven't met a sigmoid socially. The expression $\frac{1}{1+e^{-kx}}$ is the logistic function, the most graceful S-curve in all of mathematics. It takes any number on the infinite real line and gently compresses it into the interval between 0 and 1. At an input of zero it returns exactly one-half; as the input grows large and positive it eases toward 1; as it grows large and negative it eases toward 0. It never quite reaches either end — it merely approaches, with the patient resignation of someone who knows they'll never be invited fully inside.

We then subtract one-half and multiply by two, which re-centres the whole thing so it runs from −1 to +1 and sits at zero when the deviation is zero. The result is a correction factor with three moods:

- When the machine has been **overpaying** (actual RTP above target), the deviation is positive, the correction swings positive, and the machine reaches for the **tight** reels to claw the return back down.
- When the machine has been **underpaying** (actual RTP below target), the deviation is negative, the correction swings negative, and the machine reaches for the **loose** reels to nudge the return back up.
- When the machine is **on target**, the correction hovers near zero and the **standard** reels keep their post.

The genius — and I use the word with a clenched jaw — is in the *shape*. Because the sigmoid is gentle near the centre and steep at the extremes, small deviations produce small, unhurried corrections, while large deviations produce aggressive ones. The machine does not lurch. It does not oscillate wildly between feast and famine in a way an alert player might notice. It glides toward its target like a sommelier toward a table that has just ordered the second-cheapest wine: smoothly, inevitably, and entirely in its own interest.

With $k = 15$, a deviation of five percentage points (the machine has paid out 101.5% when it wanted 96.5%) produces a correction of roughly +0.36 — enough to cross into tight-reel territory and cool things down. A deviation of one percentage point produces a correction of around +0.07 — a featherweight nudge. The steepness is tuned so that ordinary statistical noise is met with a shrug, and only genuine drift provokes a response.

### Four clocks, not one

A subtle point, and a vicious one. If the machine measured its RTP over *all* spins since it booted, it would become sluggish — thousands of spins of history would anchor it so heavily that recent results barely moved the needle. If it measured RTP over only the *last few* spins, it would be hysterical, swinging wildly on the noise of a single jackpot.

So it keeps four clocks at once and blends them:

$$\text{RTP}_{\text{weighted}} = 0.10 \cdot \text{RTP}_{20} + 0.25 \cdot \text{RTP}_{100} + 0.35 \cdot \text{RTP}_{500} + 0.30 \cdot \text{RTP}_{\text{all}}$$

The last twenty spins get a 10% vote — enough to register a recent hot streak, not enough to panic. The last hundred get 25%. The last five hundred — the workhorse window, long enough to be statistically meaningful and short enough to be *current* — get the largest single share at 35%. And all-time history gets 30%, the anchor that keeps the whole apparatus tethered to reality.

It is, frankly, a beautiful piece of signal processing. It is also a machine for separating you from your money with maximal smoothness, which rather takes the shine off the craftsmanship.

### The modifiers, or: how a machine performs sympathy

The sigmoid handles the long game. Layered on top is a set of *session modifiers* — short-term adjustments that respond not to the machine's RTP but to *your emotional state*, as inferred from your recent results. These are added directly to the correction factor:

| Your situation | Modifier | Translation |
|---|---|---|
| 13+ losses in a row | −0.15 | "Oh, you poor thing. Here, have a little something." |
| 7–12 losses in a row | −0.08 | "Don't leave just yet." |
| 5+ wins in a row | +0.12 | "Let's not get carried away, shall we." |
| 120+ spins since a bonus | −0.06 | "It's been ages. You're *due.*" (You are not due. More on this sin later.) |

The first two are what the industry might, if it were honest, call *sympathy weighting*. A long losing streak is the moment a player is most likely to stand up and walk away — so the machine loosens, manufactures a modest win, and reseats you. The third is *cooling*: a player on a heater is paying out the house's money, so the machine quietly tightens to bring the celebration to a dignified close. The fourth we will return to with appropriate venom in Part the Third, because it is the mathematical engine behind one of the oldest cons in the building.

Note what is happening here. The machine is not responding to luck. It is responding to *you* — to the psychological pressure points that a losing streak or a winning streak creates — and it is adjusting its generosity to keep you in the chair at precisely the moments you are most likely to escape. That is not a game. That is a hostage negotiation conducted in reel strips.

### The other things the machine notices

Our engine, and every serious commercial one, tracks more than streaks. It watches:

- **Bet changes (chasing).** When a player who has been losing suddenly *increases* their stake, that is the unmistakable signature of chasing — the attempt to win back losses faster. A machine can detect this trivially by comparing recent bet sizes, and a cynical one tightens in response, because a chasing player has already surrendered their judgement and needs no further encouragement to keep feeding the slot.

- **Bonus drought.** A counter ticks upward every spin without a bonus and resets when one lands. Past a threshold — 120 spins, in our build — the machine begins loosening and, in our geospatial version, literally widens the radius within which your random coordinates can trigger the bonus. The drought is allowed to build tension, and then it is *relieved*, on the machine's schedule, at the machine's chosen moment.

- **Banking behaviour.** A risk-averse player who withdraws winnings rather than reinvesting them is, from the house's perspective, a leak. Detecting this pattern lets a machine adjust — perhaps offering a tempting bonus precisely when the player reaches for the exit. We implemented the detection; we declined to weaponise it, but I would be lying to you, my darlings, if I pretended the commercial machines show the same restraint.

### Volatility: the same edge, three personalities

Here is a piece of design that masquerades as player choice. The same machine can present as **low**, **medium**, or **high** volatility — and all three have *identical* RTP. What changes is the *shape of the return*, and it changes through two coordinated levers.

The first lever is the **paytable spread**. A low-volatility machine compresses its payouts: perhaps 3× at the bottom and 200× at the top, a ratio of about 67 to 1. A high-volatility machine stretches them violently: 8× at the bottom and 2,500× at the top, a ratio north of 300 to 1. Same average return; wildly different distribution.

The second lever is the **strip weighting ratio** — tight clustering versus wide spread. Low volatility loads the reels with mid-tier symbols, so wins are frequent but small, a steady drip that keeps the balance graph gently undulating. High volatility loads the reels with low-tier filler punctuated by a vanishingly rare top symbol, so the machine pays almost nothing for long stretches and then, once in a great while, erupts.

The mathematics that holds the two in balance is simply the RTP equation itself: if you widen the paytable, you must thin out the high-value symbols proportionally, so that probability times payout still sums to the same 0.965. Stretch the prizes, starve their frequency. The product is conserved; only the *experience* differs.

And the experiences could not be more different. Low volatility is a warm bath. High volatility is a series of droughts interrupted by lightning. The latter is, by a wide margin, the more addictive — because human memory is built around peaks and endings, not averages, and a player who once hit 2,500× will remember that single moment with hallucinatory clarity and forget the two hundred dead spins that paid for it. The volatility setting is sold as catering to taste. It is actually catering to *which flavour of cognitive bias you are most susceptible to.*

### The bonus menagerie, or: how to disguise variance as a gift

Bonus features are where a great deal of a machine's RTP budget is spent, and where a great deal of its psychological work is done. Each one is a small, self-contained drama whose purpose is to make the long flat stretches between wins feel like a journey toward something rather than what they actually are: a slow, statistically guaranteed bleed. Let us take them in turn.

**Free spins.** Triggered by landing a certain number of scatter symbols, a free-spins round grants the player a batch of spins — typically 10 to 25 — often with a multiplier of 2× or 3× applied to any wins. The word "free" is doing enormous work here. The spins cost the house nothing it has not already accounted for; the expected value of the entire round is baked into the machine's RTP. During free spins, machines frequently switch to a looser strip to deliver an exciting flurry of wins, knowing the overall session mathematics still balance to target. You are not being given a gift. You are being shown a trailer for a film you will never be allowed to finish.

**The pick bonus.** A screen of hidden prizes — twelve boxes, say — from which the player chooses a handful, revealing cash amounts. It *feels* like agency, like skill, like the player's choices matter. They do not. The prize pool is generated in advance, scaled by the machine's current state. In our implementation, when the engine knows it has been underpaying (correction below −0.2), the pool is inflated by 40%; when overpaying, it is shrunk by 30%. The prizes are then shuffled to random positions, so that whichever boxes you "choose," you are simply drawing from a distribution the machine has already decided upon. The pick bonus is a magic trick in which you are convinced you forced the card.

**The multiplier wheel.** A small chance — 3% on any win, in our build — to spin a wheel that multiplies the win by anywhere from 2× to 10×, the larger multipliers weighted to be far rarer. This is pure variance injection: a way to occasionally turn an ordinary win into a memorable one, manufacturing the peaks that memory clings to, all while contributing a precisely calculated and entirely modest amount to the overall return.

**Cascading reels, with progressive multipliers.** The most elegant and most dangerous of the lot. When a win lands, the winning symbols *vanish* and new symbols fall in to replace them — and the grid is evaluated again. If the new arrangement also wins, it too cascades. A single spin can chain into a cascade of five, six, seven consecutive wins. And here is the hook: each successive cascade *increases a progressive multiplier.* In our high-volatility profile, the cascade multipliers run 1×, 2×, 4×, 8×, 15×, 25× — so a long chain multiplies its final wins by twenty-five.

The mathematics is what makes this insidious. Because the base game must hit its RTP target *including* the expected value of cascades, the base paytable is calibrated *tighter* than it would otherwise be. The cascades are not a bonus layered on top of a fair game — they are a redistribution. The machine takes some of your ordinary wins away and bundles them into rare, spectacular, dopaminergic cascade chains. It concentrates the same total return into fewer, larger, more memorable events. It is, in the most literal sense, manufacturing peaks at the expense of the plateau — and peaks are what keep you spinning.

### The mathematics of the crowd, or: why some players must win

Now we return to the thought I asked you to hold. This is the part Ziegler gestures at with his multiplayer simulation, and it deserves to be stated as starkly as possible, because it is the mechanism by which an enterprise that *mathematically cannot* let the average player profit nonetheless advertises, truthfully, that people win.

Run one player for a few spins and luck dominates; the outcome is nearly a coin-flip around the RTP. Run one player for ten thousand spins and the RTP assert itself with the grim reliability of a tide — that player will end up down very close to 3.5% of everything they wagered. This is the law of large numbers, and it is the house's most loyal employee.

But now run *ten thousand players at once*, each for a modest session, which is exactly what an online casino is. The law of large numbers now applies to the *casino*, not to any individual. The casino's total take converges beautifully to its 3.5% edge. But the *distribution* of individual outcomes is wide and right-skewed: most players lose, a meaningful minority break roughly even, and a small, glittering handful win — some of them spectacularly. The mean sits below break-even. The mode sits below break-even. But the *tail* extends into genuine profit, and the people in that tail are real, and their winnings are real, and the casino will photograph them holding novelty cheques.

This is the deepest sleight of hand in the entire industry, and it requires no lying at all. "Players win every day" is *true.* "You could be next" is *true.* What goes unsaid is that for every player in the shining tail, the silent left side of the distribution has already paid for the cheque several times over — and that the casino does not care in the slightest *which* players win, because it is not betting against any of them individually. It is harvesting the variance of the entire crowd, and skimming its fixed percentage off the top of the churn. As Ziegler puts it with admirable economy: it doesn't matter who wins or loses, as long as the house keeps the fees. Every pound may eventually leave the system. The house keeps a piece of every pound on its way through.

The winners are not evidence that you can beat the house. The winners *are the house's marketing budget*, paid for entirely by the losers, and distributed by mathematics so that no one need feel personally responsible for handing out the loss.

---

## Part the Third: The Devil's Own Toybox

We come to the main event. Everything so far has been mathematics in service of the house edge — sophisticated, yes, but at least operating on the honest terrain of *odds*. What follows operates on a different terrain entirely: your perception, your memory, your nervous system. These are not techniques for changing what happens. They are techniques for changing *how what happens feels* — and feeling, not fact, is what governs whether you take the next spin.

I have catalogued every one we built. I have tried to give you the mathematics wherever mathematics is what's doing the deceiving, and the psychology where psychology is the whole of it. Steel yourself, my darlings. It is quite a collection.

### 1. Near-Miss Architecture

The machine displays a result that *almost* won — two jackpot symbols on the payline and the third sitting tantalisingly just above or below it — far more often than random chance would produce. The reels are weighted so that high-value symbols appear disproportionately in the non-winning positions adjacent to the line.

The mathematics is the tell. On a fair reel, the probability of a symbol landing one position off the payline equals its probability of landing on it. Near-miss engineering breaks this symmetry deliberately: the top symbol is made common in the row *above* the payline and rare *on* it. The player sees "so close!" at a frequency that has nothing to do with how close they actually were.

The cruelty is that the brain processes a near-miss almost identically to a win. Functional imaging shows the same reward circuitry lighting up. A near-miss is registered by your nervous system as encouragement — *you're getting warmer* — when in fact each spin is independent and you were never warm at all. It is the only architecture I know of designed specifically to make *failure* feel like *progress*.

### 2. Losses Disguised as Wins

The signature trick of the multiline era, and the one I'd nominate as the single most insidious. You bet £1 across, say, twenty lines. One line hits and pays £0.30. The machine erupts — lights, a triumphant sound, "WIN £0.30!" splashed across the screen. You have just lost seventy pence. The machine has just congratulated you for it.

The mathematics that enables this is simply the multiline structure: when your stake is spread across many lines, a single small hit returns *something*, and that something is presented with the full pageantry of victory regardless of whether it exceeds your total stake. Studies put the frequency of these "losses disguised as wins" at 30 to 40% of all spins on twenty-line machines. The player's physiological response — skin conductance, heart rate — is indistinguishable from a genuine win. Your body cannot tell the difference. The machine is counting on it.

The honest correction is trivial: show the *net*. "Won £0.30, staked £1.00, net −£0.70." We built exactly this toggle. Flip it on and the machine becomes suddenly, bracingly truthful. Flip it off and you are back in the casino, being applauded for your losses. The gap between those two experiences is the entire trick.

### 3. The "Stop" Button Illusion

A button that lets you slam the reels to a halt mid-spin. It feels like control — like skill, like timing, like *you* are landing the symbols. It is the most complete illusion in the building, because the outcome was sealed the instant you pressed spin. The stop button changes nothing. It merely skips the animation.

There is no mathematics here because there is no effect to model. That is precisely the point. The button is a placebo with a satisfying click, and research finds that players who use it bet more and play longer, having been convinced — at a level beneath conscious reasoning — that their dexterity matters. It is the gambling equivalent of the "close door" button in a lift, which in most lifts is connected to nothing whatsoever and exists solely to give the anxious something to press.

### 4. Celebration Asymmetry and Scaling

Wins are celebrated; losses are met with silence. And the celebrations *scale*: a small win gets a modest chime, a large win gets a screen-filling, sound-drenched, several-second extravaganza. There is a continuous ladder of spectacle, calibrated to the size of the win.

The asymmetry is the manipulation. Because losses produce no memorable event and wins produce escalating ones, your memory of a session is systematically distorted toward the wins. You will walk away genuinely believing you did better than you did — not because you are foolish, but because the machine has curated your memory for you, deleting the losses from the highlight reel and scoring the wins like a film climax. Memory is built from salient events. The machine controls which events are salient.

### 5. Credit Obfuscation and Bet Normalisation

The machine displays your money not as currency but as *credits.* Your £5 becomes 500 credits. A £1 bet becomes 100 credits.

This is a tax on your loss-aversion, and it works because abstraction blunts pain. "Five hundred credits" does not trigger the same protective flinch as "five pounds," even though they are identical. It is the same reason casinos have always used chips rather than cash, and the same reason it is easier to spend on a card than to hand over notes. Every layer of abstraction between you and the real money makes the real money easier to lose. The credit display is a small, deliberate act of psychological anaesthesia.

### 6. Bet Complexity Hiding

A close cousin. The machine shows you the cost *per line* rather than the total. "Just 13 pence a line!" — when you are playing eight lines and each spin actually costs £1. The true stake is obscured behind a smaller, friendlier number, and the multiplication is left for you to perform, which — in the warm, urgent, sound-saturated environment of active play — you will not.

The mathematics is a single multiplication the machine performs and then declines to show you. The per-line figure is technically accurate, which is what makes it such an elegant lie. It tells the truth about a part in order to deceive you about the whole.

### 7. Disguising Time Spent

There are no clocks on a casino floor and no windows to the world outside. Online, the machine simply omits any indication of how long you have been playing. The session timer, if it exists at all, is buried.

Time is the resource you are actually spending — spins per minute times minutes is money — and the machine works to dissolve your awareness of its passage entirely. A player who does not know they have been playing for three hours will play for a fourth. The omission is not an oversight. It is architecture.

### 8. Variable Ratio Reinforcement

This is the deep psychology beneath the entire enterprise, and it has a name from the behavioural laboratory. A *variable ratio reinforcement schedule* — rewards delivered after an unpredictable number of actions — is the single most powerful pattern for producing persistent, compulsive behaviour that B.F. Skinner ever documented. It is more durable than rewarding every action, and far more durable than rewarding on a fixed schedule. A pigeon on a variable ratio schedule will peck a lever until it collapses.

A slot machine *is* a variable ratio schedule, rendered in chrome and light. You do not know which spin will pay, only that some spin will, eventually. This unpredictability is not a side effect of randomness — it is the active ingredient. Every other trick in this catalogue is, in a sense, an amplifier bolted onto this one fundamental exploit. The machine is a Skinner box that has been to finishing school.

### 9. Drip Feed / Slow Bleed

The machine is tuned to return *small* amounts *frequently* rather than large amounts rarely (this is the low-volatility profile from Part the Second, deployed deliberately). The effect is that your balance descends in a gentle, jagged, almost imperceptible decline — a little back, a little more lost, a little back — rather than dropping in alarming lumps.

The mathematics is the same RTP, redistributed for minimal alarm. A player who loses £50 in two sudden £25 hits feels the loss sharply and may stop. A player who loses the same £50 across two hundred spins of small wins and slightly larger losses barely registers it at all. The slow bleed keeps you below the threshold of pain right up until the balance reads zero.

### 10. Phantom Wins on Inactive Lines

A win is shown — symbols align, the line lights up — on a line you did not bet on. The machine celebrates the alignment without paying you, because you hadn't activated that line. The implication, delivered without a word, is unmistakable: *if only you'd bet more lines, that would have been yours.*

It is an advertisement for a larger stake, disguised as a near-triumph, and it costs the machine nothing because no money changes hands. It is the phantom limb of slot design — a win you can see and almost feel, attached to nothing.

### 11. Sunk Cost Framing

The machine reminds you, subtly and constantly, of what you have already invested. Progress bars toward a bonus. "You're so close!" A meter that fills as you play. All of it whispers the oldest fallacy in economics: *you've put in so much, you can't stop now.*

The sunk cost fallacy is the irrational belief that past investment justifies future investment, when a clear-eyed actor considers only future prospects. The machine cultivates it assiduously, because a player who feels they have "built up" something — progress, a near-bonus, a sense of being owed — is a player who will not walk away. Every pound already lost is reframed as a reason to risk another.

### 12. Ambient Sound Design

Sound bypasses conscious thought and goes straight to the limbic system, and slot machines exploit this with a composer's precision. Wins are scored in a major key, ascending, triumphant. Losses are silent. The result is asymmetric audio reinforcement that, like celebration asymmetry, curates your emotional memory of the session toward the wins.

But it goes further. The constant ambient hum, the musical stings, the rising arpeggios on a near-miss — all of it maintains a state of low-grade arousal that keeps you engaged and blunts your judgement. Some machines play *win sounds during losses disguised as wins*, so that a net loss arrives wrapped in triumphant music. The sound is not decoration. It is a second channel of manipulation, running in parallel with the visuals, addressed to a part of your brain that does not deliberate.

### 13. Spin Speed Manipulation

The faster the spins, the more of them per minute, and spins per minute times the house edge times your stake is the rate at which you lose money. Machines are tuned for rapid play, and many offer a "turbo" mode that strips out the animations entirely. Faster spins are sold as convenience. They are, in fact, a direct multiplier on your loss rate.

The mathematics is brutally simple. At a 3.5% edge and £1 spins, ten spins a minute bleeds 35 pence a minute; sixteen spins a minute bleeds 56. The turbo button does not change your odds on any spin. It changes how many spins fit into the hour you have unknowingly committed to losing.

### 14. Bonus Teasing

The machine shows you the bonus you *almost* triggered — two of the three required scatters, the third drifting agonisingly past — and dangles meters and "anticipation" animations that suggest the bonus is imminent. In our geospatial version, a "flight meter" fills as you play, implying the bonus is charging up.

Here is the lie, stated plainly: in our honest implementation, that meter is *connected to nothing.* It fills based on spins-since-last-bonus plus random noise, and has no relationship whatsoever to the actual trigger, which is determined independently. The meter could read 95% and the bonus could be two hundred spins away. It exists solely to manufacture the sensation of approaching a reward, so that you keep playing through the dry stretch toward a finish line that recedes as you approach it.

### 15. Progressive Jackpots

A jackpot that grows with every bet placed across the network, displayed in enormous, ticking, ever-rising numerals. A small fraction of each wager — 1.5% in our build — is skimmed into the pool. The growing number creates urgency: *it's so high now, surely it's about to go.*

The mathematics that defeats the intuition: the probability of triggering the jackpot is *independent of the pool size.* A £2,000,000 jackpot is no likelier to land than a £200,000 one. The number's growth tells you nothing about your odds — it is pure theatre, engineered to produce fear of missing out. And the skim itself is quietly removed from the base game's RTP, so the jackpot is not a gift from the house but a tax on every player, pooled and paid back to one. The ticking number is the most hypnotic object on the screen, and it is hypnotising you with information that is, for decision-making purposes, entirely meaningless.

### 16. Gambler's Fallacy Exploitation

The machine actively encourages the belief that past results predict future ones. "Hot" and "cold" indicators. Streak displays. "Bonus due!" meters. In our build, a heat gauge announces "HOT ZONE" after a few wins and "DOLDRUMS" after a few losses, and a message murmurs that you're "due."

You are not due. This is the gambler's fallacy in its purest form: each spin is independent, and the machine's RNG has no memory of what came before. "Hot" makes you stay to ride a streak that does not exist; "cold" makes you stay because a win is "owed," which it is not. The indicators read your recent history — which is real — and then frame it as *prediction* — which is a lie. Both framings have the same purpose: to convince you that *the next spin* is the important one. It always is, and it never is.

(There is a delicious irony buried in Part the Second: the machine's *own* correction engine genuinely does apply a small sympathy loosening after a long losing streak — so the "you're due" message is occasionally, accidentally, slightly true. But not for the reason the player thinks, not reliably, and never enough to overcome the edge. The machine has arranged for a superstition to be just barely correlated with reality, which is the most effective way to keep a superstition alive.)

### 17. Multiline Bet Confusion

Modern machines offer bewildering arrays of line and stake combinations — 20 lines at varying per-line bets, multipliers, "ways to win" numbering in the hundreds. The complexity is not a feature for the player's benefit. It is a fog.

The confusion serves two ends. First, it obscures the true cost per spin (see Bet Complexity Hiding). Second, and more subtly, it makes the expected value of any given configuration genuinely difficult to compute on the fly, so that a player cannot easily reason about what they are actually risking or what they can actually expect back. A game simple enough to analyse is a game you might decline to play. Complexity is camouflage, and the machine wears a great deal of it.

### 18. Autoplay Acceleration

The autoplay feature, which spins repeatedly without input, is frequently tuned to run *faster* than manual play. Same odds, same RTP — but more spins per minute, and therefore a higher loss rate. In our build, autoplay runs with roughly 40% less delay between spins than manual play.

It is the spin-speed trick again, automated and disguised as convenience. The player who switches on autoplay believes they are saving effort. They are, in fact, accelerating their losses while simultaneously removing the small moments of friction — the pause before each manual spin — at which they might have reconsidered and stopped. Autoplay does not just speed up the game. It removes the exits.

---

That is eighteen. There are more — the industry is nothing if not inventive — but those are the load-bearing ones, and every single one of them survives contact with the cold light of mathematics. None of them changes your odds. All of them change your behaviour. And behaviour, in the end, is the only variable the house actually needs to control, because the odds were settled in its favour before you ever sat down.

---

## Part the Fourth: The Machine, in Rust

I promised you the code, and I am a woman of my word. We built the entire apparatus — every trick above — as a real, deployable web application: a Rust engine using the Axum framework, serving a browser front-end that is purely a display layer. All the mathematics runs on the server, where the player cannot reach it. This is itself a small honesty the commercial operators share: you genuinely cannot tamper with a slot engine you cannot see.

I'll show you the sections that matter, lightly narrated. Rust is a famously exacting language, and there is something bracing about watching a psychological exploit reduced to a function that either compiles or does not.

### The correction engine

The heart of Part the Second. Note the four windows blended at lines computing `s`, `m`, `l`, `a`; the sigmoid; and the streak modifiers reading like a list of emotional pressure points — because that is exactly what they are.

```rust
fn calc_correction(&self) -> (String, f64, f64, HashMap<String, f64>, Vec<String>) {
    // Four clocks: 20-spin, 100-spin, 500-spin, all-time windows
    let len = self.spin_history.len();
    let s = calc(&self.spin_history[len.saturating_sub(20)..]);
    let m = calc(&self.spin_history[len.saturating_sub(100)..]);
    let l = calc(&self.spin_history[len.saturating_sub(500)..]);
    let a = calc(&self.spin_history);

    // Weighted blend — the 500-spin window dominates
    let wr = s * 0.1 + m * 0.25 + l * 0.35 + a * 0.3;
    let dev = wr - TARGET_RTP;

    // The sigmoid: smooth, inevitable correction toward target
    let sig = (1.0 / (1.0 + (-SIGMOID_K * dev).exp()) - 0.5) * 2.0;

    // Session modifiers — the machine performing sympathy and cooling
    let mut sm = 0.0;
    if self.consecutive_losses > 12 { sm -= 0.15; }       // sympathy
    else if self.consecutive_losses > 6 { sm -= 0.08; }   // "don't go"
    if self.consecutive_wins > 4 { sm += 0.12; }          // cooling
    let ssb = self.spin_count.saturating_sub(self.last_bonus_spin);
    if ssb > 120 { sm -= 0.06; }                          // bonus drought

    let f = (sig + sm).clamp(-1.0, 1.0);
    let cfg = if f < -0.3 { "loose" } else if f > 0.3 { "tight" } else { "standard" };
    // ... returns the chosen reel configuration
}
```

Eighteen lines of arithmetic decide, every spin, exactly how generous to be. There is no malice in the code. The malice is in the specification.

### Volatility via strip weighting

The three reel configurations — the tight-clustering-versus-wide-spread lever from Part the Second. Read the numbers: `loose` is thick with high-value symbols (`eiffel`, `kremlin`, `globe` wilds), `tight` is starved of them.

```rust
fn strip_weights(config: &str) -> Vec<(&'static str, u32)> {
    match config {
        "loose" => vec![("desert",6),("ocean",6),/*...*/("eiffel",2),("kremlin",2),
                        ("globe",3),("plane",2)],   // generous: more wilds, more bonus
        "tight" => vec![("desert",10),("ocean",10),/*...*/("eiffel",1),("kremlin",1),
                        ("globe",1),("plane",1)],    // stingy: filler-heavy
        _ => vec![/* standard: the balanced middle */],
    }
}
```

The correction engine picks the key; this function is the lock it turns.

### The dynamic bonus radius

Our geospatial twist, and a clean illustration of bonus-drought relief. Each spin generates random coordinates; if they fall within `radius` kilometres of a real landmark, the bonus triggers. And the radius *breathes* with the correction factor:

```rust
let radius = (BASE_BONUS_RADIUS * (1.0 - corr * 0.6)).clamp(45.0, 300.0);
```

When the machine is underpaying (`corr` negative), the radius widens — up to 300 km — and bonuses land more often. When overpaying, it contracts to as little as 45 km. The "luck" of landing near the Eiffel Tower is, quietly, a function of how much the machine currently wishes to pay you.

### Losses disguised as wins

The classification that makes the single most insidious trick possible. Three lines decide whether to applaud you:

```rust
let outcome = if total_win <= 0.0 { "LOSS" }
    else if total_win < self.bet { "LDW" }      // won something, but less than you staked
    else { "WIN" };

match outcome {
    "LDW" => { self.ldw_count += 1; self.ldw_lost += self.bet - total_win; }
    // ... the front-end celebrates LDW identically to WIN — unless honesty mode is on
}
```

Note that the engine *tracks* the deception — `ldw_count`, `ldw_lost` — so that our educational front-end can later show the player exactly how much they lost while being congratulated. The commercial machines track the same numbers. They simply never show you.

### The random multiplier and the jackpot skim

Variance injection and the progressive-jackpot tax, two lines apart:

```rust
// 3% chance on any win to multiply it — manufacturing memorable peaks
let multiplier = if payline_total > 0.0 && rng.gen_bool(0.03) {
    [2.0, 3.0, 5.0][rng.gen_range(0..3)]
} else { 1.0 };

// 1.5% of every bet skimmed into the progressive pool — the tax that funds the dream
let jp = self.bet * 0.015;
self.jackpot_pool += jp;
```

### The fake meter

And finally, my favourite piece of honest dishonesty — the bonus-teasing meter that is connected to nothing. In our front-end, the "flight meter" that appears to fill toward the bonus is computed like this:

```javascript
// This meter LOOKS like it predicts the bonus. It predicts nothing.
const flightMeter = (spinsSinceBonus / 150) + randomNoise;
// The actual bonus trigger is the Haversine coordinate check — entirely separate.
```

The meter and the trigger share no causal connection whatsoever. The meter is theatre. We left a comment in the code saying so, which is a courtesy the industry has never once extended to its players.

---

## A Closing Word, Before You Go

Here is what I find genuinely remarkable, my darlings, having now taken the entire machine apart on the workbench and named every gear.

*None of the tricks are necessary to win.* The house edge alone — that demure 3.5% — guarantees the casino's profit with the patience of geology. If slot machines did nothing but spin fair reels at an honest RTP, the house would still win, inexorably, forever. The mathematics of Part the First is, by itself, completely sufficient to part you from your money.

Everything in Part the Third — every near-miss, every disguised loss, every silent defeat and screaming victory, every fake meter and accelerated autoplay — exists not to *win* but to make you *stay*. The edge ensures the house profits from each pound that passes through. The skulduggery ensures more pounds pass through, faster, from a player who feels, the entire time, that they are having a wonderful time and might just be about to win.

That is the part the polite version leaves out. The house edge is a fact of mathematics, neutral as gravity. The dark patterns are a series of deliberate choices, made by designers who understand human psychology with surgical precision and deploy it against the specific cognitive frailties that make us human: our memory's love of peaks, our weakness for near-misses, our terrible instinct that we are *due.* The maths explains why you lose. The manipulation explains why you don't leave.

Ziegler ended his fine article with a meditation on what gambling means — economically a transfer of wealth from many to few, sociologically a machine for repetition and loss. I will end mine more simply. The Prince of Morocco, faced with three caskets and a fortune riding on his choice, reached for the gold one because it glittered. Inside he found a skull and a scroll, and the scroll told him what the scroll always tells everyone who reaches for the shining thing:

*All that glisters is not gold.*

The reels glitter, my darlings. They are engineered, down to the photon and the decibel, to glitter. But you have now seen the skull inside the casket — the self-correcting engine, the curated memory, the eighteen exquisite little lies. And a trick you can see is a trick that has lost its power.

Spin if you like. It can be a perfectly pleasant way to spend an evening, provided you bring an amount you've decided in advance to lose and you treat its disappearance as the price of the lights and the sound. But do it knowing precisely what is being done to you, and by whom, and how. Do it with your eyes open.

That, in the end, is the only edge they cannot take back.

---

*Claudia G. Petersen writes about the mathematics hiding inside everyday things. The slot machine described here — Around the World in 80 Days — is a real, working educational simulator built in Rust, with every manipulation technique toggle-able on and off, so that anyone may feel the precise difference between the casino and the truth. No real money is involved. That part, at least, we kept honest.*
