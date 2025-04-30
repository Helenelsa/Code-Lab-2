import tkinter as tk
from tkinter import messagebox
import requests
import html

# API Setup
API_URL = "https://opentdb.com/api.php"
API_PARAMETERS = {
    "amount": 10,
    "category": 15,
    "type": "boolean",
}

# Colors and Fonts
BG_COLOR = "#121212"
TEXT_COLOR = "#E0E0E0"
ACCENT_BLUE = "#00FFF7"
ACCENT_GREEN = "#00FF9F"
ACCENT_RED = "#FF004D"
BUTTON_YELLOW = "#FFD700"
FONT_HEADER = ("Orbitron", 20, "bold")
FONT_QUESTION = ("Courier New", 16, "bold")
FONT_BUTTON = ("Segoe UI", 14, "bold")

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 QuizWhiz - Cyber Challenge!")
        self.root.config(bg=BG_COLOR, padx=40, pady=30)
        self.root.resizable(False, False)

        self.questions = []
        self.score = 0
        self.current_question_index = 0
        self.timer = None
        self.time_left = 10

        self.create_widgets()

    def create_widgets(self):
        self.greeting_label = tk.Label(
            self.root,
            text="⚡ Welcome to Cyber QuizWhiz! ⚡\nPress 'Start' to dive in!",
            font=FONT_HEADER,
            fg=ACCENT_BLUE,
            bg=BG_COLOR,
            justify="center",
        )
        self.greeting_label.grid(column=1, row=0, columnspan=3, pady=20)

        self.score_label = tk.Label(
            self.root, text="Score: 0", font=FONT_HEADER, fg=ACCENT_GREEN, bg=BG_COLOR
        )
        self.score_label.grid(column=3, row=1)

        self.timer_label = tk.Label(
            self.root, text="", font=FONT_BUTTON, fg=BUTTON_YELLOW, bg=BG_COLOR
        )
        self.timer_label.grid(column=2, row=2, pady=10)

        self.question_card = tk.Canvas(
            self.root, bg="#1E1E1E", width=600, height=250, highlightthickness=0
        )
        self.question_card.grid(column=1, row=3, columnspan=3, pady=20)
        self.question_text = self.question_card.create_text(
            300, 125, text="", font=FONT_QUESTION, fill=TEXT_COLOR, width=500
        )

        self.start_button = self._create_button("🚀 Start Quiz", BUTTON_YELLOW, self.start_quiz)
        self.start_button.grid(column=2, row=4, pady=15)

        self.true_button = self._create_button("✔ TRUE", ACCENT_GREEN, lambda: self.check_answer(True))
        self.true_button.grid(column=1, row=4, padx=10, pady=10)
        self.true_button.grid_forget()

        self.false_button = self._create_button("✖ FALSE", ACCENT_RED, lambda: self.check_answer(False))
        self.false_button.grid(column=3, row=4, padx=10, pady=10)
        self.false_button.grid_forget()

        self.restart_button = self._create_button("🔁 Restart", BUTTON_YELLOW, self.restart_quiz)
        self.restart_button.grid(column=2, row=5, pady=15)
        self.restart_button.grid_forget()

    def _create_button(self, text, color, command):
        return tk.Button(
            self.root,
            text=text,
            font=FONT_BUTTON,
            fg=BG_COLOR,
            bg=color,
            activebackground=color,
            activeforeground="black",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            command=command
        )

    def fetch_questions(self):
        try:
            response = requests.get(API_URL, params=API_PARAMETERS, timeout=10)
            response.raise_for_status()
            data = response.json()
            if "results" in data:
                return [
                    {
                        "question": html.unescape(q["question"]),
                        "correct_answer": q["correct_answer"].lower() == "true",
                    }
                    for q in data["results"]
                ]
            else:
                raise ValueError("Unexpected response format.")
        except (requests.RequestException, ValueError) as e:
            messagebox.showerror("Error", f"Could not fetch questions: {e}")
            return []

    def start_quiz(self):
        self.questions = self.fetch_questions()
        if not self.questions:
            self.question_card.itemconfig(
                self.question_text,
                text="⚠ Could not load questions. Please try again later.",
            )
            return

        self.score = 0
        self.current_question_index = 0

        self.greeting_label.grid_forget()
        self.start_button.grid_forget()
        self.true_button.grid(column=1, row=4)
        self.false_button.grid(column=3, row=4)
        self.update_question()

    def update_question(self):
        if self.current_question_index >= len(self.questions):
            self.end_quiz()
        else:
            q = self.questions[self.current_question_index]
            self.question_card.itemconfig(self.question_text, text=q["question"])
            self.question_card.config(bg="#1E1E1E")
            self.time_left = 10
            self.start_timer()

    def start_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"⏳ {self.time_left} sec left")
            self.time_left -= 1
            self.timer = self.root.after(1000, self.start_timer)
        else:
            self.timer_label.config(text="⏰ Time’s up!")
            self.current_question_index += 1
            self.root.after(1000, self.update_question)

    def check_answer(self, user_answer):
        if self.timer:
            self.root.after_cancel(self.timer)
        correct = self.questions[self.current_question_index]["correct_answer"]
        self.question_card.config(bg=ACCENT_GREEN if user_answer == correct else ACCENT_RED)

        if user_answer == correct:
            self.score += 1

        self.score_label.config(text=f"Score: {self.score}")
        self.current_question_index += 1
        self.root.after(800, self.update_question)

    def end_quiz(self):
        self.true_button.grid_forget()
        self.false_button.grid_forget()
        self.restart_button.grid(column=2, row=5)

        self.question_card.itemconfig(
            self.question_text,
            text=f"🎉 All done!\nYour Score: {self.score} / {len(self.questions)}",
        )
        self.timer_label.config(text="")

    def restart_quiz(self):
        if self.timer:
            self.root.after_cancel(self.timer)
        self.restart_button.grid_forget()
        self.greeting_label.grid(column=1, row=0, columnspan=3, pady=20)
        self.start_button.grid(column=2, row=4)
        self.question_card.itemconfig(self.question_text, text="")
        self.score_label.config(text="Score: 0")
        self.timer_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

