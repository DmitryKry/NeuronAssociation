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
    setWindowTitle("Оригинальная нейронная модель");
    scene->setSceneRect(0, 0, 1920, 5000);
    const int stepArr = 450;
    int index = 0;
    coefficient = 3;
        QMainWindow *secondWindow = new QMainWindow();
        secondWindow->setWindowTitle("Объедининение нейронных моделей");
        secondWindow->resize(1920, 1080);

        secondScene = new QGraphicsScene(secondWindow);
        QGraphicsView *secondView = new QGraphicsView(secondScene, secondWindow);
        secondWindow->setCentralWidget(secondView);
        secondScene->setSceneRect(0, 0, 1920, 5000);
    resArr = readModel("simpleModelFirst.txt");


    int bigArr = resArr[0].size();
    for (int i = 1; i < resArr.size(); i++){
        if (bigArr < resArr[i].size())
            bigArr = resArr[i].size();
    }/*
    for (std::vector<std::vector<double>> elem : resArr) {
        drawNeurons(elem.size(), 50 + stepArr * index++, bigArr == elem.size() ? 0 : (bigArr / elem.size()) * 1.6);
    }*/

    for (std::vector<std::vector<double>> elem : resArr) {
        int ras = bigArr == elem.size() ? 0 : ((bigArr - elem.size()) / 2);
        drawNeurons(scene, elem, 50 + stepArr * index++, ras);
    }
    for (std::vector<pointXY> tempElem : setPointes){
        for (pointXY tempPoint : tempElem){
            qDebug() << tempPoint.getX() << ' ' << tempPoint.getY() ;
        }
        qDebug() << endl;
    }

    std::vector<QGraphicsLineItem*> maitrisOne = drawWeight(scene, resArr);

    resMatrix = readModel("square_detector_model_29.h5_weights.txt");
    std::vector<QGraphicsLineItem*> maitrisTwo = drawWeight(scene, resMatrix);
    for (QGraphicsLineItem* item : maitrisTwo)
        item->setPen(QPen(Qt::red, 2));
    compare(resMatrix, resArr, maitrisTwo, maitrisOne);
    index = 0;
    bigArr *= 2;
    setPointes.clear();
    for (int i = 0; i < resArr.size(); i++) {
        std::vector<std::vector<double>> bothMatrix;

        for (std::vector<double> poDelem : resArr[i])
            bothMatrix.push_back(poDelem);

        for (std::vector<double> poDelem : resMatrix[i])
            bothMatrix.push_back(poDelem);
        int sizeBoth = bothMatrix.size();
        int ras = bigArr == bothMatrix.size() ? 0 : ((bigArr - bothMatrix.size()) / 2);
        drawNeurons(secondScene, bothMatrix, 50 + stepArr * index++, ras);
    }
    drawWeight(secondScene, resArr);

    std::vector<QGraphicsLineItem*> BothMaitrix = drawWeight(secondScene, resMatrix, true);
    for (QGraphicsLineItem* item : BothMaitrix)
        item->setPen(QPen(Qt::red, 2));
    secondWindow->show();
}
bool MainWindow::dopValue::features = false;
bool MainWindow::dopValue::matrix = false;
bool MainWindow::dopValue::input_tensor = false;
bool MainWindow::dopValue::conv_filters = false;
bool MainWindow::dopValue::exit = false;
bool MainWindow::dopValue::weights = false;
bool MainWindow::dopValue::bias = false;
bool MainWindow::dopValue::accessLister = false;
bool MainWindow::dopValue::closed = false;
MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::drawNeurons(QGraphicsScene* anotherScene, std::vector<std::vector<double>> currentLayer, int indent, double nextEnter, int plant)
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
                anotherScene->addItem(lines[lines.size() - 1]);
            }
        }
        neyrons[i]->setBrush(QBrush(Qt::white)); // Заливка
        neyrons[i]->setPen(QPen(Qt::black, 2)); // Контур

        anotherScene->addItem(neyrons[i]);
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

double MainWindow::inNumber(std::string another) {
    char numbers[10] = { '0', '1',  '2',  '3',  '4',  '5',  '6',  '7',  '8', '9' };
    double temp = 0;
    int size = 0;
    bool negativ = false;
    bool drob = false;
    int part = 0;
    for (char elem : another) {
        if (elem == '-')
            continue;
        if (elem == '.')
            break;
        size++;
    }
    if (another[0] != '-') {
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
                    temp += pow(10, (size) - i) * j;
                    break;
                }
            }
        }
    }
    return negativ == true ? temp - (temp * 2) : temp;
}

bool MainWindow::isNumber(char other) {
    char numbers[10] = { '0', '1',  '2',  '3',  '4',  '5',  '6',  '7',  '8', '9' };
    int i = 0;
    while (i < 10) {
        if (other == numbers[i++]) {
            return true;
        }
    }
    return false;
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
                examples[examples.size() - 1].push_back(inNumber(line));
                line = "";
                roolListener = false;
                continue;
            }
            if ((byte == ',') && roolListener && cheakD) {
                examples[examples.size() - 1].push_back(inNumber(line));
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

std::vector<QGraphicsLineItem*> MainWindow::drawWeight(QGraphicsScene* anotherScene, std::vector<std::vector<std::vector<double>>> anotherMatrix, bool bothChek)
{
    std::vector<QGraphicsLineItem*> strongLines;
    if (!bothChek){
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
                QGraphicsLineItem* StrongLint;
                StrongLint = new QGraphicsLineItem(setPointes[i][j].getX(), setPointes[i][j].getY(), setPointes[i + 1][maxIndex].getX(), setPointes[i + 1][maxIndex].getY());
                anotherScene->addItem(StrongLint);
                StrongLint->setPen(QPen(Qt::yellow, 2));
                strongLines.push_back(StrongLint);
            }
        }
    }
    else {
        for (int i = 0; i < anotherMatrix.size() - 1; i++){
            for (int j = anotherMatrix[i].size() - 1; j >= 0; j--){
                double maxPoint = anotherMatrix[i][j][0];
                int maxIndex = 0;
                for (int q = 0; q < anotherMatrix[i][j].size(); q++){
                    if (maxPoint < anotherMatrix[i][j][q]){
                        maxPoint = anotherMatrix[i][j][q];
                        maxIndex = q;
                    }
                }
                QGraphicsLineItem* StrongLint;
                int tempY = maxIndex;
                StrongLint = new QGraphicsLineItem(setPointes[i][j].getX(), setPointes[i][j].getY() + (stepPlant * anotherMatrix[i].size()),
                                                   setPointes[i + 1][maxIndex].getX(), setPointes[i + 1][maxIndex].getY() + (stepPlant * anotherMatrix[i][j].size()));
                anotherScene->addItem(StrongLint);
                StrongLint->setPen(QPen(Qt::yellow, 2));
                strongLines.push_back(StrongLint);
            }
        }
    }

    return strongLines;
}

std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>> MainWindow::ListenerConv2D(std::string anotherSource, std::vector<std::vector<std::vector<double>>> &biasesGive){
    std::vector<double> bias;
        std::vector<std::vector<double>> weights;

        std::vector<std::vector<std::vector<double>>> resArr;
        std::vector<std::vector<double>> tempArr;

        std::vector<double> features;
        std::vector<std::vector<double>> matrix;
        std::vector<std::vector<double>> biases;
        std::vector<std::vector<std::vector<double>>> input_tensor;
        std::vector<std::vector<std::vector<std::vector<double>>>> conv_filters;
        std::vector<std::vector<std::vector<std::vector<std::vector<double>>>>> conv_layers;


        std::string source = anotherSource;
        std::string line = "";
        std::string all = "";
        std::string Dense = "";
        int index = 0;
        const int sizeDense = 5;
        char dense[] = { 'D', 'e', 'n', 's', 'e' };
        char byte;
        bool addArray = false;
        bool roolListener = false;
        bool cheakD = false;
        int degree = 0, res = 0;
        std::ifstream infile(source);
        if (!infile.is_open()) {
            qDebug() << "Ошибка открытия файла!" << endl;
            return conv_layers;
        }
        while (infile.get(byte)) {  // читаем побайтно
            all += byte;
            if (dense[index] == byte) {
                if (++index == sizeDense)
                    break;
                MainWindow::dopValue::exit = 1;
                continue;
            }
            else index = MainWindow::dopValue::exit = 0;
            if (byte == ']' && MainWindow::dopValue::conv_filters == 0 && MainWindow::dopValue::features == 1) {
                features.push_back(inNumber(line));
                line = "";
                biases.push_back(features);
                features.clear();
                MainWindow::dopValue::clear();
                continue;
            }
            if (MainWindow::dopValue::conv_filters == 0 && MainWindow::dopValue::matrix == 0 && MainWindow::dopValue::features == 1) {
                if (byte == '-' || byte == '.' || isNumber(byte)) {
                    line += byte;
                    continue;
                }
                if (byte == ',' && !line.empty()) {
                    features.push_back(inNumber(line));
                    line = "";
                    continue;
                }
            }
            if (byte == '[' && MainWindow::dopValue::features == 0) {
                MainWindow::dopValue::features = 1;
            }
            else if (byte == '[' && MainWindow::dopValue::features == 1 && MainWindow::dopValue::matrix == 0) {
                MainWindow::dopValue::matrix = 1;
            }
            else if (byte == '[' && MainWindow::dopValue::matrix == 1 && MainWindow::dopValue::input_tensor == 0) {
                MainWindow::dopValue::input_tensor = 1;
            }
            else if (byte == '[' && MainWindow::dopValue::input_tensor == 1 && MainWindow::dopValue::conv_filters == 0) {
                MainWindow::dopValue::conv_filters = 1;
            }
            else if (MainWindow::dopValue::conv_filters == 1) {
                if (byte == '-' || byte == '.' || isNumber(byte)) {
                    line += byte;
                    continue;
                }
                if (byte == ',' && !line.empty()) {
                    features.push_back(inNumber(line));
                    line = "";
                    continue;
                }
                if (byte == ']' && !line.empty()) {
                    features.push_back(inNumber(line));
                    matrix.push_back(features);
                    MainWindow::dopValue::features = 0;
                    features.clear();
                    line = "";
                    continue;
                }
                if (byte == ']' && features.empty() && !matrix.empty()) {
                    input_tensor.push_back(matrix);
                    MainWindow::dopValue::matrix = 0;
                    matrix.clear();
                    continue;
                }
                if (byte == ']' && matrix.empty() && !input_tensor.empty()) {
                    conv_filters.push_back(input_tensor);
                    MainWindow::dopValue::input_tensor = 0;
                    input_tensor.clear();
                    continue;
                }
                if (byte == ']' && input_tensor.empty()) {
                    conv_layers.push_back(conv_filters);
                    MainWindow::dopValue::clear();
                    conv_filters.clear();
                    continue;
                }
            }

        }
        infile.close();
        biasesGive.push_back(biases);
        return conv_layers;
}

std::vector<std::vector<std::vector<double>>> MainWindow::ListenerDense(std::string anotherSource, std::vector<std::vector<std::vector<double>>> &biasesGive){
    std::vector<double> bias;
    std::vector<std::vector<double>> weights;
    std::vector<std::vector<double>> biases;
    std::vector<std::vector<std::vector<double>>> resArr;
    std::vector<std::vector<double>> tempArr;
    std::string source = "simpleModelFirst.txt";
    std::string line = "";
    std::string all = "";
    char byte;
    bool addArray = false;
    bool roolListener = false;
    bool cheakD = false;
    int degree = 0, res = 0;
    int index = 0;
    const int sizeDense = 5;
    char dense[] = { 'D', 'e', 'n', 's', 'e' };
    std::ifstream infile(source);
    bool enter = false;
    if (!infile.is_open()) {
        qDebug() << "Ошибка открытия файла!" << endl;
        return resArr;
    }
    while (infile.get(byte)) {  // читаем побайтно
        all += byte;
        if (dense[index] == byte && enter == false) {
            if (++index == sizeDense)
                enter = true;
            dopValue::exit = 1;
            continue;
        }
        else index = dopValue::exit = 0;
        if (enter) {
            if (byte == '[' && dopValue::accessLister == 1) {
                dopValue::closed = false;
                dopValue::weights = 1;
                continue;
            }
            if (byte == '[') {
                dopValue::accessLister = 1;
                continue;
            }
            if (dopValue::accessLister == 1 && (byte == '-' || byte == '.' || isNumber(byte))) {
                line += byte;
                continue;
            }
            if (byte != ',' && byte == ']' && dopValue::weights == false) {
                bias.push_back(inNumber(line));
                line = "";
                biases.push_back(bias);
                bias.clear();
                dopValue::accessLister = false;
                dopValue::closed = false;
            }
            if ((byte == ',' || byte == ']')) {
                if (byte == ']' && dopValue::closed == true) {
                    dopValue::accessLister = false;
                    dopValue::closed = false;
                    dopValue::weights = false;
                    resArr.push_back(weights);
                    weights.clear();
                    continue;

                }
                else if (dopValue::accessLister == 1 && byte == ']' && !line.empty()) {
                    bias.push_back(inNumber(line));
                    weights.push_back(bias);
                    line = "";
                    bias.clear();
                    dopValue::closed = true;
                    continue;
                }
                else if (dopValue::accessLister == 1 && byte == ',' && !line.empty()) {
                    bias.push_back(inNumber(line));
                    line = "";
                    continue;
                }

            }
        }
    }
    biasesGive.push_back(biases);
    return resArr;
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


