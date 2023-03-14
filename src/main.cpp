#include <iostream>
#include <QString>
#include <QTextStream>

int main() {
 QString str = "Hello World";
 QTextStream out(stdout);

 out << str;
 return 0;
}