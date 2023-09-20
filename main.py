# import updater
import os
import sys
import cv2
import numpy as np
from PySide2.QtWidgets import QMainWindow, QApplication, QToolBar, QDialog, QDialogButtonBox, \
                            QAction, QFileDialog, QCompleter, QGraphicsScene, QSpinBox, QLineEdit, \
                            QGraphicsView, QGraphicsItem, QWidget, QHBoxLayout, QVBoxLayout, \
                            QListView,QGraphicsRectItem, QListWidget, QLabel,QListWidgetItem, \
                            QGraphicsTextItem, QSpacerItem, QSizePolicy, QPushButton, QGraphicsPixmapItem, QFormLayout
from PySide2.QtGui import QIcon, QFontDatabase,QKeySequence, QBrush, QPen, QPixmap,QStandardItemModel, QStandardItem, QColor, QPainter,QTextOption, QImage, QPalette,QPainterPath, QRegion, QFont
from PySide2.QtCore import Qt, QStringListModel,QAbstractListModel,QRectF,QIODevice,QDataStream,QByteArray,Signal, Slot,QThread, QSize, QTimer
import random
import time
import threading

DB=["alif","ba","ta","tsa","ja","cha","kho","da","dza","ra","za","sa","sya","sha","dha","tha","dhla","aa","gha","fa","qa","ka","la","ma","na","wa","ha","ya"]

IMAGES_PATH = os.path.join("assets{}images{}".format(os.sep,os.sep))
FONT_PATH = os.path.join("assets{}font{}VanillaExtractRegular.ttf".format(os.sep,os.sep))

def random_soal(current_huruf="ya"):
    current_huruf_index = DB.index(current_huruf)
    if len(DB)-1 == current_huruf:
        DB_HURUF=DB
    else:
        DB_HURUF=DB[0:current_huruf_index+1]
    # DB_HURUF=["alif","ba","ta","tsa","ja","cha","kho","da","dza"]
    # DB_ANSWER = [["alif","ba"],["ta","alif"],["ba","ta"],["tsa","ba"],["tsa","ta"]]

    DB_ANSWER = [random.sample(DB_HURUF,3) for i in range(5)]

    print("DB_ANSWER",DB_ANSWER)
    DB_OPTIONS = [val+random.sample([ hrf for hrf in DB_HURUF if hrf not in val],2) for val in  DB_ANSWER]
    DB_OPTIONS = [random.sample(val,len(val)) for val in DB_OPTIONS]
    return DB_HURUF,DB_ANSWER,DB_OPTIONS


class ImageButton(QPushButton):
    def __init__(self, huruf,index,  parent=None):
        super(ImageButton, self).__init__(parent)
        self.huruf = huruf
        self.index =index
        self.isSelected = False
        if self.parent().current_huruf == huruf:
            self.isSelected = True
            self.setStyleSheet("background-color: purple")

    def mousePressEvent(self, event):
        if self.isEnabled:
            index = self.parent().huruf_status_buttons.index(True)
            if self.parent().huruf_buttons[index] is not self:
                self.parent().huruf_buttons[index].setStyleSheet("background-color: none")
                self.parent().huruf_status_buttons[index] = False
                self.parent().huruf_status_buttons[self.index] = True
                self.parent().current_huruf = self.huruf

            self.setStyleSheet("background-color: purple")

            self.update()
        super(ImageButton,self).mousePressEvent(event)



class NewDialog(QDialog):
    
    
    def __init__(self, main_window,icon=None,parent=None):
        super(NewDialog, self).__init__(parent)
        self.setWindowTitle("Profilku")
        self.setMinimumWidth(600)
        self.setMinimumHeight(600)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showMaximized()
        palette = self.palette()
        # palette.setColor(self.main_widget.backgroundRole(), Qt.yellow)

        palette.setColor(QPalette.Window, QColor(254, 193, 78, 255))

        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.main_window = main_window
        self.login_data = getattr(main_window,'login_data') if hasattr(main_window,'login_data') else {}
        self.contacts_tags = ["Prospects","Customers"]
        if not hasattr(main_window,'is_api_connected'):
            self.is_connected = False
        else:
            self.is_connected = getattr(main_window,'is_api_connected')

        if icon is not None:
            self.setWindowIcon(QIcon(icon))

        self._layout = QVBoxLayout(self)
        self._form_layout = QFormLayout()
        self._vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.name = QLineEdit()
        self.name.setText(self.main_window.player_name)
        self.name.setFixedHeight(100)
        self.name.setFont(QFont('Vanilla Extract', 30))
        self.name.setStyleSheet("background: #f95704;color:#95e2f6;")
        self.age = QSpinBox()
        self.age.setValue(self.main_window.player_age)
        self.age.setStyleSheet("background: #f95704;color:#95e2f6;")
        self.age.setFixedHeight(100)
        self.age.setFont(QFont('Vanilla Extract', 30))
        self.level = QSpinBox()
        self.level.setStyleSheet("background: #f95704;color:#95e2f6;")
        self.level.setMinimum(1)
        self.level.setMaximum(1)
        self.level.setValue(int(self.main_window.player_level))
        self.level.setFixedHeight(100)
        self.level.setFont(QFont('Vanilla Extract', 30))


        self.huruf = QLabel()
        self.current_huruf = self.main_window.current_huruf


        baris1 = QHBoxLayout()
        baris2 = QHBoxLayout()
        self.huruf_buttons = []
        self.huruf_status_buttons = []
        for i,huruf in enumerate(reversed(DB)):

            path = IMAGES_PATH+"{}.png".format(huruf)
            button = ImageButton(huruf,i, self)
            pixmap1 = QPixmap(QImage(path))
            iconBack = QIcon(pixmap1)
            button.setIcon(iconBack)
            button.setIconSize(QSize(50, 50))
            if i <=13:
                baris2.addWidget(button)
            else:
                baris1.addWidget(button)
            if i >=len(DB)-4:
                button.setEnabled(False)
            self.huruf_buttons.append(button)
            self.huruf_status_buttons.append(button.isSelected)
        


        self.name_label = QLabel("Nama")
        self.name_label.setFont(QFont('Vanilla Extract', 30))
        self.name_label.setStyleSheet("color: rgb(151, 10, 122)")
        self.age_label = QLabel("Umur")
        self.age_label.setFont(QFont('Vanilla Extract', 30))
        self.age_label.setStyleSheet("color: rgb(151, 10, 122)")
        self.level_label = QLabel("Jilid")
        self.level_label.setFont(QFont('Vanilla Extract', 30))
        self.level_label.setStyleSheet("color: rgb(151, 10, 122)")
        self.huruf_label = QLabel("Batas Huruf")
        self.huruf_label.setFont(QFont('Vanilla Extract', 30))
        self.huruf_label.setStyleSheet("color: rgb(151, 10, 122)")


        self._form_layout.addRow(self.name_label,self.name)
        self._form_layout.addRow(self.age_label,self.age)
        self._form_layout.addRow(self.level_label,self.level)
        self._form_layout.addRow(self.huruf_label,self.huruf)

        self.ok_button = QPushButton(self.tr("&Simpan"))
        self.ok_button.setFixedHeight(80)
        self.ok_button.setFixedWidth(100)
        self.ok_button.setStyleSheet("color: rgb(151, 10, 122)")

        self.cancel_button = QPushButton(self.tr("&Batal"))
        self.cancel_button.setFixedHeight(80)
        self.cancel_button.setFixedWidth(100)
        self.cancel_button.setStyleSheet("color: rgb(249, 87, 4)")

        self._buttons_box = QDialogButtonBox()
        self._buttons_box.addButton(self.ok_button,QDialogButtonBox.ActionRole)
        self._buttons_box.addButton(self.cancel_button, QDialogButtonBox.ActionRole)
        self.ok_button.clicked.connect(self.accept_action)
        self.cancel_button.clicked.connect(self.reject)
        

        self._layout.addLayout(self._form_layout)
        self._layout.addLayout(baris1)
        self._layout.addLayout(baris2)
        self._layout.addItem(self._vspacer)
        self._layout.addWidget(self._buttons_box)
        self.setLayout(self._layout)

    def accept_action(self):
        name = self.name.text()
        age = int(self.age.value())
        level = self.level.text()
        current_huruf = self.current_huruf
        self.main_window.updatePlayer(name,age,level,current_huruf)
        self.accept()

        
def show_new_dialog(main_window,icon=None):
    
    dialog = NewDialog(main_window,icon)
    if dialog.exec_():
        return True
    return False

class VideoThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)

    def __init__(self, parent=None):
        super(VideoThread, self).__init__(parent)
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super(VideoWidget, self).__init__(parent=None)
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 200
        self.display_height = 200
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()



    @Slot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


class ImageItem(QGraphicsRectItem):
    """docstring for ImageItem"""
    def __init__(self, *args,mw=None,**kwargs):
        super(ImageItem, self).__init__(*args,**kwargs)
        self.setAcceptDrops(True)
        self.setFlags(QGraphicsItem.ItemIsSelectable)
        self.m_text=""
        self.value=""
        self.main_window=mw
        self.index = -1
        self.page = 0
        self._brush = QBrush(Qt.black)
        self.timer = QTimer()
        self.timer.timeout.connect(self.doSomething)
        self.is_correct = False
        # self.background = QColor(151, 10, 122, 255)
        self.background = QColor("#d968aa")

    @Slot()
    def doSomething(self):
        path = IMAGES_PATH+"tanya-white.png"
        image = QBrush(QImage(path))
        self.setBrush(image)
        self.timer.stop()

    def resetValue(self):
        self.value = ""

    def setValue(self,value):
        self.value = value


    def dropEvent(self, event):
        if (event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist")):
            itemData = event.mimeData().data("application/x-qabstractitemmodeldatalist")
            stream = QDataStream(itemData, QIODevice.ReadOnly)
            row = stream.readInt32()
            col = stream.readInt32()
            print("row---", row)
            print(self.main_window.DB_OPTIONS[self.page][row],self.value)
            if self.main_window.DB_OPTIONS[self.page][row] == self.value:

                if row>=-1:

                    path = IMAGES_PATH+self.main_window.DB_OPTIONS[self.page][row]+".png"
                    
                    image =QImage(path)
                    self.setBrush(image)

                self.main_window.checkedAnswer.emit(True,self.index)
                self.is_correct = True
                event.accept()
            else:

                self.main_window.checkedAnswer.emit(False,self.index)
                path = IMAGES_PATH+"salah.png"
                image = QBrush(QImage(path))
                self.setBrush(image)

                self.timer.start(2000)

                event.ignore()
        else:
            event.ignore()

    def paint(self, painter,option, widget):
        painter.fillRect(option.rect, self.background)

        super(ImageItem ,self).paint(painter, option, widget)
        

    def setText(self, text):
        self.m_text = text
        self.update()

    def text(self):
        return self.m_text



class ListModel(QAbstractListModel):
    def __init__(self, huruf=[], parent=None):
        super(ListModel, self).__init__(parent)
        self.huruf =  huruf

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the data structure.
            text = self.huruf[index.row()]
            # Return the todo text only.
            return text

    def rowCount(self, index):
        return len(self.huruf)

class ImagesView(QGraphicsView):
    """docstring for ImagesView"""
    def __init__(self, *args, **kwargs):
        super(ImagesView, self).__init__(*args, **kwargs)

class MainWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args,**kwargs)

class ListView(QListView):
    def __init__(self, parent=None):
        super(ListView, self).__init__(parent) 
        model = ListModel(self) 
        self.setModel(model)


class Overlay(QWidget):
    def __init__(self, widget, parent=None):
        super(Overlay,self).__init__(parent)
        # self.setFixedWidth(parent.width())
        # self.setFixedHeight(parent.height())
        self.setGeometry(parent.screen_geo)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)

        self.widget = widget
        self.widget.setParent(self)
        self.showMaximized()


    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(),QBrush(QColor(0, 0, 0, 127)))
        painter.end()

    def resizeEvent(self, event):
        position_x = (self.frameGeometry().width()-self.widget.frameGeometry().width())/2
        position_y = (self.frameGeometry().height()-self.widget.frameGeometry().height())/2

        self.widget.move(position_x, position_y)
        event.accept()

class NextWidget(QWidget):
    def __init__(self, parent = None):
        super(NextWidget,self).__init__(parent)

        self.button = QPushButton()
        self.button.setFixedWidth(200)
        self.button.setFixedHeight(100)
        path1 = IMAGES_PATH+"lanjut.png"
        pixmap1 = QPixmap(QImage(path1))
        self.button.setIcon(pixmap1)
        self.button.setIconSize(pixmap1.rect().size())
        self.button.setFixedSize(pixmap1.rect().size())

        self.image_label = QLabel(self)                                                                                                                 
        path = IMAGES_PATH+"masyaAllah.png"
        pixmap = QPixmap(QImage(path))
        self.image_label.setPixmap(pixmap)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.image_label)
        self.layout().addWidget(self.button)

        self.button.clicked.connect(self.hideOverlay)

    def hideOverlay(self):
        self.parent().hide()
        self.parent().parent().nextGame(self.parent().parent().current_page)

class WinWidget(QWidget):
    def __init__(self, parent = None):
        super(WinWidget,self).__init__(parent)

        self.button = QPushButton()
        self.button.setFixedWidth(200)
        self.button.setFixedHeight(100)
        path1 = IMAGES_PATH+"main-lagi.png"
        pixmap1 = QPixmap(QImage(path1))
        self.button.setIcon(pixmap1)
        self.button.setIconSize(pixmap1.rect().size())
        self.button.setFixedSize(pixmap1.rect().size())

        self.button_quit = QPushButton()
        self.button_quit.setFixedWidth(200)
        self.button_quit.setFixedHeight(100)
        path1 = IMAGES_PATH+"keluar.png"
        pixmap1 = QPixmap(QImage(path1))
        self.button_quit.setIcon(pixmap1)
        self.button_quit.setIconSize(pixmap1.rect().size())
        self.button_quit.setFixedSize(pixmap1.rect().size())


        self.image_label = QLabel(self)                                                                                                                 
        path = IMAGES_PATH+"yeay.png"
        pixmap = QPixmap(QImage(path))
        self.image_label.setPixmap(pixmap)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.image_label)
        self.button_layout = QVBoxLayout()

        self.layout().addLayout(self.button_layout)
        self.button_layout.addWidget(self.button)
        self.button_layout.addWidget(self.button_quit)

        self.button.clicked.connect(self.hideOverlayAndRestart)
        self.button_quit.clicked.connect(self.hideOverlayAndQuit)

    def hideOverlayAndRestart(self):
        self.parent().hide()
        self.parent().parent().beforeRestartGame()

    def hideOverlayAndQuit(self):
        self.parent().hide()
        self.parent().parent().close()

class GameOverWidget(QWidget):
    def __init__(self, parent = None):
        super(GameOverWidget,self).__init__(parent)

        self.button = QPushButton()
        self.button.setFixedWidth(200)
        self.button.setFixedHeight(100)
        path1 = IMAGES_PATH+"main-lagi.png"
        pixmap1 = QPixmap(QImage(path1))
        self.button.setIcon(pixmap1)
        self.button.setIconSize(pixmap1.rect().size())
        self.button.setFixedSize(pixmap1.rect().size())

        self.button_quit = QPushButton()
        self.button_quit.setFixedWidth(200)
        self.button_quit.setFixedHeight(100)
        path1 = IMAGES_PATH+"keluar.png"
        pixmap1 = QPixmap(QImage(path1))
        self.button_quit.setIcon(pixmap1)
        self.button_quit.setIconSize(pixmap1.rect().size())
        self.button_quit.setFixedSize(pixmap1.rect().size())


        self.image_label = QLabel(self)                                                                                                                 
        path = IMAGES_PATH+"game-over.png"
        pixmap = QPixmap(QImage(path))
        self.image_label.setPixmap(pixmap)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.image_label)
        self.button_layout = QVBoxLayout()

        self.layout().addLayout(self.button_layout)
        self.button_layout.addWidget(self.button)
        self.button_layout.addWidget(self.button_quit)

        self.button.clicked.connect(self.hideOverlayAndRestart)
        self.button_quit.clicked.connect(self.hideOverlayAndQuit)

    def hideOverlayAndRestart(self):
        self.parent().hide()
        self.parent().parent().beforeRestartGame()

    def hideOverlayAndQuit(self):
        self.parent().hide()
        self.parent().parent().close()


class StartWidget(QWidget):
    def __init__(self, parent = None):
        super(StartWidget,self).__init__(parent)

        self.button = QPushButton()
        self.button.setFixedWidth(500)
        self.button.setFixedHeight(500)
        path1 = IMAGES_PATH+"bismillah.png"
        pixmap1 = QPixmap(QImage(path1))
        self.button.setIcon(pixmap1)
        self.button.setIconSize(pixmap1.rect().size())
        self.button.setFixedSize(pixmap1.rect().size())
        self.button.setFlat(True)
        self.button.setStyleSheet("QPushButton { background-color: transparent }")

        self.button_kembali = QPushButton()
        path2 = IMAGES_PATH+"kembali.png"
        pixmap2 = QPixmap(QImage(path2))
        self.button_kembali.setIcon(pixmap2)
        self.button_kembali.setIconSize(pixmap2.rect().size())
        self.button_kembali.setFixedSize(pixmap2.rect().size())
        self.button_kembali.setFlat(True)
        self.button_kembali.setStyleSheet("QPushButton { background-color: transparent }")


        self.button_mulai = QPushButton()
        path2 = IMAGES_PATH+"mulai.png"
        pixmap2 = QPixmap(QImage(path2))
        self.button_mulai.setIcon(pixmap2)
        self.button_mulai.setIconSize(pixmap2.rect().size())
        self.button_mulai.setFixedSize(pixmap2.rect().size())
        self.button_mulai.setFlat(True)
        self.button_mulai.setStyleSheet("QPushButton { background-color: transparent }")


        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.button)

        self.button_layout = QVBoxLayout()
        self.layout().addLayout(self.button_layout)        

        self.button_layout.addWidget(self.button_mulai)
        self.button_layout.addWidget(self.button_kembali)
        

        self.button.clicked.connect(self.hideOverlayAndRestart)
        self.button_mulai.clicked.connect(self.hideOverlayAndRestart)
        self.button_kembali.clicked.connect(self.hideOverlayAndCancel)

    def hideOverlayAndRestart(self):
        self.parent().hide()
        self.parent().parent().resetGame()

    def hideOverlayAndCancel(self):
        self.parent().hide()


class QuitWidget(QWidget):
    def __init__(self, parent = None):
        super(QuitWidget,self).__init__(parent)

        self.button = QPushButton()
        self.button.setFixedWidth(500)
        self.button.setFixedHeight(500)
        path1 = IMAGES_PATH+"bye.png"
        pixmap1 = QPixmap(QImage(path1))
        self.button.setIcon(pixmap1)
        self.button.setIconSize(pixmap1.rect().size())
        self.button.setFixedSize(pixmap1.rect().size())
        self.button.setFlat(True)
        self.button.setStyleSheet("QPushButton { background-color: transparent }")


        self.button_keluar = QPushButton()
        path2 = IMAGES_PATH+"keluar.png"
        pixmap2 = QPixmap(QImage(path2))
        self.button_keluar.setIcon(pixmap2)
        self.button_keluar.setIconSize(pixmap2.rect().size())
        self.button_keluar.setFixedSize(pixmap2.rect().size())
        self.button_keluar.setFlat(True)
        self.button_keluar.setStyleSheet("QPushButton { background-color: transparent }")

        self.button_kembali = QPushButton()
        path2 = IMAGES_PATH+"kembali.png"
        pixmap2 = QPixmap(QImage(path2))
        self.button_kembali.setIcon(pixmap2)
        self.button_kembali.setIconSize(pixmap2.rect().size())
        self.button_kembali.setFixedSize(pixmap2.rect().size())
        self.button_kembali.setFlat(True)
        self.button_kembali.setStyleSheet("QPushButton { background-color: transparent }")


        self.setLayout(QHBoxLayout())

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.button_keluar)
        self.button_layout.addWidget(self.button_kembali)

        self.layout().addWidget(self.button)
        self.layout().addLayout(self.button_layout)
        

        self.button_keluar.clicked.connect(self.hideOverlayAndQuit)
        self.button_kembali.clicked.connect(self.hideOverlayAndCancel)

    def hideOverlayAndCancel(self):
        self.parent().hide()

    def hideOverlayAndQuit(self):
        self.parent().hide()
        self.parent().parent().close()



class HoreWidget(QWidget):
    """docstring for ClassName"""
    def __init__(self, parent=None):
        super(HoreWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.label = QLabel(self)
        self.label.setText("<h1>HORE KAMU LANJUT KE SOAL BERIKUT</h1")
        self.next_button = QPushButton(self)
        self.next_button.setText("SOAL BERIKUTNYA")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.next_button)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):

    checkedAnswer = Signal(bool,int)
    def __init__(self, screen_geo = None):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Menyusun Huruf Hijaiyah ")
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.DB_HURUF,self.DB_ANSWER,self.DB_OPTIONS=random_soal()
        self.screen_geo = screen_geo
        self.total_pages = 5
        self.heart_images = []
        self.heart_status = 3
        self.check_images = []
        self.answer_items= []
        self.current_page = 0
        self.skor = 0
        self.answer_correct = [False,False,False]
        self.player_name = "PEMAIN"
        self.player_age = 4
        self.player_level = 1
        self.current_huruf = 'ya'
        # self.create_ui()
        self.createListWidget()
        self.createSceneAndView()
        
        self.createLayout()
        self.showMaximized()


        self.createGraphicsItems()

        self.popup = Overlay(NextWidget(),self)
        self.popup.hide()

        self.popup_win = Overlay(WinWidget(),self)
        self.popup_win.hide()

        self.popup_gameover = Overlay(GameOverWidget(),self)
        self.popup_gameover.hide()

        self.popup_restart = Overlay(StartWidget(),self)
        self.popup_restart.hide()

        self.popup_quit = Overlay(QuitWidget(),self)
        self.popup_quit.hide()

        self.start_button.clicked.connect(self.beforeRestartGame)
        self.quit_button.clicked.connect(self.beforeQuitGame)
        self.new_player_button.clicked.connect(self.showNewDialog)
        self.checkedAnswer.connect(self.checkAnswer)

    def showNewDialog(self):
        status = show_new_dialog(self)

    def updatePlayer(self,name,age,level,huruf):
        self.player_name = name
        self.player_age = age
        self.player_level = level
        self.current_huruf = huruf

        self.name_label.setText("<h1 style='text-align:center;'>{}</h1>".format(self.player_name))
        self.level_label.setText("<h1 style='text-align:center;'>{} Tahun</h1>".format(self.player_age))
        self.resetGame()

    def checkAnswer(self,is_correct,index):
        print("is_correct", is_correct,index)
        if not is_correct:
            if self.heart_status >=1:
                self.heart_status-=1

                item = self.heart_images[self.heart_status]
                path = IMAGES_PATH+"heart-grey.png"
                pixmap = QPixmap(QImage(path))
                item.setPixmap(pixmap)
                if self.heart_status == 0:
                    print("GAME OVER")
                    self.item_gameover.setHtml("<html><div style='text-align:center; color:#c82f68;backrgound-color:#c82f68;font-size:80px;'>{}</div></html>".format(self.skor))
                    self.popup_gameover.show()
                self.answer_correct[index]=is_correct

        else:

            self.answer_correct[index]=is_correct
            print(self.answer_correct)
            if all(self.answer_correct):
                self.skor = (self.current_page+1)*20
                if self.skor > 0:
                    self.item_gameover.setPos(420,0)
                # self.score_label.setText("<h1 style='text-align:center;'>SKOR: {}</h1>".format(self.skor))
                if self.current_page==self.total_pages-1:
                    self.item_gameover.setHtml("<html><div style='text-align:center; color:#c82f68;backrgound-color:#c82f68;font-size:80px;'>{}</div></html>".format(self.skor))
                    item = self.check_images[self.current_page]
                
                    self.answer_correct = [False,False,False]
                    path = IMAGES_PATH+"{}-true.png".format(self.current_page+1)
                    pixmap = QPixmap(QImage(path))
                    item.setPixmap(pixmap)
                    self.popup_win.show()
                else:
                    self.item_gameover.setHtml("<html><div style='text-align:center; color:#c82f68;backrgound-color:#c82f68;font-size:80px;'>{}</div></html>".format(self.skor))
                    item = self.check_images[self.current_page]
                
                    self.answer_correct = [False,False,False]
                    path = IMAGES_PATH+"{}-true.png".format(self.current_page+1)
                    pixmap = QPixmap(QImage(path))
                    item.setPixmap(pixmap)
                    self.current_page+=1
                    self.popup.show()

    def beforeRestartGame(self):
        self.popup_restart.show()

    def beforeQuitGame(self):
        self.popup_quit.show()


    def resetGame(self):

        self.DB_HURUF,self.DB_ANSWER,self.DB_OPTIONS=random_soal(self.current_huruf)

        self.total_pages = 5
        self.heart_status = 3
        self.current_page = 0
        self.answer_correct = [False,False,False]
        self.skor =0
        # self.score_label.setText("<h1 style='text-align:center;'>SKOR: {}</h1>".format(self.skor))
        self.item_gameover.setPos(455,0)
        self.item_gameover.setHtml("<html><div style='text-align:center; color:#c82f68;backrgound-color:#c82f68;font-size:80px;'>{}</div></html>".format(self.skor))
        for item in self.heart_images:
            path = IMAGES_PATH+"heart-pink.png"
            pixmap = QPixmap(QImage(path))
            item.setPixmap(pixmap)

        for i,item in enumerate(self.check_images):
            path = IMAGES_PATH+"{}-unanswered.png".format(i+1)
            pixmap = QPixmap(QImage(path))
            item.setPixmap(pixmap)

        self.updateListWidget(self.current_page)

        self.item0.setBrush(QColor("#FFFFFF"))
        path0 = IMAGES_PATH+"tanya-white.png"
        self.image0 = QBrush(QImage(path0))
        self.item0.setBrush(self.image0)
        self.item0.setValue(self.DB_ANSWER[self.current_page][2])
        self.item0.index=2
        self.item0.page = self.current_page

        self.item1.setBrush(QColor("#FFFFFF"))
        path1 = IMAGES_PATH+"tanya-white.png"
        self.image1 = QBrush(QImage(path1))
        self.item1.setBrush(self.image1)
        self.item1.setValue(self.DB_ANSWER[self.current_page][1])
        self.item1.index=1
        self.item1.page = self.current_page

        self.item2.setBrush(QColor("#FFFFFF"))
        path2 = IMAGES_PATH+"tanya-white.png"
        self.image2 = QBrush(QImage(path1))
        self.item2.setBrush(self.image2)
        self.item2.setValue(self.DB_ANSWER[self.current_page][0])
        self.item2.index=0
        self.item2.page = self.current_page

        # jika len huruf 2, max huruf 4
        answer = self.DB_ANSWER[self.current_page]
        x_pos =300+round((420-(len(answer)*100))/2)

        for i,huruf in enumerate(reversed(answer)) :
            item4 = self.answer_items[i]
            path4 = IMAGES_PATH+"{}.png".format(huruf)
            image4 = QPixmap(QImage(path4))
            item4.setPixmap(image4)


    def nextGame(self,page):
        val1,val2,val3 = self.DB_ANSWER[page]
        self.updateListWidget(page)

        self.item0.setBrush(QColor("#FFFFFF"))
        path0 = IMAGES_PATH+"tanya-white.png"
        self.image0 = QBrush(QImage(path0))
        self.item0.setBrush(self.image0)
        self.item0.setValue(val3)
        self.item0.index=2
        self.item0.page = page

        self.item1.setBrush(QColor("#FFFFFF"))
        path1 = IMAGES_PATH+"tanya-white.png"
        self.image1 = QBrush(QImage(path1))
        self.item1.setBrush(self.image1)
        self.item1.setValue(val2)
        self.item1.index = 1
        self.item1.page = page

        self.item2.setBrush(QColor("#FFFFFF"))
        path2 = IMAGES_PATH+"tanya-white.png"
        self.image2 = QBrush(QImage(path1))
        self.item2.setBrush(self.image2)
        self.item2.setValue(val1)
        self.item2.index = 0
        self.item2.page = page

        # jika len huruf 2, max huruf 4
        answer = self.DB_ANSWER[page]
        x_pos =300+round((420-(len(answer)*100))/2)

        for i,huruf in enumerate(reversed(answer)) :
            item4 = self.answer_items[i]
            path4 = IMAGES_PATH+"{}.png".format(huruf)
            image4 = QPixmap(QImage(path4))
            item4.setPixmap(image4)
    


    def updateListWidget(self,current_page):
        for row, filename in enumerate(self.DB_OPTIONS[current_page]):
            path = IMAGES_PATH+filename+".png"
            image1 = QImage(path)
            label1 = QLabel()
            label1.setPixmap(QPixmap(QPixmap.fromImage(image1)))
            item1 = self.list_view.item(row)
            self.list_view.setItemWidget(item1, label1)


    def createListWidget(self,current_page=0):
        
        self.list_view = QListWidget(self)
        self.list_view.setStyleSheet( """QListWidget{
                    background: #d968aa;
                }

                QListWidget::item:selected{background-color: rgb(151, 10, 122);}"
                """)
        self.list_view.setFixedWidth(135)
        self.list_view.setFixedHeight(700)
        # self.list_view.addItems(["fa","kaf","lam","nun"])
        self.list_view.setSpacing(15)
        self.list_view.setDragEnabled(True)
        for filename in self.DB_OPTIONS[current_page]:
            path = IMAGES_PATH+filename+".png"
            image1 = QImage(path)
            label1 = QLabel()
            label1.setPixmap(QPixmap(QPixmap.fromImage(image1)))
            item1 = QListWidgetItem()
            item1.setSizeHint(label1.sizeHint())
            self.list_view.addItem(item1)
            self.list_view.setItemWidget(item1, label1)
        

    def createSceneAndView(self):
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0,0,950,600)
        self.view = ImagesView(self.scene, self)
        # self.view.setBackgroundBrush(QColor(254, 193, 78, 1))
        self.view.setBackgroundBrush(QBrush(QColor(254, 193, 78, 255),Qt.SolidPattern))
        

    def createGraphicsItems(self,current_page=0,total_pages=5,level=1,variant=0):
        # next
        self.current_page = current_page
        self.item_gameover = QGraphicsTextItem()
        self.scene.addItem(self.item_gameover)
        self.item_gameover.setPos(455,0)
        # self.item_gameover.setHtml("<html><h1 style='text-align:center;'>MENYUSUN HURUF HIJAIYAH</h1></html>")
        self.item_gameover.setHtml("<html><div style='text-align:center; color:#c82f68;backrgound-color:#c82f68;font-size:80px;'>{}</div></html>".format(self.skor))

        heart_box = QRectF(0,0,50,50)
        huruf_box = QRectF(0,0,100,100)
        kalimat_box = QRectF(0,0,420,100)
        ans_box = QRectF(0,0,100,100)

        for i in range(0,3):
            item = QGraphicsPixmapItem()
            self.heart_images.append(item)
            path = IMAGES_PATH+"heart-pink.png"
            pixmap = QPixmap(QImage(path))
            item.setPixmap(pixmap)
            item.setPos(30+(50*i),10)
            self.scene.addItem(item)

        for i in range(1,6):
            item = QGraphicsPixmapItem()
            self.check_images.append(item)
            path = IMAGES_PATH+"{}-unanswered.png".format(i)
            pixmap = QPixmap(QImage(path))
            item.setPixmap(pixmap)
            item.setPos(640+(50*i),10)
            self.scene.addItem(item)


        self.item0 = ImageItem(mw=self)
        self.scene.addItem(self.item0)
        self.item0.setRect(huruf_box)
        self.item0.setPos(300,150)
        self.item0.setBrush(QColor("#FFFFFF"))
        path0 = IMAGES_PATH+"tanya-white.png"
        self.image0 = QBrush(QImage(path0))
        self.item0.setBrush(self.image0)
        self.item0.setValue(self.DB_ANSWER[current_page][2])
        self.item0.index = 2


        self.item1 = ImageItem(mw=self)
        self.scene.addItem(self.item1)
        self.item1.setRect(huruf_box)
        self.item1.setPos(430,150)
        # self.item1.setBrush(QColor("#FFFFFF"))
        self.item1.setBrush(QColor(151, 10, 122, 255))
        path1 = IMAGES_PATH+"tanya-white.png"
        self.image1 = QBrush(QImage(path1))
        self.item1.setBrush(self.image1)
        self.item1.setValue(self.DB_ANSWER[current_page][1])
        self.item1.index = 1


        self.item2 = ImageItem(mw=self)
        self.scene.addItem(self.item2)
        self.item2.setRect(huruf_box)
        self.item2.setPos(560,150)
        # self.item2.setBrush(QColor("#FFFFFF"))
        self.item2.setBrush(QColor(151, 10, 122, 255))
        path2 = IMAGES_PATH+"tanya-white.png"
        self.image2 = QBrush(QImage(path2))
        self.item2.setBrush(self.image2)
        self.item2.setValue(self.DB_ANSWER[current_page][0])
        self.item2.index = 0

        self.item3 = ImageItem()
        self.item3.setAcceptDrops(False)
        self.scene.addItem(self.item3)
        self.item3.setRect(kalimat_box)
        self.item3.setPos(270,350)
        self.item3.setBrush(QColor("#D9DDDC"))
        

        # jika len huruf 2, max huruf 4
        answer = self.DB_ANSWER[0]
        x_pos =270+round((420-(len(answer)*100))/2)

        for i,huruf in enumerate(reversed(answer)) :

            item4 = QGraphicsPixmapItem()
            self.answer_items.append(item4)
            item4.setAcceptDrops(False)
            self.scene.addItem(item4)
            item4.setPos(x_pos+(i*100),350)
            path4 = IMAGES_PATH+"{}.png".format(huruf)
            image4 = QPixmap(QImage(path4))
            item4.setPixmap(image4)

        

    def createLayout(self):
        self.main_widget =  MainWidget(self)
        # self.main_widget.setBackgroundBrush(Qt.yellow)
        palette = self.main_widget.palette()
        # palette.setColor(self.main_widget.backgroundRole(), Qt.yellow)

        palette.setColor(QPalette.Window, QColor(249, 87, 4, 255))

        self.main_widget.setPalette(palette)
        self.main_widget.setAutoFillBackground(True)
        self.main_widget.setStyleSheet("color: #95e2f6")

        self.header_widget = QWidget(self)
        self.header_layout = QVBoxLayout()
        
        self.header_widget.setLayout(self.header_layout)


        self.main_layout = QVBoxLayout()
        self.inner_layout = QHBoxLayout()


        self.player_widget = QWidget(self)
        self.player_widget
        self.player_widget.setFixedWidth(230)
        self.player_layout = QVBoxLayout()
        self.player_widget.setLayout(self.player_layout)


        self.name_label = QLabel(self)
        self.name_label.setText("<h1 style='text-align:center;'>{}</h1>".format(self.player_name))
        self.level_label = QLabel(self)
        self.level_label.setText("<h1 style='text-align:center;'>{} Tahun</h1>".format(self.player_age))
        self.score_label = QLabel(self)
        # self.score_label.setText("<h1 style='text-align:center;'>SKOR: 0</h1>")
        
        self.player_camera = VideoWidget(self)

        self.new_player_button = QPushButton(self)
        self.new_player_button.setFixedHeight(100)
        # self.new_player_button.setText("PROFIL")
        path1 = IMAGES_PATH+"profil.png"
        pixmap1 = QPixmap(QImage(path1))
        self.new_player_button.setIcon(pixmap1)
        self.new_player_button.setIconSize(pixmap1.rect().size())
        self.new_player_button.setFixedSize(pixmap1.rect().size())

        self.start_button = QPushButton(self)
        self.start_button.setFixedHeight(100)
        # self.start_button.setText("MAIN LAGI")
        path1 = IMAGES_PATH+"main-lagi.png"
        pixmap1 = QPixmap(QImage(path1))
        self.start_button.setIcon(pixmap1)
        self.start_button.setIconSize(pixmap1.rect().size())
        self.start_button.setFixedSize(pixmap1.rect().size())


        self.quit_button = QPushButton(self)
        # self.quit_button.setText("KELUAR")
        self.quit_button.setFixedHeight(100)
        path1 = IMAGES_PATH+"keluar.png"
        pixmap1 = QPixmap(QImage(path1))
        self.quit_button.setIcon(pixmap1)
        self.quit_button.setIconSize(pixmap1.rect().size())
        self.quit_button.setFixedSize(pixmap1.rect().size())


        self.playerSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.player_layout.addWidget(self.player_camera)
        self.player_layout.addWidget(self.name_label)
        self.player_layout.addWidget(self.level_label)
        self.player_layout.addWidget(self.score_label)
        self.playerSpacer2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.player_layout.addItem(self.playerSpacer)
        self.player_layout.addWidget(self.new_player_button)
        self.player_layout.addWidget(self.start_button)
        self.player_layout.addWidget(self.quit_button)
        self.player_layout.addItem(self.playerSpacer2)
        

        self.inner_layout.addWidget(self.player_widget)
        self.inner_layout.addWidget(self.view)
        self.inner_layout.addWidget(self.list_view)

        self.main_layout.addWidget(self.header_widget)
        self.main_layout.addLayout(self.inner_layout)
        self.main_widget.setLayout(self.main_layout)
    

        self.setCentralWidget(self.main_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(FONT_PATH)

    font = QFont("Vanilla Extract");
    font.setStyleHint(QFont.Monospace)
    app.setFont(font)


    screen = app.primaryScreen()
    geometry = screen.availableGeometry()
    window = MainWindow(screen_geo=geometry)
    window.show()
    sys.exit(app.exec_())