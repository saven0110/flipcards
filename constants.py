# ── constants.py ──────────────────────────────────────────────────────────────
# Edit this file to change colors, fonts, or the data file location.

import os

# Data storage
DATA_FILE = os.path.join(os.path.expanduser("~"), "flipcards_data.json")

# ── Colour palette ─────────────────────────────────────────────────────────────
BG         = "#1A1A2E"   # window background
SURFACE    = "#16213E"   # sidebar background
CARD_BG    = "#0F3460"   # card row background in deck view
CARD_FRONT = "#E94560"   # study card — question side
CARD_BACK  = "#533483"   # study card — answer side
TEXT_LIGHT = "#EAEAEA"   # primary text
TEXT_DIM   = "#8892A4"   # secondary / muted text
ACCENT     = "#E94560"   # logo accent & primary action
BTN_GREEN  = "#00B4D8"   # add / positive actions
BTN_RED    = "#FF6B6B"   # delete / destructive actions
BTN_DARK   = "#0F3460"   # neutral actions

# ── Typography ─────────────────────────────────────────────────────────────────
FONT_TITLE = ("Georgia",    22, "bold")
FONT_CARD  = ("Georgia",    20)
FONT_SMALL = ("Helvetica",  11)
FONT_BTN   = ("Helvetica",  10, "bold")
FONT_LABEL = ("Helvetica",  12)
