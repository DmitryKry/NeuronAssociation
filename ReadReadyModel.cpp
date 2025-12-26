#include <iostream>
#include <fstream>
#include <windows.h>
#include <vector>
using namespace std;
bool isNumber(char other) {
	char numbers[10] = { '0', '1',  '2',  '3',  '4',  '5',  '6',  '7',  '8', '9' };
	int i = 0;
	while (i < 10) {
		if (other == numbers[i++]) {
			return true;
		}
	}
	return false;
}
double inNumber(std::string another) {
	char numbers[10] = { '0', '1',  '2',  '3',  '4',  '5',  '6',  '7',  '8', '9' };
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
struct dopValue {
	static bool features;
	static bool matrix;
	static bool input_tensor;
	static bool conv_filters;
	static bool biases;
	static bool exit;
	static void clear() {
		dopValue::features = 0;
		dopValue::matrix = 0;
		dopValue::input_tensor = 0;
		dopValue::conv_filters = 0;
	}
};
bool dopValue::features = 0;
bool dopValue::matrix = 0;
bool dopValue::input_tensor = 0;
bool dopValue::conv_filters = 0;
bool dopValue::biases = 0;
int main()
{
	setlocale(LC_ALL, "ru");
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);
	vector<double> bias;
	vector<vector<double>> weights;

	vector<vector<vector<double>>> resArr;
	vector<vector<double>> tempArr;

	vector<double> features;
	vector<vector<double>> matrix;
	vector<vector<double>> biases;
	vector<vector<vector<double>>> input_tensor;
	vector<vector<vector<vector<double>>>> conv_filters;
	vector<vector<vector<vector<vector<double>>>>> conv_layers;


	string source = "output.txt";
	string line = "";
	string all = "";
	string Dense = "";
	int index = 0;
	const int sizeDense = 5;
	char dense[] = { 'D', 'e', 'n', 's', 'e' };
	char byte;
	bool addArray = false;
	bool roolListener = false;
	bool cheakD = false;
	int degree = 0, res = 0;
	ifstream infile(source);
	if (!infile.is_open()) {
		cout << "Ошибка открытия файла!" << endl;
		return -1;
	}
	while (infile.get(byte)) {  // читаем побайтно
		all += byte;
		if (byte == ' ') {
			features.push_back(inNumber(line));
			if (dopValue::biases != 1)
				dopValue::clear();
			line = "";
		}
		else if (byte == '\n' && dopValue::features == 0 && dopValue::biases == 0) {
			matrix.push_back(features);
			features.clear();
			dopValue::features = 1;
		}
		else if (byte == '\n' && dopValue::features == 1 && dopValue::matrix == 0) {
			input_tensor.push_back(matrix);
			matrix.clear();
			dopValue::matrix = 1;
		}
		else if (byte == '\n' && dopValue::matrix == 1 && dopValue::input_tensor == 0) {
			conv_filters.push_back(input_tensor);
			input_tensor.clear();
			dopValue::input_tensor = 1;
		}
		else if (byte == '\n' && dopValue::input_tensor == 1 && dopValue::conv_filters == 0) {
			conv_layers.push_back(conv_filters);
			conv_filters.clear();
			dopValue::conv_filters = 1;
			dopValue::biases = 1;
			dopValue::features = 0;
		}
		else if (byte == '\n' && dopValue::biases == 1 && !features.empty()) {
			biases.push_back(features);
			features.clear();
			dopValue::clear();
		}
		else if (byte == '\n' && dopValue::biases == 1 && features.empty()) {
			dopValue::biases = 0;
		}
		else if (byte == '-' || byte == '.' || isNumber(byte))
			line += byte;

	}
	infile.close();


	for (int i = 0; i < conv_layers.size(); i++) {
		for (vector<vector<vector<double>>> elemconv_filters : conv_layers[i]) {
			for (vector<vector<double>> elemInput_tensor : elemconv_filters) {
				for (vector<double> elemMatrix : elemInput_tensor) {
					for (double item : elemMatrix) {
						cout << item << ' ';
					}
					cout << endl;
				}
				cout << endl;
			}
			cout << endl;
		}
		cout << endl;

		for (double item : biases[i]) {
			cout << item << ' ';
		}
		cout << endl;

		cout << endl;
	}
}
