#ifndef NEURALNETWORKWIDGET_H
#define NEURALNETWORKWIDGET_H

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
class NeuralNetworkWidget : public QWidget
{
    Q_OBJECT
public:
    explicit NeuralNetworkWidget(QWidget *parent = nullptr);

    void drawNeurons(int countEnter, int indent);
    void drawConnections();
private:
    int inputNeurons = 5;
    int hiddenNeurons = 15;
    int outputNeurons = 1;
};

#endif // NEURALNETWORKWIDGET_H
