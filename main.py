import sys
from making import main
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

        super().__init__()
        
        self.setStyleSheet('font-family: "Noto Sans CJK JP"; font-size: 22px')
        self.setGeometry(10,10,400,225)
        self.setWindowTitle("QScrollAreaは解決")

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
        self.arranges = ["上ぞろえ", "中央ぞろえ", "下ぞろえ"]
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

        button_run = QPushButton("生成",self)
        button_run.clicked.connect(self.run)
        hbl4.addWidget(button_run)

    def change(self):
        self.upright = self.boxup.isChecked()
        self.reverse = self.boxre.isChecked()
        self.arrange = self.comboboxar.currentIndex()

    

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
        
        self.labelwi = QLabel(f"縦幅:{self.img_width} → ")
        self.labelhe  = QLabel(f"横幅:{self.img_height} → ")
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
        if self.spinwi.value()==0 or self.spinin.value() <= self.spinwi.value():
            self.img_width = self.spinwi.value()
            self.img_height = self.spinhe.value()
            self.interval = self.spinin.value()
            self.inum_d.close()
            self.sizes.setText(f"横幅:{self.img_width}, 縦幅:{self.img_height}, 間隔:{self.interval}")
        else:
            QMessageBox.critical(self.inum_d,"","間隔が横幅を超過しています！")
            self.spinin.setValue(self.spinwi.value())
        

    def file(self):
        name,ok = QFileDialog.getOpenFileNames(self)
        if(ok):
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

    def run(self):
        main(self.input_path,self.upright,self.reverse,self.arrange,self.img_width,self.img_height,self.interval,self.dest,self.name)
        QMessageBox.information(self,"","生成が終了しました！")
        # main(self.input_path, self.upright, self.reverse, self.arrange, self.width, self.height, self.interval, self.dest, self.name)
            

        # title,ok = QInputDialog.getText(self, "input window", "Input title of window.")
        # if(ok and title!=""):
        #     self.setWindowTitle(title)
        # else:
        #     self.windowTitle("ウィンドウ")

qAp = QApplication(sys.argv)
wid = Widget()
wid.show()
qAp.exec()
