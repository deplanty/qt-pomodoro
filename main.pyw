#!.venv/Scripts/pythonw

import enum
import sys

from PySide2.QtCore import Qt, QSize, QTimer, QThread
from PySide2.QtGui import QPalette, QColor, QFontDatabase
from PySide2.QtWidgets import QApplication, QMainWindow

from src.tools import Chrono
import src.preload as pl

from main_ui import MainWindowUI


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(None, Qt.WindowStaysOnTopHint)

        self.n_pomodoro = 0  # Number of pomodoro processed
        self.selection = str()
        self.chrono = Chrono()

        self.timer = QTimer()
        self.timer.setInterval(100)  # ms
        self.timer.timeout.connect(self._on_timer_timeout)

        self.thread = QThread()

        self.setWindowTitle("Pomodoro")
        self.setFixedSize(QSize(300, 200))
        self.load_styles()

        self.ui = MainWindowUI(self)
        self.ui.btn_pomodoro.clicked.connect(self._on_btn_pomodoro_clicked)
        self.ui.btn_short_br.clicked.connect(self._on_btn_short_br_clicked)
        self.ui.btn_long_br.clicked.connect(self._on_btn_long_br_clicked)
        self.ui.btn_start_pause.clicked.connect(self._on_btn_start_pause_clicked)
        self.ui.btn_next.clicked.connect(self._on_btn_next_clicked)
        self.ui.translate()

        self.ui.btn_pomodoro.animateClick()

    def load_styles(self):
        # Font
        QFontDatabase.addApplicationFont("resources/fonts/Dosis.ttf")

        # Stylesheet
        with open("resources/styles.qss") as fid:
            self.setStyleSheet(fid.read())

    # Buttons event

    def _on_btn_pomodoro_clicked(self):
        if self.selection != "pomodoro":
            self.selection = "pomodoro"
            self.adapt_selection_color("pomodoro")
            self.adapt_selection_chrono("pomodoro")
            self.n_pomodoro += 1

    def _on_btn_short_br_clicked(self):
        if self.selection != "short_break":
            if self.chrono.is_running():
                # TODO: Ask the user to cancel current timer
                ...

            self.selection = "short_break"
            self.adapt_selection_color("short_break")
            self.adapt_selection_chrono("short_break")

    def _on_btn_long_br_clicked(self):
        if self.selection != "long_break":
            self.selection = "long_break"
            self.adapt_selection_color("long_break")
            self.adapt_selection_chrono("long_break")
            self.n_pomodoro = 0

    def _on_btn_start_pause_clicked(self, start:bool):
        if start:
            self.resume()
        else:
            self.pause()

    def _on_btn_next_clicked(self):
        if self.selection == "pomodoro":
            if self.n_pomodoro >= pl.config["pomodoro"]["n_before_long"]:
                self.ui.btn_long_br.animateClick()
            else:
                self.ui.btn_short_br.animateClick()
        elif self.selection == "short_break":
            self.ui.btn_pomodoro.animateClick()
        elif self.selection == "long_break":
            self.ui.btn_pomodoro.animateClick()

        self.reset_and_pause()

    # Timer event

    def _on_timer_timeout(self):
        remaining = self.chrono.remaining
        if remaining <= 0:
            self.ui.btn_next.animateClick()
            self.activateWindow()
        else:
            self.ui.set_label_chrono(remaining)

    # Methods

    def adapt_selection_color(self, selection:str):
        color = QColor(pl.config[selection]["color"])
        # Background
        palette = self.palette()
        palette.setColor(QPalette.Window, color)
        self.setPalette(palette)
        # Foreground
        palette = self.ui.btn_start_pause.palette()
        palette.setColor(QPalette.ButtonText, color)
        self.ui.btn_start_pause.setPalette(palette)

    def adapt_selection_chrono(self, selection:str):
        self.reset_and_pause()
        interval = pl.config[selection]["duration"] * 60
        self.chrono.set_timer(interval)
        self.ui.set_label_chrono(interval)

    def pause(self):
        self.ui.pause()
        self.chrono.pause()
        self.timer.stop()

    def resume(self):
        self.ui.resume()
        self.chrono.resume()
        self.timer.start()

    def reset_and_pause(self):
        self.ui.pause()
        self.chrono.reset()
        self.timer.stop()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
