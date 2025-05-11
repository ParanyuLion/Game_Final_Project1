import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class GraphApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="news")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.frame_select = ttk.LabelFrame(self, text="Select Graph Type")
        self.frame_select.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        self.cb_graph = ttk.Combobox(self.frame_select, state="readonly", width=50)
        self.cb_graph['values'] = (
            'Pie Chart - Enemy Defeated',
            'Line Chart - Level Completed',
            'Histogram - Items Bought',
            'Bar Graph - Enemy Defeated per Minute',
            'Boxplot - Score per Minute',
            'Table - Minute Stats',
        )
        self.cb_graph.bind('<<ComboboxSelected>>', self.update_plot)
        self.cb_graph.grid(row=0, column=0, padx=10, pady=10)

        self.btn_quit = ttk.Button(self, text="Quit", command=self.master.destroy)
        self.btn_quit.grid(row=2, column=0, pady=10)

        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="news")

        self.table_frame = ttk.Frame(self)
        self.table_frame.grid(row=0, column=0, sticky="news", padx=10, pady=(0, 10))

        self.tree = ttk.Treeview(self.table_frame, show='headings')
        self.scrollbar_y = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)

        self.tree.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")

    def display_dataframe(self, df: pd.DataFrame):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(df.columns)

        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def update_plot(self, event=None):
        graph_type = self.cb_graph.get()

        self.fig.clf()
        self.ax = self.fig.add_subplot()

        self.canvas.get_tk_widget().grid_remove()
        self.table_frame.grid_remove()

        if "Pie Chart" in graph_type:
            df = pd.read_csv("data_record/enemy_defeated.csv")
            counts = df["enemy_type"].value_counts()
            self.ax.pie(counts.values, labels=counts.index, autopct='%1.1f%%')
            self.ax.set_title("Enemy Defeated Ratio")
            self.canvas.get_tk_widget().grid()

        elif "Line Chart" in graph_type:
            df = pd.read_csv("data_record/level_complete.csv")
            level_counts = df["level_complete"].value_counts().sort_index()
            self.ax.plot(level_counts.index, level_counts.values, marker='o', color='teal')
            self.ax.set_title("Number of Times Each Level Was Completed")
            self.ax.set_xlabel("Level")
            self.ax.set_ylabel("Frequency")
            self.ax.grid(True)
            self.canvas.get_tk_widget().grid()

        elif "Histogram" in graph_type:
            df = pd.read_csv("data_record/item_bought.csv")
            item_counts = df["item_name"].value_counts()
            item_counts.plot(kind='bar', ax=self.ax, color='skyblue', edgecolor='black')
            self.ax.set_title("Histogram of Items Bought")
            self.ax.set_xlabel("Item Name")
            self.ax.set_ylabel("Count")
            self.ax.tick_params(axis='x', rotation=45)
            self.canvas.get_tk_widget().grid()

        elif "Bar Graph" in graph_type:
            df = pd.read_csv("data_record/game_stats_per_min.csv")
            grouped = df.groupby("minutes")["enemy_defeated_per_min"].mean()
            grouped.plot(kind="bar", ax=self.ax, color="lightcoral", edgecolor="black")
            self.ax.set_title("Average Enemy Defeated per Minute by Time")
            self.ax.set_xlabel("Minutes")
            self.ax.set_ylabel("Average Count")
            self.ax.tick_params(axis='x', rotation=0)
            self.canvas.get_tk_widget().grid()

        elif "Boxplot" in graph_type:
            df = pd.read_csv("data_record/game_stats_per_min.csv")
            self.ax.boxplot(df["score_per_min"], vert=False, patch_artist=True,
                            boxprops=dict(facecolor='lightgreen'))
            self.ax.set_title("Score per Minute")
            self.ax.grid(True, axis='y', linestyle='--', alpha=0.6)
            self.canvas.get_tk_widget().grid()

        elif "Table - Minute Stats" in graph_type:
            df = pd.read_csv("data_record/game_stats_per_min.csv")
            grouped_df = df.groupby("minutes").mean().reset_index()
            grouped_df["minutes"] = grouped_df["minutes"].astype(int)
            grouped_df = grouped_df.round(2)
            self.display_dataframe(grouped_df.head(30))
            self.table_frame.grid()

        self.fig.tight_layout()
        self.canvas.draw()


def run_graph_window():
    root = tk.Tk()
    root.title("Game Stats - Graph Viewer")
    root.geometry("900x700")
    app = GraphApp(root)
    root.mainloop()
