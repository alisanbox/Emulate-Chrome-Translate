# Emulate-Chrome-Translate
# Auto Translate & Scroll Tool

> Open → Right-Click → Translate → Auto-Scroll → Save
> Uses Chrome's built-in translation + OS-level keypress to trigger menu

======================================================================
✅ WHAT THIS TOOL DOES
======================================================================

Automates your exact manual workflow:
  1. Opens local .txt / .html files directly in Chrome
  2. Right-clicks → opens Chrome's native context menu
  3. Sends "T" key DIRECTLY to Chrome (OS-level, not Selenium)
  4. Auto-scrolls PageDown until ACTUAL bottom reached
  5. Waits 10 seconds → extracts FULL translated text
  6. Saves with smart renaming: CH_xxx.txt → EN_xxx.txt, JP→EN

WHY THIS WORKS:
  Selenium cannot send keys to Chrome's native menu.
  pyautogui sends keys at OS level → Chrome receives them → menu works.

======================================================================
✨ FEATURES
======================================================================

  - Auto language detection (Chrome detects CN/JP automatically)
  - Accurate bottom detection (tracks scroll position, NOT height)
  - Smart rename: CH→EN, JP→EN, case-insensitive
  - Configurable timing (all delays at top of script)
  - Minimum scroll safety (always scroll at least 10 times)
  - Wait-after-scroll (configurable pause before saving)
  - Works on local files only (file:/// URLs)

======================================================================
🛠️ INSTALLATION
======================================================================

1. Install dependencies:
   pip install selenium pyautogui

2. Create 2 folders alongside the script:
   your_script.py
   to_translate/       <- PUT YOUR FILES HERE (.txt / .html)
   translated/         <- Output saved here automatically

3. Run:
   python translate_script.py

======================================================================
⚙️ CONFIGURATION (ALL SETTINGS AT TOP OF SCRIPT)
======================================================================

INPUT_FOLDER       = "to_translate"      <- Source folder
OUTPUT_FOLDER      = "translated"       <- Output folder

WINDOW_WIDTH       = 300                <- Chrome window width
WINDOW_HEIGHT      = 900                <- Chrome window height

PAGEDOWN_WAIT      = 0.6                <- Seconds after each PageDown
RIGHTCLICK_WAIT    = 1.2                <- Wait after right-click BEFORE T
WAIT_AFTER_T       = 7.0                <- Wait for translation to start
WAIT_AFTER_SCROLL  = 10.0               <- Wait at bottom BEFORE saving

BOTTOM_CONFIRM_COUNT = 3                 <- Confirm bottom X times
MIN_SCROLLS        = 10                  <- Minimum PageDown presses

--- TUNING GUIDE ---
  Menu opens but T does nothing?  -> RIGHTCLICK_WAIT = 1.8
  Translation slow?              -> WAIT_AFTER_T = 10.0
  Stops scrolling early?         -> MIN_SCROLLS = 15
  Bottom text missing?            -> WAIT_AFTER_SCROLL = 15.0
  Fast enough? Try decreasing:   -> PAGEDOWN_WAIT = 0.5

======================================================================
📖 STEP-BY-STEP WORKFLOW
======================================================================

  1. Open File    -> Chrome loads your local text file
  2. Right-Click  -> Chrome's native menu OPENS
  3. Send T Key   -> OS-level keypress -> Menu receives T -> TRANSLATE STARTS
  4. Auto-Scroll  -> PageDown until scroll position stops changing
  5. Wait         -> Pause 10s -> ensure ALL text fully translated
  6. Save         -> Rename CH/JP->EN -> write to output folder

======================================================================
🔬 TECHNICAL LOGIC
======================================================================

WHY pyautogui INSTEAD OF SELENIUM KEYS:
  Selenium send_keys() -> goes to webpage ONLY
  Chrome native menu -> cannot receive it -> IGNORED
  pyautogui.press("t") -> sent at OS level -> Chrome receives -> WORKS

BOTTOM DETECTION:
  OLD (FAILED): measure scrollHeight -> NEVER changes on long text -> STOPS EARLY
  NEW (WORKS): track window.pageYOffset -> actual scroll position -> STOPS ONLY WHEN MOVEMENT STOPS

FILENAME RENAMING RULES:
  CH_c1-100.txt    -> EN_c1-100.txt
  JP_novel.txt     -> EN_novel.txt
  ch_chapter5.txt  -> en_chapter5.txt
  JP_Volume2.html  -> EN_Volume2.html
  unknown.txt      -> unknown_en.txt (appends _en if no CH/JP found)

======================================================================
⚠️ IMPORTANT NOTES
======================================================================

  - Google Chrome must be installed on your system
  - DO NOT touch Chrome window while script runs
  - Works on LOCAL FILES ONLY (.txt / .html)
  - Internet required (Chrome fetches translation data)
  - First run may be slower — let Chrome fully load

======================================================================
📁 EXAMPLE
======================================================================

  to_translate/
      CH_Volume1.txt
      JP_Chapter5.txt

  [RUN SCRIPT]

  translated/
      EN_Volume1.txt
      EN_Chapter5.txt

======================================================================
🚀 TROUBLESHOOTING
======================================================================

  Menu opens but nothing happens? -> Increase RIGHTCLICK_WAIT to 1.8
  Translation incomplete?         -> Increase WAIT_AFTER_T to 10.0
  Stops too early?                -> Increase MIN_SCROLLS to 15
  Bottom text missing?            -> Increase WAIT_AFTER_SCROLL to 15.0

======================================================================
📋 REQUIREMENTS
======================================================================

  - Python 3.7+
  - Google Chrome (latest)
  - selenium >= 4.0
  - pyautogui >= 0.9

======================================================================
Built to work around Chrome's automation detection which blocks
translate bar and internal APIs. Uses OS-level keypress because
Selenium cannot interact with native Chrome UI elements.
======================================================================
