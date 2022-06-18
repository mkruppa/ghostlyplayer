#!/usr/bin/env python

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from mainwindow import MainWindow


def enable_qt_dark_theme(app: QApplication) -> None:
	text_color = QColor(200, 200, 200)
	background_color = QColor(40, 40, 45)
	highlight_color = QColor(50, 70, 130)

	QApplication.setStyle("Fusion")
	palette = QPalette()
	palette.setColor(QPalette.ColorRole.Window, background_color)
	palette.setColor(QPalette.ColorRole.WindowText, text_color)
	palette.setColor(QPalette.ColorRole.Text, text_color)
	palette.setColor(QPalette.ColorRole.Base, background_color)
	palette.setColor(QPalette.ColorRole.Highlight, highlight_color)
	palette.setColor(QPalette.ColorRole.Button, background_color)
	palette.setColor(QPalette.ColorRole.ButtonText, text_color)
	palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, background_color)
	app.setPalette(palette)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	enable_qt_dark_theme(app)

	window = MainWindow()
	window.show()

	app.exec()