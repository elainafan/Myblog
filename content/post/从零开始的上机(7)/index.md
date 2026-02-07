---
title: 从零开始的上机(7)
date: 2025-04-27
categories:
    - 程序设计实习
---
本次上机涉及内容：模板，STL(1)(2)。
## 字符串排序
### 描述
请按照要求对输入的字符串进行排序。

```cpp
#include <iostream>
#include <string>
#include <list>
using namespace std;

class A{
private:
	string name;
public:
	A(string n) :name(n){}
	friend bool operator < (const class A& a1, const class A &a2);
	friend bool operator == (const class A &a1, const class A &a2){
		if (a1.name.size() == a2.name.size())
			return true;
		else
			return false;
	}
	friend ostream & operator << (ostream &o, const A &a){
		o << a.name;
		return o;
	}
	string get_name() const{
		return name;
	}
	int get_size() const{
		return name.size();
	}
};
// 在此处补充你的代码
int main(int argc, char* argv[])
{
	list<A> lst;
	int ncase, n, i = 1;
	string s;
	cin >> ncase;
	while (ncase--){
		cout << "Case: "<<i++ << endl;
		cin >> n;
		for (int i = 0; i < n; i++){
			cin >> s;
			lst.push_back(A(s));
		}
		lst.sort();
		Show(lst.begin(), lst.end(), Print());

		cout << endl;
		lst.sort(MyLarge<A>());
		Show(lst.begin(), lst.end(), Print());
		cout << endl;
		lst.clear();

	}
	return 0;
}
```
### 输入
第一行是正整数 $T$ ，表示测试数据的组数，每组测试数据输入共两行。

第一行是正整数 $N$ ，表示字符串个数，第二行是 $N$ 个字符串, 字符串间用空格分离。

```
2
4
a bnss ds tsdfasg
5
aaa bbbb ccccd sa q
```
### 输出
对于每组测试数据，先输出一行：``Case: n``，如对第一组数据就输出``Case: 1``。

第二行按照字符串长度从小到大排序之后输出 $N$个字符串，字符串之间以空格间隔（不会出现字符串长度相同的情况）  

第三行按照字符串首字符ASCII码序从小到大排序之后输出 $N$ 个字符串，字符串之间以空格间隔（不会出现字符串首字母相同的情况）

```
Case: 1
a ds bnss tsdfasg
a bnss ds tsdfasg 
Case: 2
q sa aaa bbbb ccccd
aaa bbbb ccccd q sa
```
### Solution
这里我们可以看到，题目中给了我们get_name和get_size两个函数，那就把它用起来吧  
同时从友元看出，需要我们重载<这个运算符  
同时，需要写出一个MyLarge的模板类  
然后，还需要写出show和print两个函数  
最大意的地方在于之前忘记模板类的对象可以通过重载()运算符来仿函数，所以卡了一会  

```cpp
#include <iostream>
#include <list>
#include <string>

using namespace std;

class A {
private:
    string name;

public:
    A(string n) : name(n) {}
    friend bool operator<(const class A& a1, const class A& a2);
    friend bool operator==(const class A& a1, const class A& a2) {
        if (a1.name.size() == a2.name.size())
            return true;
        else
            return false;
    }
    friend ostream& operator<<(ostream& o, const A& a) {
        o << a.name;
        return o;
    }
    string get_name() const { return name; }
    int get_size() const { return name.size(); }
};
bool operator<(const class A& a1, const class A& a2) { return a1.get_size() < a2.get_size(); }
template <class T>
struct MyLarge {
    bool operator()(const T& a1, const T& a2) { return a1.get_name() < a2.get_name(); }
};
template <class T1, class T2>
void Show(T1 x, T1 y, T2 f) {
    for (auto it = x; it != y; it++) {
        f(*it);
    }
}
struct Print {
    void operator()(const A& a) const { cout << a.get_name() << ' '; }
};
// 在此处补充你的代码
int main(int argc, char* argv[]) {
    list<A> lst;
    int ncase, n, i = 1;
    string s;
    cin >> ncase;
    while (ncase--) {
        cout << "Case: " << i++ << endl;
        cin >> n;
        for (int i = 0; i < n; i++) {
            cin >> s;
            lst.push_back(A(s));
        }
        lst.sort();
        Show(lst.begin(), lst.end(), Print());

        cout << endl;
        lst.sort(MyLarge<A>());
        Show(lst.begin(), lst.end(), Print());
        cout << endl;
        lst.clear();
    }
    system("pause");
    return 0;
}
```
## 按距离排序
### 描述
根据输出完善程序。
```cpp
#include <iostream>
#include <cmath>
#include <algorithm>
#include <string>
using namespace std;
template <class T1,class T2>
struct Closer {
// 在此处补充你的代码
};

int Distance1(int n1,int n2) {
	return abs(n1-n2);
}
int Distance2(const string & s1, const string & s2)
{
	return abs((int)s1.length()- (int) s2.length());
}
int a[10] = { 0,3,1,4,7,9,20,8,10,15};
string b[6] = {"American","Jack","To","Peking","abcdefghijklmnop","123456789"};
int main()
{
	int n;string s;
	while( cin >> n >> s ) {
		sort(a,a+10,Closer<int ,int (*)(int ,int)> (n,Distance1));
		for(int i = 0;i < 10; ++i)
			cout << a[i] << "," ;
		cout << endl;
		sort(b,b+6,Closer<string,int (*)(const string &,const string &  )> (s,Distance2)); 
		for(int i = 0;i < 6; ++i)
			cout << b[i] << "," ;
		cout << endl;
	}
	return 0;
}
```
### 输入
多组数据，每组一行，是一个整数 $n$ 和一个字符串 $s$ 。

```
2 a123456
4 a12345
```
### 输出
定义两个整数的距离为两个整数差的绝对值，定义两个字符串的距离为两个字符串长度差的绝对值。

对每组数据： 

对数组 $a$ 按和 $n$ 的距离从小到大排序后输出。距离相同的，值小的排在前面。  

然后对数组 $b$ ，按照和 $s$ 的距离从小到大输出。距离相同的，字典序小的排在前面。

```
1,3,0,4,7,8,9,10,15,20,
American,Peking,123456789,Jack,To,abcdefghijklmnop,
4,3,1,7,0,8,9,10,15,20,
Peking,American,Jack,123456789,To,abcdefghijklmnop,
```
### Solution
重题，见[elainafan-从零开始的STL(1)](https://www.elainafan.one/p/%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84stl1/#%E6%8C%89%E8%B7%9D%E7%A6%BB%E6%8E%92%E5%BA%8F)。
## 回调函数
### 描述
输入 $x_1,x_2,x_3,x_4,x_5$ ，输出 $y = x_5^5 + x_4^4 + x_3^3 + x_2^2 + x_1 + 1$ 的 $y$ 的值。
```cpp
#include <algorithm>
#include <iostream>
#include <stack>
#include <queue>
#include <vector>
#include <cstring>
#include <cstdlib>
#include <string>
#include <cmath>
#include <map>
#include <set>

using namespace std;
class MyFunc
{
// 在此处补充你的代码
};
int main()
{
	int n;
	cin >> n;
	while(n--) {
		vector<MyFunc> v;
		for (int i = 0; i < 5; ++i)
			v.push_back(MyFunc(i+1));
		int ans = 1;
		for (int i = 0; i < 5; ++i)
		{
			int m;
			cin >> m;
			ans += v[i](m);
		}
		cout << ans <<endl;
	}
}
```
### 输入
多组数据。第一行是数据组数 $n$ 。

每组数据为一行，5个整数，$x_1,x_2,x_3,x_4,x_5$ 。数值不大，不必考虑溢出。

```
2
2 2 2 2 2
1 1 1 1 1
```
### 输出
对每组数据，输出一个整数 $y,y = x_5^5 + x_4^4 + x_3^3 + x_2^2 + x_1 + 1$ 。

```
63
6
```
### Solution
很明显地，这题需要使用仿函数进行计算，观察到用于转换构造函数的整型变量为 $1 \sim 5$ ，也就是幂次。

于是只需要重载``()``运算符进行幂运算即可。

```cpp
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <stack>
#include <string>
#include <vector>


using namespace std;
class MyFunc {
    int p;

public:
    MyFunc(int x) : p(x) {}
    int operator()(int x) { return pow(x, p); }
    // 在此处补充你的代码
};
int main() {
    int n;
    cin >> n;
    while (n--) {
        vector<MyFunc> v;
        for (int i = 0; i < 5; ++i) v.push_back(MyFunc(i + 1));
        int ans = 1;
        for (int i = 0; i < 5; ++i) {
            int m;
            cin >> m;
            ans += v[i](m);
        }
        cout << ans << endl;
    }
    system("pause");
    return 0;
}
```
## Printer
### 描述
完成以下程序，使得输入的整数 $x$ ，以及若干正整数，将大于 $x$ 的正整数输出。

然后输入若干字符串，将字符串长度大于 $x$ 的字符串输出。
```cpp
#include<iostream>
#include<algorithm>
#include<vector>
#include<bitset>

using namespace std;


class Printer{
// 在此处补充你的代码
int main(){

	int t;
	cin >> t;
	while(t--) {
		int n,x;
		cin>>x>>n;
		
		vector<int> intVec;
		for(int i = 0;i < n; ++i) {
			int y;
			cin >> y;
			intVec.push_back(y);
		}
		for_each(intVec.begin(), intVec.end(), Printer(x));
		cout<<endl;
		
		vector<string> strVec;
		for(int i = 0;i < n; ++i) {
			string str;
			cin >> str;
			strVec.push_back(str);
		}
		for_each(strVec.begin(), strVec.end(), Printer(x));
		cout<<endl;
	}
	return 0;
}
```
### 输入
第一行是整数 $t$ ，表示一共 $t$ 组数据，每组数据有三行。

第一行是整数 $x$ 和整数 $n$ ，第二行是 $n$ 个整数，第三行是 $n$ 个不带空格的字符串。

```
2
5 6
1 3 59 30 2 40
this is hello please me ha
1 1
4
this
```
### 输出
对每组数据，先按原序输出第一行中大于 $x$ 的正整数（数据保证会有输出）。

再按原序输出第二行中长度大于 $x$ 的字符串（数据保证会有输出）。

```
59,30,40,
please,
4,
this,
```
### Solution
首先回想``for_each``行为，``for_each(first,last,f)``可以看成以下形式：

```cpp
for (; first != last; ++first)
    f(*first);
```

因此这里仍然是要重载``()``运算符让它称为仿函数形式。

这里可以使用模板类，只重载一个``()``运算符，但是比较麻烦。所以这里选择了使用普通类，重载两次``()``运算符，较为直观。

```cpp
#include <algorithm>
#include <bitset>
#include <iostream>
#include <vector>


using namespace std;

class Printer {
private:
    int p;

public:
    Printer(int x) : p(x) {}
    void operator()(int x) {
        if (x > p) cout << x << ',';
    }
    void operator()(string x) {
        if (x.length() > p) cout << x << ',';
    }
};
// 在此处补充你的代码
int main() {
    int t;
    cin >> t;
    while (t--) {
        int n, x;
        cin >> x >> n;

        vector<int> intVec;
        for (int i = 0; i < n; ++i) {
            int y;
            cin >> y;
            intVec.push_back(y);
        }
        for_each(intVec.begin(), intVec.end(), Printer(x));
        cout << endl;

        vector<string> strVec;
        for (int i = 0; i < n; ++i) {
            string str;
            cin >> str;
            strVec.push_back(str);
        }
        for_each(strVec.begin(), strVec.end(), Printer(x));
        cout << endl;
    }
    system("pause");
    return 0;
}

```
## 矩阵排序
### 描述
创建矩阵类，要求能够输入整数类型的 $m \times n$ 矩阵，并按照元素个数，矩阵中元素之和，创建矩阵顺序对矩阵类分别排序。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

class Mat{
	int h,w;
public:
	Mat(int height,int width):h(height),w(width)
// 在此处补充你的代码
int main()
{
	vector<Mat> m;
	m.push_back(Mat(2,2));
	m.push_back(Mat(3,4));
	m.push_back(Mat(2,2));
	cin >> m[0] >> m[1] >> m[2];
	sort(m.begin(),m.end());
	cout<< m[0] << endl << m[1] << endl << m[2] <<endl;
	cout<<"*************"<<endl;
	sort(m.begin(),m.end(),comparator_1);
	cout<< m[0] << endl << m[1] << endl << m[2] <<endl;
	cout<<"*************"<<endl;
	sort(m.begin(),m.end(),comparator_2());
	cout<< m[0] << endl << m[1] << endl << m[2] <<endl;
	return 0;
}
```
### 输入
前两行是一个 $2 \times 2$矩阵，之后三行是一个 $3 \times 4$矩阵，最后两行是一个 $2 \times 2$矩阵。

```
2 3
3 4
 0 12 -3 -4
-2  2 -1  0
-1 -1 -1 -1
-1 3
-2 4
```
### 输出
先按照元素个数从小到大输出三个矩阵（大小相同时后创建的矩阵先输出）。

再按照元素之和从小到大输出三个矩阵（大小相同时后创建的矩阵先输出）。  

再按照矩阵创建顺序从先到后输出三个矩阵（矩阵排列方式与输入相同，每个元素后用一个空格进行分隔）

```
-1 3
-2 4

2 3
3 4

0 12 -3 -4
-2 2 -1 0
-1 -1 -1 -1

*************
0 12 -3 -4
-2 2 -1 0
-1 -1 -1 -1

-1 3
-2 4

2 3
3 4

*************
2 3
3 4

0 12 -3 -4
-2 2 -1 0
-1 -1 -1 -1

-1 3
-2 4
```
### Solution
其实是简单的矩阵题，观察主函数代码，发现需要实现传入长宽的转换构造函数，这个构造函数要干什么事？

首先就是要用一个指针表示二维数组，所以要向堆取空间，其次就是要记录整个矩阵大小，以及初始化矩阵和为0，还有要记录它输入的id。

至于输入id怎么来？维护一个静态成员变量就可以了。

再往下看，由于需要排序，因此需要重载``小于``运算符。

接着，由于需要输出和输入，因此需要重载输入输出运算符。
```cpp
#include <algorithm>
#include <iostream>
#include <vector>


using namespace std;

class Mat {
    int h, w;

public:
    Mat(int height, int width) : h(height), w(width) {
        p = new int[h * w];
        k++;
        id = k;
        tot = h * w;
        sum = 0;
    }
    int *p;
    int id;
    int sum;
    int tot;
    static int k;
    bool operator<(const Mat &x) {
        if (tot == x.tot) return id > x.id;
        return tot < x.tot;
    }
    friend istream &operator>>(istream &is, Mat x) {
        for (int i = 0; i <= x.h - 1; i++) {
            for (int j = 0; j <= x.w - 1; j++) {
                is >> x.p[i * x.w + j];
            }
        }
        for (int i = 0; i < x.h * x.w; i++) x.sum += x.p[i];
        return is;
    }
    friend ostream &operator<<(ostream &os, Mat x) {
        for (int i = 0; i <= x.h - 1; i++) {
            for (int j = 0; j <= x.w - 1; j++) {
                os << x.p[i * x.w + j] << ' ';
            }
            os << endl;
        }
        return os;
    }
};
int Mat::k = 0;
bool comparator_1(Mat x, Mat y) {
    for (int i = 0; i < x.tot; i++) x.sum += x.p[i];
    for (int i = 0; i < y.tot; i++) y.sum += y.p[i];
    if (x.sum == y.sum) return x.id > y.id;
    return x.sum < y.sum;
}
struct comparator_2 {
    bool operator()(Mat x, Mat y) { return x.id < y.id; }
};
// 在此处补充你的代码
int main() {
    vector<Mat> m;
    m.push_back(Mat(2, 2));
    m.push_back(Mat(3, 4));
    m.push_back(Mat(2, 2));
    cin >> m[0] >> m[1] >> m[2];
    sort(m.begin(), m.end());
    cout << m[0] << endl << m[1] << endl << m[2] << endl;
    cout << "*************" << endl;
    sort(m.begin(), m.end(), comparator_1);
    cout << m[0] << endl << m[1] << endl << m[2] << endl;
    cout << "*************" << endl;
    sort(m.begin(), m.end(), comparator_2());
    cout << m[0] << endl << m[1] << endl << m[2] << endl;
    system("pause");
    return 0;
}
```
## 数组输出
### 描述
填写代码，创建Print模板类，要求对输入的字符串数组或整数数组，用模板类进行输出并自动换行。
```cpp
#include <iostream>
#include <string>
#include <numeric>
#include <algorithm>
using namespace std;
// 在此处补充你的代码
int main(){
	string s[20];
	int num[20];
	int m,n;
	
	while(cin >> m >> n){
		for(int i=0; i<m; i++){
			cin >> s[i];
		}
		accumulate(s, s+m, Print<string>(m));
		for(int i=0; i<n; i++){
			cin >> num[i];
		}
		accumulate(num, num+n, Print<int>(n));
	}
}
```
### 输入
有多个输入样例。 
每个样例的第一行为两个整数 $m,n(m,n \leq 20)$ 。

每个样例的第二行为 $m$ 个字符串。

每个样例的第三行为 $n$ 个整数。

```
3 3
abc def hij
12 34 56
2 5
Peking University
20 18 05 1 3
```
### 输出
对每个样例输出两行。  
第一行为输入的字符串（去除空格），第二行为输入的整数（去除空格）。  

```
abcdefhij
123456
PekingUniversity
2018513
```
### Solution
这里用到了``accumulate``，回忆一下它的用法，就是``accumulate(begin,end,init)``，将从``begin``到``end``的元素都加到``init``上去。

那么，联想到之前实现过的链式加法，只需要重载加法运算符时返回``Print<T>&``型对象，也就是返回``this``指针。

而转换构造函数则传入需要加的数量``x``，完全可以通过链式调用模拟循环的形式，因为每次加完可以对成员变量``x``进行处理，以模拟每次循环。

```cpp
#include <algorithm>
#include <iostream>
#include <numeric>
#include <string>

using namespace std;
template <class T>
class Print {
    int x;

public:
    Print(int a) : x(a) {}
    Print<T>& operator+(T d) {
        x--;
        cout << d;
        if (x == 0) cout << endl;
        return *this;
    }
};
// 在此处补充你的代码
int main() {
    string s[20];
    int num[20];
    int m, n;

    while (cin >> m >> n) {
        for (int i = 0; i < m; i++) {
            cin >> s[i];
        }
        accumulate(s, s + m, Print<string>(m));
        for (int i = 0; i < n; i++) {
            cin >> num[i];
        }
        accumulate(num, num + n, Print<int>(n));
    }
    system("pause");
    return 0;
}
```
## 正向与反向输出
### 描述
输入一个的序列，首先输出原序列，每个元素之间以"---"分开。

再将序列的每个元素翻倍，并逆序输出原序列，每个元素之间以"***"分开。
```cpp
#include <cstring>
#include <cstdlib>
#include <string>
#include <iostream>
#include <vector>
#include <iterator>
using namespace std;
class C1{
// 在此处补充你的代码
};

int main()
{
    vector<int> v;
    int p;
    int size;
    int k;
    cin >> k;
    while(k--){
        cin >> size;
        v.clear();
        for(int i = 0; i < size; ++i){
            cin >> p;
            v.push_back(p);
        }
        C1 o1 = C1(size,v);
        ostream_iterator<int> it(cout,"---");
        copy(*o1, (*o1)+size, it);
        cout<<endl;
        for(int i = 0; i < size; ++i){
            o1[i]*=2;
            cout<<o1[i]<<"***";
        }
        cout<<endl;
    }    
}
```
### 输入
第一行是测试数据组数 $k$ 。  

测试数据共有 $k$ 组，每组首先输入序列长度 $n$ ，接下来 $n$ 个整数分别代表序列的 $n$ 个数。

```
1
10
1 2 3 4 5 6 7 8 9 10
```
### 输出
对于每组测试数据输出两行，分别是以"---"分割的原序列，和以"***"分割的翻倍后的逆序序列。

```
1---2---3---4---5---6---7---8---9---10---
20***18***16***14***12***10***8***6***4***2***
```
### Solution
代码要求实现``C1``类，这里需要搞懂它在干啥。

先看主函数，它接受一个``int``和``vector<int>``变量作为转换构造函数的变量，同时还需要实现一个拷贝构造函数。

然后``ostream_iterator``这一行，它是一个输出迭代器，专门输出``int``类，输出到``cout``中，每输出一个数，后面跟``---``。

接下来看到``copy``，联想之前学过的，这里是将``o1``从头开始的``size``个元素，依次复制到``cout``，每个后面跟``---``。

也就是说，需要重载``*``运算符，而它直接返回``vector<int>``的起始迭代器即可，也就是``.begin()``。

随后，还需要重载``[]``运算符，由于有修改，应该返回``int&``类型对象，注意由于输出是逆序的，因此这里也要是逆序的，前面保留的数组大小就帮了大忙。

```cpp
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <iterator>
#include <string>
#include <vector>

using namespace std;
class C1 {
private:
    int siz;
    vector<int> k;

public:
    C1(int x, vector<int> t) : siz(x), k(t) {}
    C1(C1& b) {
        siz = b.siz;
        k = b.k;
    }
    vector<int>::iterator operator*() { return k.begin(); }
    int& operator[](int x) { return k[siz - x - 1]; }
    // 在此处补充你的代码
};

int main() {
    vector<int> v;
    int p;
    int size;
    int k;
    cin >> k;
    while (k--) {
        cin >> size;
        v.clear();
        for (int i = 0; i < size; ++i) {
            cin >> p;
            v.push_back(p);
        }
        C1 o1 = C1(size, v);
        ostream_iterator<int> it(cout, "---");
        copy(*o1, (*o1) + size, it);
        cout << endl;
        for (int i = 0; i < size; ++i) {
            o1[i] *= 2;
            cout << o1[i] << "***";
        }
        cout << endl;
    }
    system("pause");
    return 0;
}
```
## 找第一个最小的
### 描述
写出 FindFirstLess 模板，用于寻找序列中小于某指定值的第一个元素。
```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;
// 在此处补充你的代码
int main()
{
	int t;
	cin >> t;
	while(t--) {
		int n ;
		string type; 
		cin >> n >> type;
		vector<int> vi;
		vector<string> vs;
		if( type == "N") {
			int a,m;
			for(int i = 0;i < n  - 1; ++i) {
				
				cin >> a;
				vi.push_back(a);
			}
			cin >> m;
			vector<int>::iterator p = FindFirstLess(vi.begin(),vi.end(),m,less<int>());
			if( p!= vi.end())
				cout << * p << endl;
			else
				cout << "Not Found" << endl; 
				
		}
		else {
			string a,m;
			for(int i = 0;i < n - 1; ++i) {
				cin >> a;
				vs.push_back(a);
			}
			cin >> m;
			vector<string>::iterator p = FindFirstLess(vs.begin(),vs.end(),m,less<string>());
			if( p!= vs.end())
				cout << * p << endl;
			else
				cout << "Not Found" << endl; 
		
		}
	}
    return 0;
}
```
### 输入
第一行是测试数据组数 $T$ ，接下来有 $2 \times T$ 行，每两行是一组测试数据。

每组数据第一行开始是一个整数，表示这组数据有 $n$ 项；接下来是一个字母，如果是'N'，表示这组数据都是整数，如果是'S'表示这组数据都是字符串。

第二行就是 $n$ 个整数，或者 $n$ 个字符串。 

```
3
4 N
28 12 7 15
4 S
Jack Tom Marry Ken
4 N
100 200 300 2
```
### 输出
对每组数据，输出第二行的前n-1项里面，第一个小于第n项的 。如果找不到，输出 "Not Found"。

```
12
Jack
Not Found
```
### Solution
这里观察到``FindFirstLess``传入了两个迭代器，一个参数，和一个判断函数。

因此需要使用模板函数，其中有三个模板类。

同时，注意到传入的两个判断函数都是``less``，因此不需要用它来判断，直接逐一比对即可，也不要想复杂去用二分啥的，这道题数据不会卡复杂度。
```cpp
##include <iostream>
#include <string>
#include <vector>
using namespace std;
template <class T1, class T2, class T3>
T1 FindFirstLess(T1 x, T1 y, T2 t, T3 f) {
    bool flag = false;
    T1 k;
    for (T1 it = x; it != y; it++) {
        if (*it < t) {
            flag = 1;
            k = it;
            break;
        }
    }
    if (flag)
        return k;
    else
        return y;
}
// 在此处补充你的代码
int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        string type;
        cin >> n >> type;
        vector<int> vi;
        vector<string> vs;
        if (type == "N") {
            int a, m;
            for (int i = 0; i < n - 1; ++i) {
                cin >> a;
                vi.push_back(a);
            }
            cin >> m;
            vector<int>::iterator p = FindFirstLess(vi.begin(), vi.end(), m, less<int>());
            if (p != vi.end())
                cout << *p << endl;
            else
                cout << "Not Found" << endl;

        } else {
            string a, m;
            for (int i = 0; i < n - 1; ++i) {
                cin >> a;
                vs.push_back(a);
            }
            cin >> m;
            vector<string>::iterator p = FindFirstLess(vs.begin(), vs.end(), m, less<string>());
            if (p != vs.end())
                cout << *p << endl;
            else
                cout << "Not Found" << endl;
        }
    }
    system("pause");
    return 0;
}
```
## 输出Fibonacci数列
### 描述
Fibonacci数列指的是数列第一项和第二项为1，之后每一项是之前两项的和所构成的数列。 现有多组数据，每组数据给出一个数字 $n$ ，请你输出Fibonacci数列的前 $n-1$项。

```cpp
#include <iostream>
#include <iterator>
using namespace std;

template<class T1, class T2>
void Copy(T1 s, T1 e, T2 x) {
    for(; s != e; ++s, ++x)
        *x = *s;
}
// 在此处补充你的代码
int main() {
	while(true) {
		int n;
		cin >> n;
		if(n == 0)
			break;
		
	    Fib f1(1), f2(n);
	    ostream_iterator<int> it(cout, " ");
	    Copy(f1, f2, it);
	    cout << endl;
	}
	return 0;
}
```
### 输入
每组数据一行，整数 $n$ ，输入以0结尾。

```
3
0
```
### 输出
对每组数据输出前 $n-1$ 项。

```
1 1
```
### Solution
在``正向和反向输出``这道题里，已经解释过了``Copy``跟``ostream_iterator``的原理了，因此这里不再解释。

然后看到``Copy``函数，这里传入了``f1``和``f2``，需要重载它的``!=``、``前自加``、``*``运算符，这是很显然的。

随后，就要考虑``for(int i=1;i<=n;i++)``怎么在``Copy``的这个循环里体现。

一个很巧妙的思路是，用一个成员变量记录当前的项数，然后不等于就重载为比较两者的项数，这个成员变量也存在于转换构造函数中。

同时，前自加就是将当前项移到斐波那契数列的下一项，并且项数加一。

最后，重载解引用就很自然地返回当前项，而因为是斐波那契数列，类中还需要存储上一项。

```cpp
#include <iostream>
#include <iterator>
using namespace std;

template <class T1, class T2>
void Copy(T1 s, T1 e, T2 x) {
    for (; s != e; ++s, ++x) *x = *s;
}
class Fib {
    int num;
    int pre;
    int tem;

public:
    Fib(int n) : num(n), pre(0), tem(1) {}
    void operator++() {
        num++;
        int cur = tem;
        cur = tem + pre;
        pre = tem;
        tem = cur;
    }
    bool operator!=(const Fib &s) { return num != s.num; }
    int operator*() { return tem; }
};
// 在此处补充你的代码
int main() {
    while (true) {
        int n;
        cin >> n;
        if (n == 0) break;

        Fib f1(1), f2(n);
        ostream_iterator<int> it(cout, " ");
        Copy(f1, f2, it);
        cout << endl;
    }
    system("pause");
    return 0;
}
```
## 改良过的CArray3d三维数组模板类
### 描述
根据输出完善程序。
```cpp
#include <iostream>
#include <iomanip>
#include <cstring>
using namespace std;
template <class T>
class CArray3D
{
// 在此处补充你的代码
};

CArray3D<int> a(3,4,5);
CArray3D<double> b(3,2,2);
void PrintA()
{
    for(int i = 0;i < 3; ++i) {
        cout << "layer " << i << ":" << endl;
        for(int j = 0; j < 4; ++j) {
            for(int k = 0; k < 5; ++k)
                cout << a[i][j][k] << "," ;
            cout << endl;
        }
    }
}
void PrintB()
{
    for(int i = 0;i < 3; ++i) {
        cout << "layer " << i << ":" << endl;
        for(int j = 0; j < 2; ++j) {
            for(int k = 0; k < 2; ++k)
                cout << b[i][j][k] << "," ;
            cout << endl;
        }
    }
}

int main()
{
    
    int No = 0;
    for( int i = 0; i < 3; ++ i )
        for( int j = 0; j < 4; ++j )
            for( int k = 0; k < 5; ++k )
                a[i][j][k] = No ++;
    PrintA();
    memset(a, -1, 60 * sizeof(int));        //注意这里
    memset(a[1][1], 0, 5 * sizeof(int));
    PrintA();
    
    for( int i = 0; i < 3; ++ i )
        for( int j = 0; j < 2; ++j )
            for( int k = 0; k < 2; ++k )
                b[i][j][k] = 10.0 / (i + j + k + 1);
    PrintB();
    int n = a[0][1][2];
    double f = b[0][1][1];
    cout << "****" << endl;
    cout << n << "," << f << endl;
    
    return 0;
}
```
### 输入
```
None
```
### 输出
```
layer 0:
0,1,2,3,4,
5,6,7,8,9,
10,11,12,13,14,
15,16,17,18,19,
layer 1:
20,21,22,23,24,
25,26,27,28,29,
30,31,32,33,34,
35,36,37,38,39,
layer 2:
40,41,42,43,44,
45,46,47,48,49,
50,51,52,53,54,
55,56,57,58,59,
layer 0:
-1,-1,-1,-1,-1,
-1,-1,-1,-1,-1,
-1,-1,-1,-1,-1,
-1,-1,-1,-1,-1,
layer 1:
-1,-1,-1,-1,-1,
0,0,0,0,0,
-1,-1,-1,-1,-1,
-1,-1,-1,-1,-1,
layer 2:
-1,-1,-1,-1,-1,
-1,-1,-1,-1,-1,
-1,-1,-1,-1,-1,
-1,-1,-1,-1,-1,
layer 0:
10,5,
5,3.33333,
layer 1:
5,3.33333,
3.33333,2.5,
layer 2:
3.33333,2.5,
2.5,2,
****
-1,3.33333
```
### Solution
唯一一个变化是，原本的``memset(a[1], -1, 60 * sizeof(int));``变为了``memset(a, -1, 60 * sizeof(int));``。

于是，使用上次的代码这里会报错，那么怎么办？

回想起``memset``传入的第一个参数通常是数组名，也就是一个指针，因此只需要实现``CArray3D``转换为``T*``类型的强制类型转换函数，即可。

关于本题其它部分的解析见[elainafan-从零开始的STL(1)](https://www.elainafan.one/p/%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84stl1/#%E5%BE%88%E9%9A%BE%E8%92%99%E6%B7%B7%E8%BF%87%E5%85%B3%E7%9A%84carray3d%E4%B8%89%E7%BB%B4%E6%95%B0%E7%BB%84%E6%A8%A1%E6%9D%BF%E7%B1%BB)。

```cpp
#include <iostream>
#include <iomanip>
#include <cstring>
using namespace std;
template <class T>
class CArray3D
{
private:
    int x,y,z;
    T* p;
public:
    CArray3D(int a,int b,int c):x(a),y(b),z(c) { 
        p=new T[x*y*z];
    }
    class CArray2D{
    private:
        int y,z;
        T* dd;
    public:
        CArray2D(T* d,int b,int c):dd(d),y(b),z(c) { }
        T* operator[](int index){
            T* t=dd+index*z;
            return t;
        }
    };
    CArray2D operator[](int index){
        T* dd=p+index*y*z;
        return CArray2D(dd,y,z);
    }
    operator T*(){
        return p;
    }
};

CArray3D<int> a(3,4,5);
CArray3D<double> b(3,2,2);
void PrintA()
{
    for(int i = 0;i < 3; ++i) {
        cout << "layer " << i << ":" << endl;
        for(int j = 0; j < 4; ++j) {
            for(int k = 0; k < 5; ++k)
                cout << a[i][j][k] << "," ;
            cout << endl;
        }
    }
}
void PrintB()
{
    for(int i = 0;i < 3; ++i) {
        cout << "layer " << i << ":" << endl;
        for(int j = 0; j < 2; ++j) {
            for(int k = 0; k < 2; ++k)
                cout << b[i][j][k] << "," ;
            cout << endl;
        }
    }
}

int main()
{
    
    int No = 0;
    for( int i = 0; i < 3; ++ i )
        for( int j = 0; j < 4; ++j )
            for( int k = 0; k < 5; ++k )
                a[i][j][k] = No ++;
    PrintA();
    memset(a, -1, 60 * sizeof(int));        //注意这里
    memset(a[1][1], 0, 5 * sizeof(int));
    PrintA();
    
    for( int i = 0; i < 3; ++ i )
        for( int j = 0; j < 2; ++j )
            for( int k = 0; k < 2; ++k )
                b[i][j][k] = 10.0 / (i + j + k + 1);
    PrintB();
    int n = a[0][1][2];
    double f = b[0][1][1];
    cout << "****" << endl;
    cout << n << "," << f << endl;
    
    return 0;
}
```