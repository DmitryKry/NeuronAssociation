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
    int stepPlant = 25;
    void drawNeurons(QGraphicsScene* anotherScene, std::vector<std::vector<double>> currentLayer, int indent, double nextEnter = 0, int plant = 25);
    std::vector<QGraphicsLineItem*> drawWeight(QGraphicsScene* anotherScene, std::vector<std::vector<std::vector<double>>> anotherMatrix, bool bothChek = false);
    void drawStrongNeurons(std::vector<std::vector<double>> currentLaye, int indent, double nextEnter = 0, int plant = 25);
    void compare(std::vector<std::vector<std::vector<double>>> MatrixOne, std::vector<std::vector<std::vector<double>>> MatrixTwo,
                 std::vector<QGraphicsLineItem*> maitrisOne, std::vector<QGraphicsLineItem*> maitrisTwo);
    std::vector<std::vector<std::vector<double>>> readModel(std::string amotherSource = "model_weights_unick.txt");
    double inNumber(std::string another);
    void clearWeight();
    bool isNumber(char other);
    std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>> ListenerConv2D(std::string anotherSource, std::vector<std::vector<std::vector<double>>> &biasesGive);
    std::vector<std::vector<std::vector<double>>> ListenerDense(std::string anotherSource, std::vector<std::vector<std::vector<double>>> &biasesGive);
    void writeConv2D(std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>> matrixConv2D, std::vector<std::vector<double>> biasesGive);
    void writeDense(std::vector<std::vector<std::vector<double>>> matrixDense, std::vector<std::vector<double>> biasesGive);
    std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>> additionLayersConv2D(std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>> A,
                                                                                                 std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>> B);
    std::vector<std::vector<std::vector<double>>> additionLayersDense(std::vector<std::vector<std::vector<double>>> A,
                                                                                                 std::vector<std::vector<std::vector<double>>> B);
    std::vector<std::vector<std::vector<double>>> additionLayersBiases(std::vector<std::vector<std::vector<double>>> A,
                                                                                                 std::vector<std::vector<std::vector<double>>> B);
    void printLayersConv2dSResSizes(const std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>>>& LayersConv2dSRes);
    void printLayersDenseSResSizes(const std::vector<std::vector<std::vector<std::vector<double>>>>& denseRes);
    void printLayersBiasesSizes(const std::vector<std::vector<std::vector<std::vector<double>>>>& biasesRes);
    Ui::MainWindow *ui;
    QGraphicsScene* scene;
    QGraphicsScene *secondScene;
    QGraphicsView* view;
    int step = 25;
    std::vector<QGraphicsEllipseItem*> neyrons;
    std::vector<std::vector<QGraphicsEllipseItem*>> neyronses;
    std::vector<QGraphicsLineItem*> lines;
    std::vector<std::vector<pointXY>> setPointes;
    std::vector<pointXY> setTemp;
    std::vector<std::vector<std::vector<double>>> resArr;
    std::vector<std::vector<std::vector<double>>> resMatrix;
    double coefficient;
    bool exitWhen = false;

    std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>>> LayersConv2dS;
    std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>>> LayersConv2dSRes;
    std::vector<std::vector<std::vector<std::vector<double>>>> dense;
    std::vector<std::vector<std::vector<std::vector<double>>>> denseRes;
    std::vector<std::vector<std::vector<std::vector<double>>>> biasesConv2D;
    std::vector<std::vector<std::vector<std::vector<double>>>> biasesDense;
    std::vector<std::vector<std::vector<std::vector<double>>>> biasesConv2DRes;
    std::vector<std::vector<std::vector<std::vector<double>>>> biasesDenseRes;


    struct dopValue {
        static bool features;
        static bool matrix;
        static bool input_tensor;
        static bool conv_filters;
        static bool exit;
        static bool weights;
        static bool bias;
        static bool accessLister;
        static bool closed;
        static void clear() {
            dopValue::features = 0;
            dopValue::matrix = 0;
            dopValue::input_tensor = 0;
            dopValue::conv_filters = 0;
            dopValue::weights = 0;
            dopValue::bias = 0;
            dopValue::accessLister = 0;
            dopValue::closed = 0;
        }
    };
};


#endif // MAINWINDOW_H
