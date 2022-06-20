import features as ft
import mainwindow as mw

if __name__ == "__main__":
    app = mw.MainWindow()
    feat = ft.Feature(app)
    app.mainloop()