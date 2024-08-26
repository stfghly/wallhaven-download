import os
import sys
import time
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
import threading
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4389.90 Safari/531.36'
}
cent = 0

class eachPageThread(threading.Thread):
    def __init__(self, url, file_name, form):
        threading.Thread.__init__(self)
        self.form = form
        self.eachPageUrl = url
        self.file_path = file_name

    def run(self):
        try:
            eachPageCollection = []
            content = open_url(self.eachPageUrl)
            soup = BeautifulSoup(content, 'lxml')
            images = soup.find('section', class_="thumb-listing-page")
            for li in images.find_all('li'):
                string = str(li.a['href'])
                eachPageCollection.append(string)

            threadingSet = []
            for eachImage in eachPageCollection:
                name = eachImage.split('/')[-1]
                eachImageUrl = f'https://w.wallhaven.cc/full/{name[0:2]}/wallhaven-{name}.jpg'
                html = requests.head(eachImageUrl)
                res = html.status_code
                ImagePosixFlag = 0
                if res == 404:
                    eachImageUrl = eachImageUrl[:-3] + 'png'
                    ImagePosixFlag = 1

                t = threading.Thread(target=downloadEachImage, args=(eachImageUrl, name, self.file_path, ImagePosixFlag))
                threadingSet.append(t)
                t.start()

                ui.set_down_nums(f'已经下载 {cent} 张')

            for eachThread in threadingSet:
                eachThread.join()
        except Exception as e:
            print(f"Error in eachPageThread: {e}")

    def get_enumerate(self):
        return threading.enumerate()

def downloadEachImage(url, name, file_path, flag):
    global cent
    fix_file_name = f'{file_path}/{name}.jpg' if flag == 0 else f'{file_path}/{name}.png'

    if not os.path.exists(fix_file_name):
        print(f"正在下载 {fix_file_name}")
        with open(fix_file_name, 'wb') as f:
            img = requests.get(url, headers=headers).content
            f.write(img)
        with lock:
            cent += 1
    else:
        print(f"发现 {fix_file_name} 存在，未下载")

def open_url(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    return response.text

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(794, 497)
        self.mesb = QMessageBox
        self.mark = [1, 1, 0]
        self.mark_2 = [1, 1, 0]
        self.file = ''
        self.sorting = 'toplist'
        self.topRange = '1M'
        self.categories = '110'
        self.purity = '110'
        font = QtGui.QFont()
        font.setPointSize(12)

        self.Button_start = QtWidgets.QPushButton(Form)
        self.Button_start.setGeometry(QtCore.QRect(510, 50, 169, 61))
        self.Button_start.setFont(font)
        self.Button_start.setObjectName("Button_start")
        self.Button_start.clicked.connect(lambda: self.start(Form))

        self.Button_choose_file = QtWidgets.QPushButton(Form)
        self.Button_choose_file.setGeometry(QtCore.QRect(320, 240, 121, 61))
        self.Button_choose_file.setFont(font)
        self.Button_choose_file.setObjectName("Button_choose_file")
        self.Button_choose_file.clicked.connect(lambda: self.thread_it(self.get_filename(Form)))

        self.Button_condition_start = QtWidgets.QPushButton(Form)
        self.Button_condition_start.setGeometry(QtCore.QRect(570, 380, 111, 51))
        self.Button_condition_start.setObjectName("Button_condition_start")
        self.Button_condition_start.clicked.connect(lambda: self.condition_down(Form))

        self.Page_input = QtWidgets.QLineEdit(Form)
        self.Page_input.setGeometry(QtCore.QRect(220, 66, 231, 31))
        self.Page_input.setObjectName("Page_input")

        self.Label_page = QtWidgets.QLabel(Form)
        self.Label_page.setGeometry(QtCore.QRect(20, 66, 181, 31))
        self.Label_page.setObjectName("Label_page")

        self.Label_down_nums = QtWidgets.QLabel(Form)
        self.Label_down_nums.setGeometry(QtCore.QRect(510, 250, 171, 41))
        self.Label_down_nums.setObjectName("Label_down_nums")
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        self.Label_down_nums.setFont(font)

        self.spinBox_nums_common = QtWidgets.QSpinBox(Form)
        self.spinBox_nums_common.setGeometry(QtCore.QRect(220, 130, 61, 31))
        self.spinBox_nums_common.setMinimum(1)
        self.spinBox_nums_common.setMaximum(500)
        self.spinBox_nums_common.setObjectName("spinBox_nums_rmf")

        self.spinBox_start_num = QtWidgets.QSpinBox(Form)
        self.spinBox_start_num.setGeometry(QtCore.QRect(280, 430, 61, 31))
        self.spinBox_start_num.setMinimum(1)
        self.spinBox_start_num.setMaximum(500)
        self.spinBox_start_num.setObjectName("spinBox_start_num")

        self.spinBox_nums_end = QtWidgets.QSpinBox(Form)
        self.spinBox_nums_end.setGeometry(QtCore.QRect(450, 430, 61, 31))
        self.spinBox_nums_end.setMinimum(1)
        self.spinBox_nums_end.setMaximum(500)
        self.spinBox_nums_end.setObjectName("spinBox_nums_end")

        self.label_start_num = QtWidgets.QLabel(Form)
        self.label_start_num.setGeometry(QtCore.QRect(200, 440, 72, 15))
        self.label_start_num.setObjectName("label_start_num")
        self.label_end_num = QtWidgets.QLabel(Form)
        self.label_end_num.setGeometry(QtCore.QRect(370, 440, 72, 15))
        self.label_end_num.setObjectName("label_end_num")

        self.Label_nums = QtWidgets.QLabel(Form)
        self.Label_nums.setGeometry(QtCore.QRect(120, 130, 91, 21))
        self.Label_nums.setObjectName("Label_nums")

        self.comboBox_time = QtWidgets.QComboBox(Form)
        self.comboBox_time.setGeometry(QtCore.QRect(250, 360, 121, 31))
        self.comboBox_time.setObjectName("comboBox_time")
        self.comboBox_time.addItems(["最新的", "近一个月的", "近三个月的", "近六个月的", "近一年的"])
        self.comboBox_time.setCurrentIndex(1)

        self.comboBox_condition = QtWidgets.QComboBox(Form)
        self.comboBox_condition.setGeometry(QtCore.QRect(400, 360, 111, 31))
        self.comboBox_condition.setObjectName("comboBox_condition")
        self.comboBox_condition.addItems(["Top榜单", "收藏榜单", "评论榜单", "Hot榜单NSFW", "随机下载"])

        self.checkBox_general = QtWidgets.QCheckBox(Form)
        self.checkBox_general.setGeometry(QtCore.QRect(30, 349, 61, 19))
        self.checkBox_general.setAutoFillBackground(True)
        self.checkBox_general.setChecked(True)
        self.checkBox_general.setObjectName("checkBox_General")
        self.checkBox_general.stateChanged.connect(lambda: self.update_categories(self.checkBox_general))

        self.checkBox_anime = QtWidgets.QCheckBox(Form)
        self.checkBox_anime.setGeometry(QtCore.QRect(100, 349, 61, 19))
        self.checkBox_anime.setAutoFillBackground(True)
        self.checkBox_anime.setChecked(True)
        self.checkBox_anime.setObjectName("checkBox_Anime")
        self.checkBox_anime.stateChanged.connect(lambda: self.update_categories(self.checkBox_anime))

        self.checkBox_people = QtWidgets.QCheckBox(Form)
        self.checkBox_people.setGeometry(QtCore.QRect(170, 349, 61, 19))
        self.checkBox_people.setAutoFillBackground(True)
        self.checkBox_people.setChecked(True)
        self.checkBox_people.setObjectName("checkBox_People")
        self.checkBox_people.stateChanged.connect(lambda: self.update_categories(self.checkBox_people))

        self.checkBox_SFW = QtWidgets.QCheckBox(Form)
        self.checkBox_SFW.setGeometry(QtCore.QRect(20, 380, 51, 31))
        self.checkBox_SFW.setAutoFillBackground(True)
        self.checkBox_SFW.setChecked(True)
        self.checkBox_SFW.setObjectName("checkBox_SFW")
        self.checkBox_SFW.stateChanged.connect(lambda: self.update_purity(self.checkBox_SFW))

        self.checkBox_sketchy = QtWidgets.QCheckBox(Form)
        self.checkBox_sketchy.setGeometry(QtCore.QRect(90, 380, 71, 31))
        self.checkBox_sketchy.setAutoFillBackground(True)
        self.checkBox_sketchy.setChecked(True)
        self.checkBox_sketchy.setObjectName("checkBox_sketchy")
        self.checkBox_sketchy.stateChanged.connect(lambda: self.update_purity(self.checkBox_sketchy))

        self.checkBox_NSFW = QtWidgets.QCheckBox(Form)
        self.checkBox_NSFW.setGeometry(QtCore.QRect(160, 380, 61, 31))
        self.checkBox_NSFW.setAutoFillBackground(True)
        self.checkBox_NSFW.setChecked(True)
        self.checkBox_NSFW.setObjectName("checkBox_NSFW")
        self.checkBox_NSFW.stateChanged.connect(lambda: self.update_purity(self.checkBox_NSFW))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "图片下载器"))
        self.Button_start.setText(_translate("Form", "按页数下载"))
        self.Button_choose_file.setText(_translate("Form", "选择目录"))
        self.Button_condition_start.setText(_translate("Form", "条件下载"))
        self.Label_page.setText(_translate("Form", "需要下载的页数"))
        self.Label_down_nums.setText(_translate("Form", ""))
        self.Label_nums.setText(_translate("Form", "每页下载数量"))
        self.label_start_num.setText(_translate("Form", "起始页数"))
        self.label_end_num.setText(_translate("Form", "结束页数"))
        self.checkBox_general.setText(_translate("Form", "General"))
        self.checkBox_anime.setText(_translate("Form", "Anime"))
        self.checkBox_people.setText(_translate("Form", "People"))
        self.checkBox_SFW.setText(_translate("Form", "SFW"))
        self.checkBox_sketchy.setText(_translate("Form", "Sketchy"))
        self.checkBox_NSFW.setText(_translate("Form", "NSFW"))

    def get_filename(self, Form):
        self.file = QFileDialog.getExistingDirectory(Form, "选择文件夹", "C:/")
        if self.file:
            self.mark_2[2] = 1
        else:
            self.mark_2[2] = 0

    def set_down_nums(self, message):
        self.Label_down_nums.setText(message)

    def thread_it(self, func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    def start(self, Form):
        if not self.mark_2[2]:
            self.mesb.warning(Form, '警告', '请选择文件目录', QMessageBox.Yes)
            return
        if not self.Page_input.text().isdigit():
            self.mesb.warning(Form, '警告', '请输入有效的页数', QMessageBox.Yes)
            return

        nums = self.spinBox_nums_common.value()
        self.mark[2] = 1
        page = int(self.Page_input.text())

        url_template = f"https://wallhaven.cc/search?categories={self.categories}&purity={self.purity}&sorting={self.sorting}&topRange={self.topRange}&page="

        for i in range(1, page + 1):
            print(f'正在爬取第 {i} 页')
            t = eachPageThread(f"{url_template}{i}", self.file, Form)
            t.start()
            t.join()

        self.mark[2] = 0
        self.mesb.warning(Form, '提示', '下载完成', QMessageBox.Yes)

    def update_categories(self, checkbox):
        categories_map = {
            "checkBox_General": 0,
            "checkBox_Anime": 1,
            "checkBox_People": 2
        }
        state = 1 if checkbox.isChecked() else 0
        self.categories = ''.join([
            str(state if categories_map[cb.objectName()] == i else 1 if getattr(self, cb).isChecked() else 0)
            for i, cb in enumerate(["checkBox_General", "checkBox_Anime", "checkBox_People"])
        ])

    def update_purity(self, checkbox):
        purity_map = {
            "checkBox_SFW": 0,
            "checkBox_sketchy": 1,
            "checkBox_NSFW": 2
        }
        state = 1 if checkbox.isChecked() else 0
        self.purity = ''.join([
            str(state if purity_map[cb.objectName()] == i else 1 if getattr(self, cb).isChecked() else 0)
            for i, cb in enumerate(["checkBox_SFW", "checkBox_sketchy", "checkBox_NSFW"])
        ])

    def condition_down(self, Form):
        if not self.mark_2[2]:
            self.mesb.warning(Form, '警告', '请选择文件目录', QMessageBox.Yes)
            return

        start_num = self.spinBox_start_num.value()
        end_num = self.spinBox_nums_end.value()
        condition = self.comboBox_condition.currentText()

        self.sorting = {
            "Top榜单": "toplist",
            "收藏榜单": "favorites",
            "评论榜单": "comments",
            "Hot榜单NSFW": "views",
            "随机下载": "random"
        }[condition]

        self.topRange = {
            "最新的": "1d",
            "近一个月的": "1M",
            "近三个月的": "3M",
            "近六个月的": "6M",
            "近一年的": "1y"
        }[self.comboBox_time.currentText()]

        url_template = f"https://wallhaven.cc/search?categories={self.categories}&purity={self.purity}&sorting={self.sorting}&topRange={self.topRange}&page="

        for i in range(start_num, end_num + 1):
            print(f'正在爬取第 {i} 页')
            t = eachPageThread(f"{url_template}{i}", self.file, Form)
            t.start()
            t.join()

        self.mesb.warning(Form, '提示', '下载完成', QMessageBox.Yes)

lock = threading.Lock()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
