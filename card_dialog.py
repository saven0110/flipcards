# ── card_dialog.py ────────────────────────────────────────────────────────────
# Modal dialog for creating or editing a single flashcard.

import tkinter as tk
from tkinter import messagebox
from constants import (
    BG, SURFACE, ACCENT, BTN_DARK,
    TEXT_LIGHT, TEXT_DIM,
    FONT_SMALL, FONT_BTN, FONT_LABEL,
)


class CardDialog(tk.Toplevel):
    """
    Popup window for adding or editing a card.

    Args:
        parent   : parent tkinter window
        deck     : name of the deck this card belongs to
        idx      : card index (None when adding a new card)
        card     : existing card dict {"front": ..., "back": ...} or None
        callback : called with (deck, idx, front, back) on save
    """

    def __init__(self, parent, deck: str, idx, card, callback):
        super().__init__(parent)
        self.deck     = deck
        self.idx      = idx
        self.callback = callback

        self.title("Edit Card" if idx is not None else "Add Card")
        self.geometry("480x320")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.grab_set()   # modal

        self._build(card)

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build(self, card):
        # Front input
        tk.Label(self, text="Front (Question)", font=FONT_LABEL,
                 bg=BG, fg=TEXT_DIM).pack(padx=20, anchor="w", pady=(18, 2))
        self.front_txt = tk.Text(
            self, height=4, font=FONT_SMALL,
            bg=SURFACE, fg=TEXT_LIGHT,
            insertbackground=TEXT_LIGHT, relief="flat", padx=8, pady=6,
        )
        self.front_txt.pack(fill="x", padx=20)

        # Back input
        tk.Label(self, text="Back (Answer)", font=FONT_LABEL,
                 bg=BG, fg=TEXT_DIM).pack(padx=20, anchor="w", pady=(12, 2))
        self.back_txt = tk.Text(
            self, height=4, font=FONT_SMALL,
            bg=SURFACE, fg=TEXT_LIGHT,
            insertbackground=TEXT_LIGHT, relief="flat", padx=8, pady=6,
        )
        self.back_txt.pack(fill="x", padx=20)

        # Pre-fill when editing
        if card:
            self.front_txt.insert("1.0", card["front"])
            self.back_txt.insert("1.0", card["back"])

        # Buttons
        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(fill="x", padx=20, pady=14)

        tk.Button(
            btn_row, text="Save", font=FONT_BTN,
            bg=ACCENT, fg=TEXT_LIGHT, activebackground=ACCENT,
            relief="flat", padx=14, pady=6, cursor="hand2",
            command=self._save,
        ).pack(side="right", padx=4)

        tk.Button(
            btn_row, text="Cancel", font=FONT_BTN,
            bg=BTN_DARK, fg=TEXT_LIGHT, activebackground=BTN_DARK,
            relief="flat", padx=14, pady=6, cursor="hand2",
            command=self.destroy,
        ).pack(side="right", padx=4)

    # ── Actions ───────────────────────────────────────────────────────────────
    def _save(self):
        front = self.front_txt.get("1.0", "end").strip()
        back  = self.back_txt.get("1.0", "end").strip()

        if not front or not back:
            messagebox.showwarning("Empty", "Both sides must have content.", parent=self)
            return

        self.destroy()
        self.callback(self.deck, self.idx, front, back)
