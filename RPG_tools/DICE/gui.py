import tkinter as tk
from tkinter import messagebox
from rpg_dan import DiceRollStorage


class DiceRollerGUI(tk.Tk):
    """Simple interface for storing and rolling dice expressions."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Gerenciador de Rolagens")
        self._build_widgets()
        self.refresh_rolls()

    def _build_widgets(self) -> None:
        tk.Label(self, text="Nome da rolagem:").grid(row=0, column=0, sticky="e")
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Expressão:").grid(row=1, column=0, sticky="e")
        self.expr_entry = tk.Entry(self)
        self.expr_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self, text="Salvar", command=self.save_roll).grid(
            row=0, column=2, rowspan=2, padx=5, pady=5
        )

        self.rolls_list = tk.Listbox(self)
        self.rolls_list.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)

        tk.Button(self, text="Rolar", command=self.roll_selected).grid(
            row=2, column=2, padx=5, pady=5, sticky="n"
        )

        self.result_var = tk.StringVar()
        tk.Label(self, textvariable=self.result_var).grid(
            row=3, column=0, columnspan=3, pady=(5, 0)
        )

    def refresh_rolls(self) -> None:
        """Refresh the listbox with current stored rolls."""
        self.rolls_list.delete(0, tk.END)
        rolls = DiceRollStorage.list_rolls()
        if isinstance(rolls, dict):
            items = [f"{name}: {expr}" for name, expr in rolls.items()]
        else:
            items = rolls
        for item in items:
            self.rolls_list.insert(tk.END, item)

    def save_roll(self) -> None:
        """Save a new roll using the provided name and expression."""
        name = self.name_entry.get().strip()
        expression = self.expr_entry.get().strip()
        if not name or not expression:
            messagebox.showwarning(
                "Entrada inválida", "Nome e expressão são obrigatórios."
            )
            return
        DiceRollStorage.add_roll(name, expression)
        self.name_entry.delete(0, tk.END)
        self.expr_entry.delete(0, tk.END)
        self.refresh_rolls()

    def roll_selected(self) -> None:
        """Roll the selected item from the listbox and show the total."""
        selection = self.rolls_list.curselection()
        if not selection:
            messagebox.showinfo("Seleção", "Selecione uma rolagem para executar.")
            return
        selected = self.rolls_list.get(selection[0])
        if ":" in selected:
            name = selected.split(":", 1)[0].strip()
        else:
            name = selected.strip()
        total = DiceRollStorage.roll(name)
        self.result_var.set(f"Total: {total}")


if __name__ == "__main__":
    app = DiceRollerGUI()
    app.mainloop()
