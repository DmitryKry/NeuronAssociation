#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <qDebug>
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    scene = new QGraphicsScene(this);
    resize(1920, 1080);
    view = new QGraphicsView(scene, this);
    setCentralWidget(view);
    scene->setSceneRect(0, 0, 1920, 5000);
    int stepArr = 450;
    int index = 0;
    coefficient = 5.5;

    resArr = readModel("model_weights_non_unickTwo.txt");


    int bigArr = resArr[0].size();
    for (int i = 1; i < resArr.size(); i++){
        if (bigArr < resArr[i].size())
            bigArr = resArr[i].size();
    }/*
    for (std::vector<std::vector<double>> elem : resArr) {
        drawNeurons(elem.size(), 50 + stepArr * index++, bigArr == elem.size() ? 0 : (bigArr / elem.size()) * 1.6);
    }*/

    for (std::vector<std::vector<double>> elem : resArr) {
        drawNeurons(elem, 50 + stepArr * index++, bigArr == elem.size() ? 0 : (bigArr / elem.size()) * coefficient);
    }
    for (std::vector<pointXY> tempElem : setPointes){
        for (pointXY tempPoint : tempElem){
            qDebug() << tempPoint.getX() << ' ' << tempPoint.getY() ;
        }
        qDebug() << endl;
    }

    std::vector<QGraphicsLineItem*> maitrisOne = drawWeight(resArr);

    resMatrix = readModel("model_weights_non_unick.txt");
    std::vector<QGraphicsLineItem*> maitrisTwo = drawWeight(resMatrix);
    for (QGraphicsLineItem* item : maitrisTwo)
        item->setPen(QPen(Qt::red, 2));
    compare(resMatrix, resArr, maitrisTwo, maitrisOne);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::drawNeurons(std::vector<std::vector<double>> currentLayer, int indent, double nextEnter, int plant)
{
    for (int i = 0, q = nextEnter == 0 ? plant : (plant * (nextEnter)) + plant; i < currentLayer.size(); i++, q += plant){
        neyrons.push_back(new QGraphicsEllipseItem(indent, q, 5, 5));
        setTemp.push_back(pointXY(indent, q));
        if (setPointes.size()){
            for (int j = 0; j < setPointes[setPointes.size() - 1].size(); j++){
                pointXY positionOne = setPointes[setPointes.size() - 1][j];
                pointXY positionTwo = setTemp[setTemp.size() - 1];
                lines.push_back(new QGraphicsLineItem(positionOne.getX(), positionOne.getY(), positionTwo.getX(), positionTwo.getY()));
                //qDebug() << positionOne.getX() << " - " << positionOne.getY() << " - " << positionTwo.getX() << " - " << positionTwo.getY() << " - ";
                lines[lines.size() - 1]->setPen(QPen(Qt::black, 1));
                scene->addItem(lines[lines.size() - 1]);
            }
        }
        neyrons[i]->setBrush(QBrush(Qt::white)); // Заливка
        neyrons[i]->setPen(QPen(Qt::black, 2)); // Контур

        scene->addItem(neyrons[i]);
    }
    setPointes.push_back(setTemp);
    qDebug() << "setPointes.size() - " << setPointes.size() << endl;
    setTemp.clear();
    neyronses.push_back(neyrons);
    neyrons.clear();
}

void MainWindow::drawStrongNeurons(std::vector<std::vector<double>> currentLayer, int indent, double nextEnter, int plant)
{
    for (int i = 0, q = nextEnter == 0 ? plant : (plant * (nextEnter)) + plant; i < currentLayer.size(); i++, q += plant){
        neyrons.push_back(new QGraphicsEllipseItem(indent, q, 5, 5));
        setTemp.push_back(pointXY(indent, q));

        neyrons[i]->setBrush(QBrush(Qt::white)); // Заливка
        neyrons[i]->setPen(QPen(Qt::black, 2)); // Контур

        scene->addItem(neyrons[i]);
    }
    setPointes.push_back(setTemp);
    setTemp.clear();
    neyronses.push_back(neyrons);
    neyrons.clear();
}

double MainWindow::inNumver(std::string another){
    int numbers[10] = { '0', '1',  '2',  '3',  '4',  '5',  '6',  '7',  '8', '9' };
    double temp = 0;
    int size = another.size();
    bool negativ = false;
    bool drob = false;
    int part = 0;
    for (char elem : another) {
        if (elem == '-')
            size--;
        if (elem == '.')
            size--;
    }
    for (int i = 0; i < another.size(); i++) {
        if (another[i] == '-') {
            negativ = true;
            continue;
        }
        for (int j = 0; j < 10; j++) {
            if (another[i] == '.') {
                drob = true;
                break;
            }
            if (another[i] == numbers[j]) {
                if (drob == true) {
                    temp += pow(10, -++part) * j;
                    break;
                }
                else {
                    temp += pow(10, (size - 2) - i) * j;
                    break;
                }
            }
        }
    }
    return negativ == true ? temp - (temp * 2) : temp;
}

std::vector<std::vector<std::vector<double>>> MainWindow::readModel(std::string amotherSource){
    std::vector<std::vector<double>> examples;
    std::vector<std::vector<std::vector<double>>> resMatrix;
    std::string line = "";
    std::string all = "";
    char byte;
    bool addArray = false;
    bool roolListener = false;
    bool cheakD = false;
    int degree = 0, res = 0;
    std::ifstream infile(amotherSource);  // Создание объекта для чтения
    if (!infile.is_open()) {
        qDebug() << "Ошибка открытия файла!" << endl;
    }
    else{
        while (infile.get(byte)) {  // читаем побайтно
            all += byte;
            if (byte == '(' && !cheakD) {
                roolListener = true;
                continue;
            }
            if (byte == ')') {
                if (line == "Dense") {
                    cheakD = true;
                    line = "";
                    roolListener = false;
                    continue;
                }
                else {
                    line = "";
                    roolListener = false;
                    continue;
                }
            }
            if (cheakD && byte == '[' && addArray) {
                examples.push_back(std::vector<double>());
                roolListener = true;
                continue;
            }
            if (cheakD && byte == '[') {
                roolListener = true;
                addArray = true;
                continue;
            }
            if (byte == ']' && !roolListener && cheakD) {
                //addArray = false;
                cheakD = false;
                line = "";
                continue;
            }
            if (byte == ']' && roolListener && cheakD) {
                examples[examples.size() - 1].push_back(inNumver(line));
                line = "";
                roolListener = false;
                continue;
            }
            if ((byte == ',') && roolListener && cheakD) {
                examples[examples.size() - 1].push_back(inNumver(line));
                line = "";
                continue;
            }
            if (byte == '[' && !roolListener) {
                cheakD = false;
                continue;
            }
            if (roolListener && byte != ' ')
                line += byte;
        }
        std::vector<std::vector<double>> tempArr;
        for (std::vector<double> elements : examples) {
            if (elements.size() != 0)
                tempArr.push_back(elements);
            for (double element : elements) {
                qDebug() << element << '\t';
            }
            qDebug() << endl;
            if (elements.size() == 0) {
                resMatrix.push_back(tempArr);
                tempArr.clear();
            }
        }
        resMatrix.push_back(tempArr);
        qDebug() << "Кол-во матриц - " << resMatrix.size() << endl;
        for (std::vector<std::vector<double>> elem : resMatrix) {
            qDebug() << "Кол-во входов - " << elem.size() << endl;
        }
    }
    return resMatrix;
}

std::vector<QGraphicsLineItem*> MainWindow::drawWeight(std::vector<std::vector<std::vector<double>>> anotherMatrix)
{
    std::vector<QGraphicsLineItem*> strongLines;
    for (int i = 0; i < anotherMatrix.size() - 1; i++){
        for (int j = 0; j < anotherMatrix[i].size(); j++){
            double maxPoint = anotherMatrix[i][j][0];
            int maxIndex = 0;
            for (int q = 0; q < anotherMatrix[i][j].size(); q++){
                if (maxPoint < anotherMatrix[i][j][q]){
                    maxPoint = anotherMatrix[i][j][q];
                    maxIndex = q;
                }
            }
            QGraphicsLineItem* StrongLint = new QGraphicsLineItem(setPointes[i][j].getX(), setPointes[i][j].getY(), setPointes[i + 1][maxIndex].getX(), setPointes[i + 1][maxIndex].getY());
            scene->addItem(StrongLint);
            StrongLint->setPen(QPen(Qt::yellow, 2));
            strongLines.push_back(StrongLint);
        }
    }
    return strongLines;
}


void MainWindow::compare(std::vector<std::vector<std::vector<double>>> MatrixOne, std::vector<std::vector<std::vector<double>>> MatrixTwo,
                         std::vector<QGraphicsLineItem*> maitrisOne, std::vector<QGraphicsLineItem*> maitrisTwo){
    for (QGraphicsLineItem* item : maitrisOne)
        qDebug() << item << ' ';
    qDebug() << '\n';
    qDebug() << 'maitrisOne.size() - ' << maitrisOne.size();
    qDebug() << '\n';
    if (MatrixOne.size() != MatrixTwo.size() ||
            MatrixOne[0].size() != MatrixTwo[0].size() ||
            MatrixOne[0][0].size() != MatrixTwo[0][0].size()) {
            qDebug() << "Матрицы имеют разные размеры!" << endl;
            return;
        }
    for (size_t i = 0; i < MatrixOne.size(); ++i) {
        for (size_t j = 0; j < MatrixOne[i].size(); ++j) {
            for (size_t k = 0; k < MatrixOne[i][j].size(); ++k) {
                if (MatrixOne[i][j][k] == MatrixTwo[i][j][k]) {
                    qDebug() << "Совпадение в индексах [" << i << "][" << j << "][" << k
                              << "]: значение = " << MatrixOne[i][j][k] << endl;
                    maitrisOne[i * j * k]->setPen(QPen(Qt::blue, 2));
                }
            }
        }
    }
}


