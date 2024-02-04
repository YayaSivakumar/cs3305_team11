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
                    border: 2px solid #2e2e2e;
                    border-radius: 10px;
                    padding: 10px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    border-color: #4f4f4f;
                    background-color: #6e6e6e;
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
            QTreeView {
                    color: #000;
            }
            QLabel {
                    color: #000;
            }
            QMessageBox {
                    color: #000;
            }
            QPushButton {
                border: 2px solid #8F8F8F;
                border-radius: 10px;
                background-color: #E0E0E0;
                padding: 10px;
                min-width: 80px;
                color: #000;
            }
            QPushButton:hover {
                border-color: #3daee9;
                background-color: #AEE0E0;
            }
            """
