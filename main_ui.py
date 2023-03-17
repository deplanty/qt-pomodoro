from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QWidget, QPushButton, QToolButton, QLabel, QHBoxLayout, QVBoxLayout


class MainWindowUI:
    def __init__(self, parent):
        frame = QWidget(parent)
        vbox = QVBoxLayout(frame)

        # Top row: select state
        top_hbox = QHBoxLayout()
        self.btn_pomodoro = QPushButton(frame)
        self.btn_pomodoro.setCheckable(True)
        self.btn_pomodoro.setAutoExclusive(True)
        self.btn_pomodoro.setCursor(Qt.PointingHandCursor)
        self.btn_pomodoro.setObjectName("push_select_pomodoro")
        top_hbox.addWidget(self.btn_pomodoro)
        self.btn_short_br = QPushButton(frame)
        self.btn_short_br.setCheckable(True)
        self.btn_short_br.setAutoExclusive(True)
        self.btn_short_br.setCursor(Qt.PointingHandCursor)
        self.btn_short_br.setObjectName("push_select_short_break")
        top_hbox.addWidget(self.btn_short_br)
        self.btn_long_br = QPushButton(frame)
        self.btn_long_br.setCheckable(True)
        self.btn_long_br.setAutoExclusive(True)
        self.btn_long_br.setCursor(Qt.PointingHandCursor)
        self.btn_long_br.setObjectName("push_select_long_break")
        top_hbox.addWidget(self.btn_long_br)
        vbox.addLayout(top_hbox)

        # Middle row: chrono
        self.label_chrono = QLabel()
        self.label_chrono.setAlignment(Qt.AlignCenter)
        self.label_chrono.setObjectName("chrono")
        vbox.addWidget(self.label_chrono)

        # Bottom row: pause and next
        bot_hbox = QHBoxLayout()
        spacer = QWidget()
        bot_hbox.addWidget(spacer)
        self.btn_start_pause = QPushButton()
        self.btn_start_pause.setCheckable(True)
        self.btn_start_pause.setObjectName("start_pause")
        self.btn_start_pause.setCursor(Qt.PointingHandCursor)
        bot_hbox.addWidget(self.btn_start_pause)
        self.btn_next = QPushButton()
        self.btn_next.setIcon(QIcon("resources/images/skip_next.svg"))
        self.btn_next.setCursor(Qt.PointingHandCursor)
        self.btn_next.setObjectName("next")
        bot_hbox.addWidget(self.btn_next)
        vbox.addLayout(bot_hbox)

        parent.setCentralWidget(frame)

    def translate(self):
        self.btn_pomodoro.setText("Pomodoro")
        self.btn_short_br.setText("Short break")
        self.btn_long_br.setText("Long break")

        self.label_chrono.setText("12:54")

        self.pause()  # Default state is pause
        # self.btn_next.setText(">|")

    def pause(self):
        self.btn_start_pause.setText("START")
        self.btn_start_pause.setChecked(False)

    def resume(self):
        self.btn_start_pause.setText("PAUSE")
        self.btn_start_pause.setChecked(True)

    def set_label_chrono(self, seconds:float):
        m, s = divmod(seconds, 60)
        self.label_chrono.setText(f"{int(m):02d}:{int(s):02d}")
