import json
import os
from PySide2 import QtWidgets, QtCore

class Window_Import_Locators(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # Window settings.
        self.setWindowTitle("Import Locators")
        self.setFixedSize(400, 600)

        # Apply the Houdini stylesheet.
        self.setStyleSheet(hou.qt.styleSheet())

        # Build layout.
        self.build_layout()

    def build_layout(self):
        """Build layout."""

        # Create vertical layout.
        lyt_principal = QtWidgets.QVBoxLayout()
        self.setLayout(lyt_principal)

        # GroupBox to import json file.
        gb_json = QtWidgets.QGroupBox()
        gb_json.setMaximumHeight(80)
        lyt_gb_json = QtWidgets.QGridLayout()
        gb_json.setLayout(lyt_gb_json)
        lyt_principal.addWidget(gb_json)

        # GroupBox to select Locators.
        gb_locators = QtWidgets.QGroupBox()
        lyt_gb_locators = QtWidgets.QVBoxLayout()
        gb_locators.setLayout(lyt_gb_locators)
        lyt_principal.addWidget(gb_locators)

        # GroupBox with Import button.
        gb_import = QtWidgets.QGroupBox()
        lyt_gb_import = QtWidgets.QVBoxLayout()
        gb_import.setLayout(lyt_gb_import)
        lyt_principal.addWidget(gb_import)

        # Text info.
        lyt_gb_json.addWidget(
        QtWidgets.QLabel("Select json file."),
        0,0)

        # Json file path.
        self.json_file = QtWidgets.QLineEdit()
        self.json_file.setReadOnly(True)
        lyt_gb_json.addWidget(self.json_file, 1,0)

        # Import json button.
        b_find_json = QtWidgets.QPushButton("Browse")
        b_find_json.clicked.connect(self.find_json)
        lyt_gb_json.addWidget(b_find_json, 1,1)

        # Checkbox to select all locators.
        self.checkbox_all = QtWidgets.QCheckBox(
        "Import all locators")
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

        # ComboBox to select the way to import.
        self.import_mode = QtWidgets.QComboBox()
        self.import_mode.addItem("Import in one Add node")
        self.import_mode.addItem("Import in different Add nodes")
        lyt_gb_import.addWidget(self.import_mode)

        # Checkbox to set convert units setting.
        self.check_convert_units = QtWidgets.QCheckBox(
        "Convert Units")
        self.check_convert_units.setChecked(1)
        lyt_gb_import.addWidget(self.check_convert_units)

        # Button to import locators to houdini.
        b_import = QtWidgets.QPushButton("Import")
        b_import.clicked.connect(self.import_locators)
        lyt_gb_import.addWidget(b_import)

    def find_json(self):
        """Window to select json file.
        And check if it is a valid json."""

        prev_file_path = os.path.dirname(self.json_file.text())
        select_file = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select json file from Maya",
            prev_file_path,
            "JSON Files (*.json)"
            )

        # Keep only the json file.
        selected_file = select_file[0]
        self.json_file.setText(selected_file)

        # Check if it is a valid json.
        is_valid = self.verify_valid_json(selected_file)

        # Update list with locators.
        if is_valid:
            self.list_locators.clear()
            self.update_locators_list(selected_file)
        else:
            self.list_locators.clear()

    def verify_valid_json(self, selected_file):
        """Check if it is a valid json.
        return True : is a valid json.
        return False : isn't a valid json."""
        
        # Check if json file exists.
        if not os.path.exists(selected_file):
            return False

        # Verify if json is valid.
        with open(selected_file, "r") as fjson:
            self.data = json.load(fjson)
            first_values = self.data.get("LocatorsFromMaya", None)
        if first_values == [0,0,0]:
            return True
        else:
            hou.ui.displayMessage("Select a valid json.")
            return False

    def update_locators_list(self, selected_file):
        """Add all locators from json to list."""

        for locator_name in self.data["locators"]:

            # Add element with the same name it has in the json.
            item = QtWidgets.QListWidgetItem(locator_name)

            # Add state to item.
            if self.checkbox_all.isChecked():
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

            # Add item to the list.
            self.list_locators.addItem(item)

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

    def import_locators(self):
        """Import locators to houdini."""

        # If there are no locators, return.
        if self.list_locators.count() == 0:
            return

        # Dic with name of locators and their coordinates.
        dic_to_export = self.get_items_to_import()

        # Import mode.
        mode = self.import_mode.currentIndex()

        # In case "Import all in a Add node"
        if mode == 0:

            # Create add node.
            obj = hou.node("/obj")
            geo_node = obj.createNode("geo")
            add_node = geo_node.createNode("add")

            # Iter by locators.
            for locator in dic_to_export.keys():

                # Add new point.
                new_p = add_node.parm("points").eval() + 1
                add_node.parm("points").set(new_p)

                px = "pt" + str(new_p-1) + "x"
                py = "pt" + str(new_p-1) + "y"
                pz = "pt" + str(new_p-1) + "z"

                # Get coordinates.
                pos = dic_to_export[locator]

                # Convert units.
                if self.check_convert_units.isChecked():
                    for eje in range(len(pos)):
                        new_val = pos[eje] / 10
                        # Save new position.
                        pos[eje] = new_val

                # Set position.
                add_node.parm(px).set(pos[0])
                add_node.parm(py).set(pos[1])
                add_node.parm(pz).set(pos[2])

        # In case "Import in different Add nodes"
        elif mode == 1:
            obj = hou.node("/obj")
            geo_node = obj.createNode("geo")

            # Iter by locators.
            for locator in dic_to_export.keys():

                # Create add node.
                add_node = geo_node.createNode("add", locator)

                # Set new point to that add node.
                add_node.parm("points").set(1)

                # Get coordinates.
                pos = dic_to_export[locator]

                # Convert units.
                if self.check_convert_units.isChecked():
                    for eje in range(len(pos)):
                        new_val = pos[eje] / 10
                        # Save new position.
                        pos[eje] = new_val

                # Set position.
                add_node.parm("pt0x").set(pos[0])
                add_node.parm("pt0y").set(pos[1])
                add_node.parm("pt0z").set(pos[2])

            # Fix layout.
            geo_node.layoutChildren()

        # Close window.
        self.close()

        # Final notification.
        hou.ui.displayMessage("Locators Imported")

    def get_items_to_import(self):
        """Get items wich will be imported.
        returns dictionary with selected items."""

        dic = {}

        # Iter by the list.
        for item_number in range(self.list_locators.count()):
            item = self.list_locators.item(item_number)

            # Check if it that item is checked.
            if item.checkState() == QtCore.Qt.Checked:
                # Get name.
                item_name = item.text()
                # Get its position.
                pos = self.data["locators"][item_name]

                # Add to dictionary.
                dic[item_name] = pos

        return dic

ui = Window_Import_Locators()
ui.show()