#include <iostream>
#include <fstream>
#include <windows.h>
#include <vector>
using namespace std;
double inNumver(std::string another) {
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

int main() {
	setlocale(LC_ALL, "ru");
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);
	vector<vector<double>> examples;
	string source = "simpleModelFirst.txt";
	string line = "";
	string all = "";
	char byte;
	bool addArray = false;
	bool roolListener = false;
	bool cheakD = false;
	int degree = 0, res = 0;
	ifstream infile(source);  // Создание объекта для чтения
	if (!infile.is_open()) {
		cout << "Ошибка открытия файла!" << endl;
		return -1;
	}
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
			examples.push_back(vector<double>());
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
	vector<vector<vector<double>>> resArr;
	vector<vector<double>> tempArr;
	for (vector<double> elements : examples) {
		if (elements.size() != 0) 
			tempArr.push_back(elements);
		for (double element : elements) {
			cout << element << '\t';
		}
		cout << endl;
		if (elements.size() == 0) {
			resArr.push_back(tempArr);
			tempArr.clear();
		}
	}
	resArr.push_back(tempArr);
	cout << "Кол-во матриц - " << resArr.size() << endl;
	/*for (vector<vector<double>> elem : resArr) {
		cout << "Кол-во входов - " << elem.size() << endl;
		for (vector<double> item : elem) {
			for (int i = 0; i < item.size(); i++) {
				cout << item[i] << ' ';
			}
			cout << endl;
		}
	}*/
	return 0;
}

