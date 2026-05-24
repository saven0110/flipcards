# ── app.py ────────────────────────────────────────────────────────────────────

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from constants import (
    BG, SURFACE, CARD_BG, CARD_FRONT,
    TEXT_LIGHT, TEXT_DIM, ACCENT,
    BTN_GREEN, BTN_RED, BTN_DARK,
    FONT_TITLE, FONT_SMALL, FONT_BTN, FONT_LABEL,
)
from data import load_data, save_data
from card_dialog import CardDialog
from study_window import StudyWindow

CARD_W    = 160   # tile width  (px)
CARD_H    = 110   # tile height (px)
CARD_GAP  = 12    # gap between tiles


class FlipCardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FlipCards")
        self.geometry("860x620")
        self.minsize(700, 520)
        self.configure(bg=BG)
        self.resizable(True, True)
        self.data = load_data()
        self._build_ui()

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        self.sidebar = tk.Frame(self, bg=SURFACE, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)
        self._build_sidebar()
        self._show_home()

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        tk.Label(self.sidebar, text="📚 FlipCards",
                 font=("Georgia", 15, "bold"), bg=SURFACE, fg=ACCENT, pady=18
                 ).pack(fill="x")
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10)
        tk.Label(self.sidebar, text="DECKS", font=("Helvetica", 9, "bold"),
                 bg=SURFACE, fg=TEXT_DIM, pady=8).pack(fill="x", padx=12, anchor="w")

        deck_frame = tk.Frame(self.sidebar, bg=SURFACE)
        deck_frame.pack(fill="both", expand=True)

        self.deck_canvas = tk.Canvas(deck_frame, bg=SURFACE, highlightthickness=0, borderwidth=0)
        sb = tk.Scrollbar(deck_frame, orient="vertical", command=self.deck_canvas.yview)
        self.deck_list_frame = tk.Frame(self.deck_canvas, bg=SURFACE)
        self.deck_list_frame.bind("<Configure>",
            lambda e: self.deck_canvas.configure(scrollregion=self.deck_canvas.bbox("all")))
        self.deck_canvas.create_window((0, 0), window=self.deck_list_frame, anchor="nw")
        self.deck_canvas.configure(yscrollcommand=sb.set)
        self.deck_canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        btn_frame = tk.Frame(self.sidebar, bg=SURFACE, pady=10)
        btn_frame.pack(fill="x", side="bottom")
        self._btn(btn_frame, "＋  New Deck", self._new_deck, BTN_GREEN).pack(fill="x", padx=12, pady=3)
        self._btn(btn_frame, "🏠  Home",     self._show_home, BTN_DARK ).pack(fill="x", padx=12, pady=3)
        self._refresh_deck_list()

    def _refresh_deck_list(self):
        for w in self.deck_list_frame.winfo_children():
            w.destroy()
        for name in self.data:
            self._deck_btn(name)

    def _deck_btn(self, name: str):
        f = tk.Frame(self.deck_list_frame, bg=SURFACE, cursor="hand2")
        f.pack(fill="x", padx=8, pady=2)

        count   = len(self.data.get(name, []))
        lbl     = tk.Label(f, text=f"  🗂  {name}", font=FONT_SMALL, bg=SURFACE,
                           fg=TEXT_LIGHT, anchor="w", pady=6)
        lbl.pack(side="left", fill="x", expand=True)
        cnt_lbl = tk.Label(f, text=str(count), font=("Helvetica", 9), bg=SURFACE, fg=TEXT_DIM)
        cnt_lbl.pack(side="right", padx=6)

        menu = tk.Menu(self, tearoff=0, bg="#1E2A45", fg=TEXT_LIGHT,
                       activebackground=ACCENT, activeforeground=TEXT_LIGHT,
                       font=FONT_SMALL, bd=0, relief="flat")
        menu.add_command(label="✎  Rename deck",  command=lambda n=name: self._rename_deck(n))
        menu.add_separator()
        menu.add_command(label="🗑  Delete deck",  command=lambda n=name: self._delete_deck(n))

        def show_menu(e):
            try:    menu.tk_popup(e.x_root, e.y_root)
            finally: menu.grab_release()

        all_w = [f, lbl, cnt_lbl]
        for w in all_w:
            w.bind("<Button-1>", lambda e, n=name: self._show_deck(n))
            w.bind("<Button-3>", show_menu)
            w.bind("<Button-2>", show_menu)

        def on_enter(e):
            for w in all_w: w.configure(bg="#1E2A45")
        def on_leave(e):
            for w in all_w: w.configure(bg=SURFACE)
        f.bind("<Enter>", on_enter)
        f.bind("<Leave>", on_leave)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _btn(self, parent, text, cmd, color=CARD_FRONT, fg=TEXT_LIGHT, **kw):
        return tk.Button(parent, text=text, font=FONT_BTN, bg=color, fg=fg,
                         activebackground=color, activeforeground=fg,
                         relief="flat", cursor="hand2", padx=10, pady=7,
                         command=cmd, **kw)

    def _clear_main(self):
        for w in self.main.winfo_children():
            w.destroy()

    # ── Home ──────────────────────────────────────────────────────────────────
    def _show_home(self):
        self._clear_main()
        total_decks = len(self.data)
        total_cards = sum(len(v) for v in self.data.values())
        tk.Label(self.main, text="Welcome back!",
                 font=("Georgia", 26, "bold"), bg=BG, fg=TEXT_LIGHT, pady=30).pack()
        tk.Label(self.main,
                 text=f"You have {total_decks} deck(s) and {total_cards} card(s) total.",
                 font=FONT_LABEL, bg=BG, fg=TEXT_DIM).pack()
        hint = ("Pick a deck from the sidebar to study or edit."
                if total_decks else "Create your first deck using '＋ New Deck'.")
        tk.Label(self.main, text=hint, font=FONT_SMALL, bg=BG, fg=TEXT_DIM, pady=6).pack()
        tk.Label(self.main, text="Tip: right-click a deck in the sidebar to rename or delete it.",
                 font=("Helvetica", 9, "italic"), bg=BG, fg=TEXT_DIM, pady=2).pack()

    # ── Deck view ─────────────────────────────────────────────────────────────
    def _show_deck(self, name: str):
        self._clear_main()
        cards = self.data.get(name, [])

        # Header
        hdr = tk.Frame(self.main, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(20, 6))
        tk.Label(hdr, text=f"🗂  {name}", font=FONT_TITLE, bg=BG, fg=TEXT_LIGHT).pack(side="left")

        # Action bar
        acts = tk.Frame(self.main, bg=BG)
        acts.pack(fill="x", padx=20, pady=4)
        self._btn(acts, "▶  Study",   lambda: self._study(name),    ACCENT   ).pack(side="left", padx=4)
        self._btn(acts, "＋ Add Card", lambda: self._add_card(name), BTN_GREEN).pack(side="left", padx=4)

        ttk.Separator(self.main, orient="horizontal").pack(fill="x", padx=20, pady=8)

        if not cards:
            tk.Label(self.main, text="No cards yet — add one above!",
                     font=FONT_LABEL, bg=BG, fg=TEXT_DIM).pack(pady=40)
            return

        # ── Scrollable grid of card tiles ─────────────────────────────────────
        container = tk.Frame(self.main, bg=BG)
        container.pack(fill="both", expand=True, padx=20, pady=4)

        canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
        sb     = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        grid_frame = tk.Frame(canvas, bg=BG)
        win_id = canvas.create_window((0, 0), window=grid_frame, anchor="nw")

        def _sync_width(e):
            canvas.itemconfig(win_id, width=e.width)
        def _sync_scroll(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
            self._reflow_grid(grid_frame, canvas)

        canvas.bind("<Configure>", lambda e: (
            canvas.itemconfig(win_id, width=e.width),
            self._reflow_grid(grid_frame, canvas)
        ))
        grid_frame.bind("<Configure>", _sync_scroll)

        def _wheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _wheel)

        # Store refs for reflow
        self._grid_frame  = grid_frame
        self._grid_canvas = canvas
        self._grid_cards  = []   # list of tile frames

        for i, card in enumerate(cards):
            tile = self._make_tile(grid_frame, name, i, card)
            self._grid_cards.append(tile)

        # Initial layout after idle so canvas has a real width
        self.after(50, lambda: self._reflow_grid(grid_frame, canvas))

    # ── Tile factory ──────────────────────────────────────────────────────────
    def _make_tile(self, parent, deck: str, idx: int, card: dict) -> tk.Frame:
        """Create a fixed-size card tile with hover-reveal edit/delete overlay."""
        tile = tk.Frame(parent, bg=CARD_BG,
                        width=CARD_W, height=CARD_H)
        tile.pack_propagate(False)   # enforce fixed size

        # Normal content
        content = tk.Frame(tile, bg=CARD_BG)
        content.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(content, text=card["front"], font=FONT_SMALL,
                 bg=CARD_BG, fg=TEXT_LIGHT, wraplength=CARD_W - 16,
                 justify="left", anchor="nw").pack(anchor="nw", padx=10, pady=(10, 2))
        tk.Label(content, text=card["back"], font=("Helvetica", 10),
                 bg=CARD_BG, fg=TEXT_DIM, wraplength=CARD_W - 16,
                 justify="left", anchor="nw").pack(anchor="nw", padx=10)

        # Hover overlay with Edit + Delete buttons
        overlay = tk.Frame(tile, bg="#0A2240")
        # (not placed until hover)

        edit_btn = tk.Button(overlay, text="✎  Edit", font=("Helvetica", 9, "bold"),
                             bg=BTN_DARK, fg=TEXT_LIGHT, activebackground=BTN_DARK,
                             relief="flat", cursor="hand2", padx=6, pady=4,
                             command=lambda i=idx, d=deck: self._edit_card(d, i))
        edit_btn.pack(fill="x", padx=10, pady=(28, 4))

        del_btn = tk.Button(overlay, text="🗑  Delete", font=("Helvetica", 9, "bold"),
                            bg=BTN_RED, fg=TEXT_LIGHT, activebackground=BTN_RED,
                            relief="flat", cursor="hand2", padx=6, pady=4,
                            command=lambda i=idx, d=deck: self._delete_card(d, i))
        del_btn.pack(fill="x", padx=10)

        def show_overlay(e):
            overlay.place(x=0, y=0, relwidth=1, relheight=1)
            overlay.lift()

        def hide_overlay(e):
            # Only hide if cursor truly left the tile
            wx, wy = tile.winfo_rootx(), tile.winfo_rooty()
            ww, wh = tile.winfo_width(), tile.winfo_height()
            mx, my = e.x_root, e.y_root
            if not (wx <= mx <= wx + ww and wy <= my <= wy + wh):
                overlay.place_forget()

        for w in [tile, content] + list(content.winfo_children()):
            w.bind("<Enter>", show_overlay)
            w.bind("<Leave>", hide_overlay)
        for w in [overlay, edit_btn, del_btn]:
            w.bind("<Enter>", show_overlay)
            w.bind("<Leave>", hide_overlay)

        return tile

    # ── Grid reflow ───────────────────────────────────────────────────────────
    def _reflow_grid(self, frame: tk.Frame, canvas: tk.Canvas):
        """Re-place tiles in a wrapping grid based on current canvas width."""
        tiles = self._grid_cards
        if not tiles:
            return

        canvas_w = canvas.winfo_width()
        if canvas_w <= 1:
            return

        cols = max(1, (canvas_w + CARD_GAP) // (CARD_W + CARD_GAP))

        for i, tile in enumerate(tiles):
            col = i % cols
            row = i // cols
            x = CARD_GAP + col * (CARD_W + CARD_GAP)
            y = CARD_GAP + row * (CARD_H + CARD_GAP)
            tile.place(x=x, y=y)

        # Update frame height so scrollregion is correct
        rows = (len(tiles) + cols - 1) // cols
        total_h = CARD_GAP + rows * (CARD_H + CARD_GAP)
        frame.configure(height=total_h)
        canvas.configure(scrollregion=(0, 0, canvas_w, total_h))

    # ── Deck CRUD ─────────────────────────────────────────────────────────────
    def _new_deck(self):
        name = simpledialog.askstring("New Deck", "Deck name:", parent=self)
        if not name: return
        name = name.strip()
        if name in self.data:
            messagebox.showwarning("Exists", f'"{name}" already exists.')
            return
        self.data[name] = []
        save_data(self.data)
        self._refresh_deck_list()
        self._show_deck(name)

    def _rename_deck(self, old_name: str):
        new_name = simpledialog.askstring("Rename", "New name:", parent=self)
        if not new_name or new_name.strip() == old_name: return
        new_name = new_name.strip()
        if new_name in self.data:
            messagebox.showwarning("Exists", f'"{new_name}" already exists.')
            return
        self.data[new_name] = self.data.pop(old_name)
        save_data(self.data)
        self._refresh_deck_list()
        self._show_deck(new_name)

    def _delete_deck(self, name: str):
        if not messagebox.askyesno("Delete", f'Delete deck "{name}" and all its cards?'): return
        del self.data[name]
        save_data(self.data)
        self._refresh_deck_list()
        self._show_home()

    # ── Card CRUD ─────────────────────────────────────────────────────────────
    def _add_card(self, deck: str):
        CardDialog(self, deck, None, None, self._on_card_saved)

    def _edit_card(self, deck: str, idx: int):
        CardDialog(self, deck, idx, self.data[deck][idx], self._on_card_saved)

    def _on_card_saved(self, deck: str, idx, front: str, back: str):
        if idx is None:
            self.data[deck].append({"front": front, "back": back})
        else:
            self.data[deck][idx] = {"front": front, "back": back}
        save_data(self.data)
        self._refresh_deck_list()
        self._show_deck(deck)

    def _delete_card(self, deck: str, idx: int):
        if not messagebox.askyesno("Delete Card", "Delete this card?"): return
        del self.data[deck][idx]
        save_data(self.data)
        self._refresh_deck_list()
        self._show_deck(deck)

    # ── Study ─────────────────────────────────────────────────────────────────
    def _study(self, deck: str):
        cards = self.data.get(deck, [])
        if not cards:
            messagebox.showinfo("Empty", "Add some cards first!")
            return
        StudyWindow(self, deck, cards)