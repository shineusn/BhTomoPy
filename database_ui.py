# -*- coding: utf-8 -*-
"""
Copyright 2016 Bernard Giroux, Elie Dumas-Lefebvre

This file is part of BhTomoPy.

BhTomoPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from borehole_ui import BoreholeUI
from borehole import Borehole
from model_ui import ModelUI
from model import Model
from mog_ui import MOGUI, MergeMog
from mog import Mog, AirShots
from info_ui import InfoUI
import time
import os
import data_manager

class DatabaseUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DatabaseUI, self).__init__()
        self.setWindowTitle("BhTomoPy/Database")
        #--- Other Modules Instance ---#
        self.actual_time = time.asctime()[11:16]
        self.bh = BoreholeUI()
        self.mog = MOGUI(self.bh)
        self.model = ModelUI(borehole=self.bh, mog=self.mog)
        self.info = InfoUI()
        self.mergemog = MergeMog(self.mog.MOGs)
        self.initUI()
        self.action_list = []
        self.filename = ''
        self.name = ''
        self.models = self.model.models
        self.boreholes = self.bh.boreholes
        self.mogs = self.mog.MOGs
        self.air = self.mog.air

        # DatabaseUI receives the signals, which were emitted by different modules, and transmits the signal to the other
        # modules in order to update them

        self.bh.bhUpdateSignal.connect(self.update_MogUI)
        self.bh.bhInfoSignal.connect(self.update_borehole_info)
        self.mog.mogInfoSignal.connect(self.update_mog_info)
        self.mog.ntraceSignal.connect(self.update_trace_info)
        self.model.modelInfoSignal.connect(self.update_model_info)
        self.mergemog.mergemoglogSignal.connect(self.update_log)
        self.bh.bhlogSignal.connect(self.update_log)
        self.mog.moglogSignal.connect(self.update_log)
        self.model.modellogSignal.connect(self.update_log)


    def update_spectra(self, Tx_list):
        self.mog.update_spectra_Tx_num_combo(Tx_list)
        self.mog.update_spectra_Tx_elev_value_label(Tx_list)

    def update_MogUI(self, list_bh):
        self.mog.update_Tx_and_Rx_Widget(list_bh)

    def update_database_info(self, name):
        self.info.update_database(name)

    def update_borehole_info(self, num):
        self.info.update_borehole(num)

    def update_mog_info(self, num):
        self.info.update_mog(num)

    def update_model_info(self, num):
        self.info.update_model(num)

    def update_trace_info(self, num):
        self.info.update_trace(num)

    def update_log(self, action):
        # Clears the log to make sure any action is not written more than once
        self.log.clear()

        # Appends the time and the action that was done
        self.action_list.append("[{}] {} " .format(self.actual_time, action))

        # Shows the Error messages in red and the others in black
        for item in self.action_list:

            if "Error:" in item:
                self.log.setTextColor(QtGui.QColor(QtCore.Qt.red))
                self.log.append(item)

            else:
                self.log.setTextColor(QtGui.QColor(QtCore.Qt.black))
                self.log.append(item)


    def show(self):
        super(DatabaseUI, self).show()

        # Gets initial geometry of the widget:
        qr = self.frameGeometry()

        # Shows it at the center of the screen
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()

        # Moves the window's center at the center of the screen
        qr.moveCenter(cp)

        # Then moves it at the top left
        translation = qr.topLeft()

        self.move(translation)
        
        if self.filename != '':
            self.load_file(self.filename)

    def openfile(self):

        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Database')[0]
        
        if filename:
            if filename[-3:] == '.db':
                self.load_file(filename)
            else:
                QtWidgets.QMessageBox.warning(self, 'Warning', "Database has wrong extension.",buttons=QtWidgets.QMessageBox.Ok)

    def load_file(self, filename):
        self.filename = filename
        
        data_manager.Session.close_all()
        data_manager.engine.dispose()
        
        data_manager.engine  = data_manager.create_engine("sqlite:///" + self.filename)
        data_manager.Session = data_manager.sessionmaker(bind=data_manager.engine)
        data_manager.session = data_manager.Session()
        data_manager.Base.metadata.create_all(data_manager.engine)
        
        try:
     
            self.bh.boreholes = data_manager.get(Borehole)
            self.mog.MOGs = data_manager.get(Mog)
            self.model.models = data_manager.get(Model)
            self.mog.air = data_manager.get(AirShots)
            
            self.update_database_info(os.path.basename(filename))
            self.update_log("Database '{}' was loaded successfully".format(os.path.basename(filename)))
     
            self.bh.update_List_Widget()
            self.bh.bh_list.setCurrentRow(0)
            self.bh.update_List_Edits()
     
            self.mog.update_List_Widget()
            self.mog.update_edits()
            self.mog.MOG_list.setCurrentRow(0)
            self.mog.update_spectra_and_coverage_Tx_num_list()
            self.mog.update_spectra_and_coverage_Tx_elev_value_label()
            self.mog.update_edits()
            self.mog.update_prune_edits_info()
            self.mog.update_prune_info()
      
            self.model.update_model_list()
            self.model.update_model_mog_list()
 
        except Exception as e:
            self.update_log("Error: Database was not recognised")
            QtWidgets.QMessageBox.warning(self, 'Warning', "Database could not be opened : '" + str(e)[:42] + "...' File may be empty or corrupted.",
                                       buttons=QtWidgets.QMessageBox.Ok)

    def savefile(self):

        try:
    
            if not self.filename:
                self.saveasfile()
                return

            data_manager.session.commit()
        
            try:
                self.model.gridui.update_model_grid()
            except:
                print("Warning : 'update_model_grid' skipped [database_ui 1]")
        
            self.update_log("Database was saved successfully")
            QtWidgets.QMessageBox.information(self, 'Success', "Database was saved successfully",
                                          buttons=QtWidgets.QMessageBox.Ok)

        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Warning', "Database could not be saved : " + str(e),
                                      buttons=QtWidgets.QMessageBox.Ok)

    def saveasfile(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Database as ...',
                                                     self.name, filter= 'Database (*.db)', )[0]
                                                     
        if filename:
            if filename != self.filename:
                self.filename = filename
                items = data_manager.get_many(Borehole, Mog, AirShots, Model)

                data_manager.Session.close_all()
                data_manager.engine.dispose()
                 
                data_manager.engine = data_manager.create_engine("sqlite:///" + filename)
                data_manager.Base.metadata.create_all(data_manager.engine)
                data_manager.Session.configure(bind=data_manager.engine)
                data_manager.session = data_manager.Session()

                for item in data_manager.get_many(Borehole, Mog, AirShots, Model):
                    data_manager.session.delete(item)
                
                items = [data_manager.session.merge(item) for item in items]
                data_manager.session.add_all(items)
                
                data_manager.session.commit()
                    
                self.bh.boreholes = data_manager.get(Borehole)
                self.mog.MOGs = data_manager.get(Mog)
                self.model.models = data_manager.get(Model)
                self.mog.air = data_manager.get(AirShots)
                
                self.update_database_info(os.path.basename(filename))
                self.update_log("Database '{}' was saved successfully".format(os.path.basename(filename)))
                    
    def editname(self):
        new_name = QtWidgets.QInputDialog.getText(self, "Change Name", 'Enter new name')

        self.name = new_name

        if new_name == '':
            return

        self.info.live_database_label.setText(str(new_name))

    def initUI(self):

        #--- Log Widget ---#
        self.log = QtWidgets.QTextEdit()
        self.log.setReadOnly(True)
        self.log.setLineWrapMode(0)

        #--- Actions ---#
        openAction = QtWidgets.QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.openfile)

        saveAction = QtWidgets.QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.savefile)

        saveasAction = QtWidgets.QAction('Save as', self)
        saveasAction.setShortcut('Ctrl+A')
        saveasAction.triggered.connect(self.saveasfile)

        editnameAction = QtWidgets.QAction('Edit database name', self)
        editnameAction.triggered.connect(self.editname)


        #--- Menubar ---#
        self.menu = QtWidgets.QMenuBar()
        filemenu = self.menu.addMenu('&File')
        filemenu.addAction(openAction)
        filemenu.addAction(saveAction)
        filemenu.addAction(saveasAction)

        editmenu = self.menu.addMenu('&Edit')
        editmenu.addAction(editnameAction)


        #--- GroupBoxes ---#
        #- Boreholes GroupBox -#
        bh_GroupBox =  QtWidgets.QGroupBox("Boreholes")
        bh_Sub_Grid   = QtWidgets.QGridLayout()
        bh_Sub_Grid.addWidget(self.bh)
        bh_GroupBox.setLayout(bh_Sub_Grid)

        #- MOGs GroupBox -#
        MOGs_GroupBox =  QtWidgets.QGroupBox("MOGs")
        MOGs_Sub_Grid   = QtWidgets.QGridLayout()
        MOGs_Sub_Grid.addWidget(self.mog)
        MOGs_GroupBox.setLayout(MOGs_Sub_Grid)

        #- Models GroupBox -#
        Models_GroupBox =  QtWidgets.QGroupBox("Models")
        Models_Sub_Grid   = QtWidgets.QGridLayout()
        Models_Sub_Grid.addWidget(self.model)
        Models_GroupBox.setLayout(Models_Sub_Grid)

        #- Info GroupBox -#
        Info_GroupBox =  QtWidgets.QGroupBox("Infos")
        Info_Sub_Grid   = QtWidgets.QGridLayout()
        Info_Sub_Grid.addWidget(self.info)
        Info_GroupBox.setLayout(Info_Sub_Grid)

        #- Big SubWidget -#
        sub_big_widget = QtWidgets.QWidget()
        sub_big_grid = QtWidgets.QGridLayout()
        sub_big_grid.addWidget(bh_GroupBox, 0, 0, 1, 1)
        sub_big_grid.addWidget(MOGs_GroupBox, 0, 1, 1, 3)
        sub_big_grid.addWidget(Models_GroupBox, 1, 0, 2, 2)
        sub_big_grid.addWidget(Info_GroupBox, 1, 2, 2, 3)
        sub_big_grid.setColumnStretch(0, 1)
        sub_big_grid.setColumnStretch(1, 1)
        sub_big_grid.setColumnStretch(2, 1)
        sub_big_widget.setLayout(sub_big_grid)
  
        #--- Grid ---#
        master_grid     = QtWidgets.QGridLayout()
        master_grid.addWidget(self.menu, 0, 0, 1, 3)
        master_grid.addWidget(sub_big_widget, 1, 0, 1, 3)
        master_grid.addWidget(self.log, 2, 0, 2, 3)
        master_grid.setContentsMargins(0, 0, 0, 0)
        master_grid.setVerticalSpacing(5)

        self.setLayout(master_grid)

class MyLogWidget(QtWidgets.QTextEdit):
    def __init__(self, parent =None):
        super(MyLogWidget, self).__init__(parent)

    def append(self, txt):
        super(MyLogWidget, self).append(txt)

        bottom = self.verticalScrollBar().maximum()
        self.verticalScrollBar().setValue(bottom)

if __name__ == '__main__':
    
    def Hook(Type, value, traceback):
        initial_ctx = traceback.tb_next
        while initial_ctx.tb_next is not None:
            initial_ctx = initial_ctx.tb_next
        sys.__excepthook__(Type, value, traceback)
    sys.excepthook = Hook # PyQt5 overrides Eclipse's exception catching. 'Hook' solves this issue.
    
    data_manager.Base.metadata.create_all(data_manager.engine)

    app = QtWidgets.QApplication(sys.argv)

    Database_ui = DatabaseUI()
    Database_ui.show()

    Database_ui.update_log("Welcome to BH TOMO Python Edition's Database")
#     Database_ui.filename = 'Database.db'
    Database_ui.bh.load_bh('testData/testConstraints/F3.xyz')
    Database_ui.bh.load_bh('testData/testConstraints/F2.xyz')
    Database_ui.mog.load_file_MOG('testData/formats/ramac/t0302.rad')
    Database_ui.mog.load_file_MOG('testData/formats/ramac/t0102.rad')
    Database_ui.model.load_model("t0302's model")
#     Database_ui.mog.plot_spectra()
#     Database_ui.mog.plot_zop()

#     Database_ui.saveasfile()

    sys.exit(app.exec_())
