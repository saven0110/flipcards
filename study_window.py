# ── study_window.py ───────────────────────────────────────────────────────────

import tkinter as tk
from tkinter import messagebox
import random
from constants import (
    BG, CARD_BACK, CARD_FRONT, TEXT_LIGHT, TEXT_DIM,
    FONT_CARD, FONT_BTN, BTN_DARK, ACCENT,
)


class StudyWindow(tk.Toplevel):
    """
    Study mode window. Cards are shuffled on open.
    Click the card (or Space) to flip. ← / → or buttons to navigate.
    """

    def __init__(self, parent, deck_name: str, cards: list):
        super().__init__(parent)
        self.title(f"Studying: {deck_name}")
        self.geometry("620x440")
        self.minsize(500, 380)
        self.configure(bg=BG)

        self.cards   = list(cards)
        self.index   = 0
        self.flipped = False
        random.shuffle(self.cards)

        self._build()
        self._show_card()

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build(self):
        self.header = tk.Label(self, font=("Helvetica", 11), bg=BG, fg=TEXT_DIM)
        self.header.pack(pady=(16, 4))

        card_frame = tk.Frame(self, bg=BG)
        card_frame.pack(fill="both", expand=True, padx=30, pady=6)

        self.card_canvas = tk.Canvas(card_frame, bg=BG,
                                     highlightthickness=0, cursor="hand2")
        self.card_canvas.pack(fill="both", expand=True)
        self.card_canvas.bind("<Button-1>",  lambda e: self._toggle_flip())
        self.card_canvas.bind("<Configure>", self._on_resize)

        self.hint = tk.Label(self, text="Click card to flip  (or press Space)",
                             font=("Helvetica", 9, "italic"), bg=BG, fg=TEXT_DIM)
        self.hint.pack()

        nav = tk.Frame(self, bg=BG)
        nav.pack(pady=12)

        self.prev_btn = tk.Button(
            nav, text="◀  Prev", font=FONT_BTN,
            bg=BTN_DARK, fg=TEXT_LIGHT, activebackground=BTN_DARK,
            relief="flat", padx=14, pady=7, cursor="hand2",
            command=self._prev,
        )
        self.prev_btn.pack(side="left", padx=6)

        tk.Button(
            nav, text="🔀  Shuffle", font=FONT_BTN,
            bg=CARD_BACK, fg=TEXT_LIGHT, activebackground=CARD_BACK,
            relief="flat", padx=14, pady=7, cursor="hand2",
            command=self._shuffle,
        ).pack(side="left", padx=6)

        # Next button — always enabled; label changes on last card
        self.next_btn = tk.Button(
            nav, text="Next  ▶", font=FONT_BTN,
            bg=BTN_DARK, fg=TEXT_LIGHT, activebackground=BTN_DARK,
            relief="flat", padx=14, pady=7, cursor="hand2",
            command=self._next,
        )
        self.next_btn.pack(side="left", padx=6)

        self.bind("<Left>",  lambda e: self._prev())
        self.bind("<Right>", lambda e: self._next())
        self.bind("<space>", lambda e: self._toggle_flip())

    # ── Card rendering ────────────────────────────────────────────────────────
    def _draw_card(self, text: str, color: str, label: str):
        c = self.card_canvas
        c.delete("all")
        w = c.winfo_width()  or 560
        h = c.winfo_height() or 250
        r = 18

        pts = [r, 0, w-r, 0, w, r, w, h-r, w-r, h, r, h, 0, h-r, 0, r]
        c.create_polygon(pts, fill=color, smooth=True)
        c.create_text(18, 14, text=label, anchor="nw",
                      font=("Helvetica", 8, "bold"), fill="white")
        c.create_text(w // 2, h // 2, text=text, font=FONT_CARD,
                      fill=TEXT_LIGHT, width=w - 60, justify="center")
        c.create_text(w - 14, h - 12, text="↩", anchor="se",
                      font=("Helvetica", 14), fill="white")

    def _on_resize(self, _event=None):
        if not self.cards:
            return
        card = self.cards[self.index]
        if self.flipped:
            self._draw_card(card["back"],  CARD_BACK,  "ANSWER")
        else:
            self._draw_card(card["front"], CARD_FRONT, "QUESTION")

    # ── Navigation ────────────────────────────────────────────────────────────
    def _show_card(self):
        total      = len(self.cards)
        is_last    = self.index == total - 1
        self.header.config(text=f"Card {self.index + 1} of {total}")
        self.flipped = False
        self._draw_card(self.cards[self.index]["front"], CARD_FRONT, "QUESTION")
        self.hint.config(text="Click card to flip  (or press Space)")

        # Prev: disabled on first card
        self.prev_btn.config(state="normal" if self.index > 0 else "disabled")

        # Next: always enabled — label signals "done" on last card
        if is_last:
            self.next_btn.config(text="Done  ✓", bg=ACCENT)
        else:
            self.next_btn.config(text="Next  ▶", bg=BTN_DARK)

    def _toggle_flip(self):
        card = self.cards[self.index]
        if not self.flipped:
            self._draw_card(card["back"],  CARD_BACK,  "ANSWER")
            self.hint.config(text="Click again to flip back")
            self.flipped = True
        else:
            self._draw_card(card["front"], CARD_FRONT, "QUESTION")
            self.hint.config(text="Click card to flip  (or press Space)")
            self.flipped = False

    def _next(self):
        if self.index < len(self.cards) - 1:
            self.index += 1
            self._show_card()
        else:
            # Last card — ask to restart or close
            restart = messagebox.askyesno(
                "Deck complete!",
                "You've gone through all the cards.\n\nShuffle and go again?",
                parent=self,
            )
            if restart:
                self._shuffle()
            else:
                self.destroy()

    def _prev(self):
        if self.index > 0:
            self.index -= 1
            self._show_card()

    def _shuffle(self):
        random.shuffle(self.cards)
        self.index = 0
        self._show_card()