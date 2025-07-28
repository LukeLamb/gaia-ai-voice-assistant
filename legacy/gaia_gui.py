import tkinter as tk
from tkinter import ttk
from voice_agent import GaiaAgent

class GaiaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gaia - Local AI Assistant")
        self.root.geometry("700x500")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Logs Tab
        self.log_frame = tk.Frame(self.notebook)
        self.log_area = tk.Text(self.log_frame, wrap=tk.WORD, height=20, width=80)
        self.log_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.log_scroll = tk.Scrollbar(self.log_frame, command=self.log_area.yview)
        self.log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_area.config(yscrollcommand=self.log_scroll.set)
        self.notebook.add(self.log_frame, text="Logs")

        # Conversation Tab
        self.chat_frame = tk.Frame(self.notebook)
        self.chat_area = tk.Text(self.chat_frame, wrap=tk.WORD, height=20, width=80, bg="#f9f9f9")
        self.chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat_scroll = tk.Scrollbar(self.chat_frame, command=self.chat_area.yview)
        self.chat_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_area.config(yscrollcommand=self.chat_scroll.set)
        self.notebook.add(self.chat_frame, text="Conversation")

        # Status and Controls
        self.status_label = tk.Label(root, text="Status: Idle", font=("Arial", 12))
        self.status_label.pack(pady=5)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        self.start_button = tk.Button(btn_frame, text="Start Gaia", command=self.start_gaia, width=15, bg="green", fg="white")
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.pause_button = tk.Button(btn_frame, text="Pause Gaia", command=self.toggle_pause, width=15, bg="orange", fg="white")
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.stop_button = tk.Button(btn_frame, text="Stop Gaia", command=self.stop_gaia, width=15, bg="red", fg="white")
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.gaia_agent = GaiaAgent(log_callback=self.log_event)
        self.paused = False
        self.root.protocol("WM_DELETE_WINDOW", self.stop_gaia)

        self.log("Welcome to Gaia!")

    def start_gaia(self):
        if not self.gaia_agent.running:
            self.log("Starting Gaia...")
            self.status_label.config(text="Status: Listening")
            self.gaia_agent.start()

    def toggle_pause(self):
        if not self.gaia_agent.running:
            return
        if not self.paused:
            self.gaia_agent.pause()
            self.status_label.config(text="Status: Paused")
            self.pause_button.config(text="Resume Gaia")
        else:
            self.gaia_agent.resume()
            self.status_label.config(text="Status: Listening")
            self.pause_button.config(text="Pause Gaia")
        self.paused = not self.paused

    def stop_gaia(self):
        if self.gaia_agent.running:
            self.log("Stopping Gaia...")
            self.status_label.config(text="Status: Stopped")
            self.gaia_agent.stop()
        self.root.quit()

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def log_event(self, message):
        self.log(message)
        if message.lower().startswith("you said:"):
            self.chat_area.insert(tk.END, f"🧑 You: {message[9:].strip()}\n\n")
        elif message.lower().startswith("ai:"):
            self.chat_area.insert(tk.END, f"🤖 Gaia: {message[3:].strip()}\n\n")
        self.chat_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = GaiaGUI(root)
    root.mainloop()





