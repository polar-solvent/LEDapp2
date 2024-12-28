import sys
import shutil
import re
import math
from making import main as make, shape
from showing import main as show
from PyQt6.QtWidgets import QApplication,QWidget,QLineEdit,QMessageBox,QSpinBox,QDialog,QComboBox,QScrollArea,QSizePolicy,QHBoxLayout,QVBoxLayout,QPushButton,QCheckBox,QFileDialog,QLabel,QInputDialog
from PyQt6.QtCore import Qt

class Widget(QWidget):
    def __init__(self):
        self.input_path = []
        self.upright = False
        self.reverse = False
        self.arrange = 0
        self.img_width = 0
        self.img_height = 0
        self.interval = 1
        self.dest = "./assets/dest"
        self.name = "frame"
        self.widths = 0
        self.heights = 0

        super().__init__()
        
        self.setStyleSheet('font-family: "Noto Sans CJK JP"; font-size: 22px')
        self.setGeometry(10,10,400,225)
        self.setWindowTitle("LEDapp")

        vbl = QVBoxLayout()
        self.setLayout(vbl)

        hbl1 = QHBoxLayout()
        vbl.addLayout(hbl1)

        self.boxup = QCheckBox("upright", self)
        hbl1.addWidget(self.boxup)
        self.boxup.toggled.connect(self.change)

        self.boxre = QCheckBox("reverse", self)
        hbl1.addWidget(self.boxre)
        self.boxre.toggled.connect(self.change)

        self.comboboxar = QComboBox()
        hbl1.addWidget(self.comboboxar)
        self.arranges = ["上(左)ぞろえ", "中央ぞろえ", "下(右)ぞろえ"]
        for line in self.arranges:
            self.comboboxar.addItem(line)
        self.combotest = QLabel("")
        self.comboboxar.currentTextChanged.connect(self.change)
        self.comboboxar.setCurrentIndex(0)
        hbl1.addWidget(self.combotest)

        self.sizes = QLabel(f"横幅:{self.img_width}, 縦幅:{self.img_height}, 間隔:{self.interval}")
        hbl1.addWidget(self.sizes)
        self.size_button = QPushButton("サイズ変更", self)
        self.size_button.clicked.connect(self.insert_number)
        hbl1.addWidget(self.size_button)


        hbl2 = QHBoxLayout()
        vbl.addLayout(hbl2)

        self.filearea = QScrollArea(self)
        self.filename = QLabel("ファイル名", self.filearea)
        self.filearea.setWidget(self.filename)
        hbl2.addWidget(self.filearea)

        button_file = QPushButton("画像選択",self)
        button_file.clicked.connect(self.file)
        hbl2.addWidget(button_file)

        hbl2_5 = QHBoxLayout()
        vbl.addLayout(hbl2_5)

        button_show = QPushButton("作成される画像群を閲覧",self)
        button_show.clicked.connect(self.simulate)
        hbl2_5.addWidget(button_show)

        hbl3 = QHBoxLayout()
        vbl.addLayout(hbl3)

        self.destarea = QScrollArea(self)
        self.destname = QLabel(str(self.dest), self.destarea)
        self.destarea.setWidget(self.destname)
        hbl3.addWidget(self.destarea)

        button_dest = QPushButton("保存ディレクトリ",self)
        button_dest.clicked.connect(self.choose_dest)
        hbl3.addWidget(button_dest)

        hbl4 = QHBoxLayout()
        vbl.addLayout(hbl4)

        name_string = QLabel("保存名:")
        self.insert_name = QLineEdit("frame",self)
        self.insert_name.textEdited.connect(self.name_pushed)
        hbl4.addWidget(name_string)
        hbl4.addWidget(self.insert_name)

        button_run = QPushButton("画像群の保存",self)
        button_run.clicked.connect(self.run)
        hbl4.addWidget(button_run)

        button_save = QPushButton("動画として保存",self)
        button_save.clicked.connect(self.save)
        hbl4.addWidget(button_save)

    def change(self):
        if self.boxup.isChecked() == 0 and (self.img_width == 0 or self.img_width>=self.interval) or self.boxup.isChecked() == 1 and (self.img_height == 0 or self.img_height>=self.interval):
            self.upright = self.boxup.isChecked()
            self.reverse = self.boxre.isChecked()
            self.arrange = self.comboboxar.currentIndex()
            if self.upright == 0:
                self.img_height = max(self.heights)
                self.img_width = sum(self.widths)
            else:
                self.img_height = sum(self.heights)
                self.img_width = max(self.widths)
            self.sizes.setText(f"横幅:{self.img_width}, 縦幅:{self.img_height}, 間隔:{self.interval}")

        elif self.boxup.isChecked() == 0:
            QMessageBox.critical(self,"","間隔が横幅を超過しています！")
            self.boxup.setCheckState(Qt.CheckState.Checked)
        elif self.boxup.isChecked() == 1:
            QMessageBox.critical(self,"","間隔が縦幅を超過しています！")
            self.boxup.setCheckState(Qt.CheckState.Unchecked)

    def insert_number(self):
        self.inum_d = QDialog()
        self.inum_d.setWindowTitle("サイズの入力")
        self.inum_d.setStyleSheet('font-family: "Noto Sans CJK JP"; font-size: 22px')
        self.inum_d.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.spinwi, self.spinhe, self.spinin = QSpinBox(), QSpinBox(), QSpinBox()
        for spin in (self.spinwi, self.spinin, self.spinhe):
            spin.setRange(0,0xFFFF)
            spin.setSingleStep(1)
        self.spinin.setRange(1,0xFFFF)
        self.spinwi.setValue(self.img_width)
        self.spinhe.setValue(self.img_height)
        self.spinin.setValue(self.interval)
        
        self.labelwi = QLabel(f"横幅:{self.img_width} → ")
        self.labelhe  = QLabel(f"縦幅:{self.img_height} → ")
        self.labelin = QLabel(f"間隔:{self.interval} → ")

        vbli = QVBoxLayout()
        self.inum_d.setLayout(vbli)
        hbli1 = QHBoxLayout()
        vbli.addLayout(hbli1)

        hbli1.addWidget(self.labelwi)
        hbli1.addWidget(self.spinwi)

        hbli2 = QHBoxLayout()
        vbli.addLayout(hbli2)

        hbli2.addWidget(self.labelhe)
        hbli2.addWidget(self.spinhe)

        hbli3 = QHBoxLayout()
        vbli.addLayout(hbli3)

        hbli3.addWidget(self.labelin)
        hbli3.addWidget(self.spinin)

        self.insert_button = QPushButton("入力完了",self.inum_d)
        self.insert_button.clicked.connect(self.check_wi)
        hbli4 = QHBoxLayout()
        vbli.addLayout(hbli4)
        hbli4.addWidget(self.insert_button)

        self.inum_d.exec()

    def check_wi(self):
        if self.upright == 0 and (self.spinwi.value()==0 or self.spinin.value() <= self.spinwi.value()):
            self.img_width = self.spinwi.value()
            self.img_height = self.spinhe.value()
            self.interval = self.spinin.value()
            self.inum_d.close()
            self.sizes.setText(f"横幅:{self.img_width}, 縦幅:{self.img_height}, 間隔:{self.interval}")
        elif self.upright == 1 and (self.spinhe.value()==0 or self.spinin.value() <= self.spinhe.value()):
            self.img_width = self.spinwi.value()
            self.img_height = self.spinhe.value()
            self.interval = self.spinin.value()
            self.inum_d.close()
            self.sizes.setText(f"横幅:{self.img_width}, 縦幅:{self.img_height}, 間隔:{self.interval}")
        elif self.upright == 0:
            QMessageBox.critical(self.inum_d,"","間隔が横幅を超過しています！")
            self.spinin.setValue(self.spinwi.value())
        elif self.upright == 1:
            QMessageBox.critical(self.inum_d,"","間隔が縦幅を超過しています！")
            self.spinin.setValue(self.spinhe.value())
        

    def file(self):
        name,ok = QFileDialog.getOpenFileNames(self)
        if(ok):
            if shape(name) == 1:
                QMessageBox.critical(self,"","画像形式のファイルを選択してください！")
            else:
                h,w,c = shape(name)
                self.widths = w
                self.heights = h
                if self.upright == 0:
                    self.img_height = max(h)
                    self.img_width = sum(w)
                else:
                    self.img_height = sum(h)
                    self.img_width = max(w)
                self.interval = 1
                self.sizes.setText(f"横幅:{self.img_width}, 縦幅:{self.img_height}, 間隔:{self.interval}")

                self.input_path = name
                self.filename = QLabel(", ".join(name), self.filearea)
                self.filearea.setWidget(self.filename)

    def choose_dest(self):
        name = QFileDialog.getExistingDirectory(self,"保存ディレクトリ")
        self.dest = name
        self.destname = QLabel(str(self.dest), self.destarea)
        self.destarea.setWidget(self.destname)

    def name_pushed(self):
        self.name = self.insert_name.text()

    def simulate(self):
        if self.input_path!=[]:
            make(self.input_path,self.upright,self.reverse,self.arrange,self.img_width,self.img_height,self.interval,"./.temp")
        else:
            QMessageBox.critical(self,"","画像を選択してください！")
            return
        if self.upright:
            speed = (self.img_height+sum(self.heights))//self.interval
        else:
            speed = (self.img_width+sum(self.widths))//self.interval
        if speed > 0xFFFF:
            QMessageBox.critical(self,"","画像の横幅を小さくするか、間隔を大きくしてください！")
        else:
            show("./.temp/frame_0.bmp", math.ceil(speed/2))
        shutil.rmtree("./.temp/")

    def run(self):
        if self.input_path!=[]:
            make(self.input_path,self.upright,self.reverse,self.arrange,self.img_width,self.img_height,self.interval,"./.temp")
        else:
            QMessageBox.critical(self,"","画像を選択してください！")
            return
        if not re.fullmatch(r"[-\w]+", self.name):
            QMessageBox.critical(self,"","保存名は英数字、'-'、'_'のみが使えます！")
        else:
            make(self.input_path,self.upright,self.reverse,self.arrange,self.img_width,self.img_height,self.interval,self.dest,self.name)
            QMessageBox.information(self,"","保存が終了しました！")
        # main(self.input_path, self.upright, self.reverse, self.arrange, self.width, self.height, self.interval, self.dest, self.name)
            

        # title,ok = QInputDialog.getText(self, "input window", "Input title of window.")
        # if(ok and title!=""):
        #     self.setWindowTitle(title)
        # else:
        #     self.windowTitle("ウィンドウ")

    def save(self):
        if self.input_path!=[]:
            make(self.input_path,self.upright,self.reverse,self.arrange,self.img_width,self.img_height,self.interval,"./.temp")
        else:
            QMessageBox.critical(self,"","画像を選択してください！")
            return
        if not re.fullmatch(r"[-\w]+\.(mp4|gif)", self.name):
            QMessageBox.critical(self,"","保存名は英数字、'-'、'_'のみが使え、\n動画の保存には拡張子'mp4'または'gif'が必要です！")
        else:
            self.speed()
            make(self.input_path,self.upright,self.reverse,self.arrange,self.img_width,self.img_height,self.interval,"./.temp")
            show("./.temp/frame_0.bmp",self.spinsp.value(),f"{self.dest}/{self.name}")
            shutil.rmtree("./.temp/")
            QMessageBox.information(self,"","保存が終了しました！")

    def speed(self):
        self.spd = QDialog()
        self.spd.setWindowTitle("1秒あたりに写す画像数の入力")
        self.spd.setStyleSheet('font-family: "Noto Sans CJK JP"; font-size: 22px')
        self.spd.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.labelsp = QLabel("1秒あたりに写す画像数:")
        self.spinsp = QSpinBox()
        self.spinsp.setRange(1,0xFFFF)
        self.spinsp.setSingleStep(1)
        self.spinsp.setValue(60)
        vbls = QVBoxLayout()
        hbls1 = QHBoxLayout()
        self.spd.setLayout(vbls)
        vbls.addLayout(hbls1)
        hbls1.addWidget(self.labelsp)
        hbls1.addWidget(self.spinsp)

        self.finish_button = QPushButton("入力完了",self.spd)
        self.finish_button.clicked.connect(self.spd.close)
        hbls2 = QHBoxLayout()
        vbls.addLayout(hbls2)
        hbls2.addWidget(self.finish_button)

        self.spd.exec()

        


qAp = QApplication(sys.argv)
wid = Widget()
wid.show()
qAp.exec()
