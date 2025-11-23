#include "neuralnetworkwidget.h"

NeuralNetworkWidget::NeuralNetworkWidget(QWidget *parent)
    : QWidget(parent)
{
    resize(800, 600); // Начальный размер, но можно менять
    setMinimumSize(400, 300);
}

void NeuralNetworkWidget::drawNeurons(int countEnter, int indent)
{
    QGraphicsScene *scene = new QGraphicsScene(this);
    int step = 10;
    std::vector<QGraphicsEllipseItem*> circles;
    for (int i = 0; i < countEnter; i++, step += step){
        circles.push_back(new QGraphicsEllipseItem(indent, 0 - step, 100, 100));
        scene->addItem(circles[i]);
    }

}

void NeuralNetworkWidget::drawConnections()
{

}
