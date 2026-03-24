import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import matplotlib.pyplot as plt

from logger import setup_logger
from parser import parse_log
from model import detect_anomalies
from report import save_report
import json
import os

logger = setup_logger()

with open("config.json", "r") as f:
    config = json.load(f)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Log Anomaly Detector")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f6f8")

        self.file_path = ""

        self.style = ttk.Style()
        self.style.theme_use("default")

        self.configure_styles()
        self.create_widgets()

    def configure_styles(self):
        # Buttons style (світліші + “rounded effect” через padding)
        self.style.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=8
        )

        # Treeview style
        self.style.configure(
            "Treeview",
            background="white",
            foreground="black",
            rowheight=25,
            fieldbackground="white"
        )

        self.style.configure(
            "Treeview.Heading",
            background="#e0e0e0",
            foreground="black"
        )

    def create_widgets(self):
        # ===== TOP FRAME =====
        top_frame = tk.Frame(self.root, bg="#f4f6f8")
        top_frame.pack(pady=15)

        self.file_label = tk.Label(
            top_frame,
            text="No file selected",
            bg="#f4f6f8",
            fg="#333",
            font=("Segoe UI", 11)
        )
        self.file_label.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(top_frame, bg="#f4f6f8")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Load Log File",
            command=self.load_file,
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            padx=12,
            pady=6,
            relief="flat"
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Analyze",
            command=self.analyze,
            bg="#2196F3",
            fg="white",
            activebackground="#1976D2",
            padx=12,
            pady=6,
            relief="flat"
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="Exit",
            command=self.root.quit,
            bg="#f44336",
            fg="white",
            activebackground="#d32f2f",
            padx=12,
            pady=6,
            relief="flat"
        ).grid(row=0, column=2, padx=5)

        # ===== TABLE =====
        table_frame = tk.Frame(self.root, bg="#f4f6f8")
        table_frame.pack(fill="both", expand=True, padx=15, pady=15)

        columns = ("time", "level", "value", "anomaly")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ===== STATUS BAR =====
        self.status = tk.Label(
            self.root,
            text="Ready",
            bg="#eaeaea",
            fg="#333",
            anchor="w"
        )
        self.status.pack(fill="x", side="bottom")

    def load_file(self):
        self.file_path = filedialog.askopenfilename()

        if self.file_path:
            self.file_label.config(text=os.path.basename(self.file_path))
            self.status.config(text="File loaded")
            logger.info(f"Loaded file: {self.file_path}")

    def analyze(self):
        if not self.file_path:
            messagebox.showwarning("Warning", "Please select a file first")
            return

        try:
            df = parse_log(self.file_path)
            df = detect_anomalies(df, config["contamination"])

            save_report(df)

            self.show_table(df)
            self.show_graph(df)

            self.status.config(text="Analysis completed")
            logger.info("Analysis completed")

        except Exception as e:
            logger.error(str(e))
            messagebox.showerror("Error", str(e))

    def show_table(self, df):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for _, row in df.iterrows():
            self.tree.insert("", "end", values=(
                row["time"],
                row["level"],
                row["value"],
                "YES" if row["anomaly"] == 1 else "NO"
            ))

    def show_graph(self, df):
        plt.style.use("seaborn-v0_8")

        plt.figure(figsize=(8, 4))

        plt.plot(df["value"], label="Values", linewidth=2)

        anomalies = df[df["anomaly"] == 1]

        plt.scatter(
            anomalies.index,
            anomalies["value"],
            color='red',
            s=50,
            label="Anomalies"
        )

        plt.title("Log Anomaly Detection", fontsize=14)
        plt.xlabel("Index")
        plt.ylabel("Value")

        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()