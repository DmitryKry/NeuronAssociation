#include <iostream>
#include <fstream>
#include <windows.h>
#include <vector>
using namespace std;
bool isNumber(char other) {
	char numbers[10] = { '0', '1',  '2',  '3',  '4',  '5',  '6',  '7',  '8', '9' };
	int i = 0;
	while (i < 10){
		if (other == numbers[i++]) {
			return true;
		}
	}
	return false;
}
double inNumber(std::string another) {
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
struct dopValue {
	static bool weights;
	static bool bias;
	static bool accessLister;
	static bool closed;
	static bool exit;
};
bool dopValue::weights = 0;
bool dopValue::bias = 0;
bool dopValue::accessLister = 0;
bool dopValue::closed = 0;
bool dopValue::exit = 0;
int main()
{
	setlocale(LC_ALL, "ru");
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);
	vector<double> bias;
	vector<vector<double>> weights;
	vector<vector<double>> biases;
	vector<vector<vector<double>>> resArr;
	vector<vector<double>> tempArr;
	string source = "simpleModelFirst.txt";
	string line = "";
	string all = "";
	char byte;
	bool addArray = false;
	bool roolListener = false;
	bool cheakD = false;
	int degree = 0, res = 0;
	int index = 0;
	const int sizeDense = 5;
	char dense[] = { 'D', 'e', 'n', 's', 'e' };
	ifstream infile(source);
	bool enter = false;
	if (!infile.is_open()) {
		cout << "Ошибка открытия файла!" << endl;
		return -1;
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
	
	for (int i = 0; i < resArr.size(); i++) {
		for (vector<double> elem : resArr[i]) {
			for (double item : elem)
				cout << item << ' ';
			cout << endl;
		}
		cout << endl;
		for (double item : biases[i])
			cout << item << ' ';
		cout << endl;
		cout << endl;
	}

	for (int i = 0; i < resArr.size(); i++) {
		for (vector<double> elem : resArr[i]) {
			for (double item : elem)
				if (item > 10 || item < -10)
					cout << item << ' ';
		}
		cout << endl;
		for (double item : biases[i])
			if (item > 10 || item < -10)
				cout << item << ' ';
	}
}
