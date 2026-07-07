---
title: 从零开始的输入输出和模板
date: 2025-04-16
categories:
    - 算法
slug: 从零开始的输入输出和模板
hidden: true
seriesOrder: 14
---
## 简单的SumArray
### 描述
根据输出完善程序，不得编写SumArray函数。
```cpp
#include <iostream>
#include <string>
using namespace std;
template <class T>
T SumArray(
// 在此处补充你的代码
}
int main() {
	string array[4] = { "Tom","Jack","Mary","John"};
	cout << SumArray(array,array+4) << endl;
	int a[4] = { 1, 2, 3, 4};  //提示：1+2+3+4 = 10
	cout << SumArray(a,a+4) << endl;
	return 0;
}
```
### 输入
```
None
```
### 输出
```
TomJackMaryJohn
10
```
### Solution
首先，这题需要实现一个模板函数，这个函数因为传入了``array,array+4``这样的类型（在ICS中会学到这是两个指针），因此它获取的是两个``T*``参数。

然后，通过指针类型进行遍历，即``for(T* i=a+1;i<b;i++)``，一步步通过解引用累加即可。

```cpp
#include <iostream>
#include <string>
using namespace std;
template <class T>
T SumArray(T *a, T *b) {
    T c = *a;
    for (T *i = a + 1; i < b; i++) {
        c += *i;
    }
    return c;
    // 在此处补充你的代码
}
int main() {
    string array[4] = {"Tom", "Jack", "Mary", "John"};
    cout << SumArray(array, array + 4) << endl;
    int a[4] = {1, 2, 3, 4};  // 提示：1+2+3+4 = 10
    cout << SumArray(a, a + 4) << endl;
    return 0;
}
```
## 简单的foreach
### 描述
根据输出完善程序，不得编写MyForeach函数。
```cpp
#include <iostream>
#include <string>
using namespace std;
// 在此处补充你的代码
void Print(string s)
{
	cout << s;
}
void Inc(int & n)
{
	++ n;
}
string array[100];
int a[100];
int main() {
	int m,n;
	while(cin >> m >> n) {
		for(int i = 0;i < m; ++i)
			cin >> array[i];
		for(int j = 0; j < n; ++j)
			cin >> a[j];
		MyForeach(array,array+m,Print);		 
		cout << endl;
		MyForeach(a,a+n,Inc);		 
		for(int i = 0;i < n; ++i)
			cout << a[i] << ",";
		cout << endl;
	}
	return 0;
}
```
### 输入
多组数据，每组数据第一行是两个整数 $m$ 和 $n$ ,都不超过 $50$ 。

第二行是 $m$ 个不带空格的字符串，第三行是 $n$ 个整数。

```
3 4
Tom Mike Jack
1 2 3 4
1 2
Peking
100 200
```
### 输出
对每组数据，第一行输出所有输入字符串连在一起的结果，第二行输出输入中的每个整数加1的结果。

```
TomMikeJack
2,3,4,5,
Peking
101,201,
```
### Solution
这里发现需要实现一个``MyForeach``函数，传入一个``T*``指针表示开头，一个``T*``指针表示结尾，还传入一个函数。

这里需要多写一个模板类，用于表示这个函数，又由于可以读取到传入函数都是void类型，因此可以写成这种形式``void f(T2 t)``。

接下来跟上题一样，遍历指针对应的地址空间，并对每个元素进行``f``操作即可。

```cpp
#include <iostream>
#include <string>
using namespace std;
template <class T1, class T2>
void MyForeach(T1 *a, T1 *b, void f(T2 t)) {
    for (T1 *i = a; i < b; i++) {
        f(*i);
    }
}
// 在此处补充你的代码
void Print(string s) { cout << s; }
void Inc(int &n) { ++n; }
string array[100];
int a[100];
int main() {
    int m, n;
    while (cin >> m >> n) {
        for (int i = 0; i < m; ++i) cin >> array[i];
        for (int j = 0; j < n; ++j) cin >> a[j];
        MyForeach(array, array + m, Print);
        cout << endl;
        MyForeach(a, a + n, Inc);
        for (int i = 0; i < n; ++i) cout << a[i] << ",";
        cout << endl;
    }
    return 0;
}
```
## 简单的Filter
### 描述
根据输出完善程序，不得编写Filter函数。
```cpp
#include <iostream>
#include <string>
using namespace std;
// 在此处补充你的代码
bool LargerThan2(int n)
{
	return n > 2;
}
bool LongerThan3(string s) 
{
	return s.length() > 3;
}

string as1[5] = {"Tom","Mike","Jack","Ted","Lucy"};
string as2[5];
int  a1[5] = { 1,2,3,4,5};
int a2[5];
int main() {
	string * p = Filter(as1,as1+5,as2,LongerThan3);
	for(int i = 0;i < p - as2; ++i)
		cout << as2[i];
	cout << endl; 
	int * p2 = Filter(a1,a1+5,a2,LargerThan2);
	for(int i = 0;i < p2-a2; ++i)
		cout << a2[i] << ",";
	return 0;
}
```
### 输入
```
None
```
### 输出
```
MikeJackLucy
3,4,5,
```
### Solution
跟上题的思路挺像的，无非是传入的函数由``void``类型变为了``bool``类型，这里就不多讲了。

还有，``filter``函数的逻辑是，如果满足给定条件，就将当前变量传到给定的``dst``中，否则什么都不做。

```cpp
#include <iostream>
#include <string>
using namespace std;
template<class T1,class T2>
T1* Filter(T1 *a,T1 *b,T1 *c,bool f(T2 t)){
	for(T1 *i=a;i<b;i++){
		if(f(*i)){
			*c=*i;
			c++;
		} 
	}
	return c;
}
bool LargerThan2(int n)
{
	return n > 2;
}
bool LongerThan3(string s) 
{
	return s.length() > 3;
}

string as1[5] = {"Tom","Mike","Jack","Ted","Lucy"};
string as2[5];
int  a1[5] = { 1,2,3,4,5};
int a2[5];
int main() {
	string * p = Filter(as1,as1+5,as2,LongerThan3);
	for(int i = 0;i < p - as2; ++i)
		cout << as2[i];
	cout << endl; 
	int * p2 = Filter(a1,a1+5,a2,LargerThan2);
	for(int i = 0;i < p2-a2; ++i)
		cout << a2[i] << ",";
	return 0;
}
```
## 你真的搞清楚为啥 while(cin >> n) 能成立了吗？
### 描述
读入两个整数，输出两个整数，直到碰到-1。
```cpp
#include <iostream>
using namespace std;
class MyCin
{
// 在此处补充你的代码
};
int main()
{
    MyCin m;
    int n1,n2;
    while( m >> n1 >> n2) 
        cout  << n1 << " " << n2 << endl;
    return 0;
}
```
### 输入
多组数据，每组一行，是两个整数。

```
12 44
344 555
-1
2 3
```
### 输出
对每组数据，原样输出，当碰到输入中出现-1时，程序结束，输入中保证会有-1。

```
12 44
344 555
```
### Solution
首先，查询``while(cin>>n)``的原理，如下：

```cpp
while (true) {
    cin >> n;
    if (cin 处于失败状态) break;
    // 使用 n
}
```

从老师的讲义中，也知道它是由一个``istream``类函数和一个``bool``类函数组成的。

同时，``istream``函数应该返回它自己，以更好地实现下一次调用，它还应该被当成条件，判断能不能继续输入。

这就说明，需要有一个``bool``型变量，它初始化为``true``，当输入为``-1``时变为``false``。

同时，需要重载输入运算符，用于判断条件，里面可以使用``cin``，并且返回类型为``MyCin&``，即``this指针``。

最后，需要实现``Mycin``到``bool``的强制转换函数，因为``while``在执行完``m>>n1>>n2``后需要判断其真假。

```cpp
#include <iostream>
using namespace std;
class MyCin {
private:
    bool flag;

public:
    MyCin() : flag(true) {}
    MyCin &operator>>(int &n) {
        if (!flag) return *this;
        cin >> n;
        if (n == -1) flag = false;
        return *this;
    }
    operator bool() { return flag; }
    // 在此处补充你的代码
};
int main() {
    MyCin m;
    int n1, n2;
    while (m >> n1 >> n2) cout << n1 << " " << n2 << endl;
    return 0;
}
```
## 山寨版istream_iterator
### 描述
模仿C++标准模板库istream_iterator用法，实现CMyistream_iterator使得程序按要求输出。

```cpp
#include <iostream>
#include <string>

using namespace std;
template <class T>
class CMyistream_iterator
{
// 在此处补充你的代码
};



int main()  
{ 
	int t;
	cin >> t;
	while( t -- ) {
		 CMyistream_iterator<int> inputInt(cin);
		 int n1,n2,n3;
		 n1 = * inputInt; //读入 n1
		 int tmp = * inputInt;
		 cout << tmp << endl;
		 inputInt ++;   
		 n2 = * inputInt; //读入 n2
		 inputInt ++;
		 n3 = * inputInt; //读入 n3
		 cout << n1 << " " << n2<< " " << n3 << " ";
		 CMyistream_iterator<string> inputStr(cin);
		 string s1,s2;
		 s1 = * inputStr;
		 inputStr ++;
		 s2 = * inputStr;
		 cout << s1 << " " << s2 << endl;
	}
	 return 0;  
}
```
### 输入
第一行是整数 $t$ ，表示有 $t$ 组数据。

每组数据一行，三个整数加两个字符串。字符串是不含空格的。

```
2
79 90 20 hello me
12 34 19 take up
```
### 输出
对每组数据，输出二行，在第一行输出第一个数，第二行原样输出输入的内容。

```
79
79 90 20 hello me
12
12 34 19 take up
```
### 提示
C++标准模板库 istream_iterator模版使用说明：

其构造函数执行过程中就会要求输入，然后每次执行++，则读取输入流中的下一个项目，执行 * 则返回上次从输入流中读取的项目。例如，下面程序运行时，就会等待用户输入数据，输入数据后程序才会结束：

```cpp
#include
#include
using namespace std;
int main() {
istream_iterator inputInt(cin);
return 0;
}
```
下面程序运行时，如果输入 $12 34$ ，程序输出结果是 $12,12$ 。
```cpp
#include
#include
using namespace std;
int main()
{
istream_iterator inputInt(cin);
cout << * inputInt << "," << * inputInt << endl;
return 0;
}
```
下面程序运行时，如果输入 $12 34 56$ 程序输出结果是 $12,56$ 。
```cpp
#include
#include
using namespace std;
int main()
{
istream_iterator inputInt(cin);
cout << * inputInt << "," ;
inputInt ++;
inputInt ++;
cout << * inputInt;
return 0;
}
```
### Solution
很容易发现，需要实现一个转换构造函数，传入的变量是``cin``，也就是``istream&``型变量，因此需要一个``istream&``型成员变量。

接着，注意到提示中写的，需要重载``后自加``和``*``两个运算符，而需要上一次读取的变量，就需要使用一个成员变量存储上一次输入的变量，以便输出。

```cpp
#include <iostream>
#include <string>

using namespace std;
template <class T>
class CMyistream_iterator {
private:
    istream& ist;
    T n;

public:
    CMyistream_iterator() {}
    CMyistream_iterator(istream& ist) : ist(ist) { ist >> n; }
    T operator*() { return n; }
    void operator++(int) { ist >> n; }
    // 在此处补充你的代码
};

int main() {
    int t;
    cin >> t;
    while (t--) {
        CMyistream_iterator<int> inputInt(cin);
        int n1, n2, n3;
        n1 = *inputInt;  // 读入 n1
        int tmp = *inputInt;
        cout << tmp << endl;
        inputInt++;
        n2 = *inputInt;  // 读入 n2
        inputInt++;
        n3 = *inputInt;  // 读入 n3
        cout << n1 << " " << n2 << " " << n3 << " ";
        CMyistream_iterator<string> inputStr(cin);
        string s1, s2;
        s1 = *inputStr;
        inputStr++;
        s2 = *inputStr;
        cout << s1 << " " << s2 << endl;
    }
    return 0;
}
```
## 这个模板并不难
### 描述
根据输出完善程序。
```cpp
#include <iostream>
#include <string>
#include <cstring>
using namespace std;
template <class T>  
class myclass {
// 在此处补充你的代码
~myclass( ) {
		delete [] p;
	}
	void Show()
	{
		for( int i = 0;i < size;i ++ ) {
			cout << p[i] << ",";
		}
		cout << endl;
	}
};
int a[100];
int main() {
	char line[100];
	while( cin >> line ) {
		myclass<char> obj(line,strlen(line));;
		obj.Show();
		int n;
		cin >> n;
		for(int i = 0;i < n; ++i)
			cin >> a[i];
		myclass<int> obj2(a,n);
		obj2.Show();
	}
	return 0;
}
```
### 输入
多组数据，每组第一行是一个不含空格的字符串。 
 
第二行是整数 $n$ ，第三行是 $n$ 个整数。  

```
Tom 
3
3 4 5
Jack
4
1 2 3 4
```
### 输出
对每组数据，先依次输出输入字符串的每个字母，并且在每个字母后面加逗号。

然后依次再输出输入的 $n$ 个整数 ，在每个整数后面加逗号。

```
T,o,m,
3,4,5,
J,a,c,k,
1,2,3,4,
```
### Solution
首先观察到，``myclass``类传入一个``T*``和一个``int``类对象，用于转换构造函数。

同时可以知道，后者代表前者的长度，因此应该在转换构造函数内就为类中指针取这么多的堆空间，并用原指针中的数据初始化。

接着还需要实现``Show``函数，即打印类内指针对应的内容。

最后，实现析构函数，释放类内指针申请的堆内存即可。
```cpp
#include <cstring>
#include <iostream>
#include <string>

using namespace std;
template <class T>
class myclass {
    int size;
    T* p;

public:
    myclass(T* k, int b) : size(b) {
        p = new T[size];
        for (int i = 0; i < size; i++) {
            p[i] = k[i];
        }
    }
    // 在此处补充你的代码
    ~myclass() { delete[] p; }
    void Show() {
        for (int i = 0; i < size; i++) {
            cout << p[i] << ",";
        }
        cout << endl;
    }
};
int a[100];
int main() {
    char line[100];
    while (cin >> line) {
        myclass<char> obj(line, strlen(line));
        ;
        obj.Show();
        int n;
        cin >> n;
        for (int i = 0; i < n; ++i) cin >> a[i];
        myclass<int> obj2(a, n);
        obj2.Show();
    }
    system("pause");
    return 0;
}
```
## 排序，又见排序!
### 描述
自己编写一个能对任何类型的数组进行排序的mysort函数模版。只能写一个mysort模板，不能写mysort函数！
```cpp
#include <iostream>
using namespace std;

bool Greater2(int n1,int n2) 
{
	return n1 > n2;
}
bool Greater1(int n1,int n2) 
{
	return n1 < n2;
}
bool Greater3(double d1,double d2)
{
	return d1 < d2;
}

template <class T1,class T2>
void mysort(
// 在此处补充你的代码
#define NUM 5
int main()
{
    int an[NUM] = { 8,123,11,10,4 };
    mysort(an,an+NUM,Greater1); //从小到大排序 
    for( int i = 0;i < NUM; i ++ )
       cout << an[i] << ",";
    mysort(an,an+NUM,Greater2); //从大到小排序 
    cout << endl;
    for( int i = 0;i < NUM; i ++ )
        cout << an[i] << ","; 
    cout << endl;
    double d[6] = { 1.4,1.8,3.2,1.2,3.1,2.1};
    mysort(d+1,d+5,Greater3); //将数组从下标1到下标4从小到大排序 
    for( int i = 0;i < 6; i ++ )
         cout << d[i] << ","; 
	return 0;
}
```
### 输入
```
None
```
### 输出
```
4,8,10,11,123,
123,11,10,8,4,
1.4,1.2,1.8,3.1,3.2,2.1,
```
### Solution
看到这道题，第一反应肯定是计概中最先碰到的冒泡排序，码量小，实现难度小。

再观察，``mysort``中仍然传入一个``T*``起始指针和一个``T*``终止指针，并传入一个``bool``比较函数（用``bool f(T2 c,T2 d)``表示），于是直接模拟冒泡即可。

```cpp
#include <iostream>
using namespace std;

bool Greater2(int n1, int n2) { return n1 > n2; }
bool Greater1(int n1, int n2) { return n1 < n2; }
bool Greater3(double d1, double d2) { return d1 < d2; }

template <class T1, class T2>
void mysort(T1 *a, T1 *b, bool f(T2 c, T2 d)) {
    for (T1 *i = a; i < b; i++) {
        for (T1 *j = i + 1; j < b; j++) {
            if (!f(*i, *j)) {
                swap(*i, *j);
            }
        }
    }
}
// 在此处补充你的代码
#define NUM 5
int main() {
    int an[NUM] = {8, 123, 11, 10, 4};
    mysort(an, an + NUM, Greater1);  // 从小到大排序
    for (int i = 0; i < NUM; i++) cout << an[i] << ",";
    mysort(an, an + NUM, Greater2);  // 从大到小排序
    cout << endl;
    for (int i = 0; i < NUM; i++) cout << an[i] << ",";
    cout << endl;
    double d[6] = {1.4, 1.8, 3.2, 1.2, 3.1, 2.1};
    mysort(d + 1, d + 5, Greater3);  // 将数组从下标1到下标4从小到大排序
    for (int i = 0; i < 6; i++) cout << d[i] << ",";
    system("pause");
    return 0;
}
```