def dark_style():
    return '''
                QMainWindow {
                    background-color: #2e2e2e;
                }
                QLabel {
                    color: #fff;
                }
                QTreeView {
                    background-color: #393939;
                    color: #fff;
                }
                QPushButton {
                    background-color: #5e5e5e;
                    color: #fff;
                    border: 1px solid #2e2e2e;
                }
                QMessageBox {
                    background-color: #393939;
                    color: #fff;
                }
            '''


def light_style():
    return """
            QMainWindow {
                background-color: #F5F5F5;
            }
            QPushButton {
                border: 2px solid #8F8F8F;
                border-radius: 10px;
                background-color: #E0E0E0;
                padding: 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                border-color: #3daee9;
                background-color: #AEE0E0;
            }
            """
