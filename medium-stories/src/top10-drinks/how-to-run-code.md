[I'm afraid i have to make an assumption here - even though you're reading this bit so you're interested in getting the code running, we'll assume you're using win10/11, and can cope with a little bit of the scary idea of opening the rabbithole that is a 'CMD terminal'. And don't worry, i'm keeping it simple as possible - lot's of automatic self installing things where possible and a nice simple 'venv' environment for python.]


1. For the python code;

Installing Python 3.12 via Winget (a 'Package Manager' Built-in to win10/11 -i.e. it does it for you):
Win10/11 ships with winget (if not, it'll auto-fetch from MS Store). This pulls the official Python from python.org, pre-configured for 'PATH' and 'scripts'.

Click the start button, type `cmd` and select command prompt, then when it pops up, type:
```cmd
winget install --id Python.Python.3.12
```

Post-install:
Close & reopen CMD (you  need to do this because the CMD terminal window won't know where to find the stuff you just installed otherwise - i.e. it's to refresh 'PATH'.)

It's wise to verify it installed right by typing
```cmd
python --version
```
It should echo `Python 3.12.x`.
(If winget gripes (rare on modern Win), as a fallback you can download the installer from python.org/downloads, run it, check "Add Python to PATH" during setup.)


Step 1: Creating a 'venv'
Next you'll need to create a project folder and 'environment' to run the python scripts in:

Open/re-open CMD and type:
```cmd
mkdir C:\code\top10-drinks
cd C:\code\top10-drinks
```

Then we create the venv (this forges the isolated env dir)
```cmd
python -m venv venv
```

This spins up venv/ with its own Scripts/ (for binaries), Lib/ (for site-packages), and Include/ — a self-contained Python realm.

Step 2: Activate the Venv
Activation hooks the env's Python/binaries to your 'shell session' — you'll see your prompt prefixed with (venv) for visual cue.
So, to run 'activate' (note the backslashes for Win paths; runs activate.bat)
```cmd
venv\Scripts\activate.bat
```
Your prompt morphs: (venv) C:\code\top10-drinks>.

Step 3: Install Dependencies and Use the Env
NumPy for data, Pandas for structuring, Matplotlib for rendering, Seaborn for polish.
```cmd
pip install numpy pandas matplotlib seaborn
```

You should see the screen blur with scrolling displays of things being installed.
Once it's finished installing all the deps you're ready to run the python scripts.

copy the code in the python code blocks previously in the article, paste each piece of code into a `.txt` file and then rename the file `<filename>.py` and save in `C:/code/top10-drinks/`

To run a given script, type in a CMD terminal after navigating to `C:/code/top10-drinks` and ensuring the `venv` is activated - look for the (venv) before the prompt - the following:
```cmd
Python <filename>.py
```

When you hit [enter] your script should run and results will follow!


2. For the Rust code;

Installing Rust via Rustup (The Official Rust Toolchain Manager)
Rustup 'bootstraps' the compiler, Cargo (Rust's build system, akin to Python's pip but with 'borrow-checked' safety), and std libs.

Download `rustup-init.exe` from `rust-lang.org/tools/install`, then:

As above, open a CMD terminal window, then type: 
```cmd
cd C:/Users/<insert username>/Downloads
rustup-init.exe -y
```

The -y auto-accepts defaults (stable toolchain, adds to 'PATH').

Post-install:
Close & reopen CMD, verify byt typing the follwing in a CMD terminal:
```cmd
rustc --version
```
it'll echo something like, e.g., "rustc 1.82.0"

Also in CMD terminal type 
```cmd
cargo --version
```




Navigate to your to your project workspace (e.g., ~/projects or C:\dev), then invoke:
```cmd
cargo new market-sim --bin
```

This scaffolds:

- `market_sim/` (the root dir)
  - `Cargo.toml` (a manifest, like a package.json but for Rust's edition-aware compilation)
  - `src/` (source dir)
    - `main.rs` (entry point, where your code lives)
  - `.gitignore` (standard exclusions for git [you can ignore this])

Cargo defaults to a "Hello, world!" in `main.rs` which is where Rust stores scripts so we'll overwrite the default `src/main.rs` with the full, complete code from earlier in the article — it's self-contained, compiles cleanly under edition 2021, and should run fine.

you'll also need to put some actual content into `cargo.toml` - past this into `cargo.toml`:
(This code uses only std. crates [no external crates], so the manifest is minimal. Cargo auto-generates this on init, but to be sure, here's the exact, complete content — paste it into Cargo.toml)
```
[package]
name = "market-sim"
version = "0.1.0"
edition = "2021"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]
```

This sets you for ready to compile our `market-sim` artifact.


Breakdown for Your Learning:
- `[package]`: Defines the crate metadata. `name` is your binary/executable name (run as `market-sim` post-build). `version` starts semantic; `edition = "2021"` enables modern Rust features like const generics — safe for this code.
- `[dependencies]`: Empty here, as we're pure std. If we were to add crates later (e.g., `rand = "0.8.5"` for stochastic market chaos), we would declare them here; Cargo fetches them during `cargo build`.
- No `[lib]` section needed — this is `--bin` for a binary, not a library crate.

Finally, to compile and run:

From the project root (C:/Users/<insert username>/Downloads/top10-drinks/market-sim/):
```cmd
cargo build  # Compiles debug build
cargo run    # Builds and executes, printing the sim outputs
```

That should be it - you should now be seeing, on screen in the terminal window, the exact output i used for this article!

---
