import os
import webbrowser


if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:8000')
    os.system("shiny run --reload app.py")