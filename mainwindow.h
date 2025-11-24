#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QWidget>
#include <QWidget>
#include <QPainter>
#include <QPen>
#include <QBrush>
#include <QColor>
#include <QApplication>
#include <QtWidgets>
#include <QApplication>
#include <QGraphicsScene>
#include <QGraphicsItem>
#include <QGraphicsView>
#include <QApplication>
#include <QObject>
#include <QBrush>
#include <QTimer>
#include <QGraphicsScene>
#include <QGraphicsView>
#include <QGraphicsLineItem>
#include <QGraphicsItem>
#include <QMainWindow>
#include <fstream>
namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    class pointXY{
        public:
        pointXY(int x, int y) : X(x), Y(y) {

        }
        int getX(){
            return X;
        }
        int getY(){
            return Y;
        }
    private:
        int X, Y;
    };

private:
    void drawNeurons(std::vector<std::vector<double>> currentLayer, int indent, double nextEnter = 0, int plant = 25);
    void drawWeight();
    void drawStrongNeurons(std::vector<std::vector<double>> currentLaye, int indent, double nextEnter = 0, int plant = 25);
    std::string source = "model_weights_unick.txt";
    void readModel();
    double inNumver(std::string another);
    void clearWeight();
    Ui::MainWindow *ui;
    QGraphicsScene* scene;
    QGraphicsView* view;
    int step = 25;
    std::vector<QGraphicsEllipseItem*> neyrons;
    std::vector<std::vector<QGraphicsEllipseItem*>> neyronses;
    std::vector<QGraphicsLineItem*> lines;
    std::vector<std::vector<pointXY>> setPointes;
    std::vector<pointXY> setTemp;
    std::vector<std::vector<std::vector<double>>> resArr;
    double coefficient;
    bool exitWhen = false;
};


#endif // MAINWINDOW_H
