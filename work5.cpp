#include <iostream>
using namespace std;
int main() 
{
    int age = 25;
if (age >= 18 && age < 60) {
    cout << "You are an adult." << endl;
} else if (age >= 60) {
    cout << "You are a senior citizen." << endl;
} else {
    cout << "You are a minor." << endl;
}
return 0;
}
