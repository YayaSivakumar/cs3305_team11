class ToastStyle:
    def __init__(self, opacity=1.0, font_size=12):
        self.opacity = opacity
        self.font_size = font_size

    def get_main_style(self):
        return f'''
            border: 2px solid #2e2e2e;
            border-radius: 10px;
            padding: 10px;
            opacity: {self.opacity};
            font-size: {self.font_size}px;
        '''

    def get_label_style(self):
        return f'''
            color: #000000;
            font-size: {self.font_size}px;
        '''

    def get_close_style(self):
        return f'''
            color: #000000
            font-size: {self.font_size}px;
        '''
#        alignment styling to put to top right


class SuccessStyle(ToastStyle):
    def get_style(self):
        return f'''
            background-color: rgba(76, 175, 80, {self.opacity});
            color: #000000;
        '''


class AlertStyle(ToastStyle):
    def get_style(self):
        return f'''
            background-color: rgba(255, 193, 7, {self.opacity});
            color: #000000;
        '''


class ErrorStyle(ToastStyle):
    def get_style(self):
        return f'''
            background-color: rgba(244, 67, 54, {self.opacity});
            color: #000000;
        '''


class InfoStyle(ToastStyle):
    def get_style(self):
        return f'''
            background-color: rgba(51, 51, 51, {self.opacity});
            color: #000000;
        '''
