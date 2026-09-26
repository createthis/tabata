# tabatha.py — 10s lead-in, 8 rounds × (20s work + 10s rest), with real beeps on Mac
import time, sys, subprocess

ROUNDS, WORK, REST, LEAD = 8, 20, 10, 5
VOICE = False  # set True to also hear "work" / "rest" spoken aloud

MAC = "/System/Library/Sounds/"
MAC_MAP = {"tick": "Tink.aiff", "work": "Hero.aiff", "rest": "Basso.aiff",
           "end": "Ping.aiff", "go": "Glass.aiff", "done": "Hero.aiff"}
WIN_MAP = {"tick": (1000, 80), "work": (800, 150), "rest": (500, 300),
           "end": (1500, 400), "go": (2500, 600), "done": (2000, 600)}

def cue(name):
    """Named sound cue. Mac plays real system sounds via afplay (non-blocking)."""
    if sys.platform == "darwin":
        subprocess.Popen(["afplay", MAC + MAC_MAP[name]],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif sys.platform == "win32":
        import winsound
        f, ms = WIN_MAP[name]
        winsound.Beep(f, ms)
    else:
        print('\a', end='', flush=True)  # terminal bell fallback

def speak(word):
    if VOICE and sys.platform in ("darwin", "linux"):
        subprocess.Popen(["say", word],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def countdown(sec, label):
    for i in range(sec, 0, -1):
        if i <= 3: cue("tick")          # ticks on last 3 seconds
        print(f"\r{label} {i:2d}  ", end=""); time.sleep(1)
    cue("end")                          # end-of-phase chime

# ---- 10-second lead-in ----
print("Get ready — start in 10...")
for i in range(LEAD, 0, -1):
    print(f"\rLead-in {i:2d}  ", end=""); time.sleep(1)
cue("go")  # long high beep: round 1 is about to start

# ---- work/rest rounds ----
for r in range(1, ROUNDS + 1):
    print(f"Round {r}/{ROUNDS}")
    cue("work"); speak("work")          # high beep = work starts
    countdown(WORK, "WORK")
    if r < ROUNDS:
        cue("rest"); speak("rest")      # long low beep = rest starts
        countdown(REST, "REST")

print("Done! Total time: 4:00")
cue("done")
