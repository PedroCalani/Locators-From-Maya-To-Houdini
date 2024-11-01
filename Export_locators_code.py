import maya.cmds as cmds
import json
import os
from PySide6 import QtWidgets, QtCore

class Window_Export_Locators(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # Window settings.
        self.setWindowTitle("Export Locators")
        self.setFixedSize(400, 600)

        # Build layout.
        self.build_layout()

    def build_layout(self):
        """Build layout."""

        # Create vertical layout.
        lyt_principal = QtWidgets.QVBoxLayout()
        self.setLayout(lyt_principal)

        # GroupBox with json file settings.
        gb_json = QtWidgets.QGroupBox()
        gb_json.setMaximumHeight(150)
        lyt_gb_json = QtWidgets.QGridLayout()
        gb_json.setLayout(lyt_gb_json)
        lyt_principal.addWidget(gb_json)

        # GroupBox to select Locators.
        gb_locators = QtWidgets.QGroupBox()
        lyt_gb_locators = QtWidgets.QVBoxLayout()
        gb_locators.setLayout(lyt_gb_locators)
        lyt_principal.addWidget(gb_locators)

        # GroupBox with Export button.
        gb_export = QtWidgets.QGroupBox()
        lyt_gb_export = QtWidgets.QVBoxLayout()
        gb_export.setLayout(lyt_gb_export)
        lyt_principal.addWidget(gb_export)

        # Text info.
        lyt_gb_json.addWidget(
        QtWidgets.QLabel(
        "Replace an existing json or Create a new."),
        0,0)

        # Json file.
        self.json_file = QtWidgets.QLineEdit()
        self.json_file.setReadOnly(True)
        lyt_gb_json.addWidget(self.json_file, 1,0)

        # Select folder button.
        b_select_folder = QtWidgets.QPushButton("Select Json")
        b_select_folder.clicked.connect(self.select_folder)
        lyt_gb_json.addWidget(b_select_folder, 1,1)

        # Checkbox to select all locators.
        self.checkbox_all = QtWidgets.QCheckBox(
        "export all locators")
        self.checkbox_all.setChecked(1)
        self.checkbox_all.clicked.connect(
        self.update_all_locators)
        lyt_gb_locators.addWidget(self.checkbox_all)

        # List with locators.
        self.list_locators = QtWidgets.QListWidget()
        self.list_locators.itemChanged.connect(
        self.item_state_changed)
        self.list_locators.setSelectionMode(
        QtWidgets.QAbstractItemView.ExtendedSelection)
        lyt_gb_locators.addWidget(self.list_locators)

        # Load locators.
        self.load_locators()

        # Button to export locators.
        b_export = QtWidgets.QPushButton("Export")
        b_export.clicked.connect(self.export_locators)
        lyt_gb_export.addWidget(b_export)

    def load_locators(self):
        """Load all scene locators in the list."""

        # Get all locators.
        self.all_locators_in_scene = cmds.ls(type="locator")

        for l in self.all_locators_in_scene:
            # Create new item.
            item = QtWidgets.QListWidgetItem(l)

            # Apply state.
            if self.checkbox_all.isChecked():
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

            # Add item to list.
            self.list_locators.addItem(item)

    def select_folder(self):
        """"Window to select where save json file."""

        # Open window to configure json.
        info = "Select where save the Json File."
        prev_file = self.json_file.text()
        new_file = QtWidgets.QFileDialog.getSaveFileName(
            self, info, prev_file,
            "JSON File (*.json)"
        )

        # Add file to json_file widget.
        selected = new_file[0]
        if selected != "":
            self.json_file.setText(selected)

    def update_all_locators(self, state):
        """Change all item states at the same time."""
        
        # Check state of checkbox.
        if state == True: checked = QtCore.Qt.Checked
        if state == False: checked = QtCore.Qt.Unchecked

        # Update states.
        for locator in range(self.list_locators.count()):
            current_locator = self.list_locators.item(locator)
            current_locator.setCheckState(checked)

    def item_state_changed(self, item):
        """Change state of selected items."""

        # Current state.
        state = item.checkState()

        # Update checkbox_all.
        if self.checkbox_all.isChecked():
            if state == QtCore.Qt.Unchecked:
                self.checkbox_all.setChecked(False)

        # Update state on all selected items.
        selected_items = self.list_locators.selectedItems()
        for i in selected_items:
            i.setCheckState(state)

    def export_locators(self):
        """export locators to houdini."""

        print("PUSH")
        # If there are no locators, return.
        if self.list_locators.count() == 0:
            print("0")
            return

        dic = {
            "LocatorsFromMaya" : [0,0,0],
            "locators" : {}
            }

        # Dic with name of locators and their coordinates.
        dic["locators"] = self.get_items_to_export()

        # Write json.
        with open(self.json_file.text(), "w") as jfile:
            json.dump(dic, jfile, indent=4)

        # Close window.
        self.close()

        # Final Notification.
        cmds.confirmDialog(title="Locators Exported.", 
                   message="Json file has been created.", 
                   button=['OK'], 
                   defaultButton='OK')

    def get_items_to_export(self):
        """Get items wich will be exported.
        returns dictionary with selected items."""

        dic = {"locators": {}}

        # Iter by the list.
        for item_number in range(self.list_locators.count()):
            item = self.list_locators.item(item_number)

            # Check if it that item is checked.
            if item.checkState() == QtCore.Qt.Checked:

                # Get name.
                item_name = item.text()
                print(f"ITEM NAME: {item_name}")

                # Node transform.
                transform_node = cmds.listRelatives(
                    item_name, parent=True)[0]

                pos = cmds.xform(
                    transform_node,
                    query=True, 
                    translation=True,
                    worldSpace=True
                    )

                # Save in dictionary.
                dic["locators"][item_name] = pos

        return dic["locators"]

if __name__ == "__main__":
    ui = Window_Export_Locators()
    ui.show()