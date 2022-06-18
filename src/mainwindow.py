from ui.MainWindow import Ui_MainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem
from subprocess import Popen
from youtube import YouTube

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.search_lineEdit.returnPressed.connect(self.search)
		self.more_pushButton.clicked.connect(self.continue_search)
		self.results_listWidget.itemDoubleClicked.connect(self.play)
		self.sort_by_date_checkBox.clicked.connect(self.search)

		self.ghostly = YouTube()
		self.update_continue_button()

	def search(self):
		self.results_listWidget.clear()
		self.ghostly.clear()
		self.update_continue_button()

		if self.search_lineEdit.text():
			self.ghostly.search(self.search_lineEdit.text(), self.sort_by_date_checkBox.isChecked())
			self.update_results_list()
			self.update_continue_button()

	def continue_search(self):
		self.ghostly.continue_search()
		self.update_results_list()
		self.update_continue_button()

	def play(self, item: QListWidgetItem):
		video_id = item.data(Qt.ItemDataRole.UserRole)
		max_video_quality = "720"
		Popen(["mpv", "--hwdec=auto", "--vo=gpu",
			f"--ytdl-format=bestvideo[height<=?{max_video_quality}]+bestaudio/best",
			f"https://www.youtube.com/watch?v={video_id}"])

	def update_continue_button(self):
		self.more_pushButton.setEnabled(self.ghostly.can_continue_search())

	def update_results_list(self):
		for video in self.ghostly.search_results[-1]:
			item = QListWidgetItem(video.title)
			item.setData(Qt.ItemDataRole.UserRole, video.id)
			self.results_listWidget.addItem(item)