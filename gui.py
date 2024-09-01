

from PyQt6 import QtCore, QtGui, QtWidgets
import forest_synth
import sys


class SynthUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SynthUI, self).__init__(parent)
        self.setMinimumSize(1000, 500)
        
        self.slider_count = 4
    
        self.sliders = [QtWidgets.QSlider(self) for _ in range(self.slider_count)]
        for slider in self.sliders:
            styles = "QSlider::groove:vertical { background: white; position: absolute; left: 8px; right: 7px; }"
            styles += "QSlider::handle:vertical { height: 11px; background: #979EA8; margin: 0 -4px; border-style:solid; border-color: grey;border-width:1px;border-radius:3px}"
            styles += "QSlider::sub-page:vertical { background: #979EA8; border-style:solid; border-color: grey;border-width:1px;border-radius:2px}"
            styles += "QSlider::add-page:vertical { background: #979EA8; border-style:solid; border-color: grey;border-width:1px;border-radius:2px}"
            slider.setStyleSheet(styles)
            slider.setFixedWidth(200)
            slider.setTickInterval(10)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setSingleStep(1)
            slider.setPageStep(10)
            slider.setTickInterval(10)
            slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksRight)
            slider.setSliderPosition(50)

        buttonBox = QtWidgets.QGroupBox(self)
        
        buttonStyle = "border-radius : 50"
        self.button = QtWidgets.QPushButton(buttonBox)
        self.button.setFixedHeight(100)
        self.button.setFixedWidth(100)
        self.button.clicked.connect(self.button_press)
        #self.button.setStyleSheet(buttonStyle)

        buttonLayout = QtWidgets.QVBoxLayout()
        buttonLayout.addWidget(self.button)

        buttonBox.setLayout(buttonLayout)

        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.setContentsMargins(20, 20, 20, 20)
        for slider in self.sliders:
            mainLayout.addWidget(slider)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)


        self.synth = forest_synth.ForestSynth()
        self.synth.run()


    def button_press(self):
        print("press")
        self.synth.state.speak(0)

if __name__ == "__main__":

    import sys

    app = QtWidgets.QApplication(sys.argv)
    synth = SynthUI()
    synth.show()
    sys.exit(app.exec())