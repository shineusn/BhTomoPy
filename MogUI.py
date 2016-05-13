
import sys
from PyQt4 import QtGui, QtCore


class MOGUI(QtGui.QFrame):
    def __init__(self, parent=None):
        super(MOGUI, self).__init__()
        self.setWindowTitle("bh_thomoPy/MOGs")
        self.initUI()

    def initUI(self):


        class  MyQLabel(QtGui.QLabel):
            def __init__(self, label, ha='left',  parent=None):
                super(MyQLabel, self).__init__(label,parent)
                if ha == 'center':
                    self.setAlignment(QtCore.Qt.AlignCenter)
                elif ha == 'right':
                    self.setAlignment(QtCore.Qt.AlignRight)
                else:
                    self.setAlignment(QtCore.Qt.AlignLeft)

        #------- Widgets Creation -------#
        #--- Buttons Set ---#
        btn_Add_MOG                 = QtGui.QPushButton("Add MOG")
        btn_Remove_MOG              = QtGui.QPushButton("Remove MOG")
        btn_Air_Shot_Before         = QtGui.QPushButton("Air Shot Before")
        btn_Air_Shot_After          = QtGui.QPushButton("Air Shot After")
        btn_Rename                  = QtGui.QPushButton("Rename")
        btn_Import                  = QtGui.QPushButton("Import")
        btn_Merge                   = QtGui.QPushButton("Merge")
        btn_Raw_Data                = QtGui.QPushButton("Raw Data")
        btn_Trace_ZOP               = QtGui.QPushButton("Trace ZOP")
        btn_Spectra                 = QtGui.QPushButton("Spectra")
        btn_Stats_tt                = QtGui.QPushButton("Stats tt")
        btn_Stats_Ampl              = QtGui.QPushButton("Stats Ampl.")
        btn_Ray_Coverage            = QtGui.QPushButton("Ray Coverage")
        btn_Export_tt               = QtGui.QPushButton("Export tt")
        btn_export_tau              = QtGui.QPushButton("Export tau")
        btn_Prune                   = QtGui.QPushButton("Prune")

        #--- List ---#
        MOG_list = QtGui.QListWidget()

        #--- combobox ---#
        Type_combo = QtGui.QComboBox()
        Tx_combo = QtGui.QComboBox()
        Rx_combo = QtGui.QComboBox()
        Type_combo.addItem(" Crosshole ")
        Type_combo.addItem(" VSP/VRP ")

        #--- Checkbox ---#
        Air_shots_checkbox                  = QtGui.QCheckBox("Use Air Shots")
        Correction_Factor_checkbox          = QtGui.QCheckBox("Fixed Time Step Correction Factor")

        #--- Labels ---#
        Type_label                          = MyQLabel('Type:', ha='right')
        Tx_label                            = MyQLabel('Tx:', ha='right')
        Rx_label                            = MyQLabel('Rx:', ha='right')
        Nominal_Frequency_label             = MyQLabel('Nominal Frequency of Antenna:', ha='right')
        Rx_Offset_label                     = MyQLabel('Antenna Feedpoint Offset - Rx:', ha='right')
        Tx_Offset_label                     = MyQLabel('Antenna Feedpoint Offset - Tx:', ha='right')
        Multiplication_Factor_label         = MyQLabel('Std Dev. Multiplication Factor:', ha='right')
        Date_label                          = MyQLabel('Date:', ha='right')

        #--- Edits ---#
        Air_Shot_Before_edit                = QtGui.QLineEdit()
        Air_Shot_After_edit                 = QtGui.QLineEdit()
        Nominal_Frequency_edit              = QtGui.QLineEdit()
        Rx_Offset_edit                      = QtGui.QLineEdit()
        Tx_Offset_edit                      = QtGui.QLineEdit()
        Correction_Factor_edit              = QtGui.QLineEdit()
        Multiplication_Factor_edit          = QtGui.QLineEdit()
        Date_edit                           = QtGui.QLineEdit()


        #--- Sub Widgets ---#

        #- Sub AirShots Widget-#
        Sub_AirShots_Widget = QtGui.QWidget()
        Sub_AirShots_Grid   = QtGui.QGridLayout()
        Sub_AirShots_Grid.addWidget(Type_label, 0, 1)
        Sub_AirShots_Grid.addWidget(Tx_label, 1, 1)
        Sub_AirShots_Grid.addWidget(Rx_label, 2, 1)
        Sub_AirShots_Grid.addWidget(Type_combo, 0, 2, 1, 2)
        Sub_AirShots_Grid.addWidget(Tx_combo, 1, 2, 1, 2)
        Sub_AirShots_Grid.addWidget(Rx_combo, 2, 2, 1, 2)
        Sub_AirShots_Grid.addWidget(Air_shots_checkbox, 3, 0)
        Sub_AirShots_Grid.addWidget(btn_Air_Shot_Before, 4, 0, 1, 2)
        Sub_AirShots_Grid.addWidget(btn_Air_Shot_After, 5, 0, 1, 2)
        Sub_AirShots_Grid.addWidget(Air_Shot_Before_edit, 4, 2, 1, 2)
        Sub_AirShots_Grid.addWidget(Air_Shot_After_edit, 5, 2, 1, 2)
        Sub_AirShots_Widget.setLayout(Sub_AirShots_Grid)


        #- Sub Labels, Checkbox and Edits Widget -#
        Sub_Labels_Checkbox_and_Edits_Widget = QtGui.QWidget()
        Sub_Labels_Checkbox_and_Edits_Grid   = QtGui.QGridLayout()
        Sub_Labels_Checkbox_and_Edits_Grid.addWidget(Nominal_Frequency_label,0, 1)
        Sub_Labels_Checkbox_and_Edits_Grid.addWidget(Rx_Offset_label,1, 1)
        Sub_Labels_Checkbox_and_Edits_Grid.addWidget(Correction_Factor_checkbox, 3, 1)
        Sub_Labels_Checkbox_and_Edits_Grid.addWidget(Tx_Offset_label,2, 1)
        Sub_Labels_Checkbox_and_Edits_Grid.addWidget(Multiplication_Factor_label,4, 1)
        Sub_Labels_Checkbox_and_Edits_Grid.addWidget(Date_label,7, 1)
        Sub_Labels_Checkbox_and_Edits_Grid.addWidget(Nominal_Frequency_edit,0, 2)
        Sub_Labels_Checkbox_and_Edits_Grid.addWidget(Rx_Offset_edit,1, 2)
        Sub_Labels_Checkbox_and_Edits_Grid.addWidget(Tx_Offset_edit,2, 2)
        Sub_Labels_Checkbox_and_Edits_Grid.addWidget(Correction_Factor_edit,3, 2)
        Sub_Labels_Checkbox_and_Edits_Grid.addWidget(Multiplication_Factor_edit,4, 2)
        Sub_Labels_Checkbox_and_Edits_Grid.addWidget(Date_edit, 7, 2)
        Sub_Labels_Checkbox_and_Edits_Widget.setLayout(Sub_Labels_Checkbox_and_Edits_Grid)

        #- Sub Right Buttons Widget -#
        sub_right_buttons_widget = QtGui.QWidget()
        sub_right_buttons_Grid   = QtGui.QGridLayout()
        sub_right_buttons_Grid.addWidget(btn_Rename, 1, 1)
        sub_right_buttons_Grid.addWidget(btn_Import, 1, 2)
        sub_right_buttons_Grid.addWidget(btn_Merge, 1, 3)
        sub_right_buttons_Grid.addWidget(btn_Raw_Data, 2, 1)
        sub_right_buttons_Grid.addWidget(btn_Trace_ZOP, 2, 2)
        sub_right_buttons_Grid.addWidget(btn_Spectra, 2, 3)
        sub_right_buttons_Grid.addWidget(btn_Stats_tt, 3, 1)
        sub_right_buttons_Grid.addWidget(btn_Stats_Ampl, 3, 2)
        sub_right_buttons_Grid.addWidget(btn_Ray_Coverage, 3, 3)
        sub_right_buttons_Grid.addWidget(btn_Export_tt, 4, 1)
        sub_right_buttons_Grid.addWidget(btn_export_tau, 4, 2)
        sub_right_buttons_Grid.addWidget(btn_Prune, 4, 3)
        sub_right_buttons_Grid.setVerticalSpacing(0)
        sub_right_buttons_Grid.setHorizontalSpacing(0)
        sub_right_buttons_Grid.setRowStretch(0, 100)
        sub_right_buttons_Grid.setRowStretch(5, 100)
        sub_right_buttons_Grid.setColumnStretch(0, 100)
        sub_right_buttons_Grid.setColumnStretch(5, 100)
        sub_right_buttons_widget.setLayout(sub_right_buttons_Grid)

        #- MOG and list Sub Widget -#
        sub_MOG_and_List_widget = QtGui.QWidget()
        sub_MOG_and_List_Grid   = QtGui.QGridLayout()
        sub_MOG_and_List_Grid.addWidget(btn_Add_MOG, 0, 0, 1, 2)
        sub_MOG_and_List_Grid.addWidget(btn_Remove_MOG, 0, 2, 1, 2)
        sub_MOG_and_List_Grid.addWidget(MOG_list, 1, 0, 1, 4)
        sub_MOG_and_List_widget.setLayout(sub_MOG_and_List_Grid)

        #------- Grid Disposition -------#
        master_grid     = QtGui.QGridLayout()
        #--- Sub Widgets Disposition ---#
        master_grid.addWidget(sub_MOG_and_List_widget, 0, 0)
        master_grid.addWidget(sub_right_buttons_widget, 0, 1)
        master_grid.addWidget(Sub_Labels_Checkbox_and_Edits_Widget, 1, 1)
        master_grid.addWidget(Sub_AirShots_Widget, 1, 0)
        self.setLayout(master_grid)





if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    MOGUI_ui = MOGUI()
    MOGUI_ui.show()

    sys.exit(app.exec_())