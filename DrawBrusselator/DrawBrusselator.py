#
# ブラッセレータの方程式を差分で計算し位相図を描く
#
# Reference
#   郡宏,「振動と同期の数学的思考法I」,時間生物学, Vol.18 ,No.1,(2012),http://chronobiology.jp/journal/JSC2012-2-080.pdf
#   yukara_13,「【Python】 ぬるぬる動くスペクトルアナライザを作ろう！！」, http://yukara-13.hatenablog.com/entry/2013/12/05/025655
#
import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import pyaudio as pa

###パラメーター
# 微分方程式離散化のための微少時間
dt=0.1   
# ブラッセレータの方程式のパラメータ
a=1
b=2.8

### 差分化ブラッセレータの式
# x[n]=f(x[n-1],y[n-1],a,b)を求める関数
def xn(xp,yp):
    return dt*xp**2*yp+(1-(1+b)*dt)*xp+a*dt
# y[n]=f(x[n-1],y[n-1],a,b)を求める関数
def yn(xp,yp):
    return (1-dt*xp**2)*yp+b*dt*xp


wave = np.array([])

### グラフウィンドウの定義
def plot():
    ### 配列x[n],y[n]の準備．用意された要素数の点を描く
    x = np.zeros(2000)
    y = np.zeros(2000)

    ### アプリケーション作成
    app = QtGui.QApplication([])
    app.quitOnLastWindowClosed()

    ### メインウィンドウ
    mainWindow = QtGui.QMainWindow()
    mainWindow.resize(800, 800) # ウィンドウサイズ

    ### キャンバス
    centralWid = QtGui.QWidget()
    mainWindow.setCentralWidget(centralWid)

    ### レイアウト
    lay = QtGui.QVBoxLayout()
    centralWid.setLayout(lay)
    
    ### グラフ表示用ウィジット
    plotWid = pg.PlotWidget(name="DrawBrusselator")
    plotItem = plotWid.getPlotItem()
    plotItem.setMouseEnabled(y = False)
    plotItem.setYRange(min(y), max(y))
    plotItem.setXRange(min(x), max(x))
    ### Axis
    yAxis = plotItem.getAxis('left')

    ### キャンバスにウィジットをのせる
    lay.addWidget(plotWid)
    
    ### ウィンドウ表示
    mainWindow.show()

    ### グラフを描き続ける
    while True:
        xp = x[-1]
        yp = y[-1]
        # 点列に新しい要素を加える．FIFO動作
        x = np.delete(np.append(x,xn(xp,yp)),0)
        y = np.delete(np.append(y,yn(xp,yp)),0)
        try:
            plotItem.setYRange(0, 5)
            plotItem.setXRange(0, 5)
            plotItem.plot(x,y, clear = True) # clearフラグを付けるとグラフを書き直す
        except KeyboardInterrupt :
            sys.exit(0)
        QtGui.QApplication.processEvents()

    
if __name__ == "__main__":
    plot()
