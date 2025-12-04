#!/usr/bin/env python3
"""
Dank / Gen-Z Password Strength & Crack-Time Checker (PyQt5)
- Live strength meter
- Length counter
"""

import sys
import string
import math
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QLabel, QPushButton, QProgressBar, QTextEdit, QGroupBox
)

# ---- password analysis helpers ----

def estimate_charset_size(pwd: str) -> int:
    has_lower = any(c.islower() for c in pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_special = any(c in string.punctuation for c in pwd)

    size = 0
    if has_lower:
        size += 26
    if has_upper:
        size += 26
    if has_digit:
        size += 10
    if has_special:
        size += len(string.punctuation)
    return size

def pretty_time(seconds: float) -> str:
    if seconds < 1:
        return "less than a second"
    mins = seconds / 60
    hours = mins / 60
    days = hours / 24
    years = days / 365

    if seconds < 60:
        return f"{seconds:.0f} seconds"
    if mins < 60:
        return f"{mins:.1f} minutes"
    if hours < 48:
        return f"{hours:.1f} hours"
    if days < 365:
        return f"{days:.1f} days"
    if years < 100:
        return f"{years:.1f} years"
    if years < 1_000_000:
        return f"{years:.1f} years (aka ages)"
    return "astronomically long (math flex only)"

def rough_crack_time(pwd: str, score: int) -> str:
    if not pwd:
        return "n/a (no password yet)"

    charset = estimate_charset_size(pwd)
    if charset == 0:
        return "n/a (no valid characters)"

    comb_log10 = len(pwd) * math.log10(charset)
    guesses_per_sec = 1e9
    seconds_log10 = comb_log10 - math.log10(2 * guesses_per_sec)

    if seconds_log10 > 300:
        seconds = float("inf")
    else:
        seconds = 10 ** seconds_log10

    if score <= 2:
        if len(pwd) < 8:
            return "likely seconds to a few minutes with common attack tools"
        elif len(pwd) < 12:
            return "maybe minutes to hours, but still easy if it's a real word / pattern"
        else:
            return "hours at best; weak patterns or leaked lists can make it much faster"
    elif score == 3:
        return "roughly hours to days in pure brute‑force, less if based on real words or patterns"
    elif score == 4:
        return "days to months in brute‑force math; decent against casual attackers"
    else:
        if seconds == float("inf"):
            return "astronomically long with pure brute‑force (theoretical math only)"
        return pretty_time(seconds)

def evaluate_password(pwd: str):
    length_ok = len(pwd) >= 8
    has_lower = any(c.islower() for c in pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_special = any(c in string.punctuation for c in pwd)

    score = sum([length_ok, has_lower, has_upper, has_digit, has_special])

    charset = estimate_charset_size(pwd)
    if pwd and charset:
        _entropy_bits = len(pwd) * math.log2(charset)

    crack_text = rough_crack_time(pwd, score)

    if len(pwd) == 0:
        verdict = "Type something bruh 👀 (no ghosting the input)."
        label = "Idle"
        color = "#808080"
    elif score <= 2:
        verdict = "Full L password 😵‍💫\nEzz to crack, attackers farming you for XP."
        label = "Weak"
        color = "#ff4d4f"
    elif score == 3:
        verdict = "Low‑key mid 😶\nNot trash, but still not main‑character energy."
        label = "Okay‑ish"
        color = "#ffa940"
    elif score == 4:
        verdict = "Valid password ngl 💯\nAlmost dank, add a bit more spice."
        label = "Strong‑ish"
        color = "#fadb14"
    else:
        verdict = "DANK W password 🔐🔥\nBrute‑force scripts just rage quit."
        label = "Peak"
        color = "#52c41a"

    details = []
    details.append(f"Length ≥ 8: {'✅' if length_ok else '❌'} (no baby passwords'NOOB')")
    details.append(f"Lowercase letter: {'✅' if has_lower else '❌'}")
    details.append(f"Uppercase letter: {'✅' if has_upper else '❌'} (CAPS = extra drip)")
    details.append(f"Number: {'✅' if has_digit else '❌'} (digits = extra armor)")
    details.append(f"Special char (!@#$ etc.): {'✅' if has_special else '❌'} (symbols = true sigma move)")
    details.append("")
    details.append(
        "It would take, in a pure brute‑force math world : "
        f"{crack_text}"
    )

    return {
        "score": score,
        "label": label,
        "color": color,
        "verdict": verdict,
        "details": "\n".join(details),
        "length": len(pwd)
    }

# ---- main GUI ----

class PasswordCheckerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Checker Tool 🔐")
        self.resize(1100, 700)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0e27, stop:0.5 #1a1f3a, stop:1 #0f1729);
                color: #e5e7eb;
                font-family: 'Segoe UI', 'Ubuntu', 'Roboto', sans-serif;
            }
            QLineEdit {
                padding: 12px 14px;
                min-height: 38px;
                border-radius: 8px;
                border: 2px solid #2d3748;
                background-color: #1a202c;
                color: #e5e7eb;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #06b6d4;
                background-color: #111827;
            }
            QPushButton {
                padding: 8px 14px;
                border-radius: 6px;
                background-color: #1f2937;
                color: #e5e7eb;
                border: 1.5px solid #2d3748;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #374151;
                border: 1.5px solid #06b6d4;
            }
            QGroupBox {
                border: 2px solid #2d3748;
                border-radius: 8px;
                margin-top: 10px;
                background-color: rgba(30, 41, 59, 0.6);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
                color: #06b6d4;
                font-weight: bold;
                font-size: 13px;
            }
            QTextEdit {
                background-color: #1a202c;
                border-radius: 8px;
                border: 2px solid #2d3748;
                color: #e5e7eb;
                padding: 10px;
                font-size: 16px;    /* bigger details font */
            }
            QProgressBar {
                border: 2px solid #2d3748;
                border-radius: 6px;
                background-color: #0f172a;
                height: 22px;
            }
            QProgressBar::chunk {
                border-radius: 4px;
                background-color: #ef4444;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Cyb3R P@ss T00L 🧪⚡")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #06b6d4; letter-spacing: 2px;")

        subtitle = QLabel("Real‑time strength & cyber‑vibes ")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #9ca3af; font-size: 12px;")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        input_group = QGroupBox("Input 🔤")
        input_v = QVBoxLayout()
        input_v.setSpacing(10)

        pwd_row = QHBoxLayout()
        self.pwd_input = QLineEdit()
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.setPlaceholderText("Type your password here buddy")
        self.pwd_input.setMinimumHeight(40)

        self.eye_btn = QPushButton("👁")
        self.eye_btn.setCheckable(True)
        self.eye_btn.setFixedWidth(40)
        self.eye_btn.setToolTip("Show / hide password")

        pwd_row.addWidget(self.pwd_input)
        pwd_row.addWidget(self.eye_btn)

        length_row = QHBoxLayout()
        self.length_label = QLabel("Length: 0")
        self.length_label.setStyleSheet("color: #9ca3af; font-size: 12px;")
        length_row.addWidget(self.length_label)
        length_row.addStretch()

        input_v.addLayout(pwd_row)
        input_v.addLayout(length_row)
        input_group.setLayout(input_v)
        main_layout.addWidget(input_group)

        strength_group = QGroupBox("Strength Meter 📊")
        strength_h = QHBoxLayout()
        strength_left = QVBoxLayout()

        self.strength_label = QLabel("Status: Idle (no sauce yet)")
        self.strength_label.setStyleSheet("color: #e5e7eb; font-weight: 600; font-size: 14px;")

        self.bar = QProgressBar()
        self.bar.setRange(0, 5)
        self.bar.setValue(0)
        self.bar.setTextVisible(False)

        self.verdict_label = QLabel("Start typing to get the vibe check 👇")
        self.verdict_label.setWordWrap(True)
        v_font = QFont()
        v_font.setPointSize(13)          
        v_font.setBold(True)
        self.verdict_label.setFont(v_font)
        self.verdict_label.setStyleSheet("color: #e5e7eb;")

        strength_left.addWidget(self.strength_label)
        strength_left.addWidget(self.bar)
        strength_left.addWidget(self.verdict_label)

        strength_h.addLayout(strength_left, 2)
        strength_group.setLayout(strength_h)
        main_layout.addWidget(strength_group)

        details_group = QGroupBox("Details & Glow‑Up Tips ✨")
        details_layout = QVBoxLayout()
        self.details_box = QTextEdit()
        self.details_box.setReadOnly(True)
        self.details_box.setMinimumHeight(130)
        details_layout.addWidget(self.details_box)
        details_group.setLayout(details_layout)
        main_layout.addWidget(details_group)

        privacy = QLabel(
            "Your passwords are never stored. Privacy and security are our top priorities."
        )
        privacy.setAlignment(Qt.AlignCenter)
        privacy.setStyleSheet("color: #6b7280; font-size: 11px; padding-top: 5px;")
        main_layout.addWidget(privacy)

        self.setLayout(main_layout)

        self.pwd_input.textChanged.connect(self.update_strength)
        self.eye_btn.toggled.connect(self.toggle_password_visibility)

        self.update_strength()

    def toggle_password_visibility(self, checked: bool):
        if checked:
            self.pwd_input.setEchoMode(QLineEdit.Normal)
            self.eye_btn.setText("🙈")
        else:
            self.pwd_input.setEchoMode(QLineEdit.Password)
            self.eye_btn.setText("👁")

    def update_strength(self):
        pwd = self.pwd_input.text()
        result = evaluate_password(pwd)

        self.length_label.setText(f"Length: {result['length']}")
        self.bar.setValue(result["score"])
        self._set_bar_color(result["color"])

        self.strength_label.setText(f"Status: {result['label']}")
        self.verdict_label.setText(result["verdict"])
        self.details_box.setPlainText(result["details"])

    def _set_bar_color(self, hex_color: str):
        self.bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid #2d3748;
                border-radius: 6px;
                background-color: #0f172a;
                height: 22px;
            }}
            QProgressBar::chunk {{
                border-radius: 4px;
                background-color: {hex_color};
            }}
        """)

def main():
    app = QApplication(sys.argv)

    # Make global font larger
    base_font = app.font()
    base_font.setPointSize(11) 
    app.setFont(base_font)

    gui = PasswordCheckerGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
