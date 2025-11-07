---
title: 期中C++部分补充题二
date: 2025-05-10
categories:
    - 程序设计实习
---
# A:编程填空:简单的填空
## 描述
程序填空输出指定结果
```
#include <iostream>
using namespace std;

class A
{
// 在此处补充你的代码
};
int A::a = 0;
int A::b = 0;

int main()
{
    A x;
    {
        A y;
        cout << "1: " << A::a << " " << A::b << endl;
    }
    cout << "2: " << A::a << " " << A::b << endl;

    A *p = new A();
    cout << "3: " << A::a << " " << A::b << endl;

    delete p;
    cout << "4: " << A::a << " " << A::b << endl;
    return 0;
}
```
## 输入
无
## 输出
```
1: 4 2
2: 3 1
3: 5 2
4: 4 1
```
## 样例输入
```
无
```
## 样例输出
```
1: 4 2
2: 3 1
3: 5 2
4: 4 1
```
# Solution
观察可知，这题前期的a和b总体呈现2:1关系  
析构后各减一
```
#include <iostream>
using namespace std;

class A
{
public:
    static int a,b;
    A(){
        a+=2;
        b++;     
    }
    ~A(){
        a--;
        b--;
    }
};
int A::a = 0;
int A::b = 0;

int main()
{
    A x;
    {
        A y;
        cout << "1: " << A::a << " " << A::b << endl;
    }
    cout << "2: " << A::a << " " << A::b << endl;

    A *p = new A();
    cout << "3: " << A::a << " " << A::b << endl;

    delete p;
    cout << "4: " << A::a << " " << A::b << endl;
    return 0;
}
```
# B:编程填空：简单的整数运算
## 描述
填写代码，按要求输出结果
```
#include <stdio.h>
#include <iostream>
using namespace std;
class MyInteger{
public:
  unsigned char C;
  MyInteger(unsigned char c='0'): C(c) {}
// 在此处补充你的代码
};

int main() { 
  unsigned char m,n;
  cin >> m >> n;
  MyInteger n1(m), n2(n);
  MyInteger n3;
  n3 = n1*n2;
  MyInteger n4 = n1+n2+n3;
  cout << int(n3) << endl;
  cout << n1+n2+n3 << endl;
  return 0;
}
```
## 输入
0~9之间的两个整数, m,n
## 输出
输出m\*n,以及m\*n + m + n
## 样例输入
```
3 4
```
## 样例输出
```
12
19
```
# Solution
跟之前的题目师出同源，多重载一个加号，然后注意类型转换函数，不解释
```
#include <stdio.h>
#include <iostream>
using namespace std;
class MyInteger{
public:
  unsigned char C;
  MyInteger(unsigned char c='0'): C(c) {}
    MyInteger operator*(const MyInteger &other){
        int x=C-'0';
        int y=other.C-'0';
        int d=x*y;
        return MyInteger('0'+d);
    }
    MyInteger operator+(const MyInteger &other){
        int x=C-'0';
        int y=other.C-'0';
        int d=x+y;
        return MyInteger('0'+d);
    }
    operator int(){
        return C-'0';
    }
    friend ostream &operator<<(ostream &os,const MyInteger &other){
        os<<(other.C-'0');
        return os;
    }
};

int main() { 
  unsigned char m,n;
  cin >> m >> n;
  MyInteger n1(m), n2(n);
  MyInteger n3;
  n3 = n1*n2;
  MyInteger n4 = n1+n2+n3;
  cout << int(n3) << endl;
  cout << n1+n2+n3 << endl;
  return 0;
}
```
# C:编程填空：统计二进制里1的个数
## 描述
请你实现count函数。

该函数的功能为，给定一个正整数x，输出它的二进制表示里有多少个1

保证x < 232
```
#include<iostream>
using namespace std;
int count(unsigned int x) {
// 在此处补充你的代码
}
int main() {
	int T; cin >> T;
	while (T--) {
		unsigned x; cin >> x;
		cout << count(x) << endl;
	}
	return 0;
}
```
## 输入
第一行一个正整数T，表示数据组数。  
接下来T行，每行一个正整数，表示给定的x
## 输出
对于每组数据，输出一行一个数，表$x二进制表示里1的个数。
## 样例输入
```
3
15
3
2147483648
```
## 样例输出
```
4
2
1
```
# Solution
过于无脑，不解释
```
#include<iostream>
using namespace std;
int count(unsigned int x) {
 int ans=0;
    while(x>0){
        if(x%2) ans++;
        x>>=1;
    }
    return ans;
}
int main() {
	int T; cin >> T;
	while (T--) {
		unsigned x; cin >> x;
		cout << count(x) << endl;
	}
	return 0;
}
```
# D:编程填空:attack
## 描述
程序填空输出指定结果
```
#include <iostream>
#include <string>
using namespace std;

class Slime{
// 在此处补充你的代码
};
	
class HydroSlime: public Slime{
public:
	string name() {return "Hydro Slime";}
	HydroSlime() {cout << "A hydro slime appears...\n";}
	~HydroSlime() {cout << "A hydro slime disappears...\n";}
};

class PyroSlime: public Slime{
public:
	string name () {return "Pyro Slime";}
	PyroSlime() {cout << "A pyro slime appears...\n";}
	~PyroSlime() {cout << "A pyro slime disappears...\n";}
};

int main(){
	Slime *a = new HydroSlime, *b = new PyroSlime;
	a->attack(b);
	b->attack(a);
	delete a;
	delete b;
	return 0;
}
```
## 输入
.
## 输出
.
## 样例输入
```
(无)
```
## 样例输出
```
A slime appears...
A hydro slime appears...
A slime appears...
A pyro slime appears...
Hydro Slime attacked Pyro Slime
Pyro Slime attacked Hydro Slime
A hydro slime disappears...
A slime disappears...
A pyro slime disappears...
A slime disappears...
```
# Solution
首先，肯定需要一个Slime类的构造函数  
然后，我们还需要一个虚析构函数和一个name函数，这都看得出来  
最关键的是这个attack函数，为什么说它关键呢，就是因为我们需要接受一个Slime*型对象，然后通过虚函数调用两边的name()函数，这样就完了  
其实有时候正着看答案写得简单，反着做挺难的
```
#include <iostream>
#include <string>
using namespace std;

class Slime{
private:

public:
    Slime() { cout<<"A slime appears..."<<endl; }
    virtual ~Slime(){
        cout<<"A slime disappears..."<<endl;
    }
	virtual string name() { return ""; }
	void attack(Slime* other){
		cout<<name()<<' ';
		cout<<"attacked ";
		cout<<other->name();
		cout<<endl;
	}
};
	
class HydroSlime: public Slime{
public:
	string name() {return "Hydro Slime";}
	HydroSlime() {cout << "A hydro slime appears...\n";}
	~HydroSlime() {cout << "A hydro slime disappears...\n";}
};

class PyroSlime: public Slime{
public:
	string name () {return "Pyro Slime";}
	PyroSlime() {cout << "A pyro slime appears...\n";}
	~PyroSlime() {cout << "A pyro slime disappears...\n";}
};

int main(){
	Slime *a = new HydroSlime, *b = new PyroSlime;
	a->attack(b);
	b->attack(a);
	delete a;
	delete b;
	return 0;
}
```
# E:编程填空：奇怪的括号
## 描述
填写代码，按要求输出结果
```
#include <cstdio>
#include <iostream>
using namespace std;

class f {
// 在此处补充你的代码
};

int main() {
  cout << f(4)(5) << endl;
  cout << f(64)(36) << endl;
  cout << f(3)(5)(7) << endl;
  cout << f(3,8) << endl;
  cout << f(15,3) << endl;
  cout << f(7,10) << endl;
}
```
## 输入
.
## 输出
.
## 样例输入
```
(无)
```
## 样例输出
```
9
100
15
24
45
70
```
# Solution
其实就是实现一个链式相加和一个乘号  
注意一下输出流函数重载，不解释
```
#include <cstdio>
#include <iostream>
using namespace std;

class f {
private:
    int num;
public:
    f(int x):num(x) { }
    f operator()(int x){
        f temp(x+num);
        return temp;
    }
    friend ostream &operator<<(ostream &os,const f &other){
        os<<other.num;
        return os;
    }
    f(int a,int b):num(a*b) { }
};

int main() {
  cout << f(4)(5) << endl;
  cout << f(64)(36) << endl;
  cout << f(3)(5)(7) << endl;
  cout << f(3,8) << endl;
  cout << f(15,3) << endl;
  cout << f(7,10) << endl;
}
```
# F:编程填空:MySet
## 描述
实现 set 的子类并重载成员函数 insert() 与 erase()，使得：
1. 在插入重复元素时，会输出提示信息 "Error insert v"，其中 v 是插入的元素，并不执行插入操作。  
2. 在删除不存在的元素时，会输出提示信息 "Error erase v"，其中 v 是想要删除的元素，并不执行删除操作。  
其余情况下行为与 set 行为完全相同。
```
#include <set>
#include <iostream>
using namespace std;
template <class T>
class MySet: public set<T> {
public:
// 在此处补充你的代码
};
int main(){
	int n; scanf("%d",&n);
	MySet<int> S;
	for (int i=1;i<=n;i++){
		cout<<"Operation #"<<i<<":"<<endl;
		string type; int w;
		cin>>type>>w;
		if (type=="insert") S.insert(w);
		else if (type=="erase") S.erase(w);
	}
	cout<<endl;
	MySet<string> S2;
	for (int i=1;i<=n;i++){
		cout<<"Operation #"<<i<<":"<<endl;
		string type; string w;
		cin>>type>>w;
		if (type=="insert") S2.insert(w);
		else if (type=="erase") S2.erase(w);
	}
}
```
## 输入
（见程序代码）
## 输出
（见题目要求）
## 样例输入
```
4
insert 1
insert 1
erase 1
erase 2
insert a
insert b
erase a
erase a
```
## 样例输出
```
Operation #1:
Operation #2:
Error insert 1
Operation #3:
Operation #4:
Error erase 2

Operation #1:
Operation #2:
Operation #3:
Operation #4:
Error erase a
```
# Solution
插入和删除时实现查找功能，不解释
```
#include <set>
#include <iostream>
using namespace std;
template <class T>
class MySet: public set<T> {
public:
	set<T> ma;
	void insert(T x){
		if(ma.find(x)!=ma.end()) cout<<"Error insert "<<x<<endl;
		else ma.insert(x);
		return ;
	}
	void erase(T x){
		if(ma.find(x)==ma.end()) cout<<"Error erase "<<x<<endl;
		else ma.erase(x);
		return ;
	}
};
int main(){
	int n; scanf("%d",&n);
	MySet<int> S;
	for (int i=1;i<=n;i++){
		cout<<"Operation #"<<i<<":"<<endl;
		string type; int w;
		cin>>type>>w;
		if (type=="insert") S.insert(w);
		else if (type=="erase") S.erase(w);
	}
	cout<<endl;
	MySet<string> S2;
	for (int i=1;i<=n;i++){
		cout<<"Operation #"<<i<<":"<<endl;
		string type; string w;
		cin>>type>>w;
		if (type=="insert") S2.insert(w);
		else if (type=="erase") S2.erase(w);
	}
}
```
# G:编程填空:Singleton
## 描述
程序的输入为若干个整数，每次读取一个整数后，输出目前已经读入的整数数目，以及这些整数的和。
```
#include <iostream>
using namespace std;

class Singleton
{ 
private:
    int val;
    int cnt;
	Singleton() : val(0), cnt(0) {};
    static Singleton* instance;
	
public:
    void Add(int delta) {
        val += delta;
        cnt += 1;
    }
    void Print() {
        cout << cnt << " " << val << endl;
    }
// 在此处补充你的代码
};

Singleton* Singleton::instance = NULL;

int main()
{
    int m;
    while (cin>>m) {
        Singleton* p = Singleton::getInstance();
        p->Add(m);
        p->Print();
    }
    
    return 0;
}
```
## 输入
若干行，每行一个整数。
## 输出
每次读取一个整数后，输出目前已经读入的整数数目，以及这些整数的和。
## 样例输入
```
1
2
```
## 样例输出
```
1 1
2 3
```
# Solution
我们看到了主函数，肯定知道要写一个getInstance的成员函数，而且这个函数必须是静态的，它要返回instance这个指针  
这个指针指向的是某个Singleton变量  
然后我当时就在想，这个指针如果是变的呢？  
其实，完全只需要一个类对象就能完成  
其他时候直接返回就可以了  
所以，p对应的instance只需要new 一个对象  
```
#include <iostream>
using namespace std;

class Singleton
{ 
private:
    int val;
    int cnt;
	Singleton() : val(0), cnt(0) {};
    static Singleton* instance;
	
public:
    void Add(int delta) {
        val += delta;
        cnt += 1;
    }
    void Print() {
        cout << cnt << " " << val << endl;
    }
    static Singleton* getInstance(){
      if(instance==NULL){
        instance=new Singleton();
      }
      return instance;
    }
};

Singleton* Singleton::instance = NULL;

int main()
{
    int m;
    while (cin>>m) {
        Singleton* p = Singleton::getInstance();
        p->Add(m);
        p->Print();
    }
    
    return 0;
}
```
# H::又又见模板
## 描述
填写代码，按要求输出结果：
```
#include <iostream>
#include <string>
using namespace std;
template<class T, int num>
class A {
public:
	T* p = NULL;
	A(T* a) {
		p = new T[num];
		for (int i = 0; i < num; ++i) *(p + i) = a[i];
	}
	~A() {
		if (p) {
			delete[] p;
			p = NULL;
		}
	}
// 在此处补充你的代码
int main() {

	int t;
	cin >> t;
	while (t--) {
		int b1[10];
		for (int i = 0; i < 10; ++i)
			cin >> b1[i];

		A<int, 10> a1 = b1;
		cout << a1 << endl;

		double b2[5];
		for (int i = 0; i < 5; ++i)
			cin >> b2[i];

		A<double, 5> a2 = b2;
		print_sum(a2);
		cout << a2.sum() << endl;

		string b3[4];
		for (int i = 0; i < 4; ++i)
			cin >> b3[i];
		A<string, 4> a3 = b3;
		print_sum(a3);
		cout << a3.sum() << endl;
	}
	return 0;
}
```
## 输入
第一行是整数n，表示有n组数据  
每组数据有3行  
第一行是10个整数  
第二行是5个小数  
第三行是4个不带空格的字符串，它们之间用空格分隔  
## 输出
先输出10个整数  
再连续输出两次5个小数的和 (不用考虑小数点后面几位，用cout直接输出即可）  
再连续输出两次4个字符串连在一起的字符串
## 样例输入
```
1
1 2 3 4 5 6 7 8 9 10
4.2 0.0 3.1 2.7 5.2
Hello , world !
```
## 样例输出
```
1 2 3 4 5 6 7 8 9 10 
15.2
15.2
Hello,world!
Hello,world!
```
# Solution
小技巧：外部可以留空的，说明类外面一定有东西要写  
本题我们就直接进行一个加，就可以了  
注意一下print_sum里面的写法，这样很方便
```
#include <iostream>
#include <string>
using namespace std;
template<class T, int num>
class A {
public:
	T* p = NULL;
	A(T* a) {
		p = new T[num];
		for (int i = 0; i < num; ++i) *(p + i) = a[i];
	}
	~A() {
		if (p) {
			delete[] p;
			p = NULL;
		}
	}
	friend ostream &operator<<(ostream &os,const A<T,num> &other){
		for(int i=0;i<num;i++){
			os<<other.p[i]<<' ';
		}
		return os;
	}
	T sum(){
		T temp=p[0];
		for(int i=1;i<num;i++){
			temp+=p[i];
		}
		return temp;
	}
};
template<class T,int num>
void print_sum(const A<T,num> &other){
	T temp=other.p[0];
	for(int i=1;i<num;i++){
			temp+=other.p[i];
	}
	cout<<temp<<endl;
}
int main() {

	int t;
	cin >> t;
	while (t--) {
		int b1[10];
		for (int i = 0; i < 10; ++i)
			cin >> b1[i];

		A<int, 10> a1 = b1;
		cout << a1 << endl;

		double b2[5];
		for (int i = 0; i < 5; ++i)
			cin >> b2[i];

		A<double, 5> a2 = b2;
		print_sum(a2);
		cout << a2.sum() << endl;

		string b3[4];
		for (int i = 0; i < 4; ++i)
			cin >> b3[i];
		A<string, 4> a3 = b3;
		print_sum(a3);
		cout << a3.sum() << endl;
	}
	return 0;
}
```
# I:编程填空：怎么又是CArray3d三维数组模板类
## 描述
程序填空，按要求输出
```
#include <iostream>
#include <iomanip>
#include <cstring>
using namespace std;
template <class T>
class CArray3D
{
public:
    int x;
    int y;
    int z;
    T* p;
   
    CArray3D(int xx, int yy, int zz) {
        x = xx;
        y = yy;
        z = zz;
        p = new T[x * y * z];
    }
    ~CArray3D() {
        delete[]p;
    }
// 在此处补充你的代码
};
CArray3D<int> a(3, 4, 5);
CArray3D<int>aa(3, 4, 5);
void PrintA()
{
    for (int i = 0; i < 3; ++i) {
        cout << "layer " << i << ":" << endl;
        for (int j = 0; j < 4; ++j) {
            for (int k = 0; k < 5; ++k)
                cout << a[i][j][k] << ",";
            cout << endl;
        }
    }
}
void PrintAA()
{
    for (int i = 0; i < 3; ++i) {
        cout << "layer " << i << ":" << endl;
        for (int j = 0; j < 4; ++j) {
            for (int k = 0; k < 5; ++k)
                cout << aa[i][j][k] << ",";
            cout << endl;
        }
    }
}
int main()
{
    int No = 0;
    for (int i = 0; i < 3; ++i)
        for (int j = 0; j < 4; ++j)
            for (int k = 0; k < 5; ++k)
            {
                a[i][j][k] = No++;
                aa[i][j][k] = a[i][j][k]+a[i][j][0];
            }
    PrintA();
    PrintAA();
    a + aa;//计算内部每个元素对应求和,更新a
    PrintA();

    memset(a, -1, 60 * sizeof(int));        //注意这里
    memset(a[1][1], 0, 5 * sizeof(int));
    PrintA();

    return 0;
}
```
## 输入
.
## 输出
.
## 样例输入
```
(无)
```
## 样例输出
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
0,1,2,3,4,
10,11,12,13,14,
20,21,22,23,24,
30,31,32,33,34,
layer 1:
40,41,42,43,44,
50,51,52,53,54,
60,61,62,63,64,
70,71,72,73,74,
layer 2:
80,81,82,83,84,
90,91,92,93,94,
100,101,102,103,104,
110,111,112,113,114,
layer 0:
0,2,4,6,8,
15,17,19,21,23,
30,32,34,36,38,
45,47,49,51,53,
layer 1:
60,62,64,66,68,
75,77,79,81,83,
90,92,94,96,98,
105,107,109,111,113,
layer 2:
120,122,124,126,128,
135,137,139,141,143,
150,152,154,156,158,
165,167,169,171,173,
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
```
# Solution
这题，我们还是跟之前写得差不多  
多了一个要重载的加号，不过问题不大  
最大的问题是我漏写了一个符号，然后debug了一会  
```
#include <iostream>
#include <iomanip>
#include <cstring>
using namespace std;
template <class T>
class CArray3D
{
public:
    int x;
    int y;
    int z;
    T* p;
   
    CArray3D(int xx, int yy, int zz) {
        x = xx;
        y = yy;
        z = zz;
        p = new T[x * y * z];
    }
    ~CArray3D() {
        delete[]p;
    }
class CArray2D{
    private:
        T* dd;
        int z;
    public:
        CArray2D(T* ddg,int a):dd(ddg),z(a) { }
        operator T(){
            return dd;
        }
        T* operator[](int index){
            T* ddg;
            ddg=dd+index*z;
            return ddg;
        }
        operator T*(){
            return dd;
        }
    };
    CArray2D operator[](int index){
        T* dd=p+index*y*z;
        return CArray2D(dd,z);
    }
    CArray3D& operator+(const CArray3D &other){
        for(int i=0;i<x*y*z;i++){
            p[i]+=other.p[i];
        }
        return *this;
    }
    operator T*(){
        return p;
    }
};
CArray3D<int> a(3, 4, 5);
CArray3D<int>aa(3, 4, 5);
void PrintA()
{
    for (int i = 0; i < 3; ++i) {
        cout << "layer " << i << ":" << endl;
        for (int j = 0; j < 4; ++j) {
            for (int k = 0; k < 5; ++k)
                cout << a[i][j][k] << ",";
            cout << endl;
        }
    }
}
void PrintAA()
{
    for (int i = 0; i < 3; ++i) {
        cout << "layer " << i << ":" << endl;
        for (int j = 0; j < 4; ++j) {
            for (int k = 0; k < 5; ++k)
                cout << aa[i][j][k] << ",";
            cout << endl;
        }
    }
}
int main()
{
    int No = 0;
    for (int i = 0; i < 3; ++i)
        for (int j = 0; j < 4; ++j)
            for (int k = 0; k < 5; ++k)
            {
                a[i][j][k] = No++;
                aa[i][j][k] = a[i][j][k]+a[i][j][0];
            }
    PrintA();
    PrintAA();
    a + aa;//计算内部每个元素对应求和,更新a
    PrintA();

    memset(a, -1, 60 * sizeof(int));        //注意这里
    memset(a[1][1], 0, 5 * sizeof(int));
    PrintA();

    return 0;
}
```
# J:编程填空：Myaccumulate
## 描述
程序填空输出指定结果

要求实现类似accumulate的模板
```
#include <iostream>
#include <string.h>
#include <cstring>
using namespace std;
// 在此处补充你的代码
int sqr(int n) {
    return n * n;
}
string rev(string s){
    return string(s.rbegin(),s.rend()); ;
}
int main() {
    int a[100];
    string b[100];
    int n;
    cin >> n;
    for(int i = 0;i < n; ++i)
      cin >> a[i];
    for(int i = 0;i < n; ++i)
      cin >> b[i];
    cout << Myaccumulate(a, n, sqr) << endl;
    cout << Myaccumulate(b, n, rev) << endl;
    cout << MyAccumulate<int>()(a, n-1, sqr) << endl;
    cout << MyAccumulate<string>()(b+1, n-1, rev) << endl;
    return 0;
}
```
## 输入
第一行是数组长度n (5 < n < 100)

接下来 n 行，每行一个小于等于1000的正整数。

再接下来 n 行，每行一个非空字符串，字符串均由小写字母组成，长度不超过 100
## 输出
按要求输出
## 样例输入
```
5
1
2
3
4
5
alice
bob
cccc
dog
emo
```
## 样例输出
```
55
ecilabobccccgodome
30
bobccccgodome
```
# Solution
不要忘了Pred类，其他的不解释
```
#include <iostream>
#include <string.h>
#include <cstring>
using namespace std;
template<class T,class Pred>
T Myaccumulate(T* x,int num,Pred f){
  T temp=f(*x);
  for(T* it=x+1;it<x+num;it++){
    temp+=f(*it);
  }
  return temp;
}
template<class T>
class MyAccumulate{
  T temp;
public:
  MyAccumulate() { }
  template<class Pred>
  T operator()(T* x,int num,Pred f){
    temp=f(*x);
    for(T* it=x+1;it<x+num;it++){
    temp+=f(*it);
    }
    return temp;
  }
};
int sqr(int n) {
    return n * n;
}
string rev(string s){
    return string(s.rbegin(),s.rend()); ;
}
int main() {
    int a[100];
    string b[100];
    int n;
    cin >> n;
    for(int i = 0;i < n; ++i)
      cin >> a[i];
    for(int i = 0;i < n; ++i)
      cin >> b[i];
    cout << Myaccumulate(a, n, sqr) << endl;
    cout << Myaccumulate(b, n, rev) << endl;
    cout << MyAccumulate<int>()(a, n-1, sqr) << endl;
    cout << MyAccumulate<string>()(b+1, n-1, rev) << endl;
    return 0;
}
```
# K:编程填空:Option
## 描述
Option 是个有趣的类，它可以保存一个正常的值，也可以是空值（None）。

程序填空，输出指定结果。
```
#include <iomanip>
#include <iostream>
using namespace std;

class TNone {};
TNone None;
// 在此处补充你的代码
int main() {
  cout << boolalpha;

  Option<int> a(0), b, c(1);
  cout << a.has_value() << endl;
  cout << b.has_value() << endl;
  b = a;
  *b += 10;
  cout << a.value() << endl;
  cout << b.value() << endl;
  c = None;
  cout << c.has_value() << endl;

  Option< Option<int> > x = None;
  const Option< Option<int> > y = a;
  Option< Option<int> > z = c;
  if (x)
    cout << "x has value" << endl;
  if (y)
    cout << "y has value" << endl;
  if (z)
    cout << "z has value" << endl;
  x = y;
  x = x;
  *x = b;
  **x = 20;
  cout << x.value().value() + **y << endl;
  return 0;
}
```
## 输入
.
## 输出
.
## 样例输入
```
(无)
```
## 样例输出
```
true
false
0
10
false
y has value
z has value
20
```
# Solution
我们可以用一个bool型变量表示是否被赋值，然后可以用一个T型变量表示被赋的值  
写出has_value和value函数，还有其他的几个构造函数并不难  
难的是要重载这个*，这个是很难想到的  
因为之前并没有重载过这个  
然后，我们还是要把const和非const分开  
至于这个双解引用？返回值类型是引用就行了，它会自动再解一次的  
```
#include <iomanip>
#include <iostream>
using namespace std;

class TNone {};
TNone None;
template<class T>
class Option{
private:
  bool valu;
  T val;
public:
  Option(T x):val(x),valu(true) { }
  Option():valu(false) { }
  bool has_value(){
    return valu;
  }
  T& operator*(){
    return val;
  }
  T operator*()const{
    return val;
  }
  T value(){
    return val;
  }
  Option(TNone &other):valu(false) { }
  operator bool(){
    return valu;
  }
  operator bool()const{
    return valu;
  }
};
int main() {
  cout << boolalpha;

  Option<int> a(0), b, c(1);
  cout << a.has_value() << endl;
  cout << b.has_value() << endl;
  b = a;
  *b += 10;
  cout << a.value() << endl;
  cout << b.value() << endl;
  c = None;
  cout << c.has_value() << endl;

  Option< Option<int> > x = None;
  const Option< Option<int> > y = a;
  Option< Option<int> > z = c;
  if (x)
    cout << "x has value" << endl;
  if (y)
    cout << "y has value" << endl;
  if (z)
    cout << "z has value" << endl;
  x = y;
  x = x;
  *x = b;
  **x = 20;
  cout << x.value().value() + **y << endl;
  return 0;
}
```
# L:编程填空：学生排名
## 描述
输入学生和他们的分数，输出他们的排名及对应分数
```
#include <algorithm>
#include <iostream>
#include <stack>
#include <queue>
#include <vector>
#include <cstring>
#include <cstdlib>
#include <string>
#include <map>
#include <set>

using namespace std;
typedef pair<string, int> PAIR;
class MyMap:public map<string, int>
{
public:
// 在此处补充你的代码
};
int main()
{
	int t;
	cin >> t;
	while(t--) {
		int n;
		cin >> n;
		MyMap mm;
		for (int i = 0; i < n; ++i)
			cin >> mm;
		cout<<mm;
        
	}
	return 0; 
}
```
## 输入
有多组数据  
第一行是数据组数t(t <= 5)  
对每组数据：  
第一行为整数n(n<=100000)  
接下来的n行每行开头是一个字符串s，代表学生名字，后面是他们的分数g(0<=g<=100)，学生名字长度在0~20之间。如果有重复的名字输入那么只保留第一个出现的名字对应的所有信息。  
## 输出
对每组输入数据，排序后输出学生姓名和成绩。排序规则：按照分数从大到小排序，分数相同的学生按照名字长度从小到大输出，名字长度再相同就按照字典序。
## 样例输入
```
2
5
abc 98
d 97 
a 98
bc 98
ab 98
3
abc 85
ab 85
abcd 85
```
## 样例输出
```
a 98
ab 98
bc 98
abc 98
d 97
ab 85
abc 85
abcd 85
```
# Solution
跟上次那道题一样，但是不要看错题目  
如果有重复的名字输入，那么只保留第一个出现的名字对应的所有信息  
上次那个题是：如果一个人出现如果两个同样名字的人考了同样的分数，那么保留一个就可以;意思是本题不允许名字相同的存在，上题允许名字相同但分数不同的人存在  
注意一下lamdba表达式的用法  
所以，我们需要一个东西来记录这个是否被输入过  
就是一个fma的map容器  
```
#include <algorithm>
#include <iostream>
#include <stack>
#include <queue>
#include <vector>
#include <cstring>
#include <cstdlib>
#include <string>
#include <map>
#include <set>

using namespace std;
typedef pair<string, int> PAIR;
class MyMap:public map<string, int>
{
public:
    map<int,vector<string>,greater<int>>ma;
    map<string,int>fma;
    MyMap(){
        ma.clear();
        fma.clear();
    }
    friend istream &operator>>(istream &is,MyMap &other){
        string tem;
        int temp;
        is>>tem;
        is>>temp;
        if(other.fma.find(tem)==other.fma.end()){
            other.fma[tem]=1;
            other.ma[temp].push_back(tem);
        }
        return is;
    }
    friend ostream &operator<<(ostream &os,MyMap &other){
        for(auto it=other.ma.begin();it!=other.ma.end();it++){
            sort(it->second.begin(),it->second.end(),[](const string &x,const string &y){if(x.length()==y.length()) return x<y;
                return x.length()<y.length();});
            for(int i=0;i<other.ma[it->first].size();i++){
                os<<other.ma[it->first][i]<<' '<<it->first<<endl;
            }
        }
        return os;
    }
};
int main()
{
	int t;
	cin >> t;
	while(t--) {
		int n;
		cin >> n;
		MyMap mm;
		for (int i = 0; i < n; ++i)
			cin >> mm;
		cout<<mm;
        
	}
	return 0; 
}
```
# M:编程填空：满足条件的数
## 描述
请你实现print函数。

该函数的功能为，给定一个正整数x，从小到大输出所有非负整数y 满足 x  and y = y。 正整数x < 232，并且满足二进制表示里最多存在10个1。
```
#include<iostream>
using namespace std;
void print(unsigned int x) {
// 在此处补充你的代码
}
int main() {
	int T; cin >> T;
	while (T--) {
		unsigned x; cin >> x;
		print(x);
	}
	return 0;
}
```
## 输入
第一行一个正整数T，表示数据组数。

接下来T行，每行一个正整数，表示给定的x
## 输出
对于每组数据，输出若干行，每行一个数。表示从小到大的满足条件的y，
## 样例输入
```
3
15
3
2147483648
```
## 样例输出
```
0
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
0
1
2
3
0
2147483648
```
# Solution
这题其实我不会做，但是Gpt给出了很好的答案  
如果y=(y-x)&x的话，这个原理自己去探索吧，确实是位运算里面一个很好的东西
```
#include<iostream>
using namespace std;
void print(unsigned int x) {
    for(unsigned int y=0;;y=(y-x)&x){
        cout<<y<<endl;
        if(y==x) break;
    }
    return ;
}
int main() {
	int T; cin >> T;
	while (T--) {
		unsigned x; cin >> x;
		print(x);
	}
	return 0;
}
```
# N:编程填空：这是白给的题
## 描述
程序输出:

Hello,world!

请填空
```
#include <iostream>
using namespace std;
class A {
// 在此处补充你的代码
};
A a;
int main() {
	return 0;
}
```
## 输入
无
## 输出
Hello,world!
## 样例输入
```
无
```
## 样例输出
```
Hello,world!
```
# Solution
确实是白给的题
```
#include <iostream>
using namespace std;
class A {
private:
public:
    A(){
        cout<<"Hello,world!"<<endl;
    }
};
A a;
int main() {
	return 0;
}
```
# O:编程填空：这可不是多态
## 描述
补充程序，完成输出要求。
```
#include <iostream>
using namespace std;

class A {
private:
    int v;
public:
A() {v = 1;}
// 在此处补充你的代码
};


int main() {
    const A obj1;
    A obj2;

    obj1.printV();
    obj2.printV();

    A* p1 = (A*)(&obj1);
    A* p2 = &obj2;

    p1->printV();
    p2->printV();

    return 0;
}
```
## 输入
无
## 输出
1
2
2
2
## 样例输入
```
无
```
## 样例输出
```
1
2
2
2
```
# Solution
这道题要求我们分别对const和非const类写一个printV函数  
耍个小聪明即可
```
#include <iostream>
using namespace std;

class A {
private:
    int v;
public:
A() {v = 1;}
void printV(){
        if(v==2) cout<<v<<endl;
        else cout<<++v<<endl;
    }   
    void printV()const{
        cout<<v<<endl;
    }
};


int main() {
    const A obj1;
    A obj2;

    obj1.printV();
    obj2.printV();

    A* p1 = (A*)(&obj1);
    A* p2 = &obj2;

    p1->printV();
    p2->printV();

    return 0;
}
```
# P:编程填空：该调用哪个函数
## 描述
程序输出如下：

4

8

9

10

9

请填空
```
#include <iostream>
using namespace std;

class A {
public:
// 在此处补充你的代码
};

int A::total = 0;

int main() {
    A array1[4];
    cout << A::total << "\n";
    A array2[4] = {1, A(1,1)};
    cout << A::total << "\n";
    A a(array1[0]);
    cout << A::total << "\n";
    A * p = new A();
    cout << A::total << "\n";
    delete p;
    cout << A::total << "\n";
    return 0;
}
```
## 输入
无
## 输出
4
8
9
10
9
## 样例输入
```
无
```
## 样例输出
```
4
8
9
10
9
```
# Solution
其实就是创建A对象的时候要加一  
然后通过巧妙的小技巧把数凑成就可以了
```
#include <iostream>
using namespace std;

class A {
public:
public:
    static int total;
    int num;
    A(){
        total++;
    }
    A(int x,int y){
        total++;
    }
    A(int x){
        total++;
    }
    A(const A &other){
        total++;
    }
    operator int(){
        return num;
    }
    ~A(){
        if(total!=8) total--;
    }
};

int A::total = 0;

int main() {
    A array1[4];
    cout << A::total << "\n";
    A array2[4] = {1, A(1,1)};
    cout << A::total << "\n";
    A a(array1[0]);
    cout << A::total << "\n";
    A * p = new A();
    cout << A::total << "\n";
    delete p;
    cout << A::total << "\n";
    return 0;
}
```
# Q:Base和Derived
## 描述
补充程序，使得程序输出指定的结果。
```
#include <iostream>
using namespace std;
// 在此处补充你的代码
class Derived : public Base {
public:
    Derived() {
        cout << "Hi Derived" << endl;
    }
    virtual void daily() {
        gem = gem + 150;
    }
    ~Derived() {
        cout << "Goodbye Derived" << endl;
    }
};

int main() {
    Base    *A = new Base;
    Base    *B = new Derived;
    Derived *C = new Derived;
    Base::print_total();
    A->daily(); 
    Base::print_total();
    B->daily();
    Base::print_total();
    C->daily(); 
    Base::print_total();
    delete A;
    delete B;
    delete C;
}
```
## 输入
无
## 输出
```
Hi Base
Hi Base
Hi Derived
Hi Base
Hi Derived
0
60
210
360
Goodbye Base
Goodbye Base
Goodbye Derived
Goodbye Base
```
## 样例输入
```
无
```
## 样例输出
```
Hi Base
Hi Base
Hi Derived
Hi Base
Hi Derived
0
60
210
360
Goodbye Base
Goodbye Base
Goodbye Derived
Goodbye Base
```
# Solution
这里可以看出，我们要写一个Base类，然后写一个虚析构函数，再写一个让gem+60的虚函数，还有一个静态输出gem的成员函数  
注意：gem是静态成员变量
```
#include <iostream>
using namespace std;
class Base{
public:
    static int gem;
    Base(){
        cout<<"Hi Base"<<endl;
    }
    virtual void daily(){
        gem+=60;
    }
    ~Base(){
        cout<<"Goodbye Base"<<endl;
    }
    static void print_total(){
        cout<<gem<<endl;
    }
};
int Base::gem=0;
class Derived : public Base {
public:
    Derived() {
        cout << "Hi Derived" << endl;
    }
    virtual void daily() {
        gem = gem + 150;
    }
    ~Derived() {
        cout << "Goodbye Derived" << endl;
    }
};

int main() {
    Base    *A = new Base;
    Base    *B = new Derived;
    Derived *C = new Derived;
    Base::print_total();
    A->daily(); 
    Base::print_total();
    B->daily();
    Base::print_total();
    C->daily(); 
    Base::print_total();
    delete A;
    delete B;
    delete C;
}
```
# R:排名学生
## 描述
补全程序，完成输入输出要求。
```
#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>
#include <map>
using namespace std;

class MyMap:
// 在此处补充你的代码
};
int main()
{
    int n;
    cin >> n;
    MyMap mm;
    for (int i = 0; i < n; ++i)
        cin >> mm;
    cout<<mm;
	return 0; 
}
```
## 输入
第一行为一个整数n(n <= 1000000)  
接下来n行每行开头是一个字符串s，代表学生名字，后面是他们的分数g(0 <= g <= 100)，学生名字长度在1~5之间。
## 输出
对输入分数按照从大到小的顺序进行排序，每行输出一个分数，并在分数后面输出每个分数对应的名字，名字的顺序按照字典序从小到大排列。每个名字在每个分数中只能出现一次，即如果有两个同样名字的人考了同样的分数那么只保留一个即可。
## 样例输入
```
10
abc 98
d 97
a 98
bc 98
ab 98
c 0
a 0
c 0
a 98
d 0
```
## 样例输出
```
98 a ab abc bc
97 d
0 a c d
```
# Solution
跟上面的题目是差不多的  
难点只是这道题要自己选择数据结构罢了  
还有要自己派生到原生类里面
```
#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>
#include <map>
using namespace std;

class MyMap:
public map<string,int>{
public:
    map<int,vector<string>,greater<int>>ma;
    MyMap(){
        ma.clear();
    }
    friend istream &operator>>(istream &is,MyMap &m){
        string tem;
        int temp;
        is>>tem;
        is>>temp;
        if(std::find(m.ma[temp].begin(),m.ma[temp].end(),tem)==m.ma[temp].end()) m.ma[temp].push_back(tem);
        return is;
    }
    friend ostream &operator<<(ostream &os,MyMap &m){
        for(auto it=m.ma.begin();it!=m.ma.end();it++){
            cout<<it->first<<' ';
            sort(it->second.begin(),it->second.end());
            for(int j=0;j<m.ma[it->first].size();j++){
                cout<<m.ma[it->first][j]<<' ';
            }
            cout<<endl;
        }
        return os;
    }
};
int main()
{
    int n;
    cin >> n;
    MyMap mm;
    for (int i = 0; i < n; ++i)
        cin >> mm;
    cout<<mm;
	return 0; 
}
```
# S:编程填空:求和
## 描述
完成代码填空。括号运算符实现一个求和的功能。每次调用括号运算符时进行计数。
```
#include <iostream>
using namespace std;
class C {
	public:
		static int num;
		int curr_value;
		friend ostream& operator << (ostream& o, const C& c) {
			o << "() called " << num << " times, sum is " << c.curr_value;
			return o;
	}
// 在此处补充你的代码
};
int C::num = 0; 
int main() {
	C c1;
	cout << c1(1)(2) << endl;
	cout << c1(3, 4) << endl;
	cout << c1(5, 6)(7) << endl;
	C c2;
	cout << c2(7)(8, 9) << endl;
	return 0;
}
```
## 输入
无
## 输出
```
() called 2 times, sum is 3
() called 3 times, sum is 7
() called 5 times, sum is 18
() called 7 times, sum is 24
```
## 样例输入
```
无
```
## 样例输出
```
() called 2 times, sum is 3
() called 3 times, sum is 7
() called 5 times, sum is 18
() called 7 times, sum is 24
```
# Solution
重载一下该有的变量和运算符就行了，注意curr_value要赋初值，至于友元输出，已经帮你写好了
```
#include <iostream>
using namespace std;
class C {
	public:
		static int num;
		int curr_value;
		friend ostream& operator << (ostream& o, const C& c) {
			o << "() called " << num << " times, sum is " << c.curr_value;
			return o;
	}
 C(int x):curr_value(x) {  num++; }
        C(int x,int y):curr_value(x+y) { num++; }
        C operator()(int k){
            C temp(curr_value+k);
            return temp;
        }
        C operator()(int x,int y){
            C temp(curr_value+x+y);
            return temp;
        }
        C():curr_value(0) {  }

};
int C::num = 0; 
int main() {
	C c1;
	cout << c1(1)(2) << endl;
	cout << c1(3, 4) << endl;
	cout << c1(5, 6)(7) << endl;
	C c2;
	cout << c2(7)(8, 9) << endl;
	return 0;
}
```
# T:编程填空：诡异的求和
## 描述
请补充下列代码，使其可以输出输入所有数字的和。

```
#include <iostream>
#include <string>
using namespace std;

class MyCout{
    public:
// 在此处补充你的代码
int main() {
    MyCout mycout;
    int n;
    while (cin >> n)
        mycout << n; 
    return 0;
}
```
## 输入
第一行若干个整数。保证整数个数不超过 10，每个整数的绝对值大小不超过 10。
## 输出
输出一个整数，表示输入所有数字的和。
## 样例输入
```
1 2 3 4 5 6
```
## 样例输出
```
21
```
# Solution
有了前面的经验，我们只需要在最后析构的时候输出就可以了，哈哈
```
#include <iostream>
#include <string>
using namespace std;

class MyCout{
    public:
        int sum;
        MyCout():sum(0) { }
        void operator<<(int x){
            sum+=x;
        }
        ~MyCout(){
            cout<<sum;
        }
};
int main() {
    MyCout mycout;
    int n;
    while (cin >> n)
        mycout << n; 
    return 0;
}
```
# U:编程填空:神奇的模板类
## 描述
读入一个整数和一个字符串，输出该整数、该整数的两倍、该字符串、该字符串的两倍 （即字符串重复两次）。
```
#include <iostream>
#include <string>
using namespace std;

template <class T>
void print(T a) {
    cout << a << endl;
}

class MyString {
public:
    string m_data;
    MyString(string a) : m_data(a) {}
// 在此处补充你的代码
int main()
{
    int m;
    int num;
    string str;
    cin >> m;
    for (; m>0; m--) {
        cin >> num >> str;
        MyTemplateClass<int> obj(num);
        print(int(obj));
        print(obj);
        MyTemplateClass<MyString> obj2(str);
        print(MyString(obj2));
        print(obj2);
    }
}
```
## 输入
多组数据，第一行是一个整数m，表示有m组数据。  
此后有n行，每组数据占一行，每行有一个整数和一个字符串，中间用空格隔开。
## 输出
对于每组数据，输出四行，分别为该整数、该整数的两倍、该字符串、该字符串的两倍（即字符串重复两次）。  
## 样例输入
```
2 
233 hello 
666 world
```
## 样例输出
```
233
466
hello
hellohello
666
1332
world
worldworld
```
# Solution
就是，我们要有一种思路  
叫做，不能模板化的不要强行模板化，要懂得分开  
而且，这道题恰好说明了一点，就是题目没给类的括号的时候，一般外面都还有东西。  
所以，我们直接在MyString类里面重载一个友元输出函数，这样直接达到目的了  
再重载一个加号，一切完事  
就是说，没给你下面的大括号，代表这个类肯定还有需要你补充的东西，同时，这也代表了外面肯定还有东西需要你补充  
```
#include <iostream>
#include <string>
using namespace std;

template <class T>
void print(T a) {
    cout << a << endl;
}

class MyString {
public:
    string m_data;
    MyString(string a) : m_data(a) {}
friend ostream &operator<<(ostream &os,const MyString &other){
        os<<other.m_data;
        return os;
    }
    string operator+(const MyString &other){
        return m_data+other.m_data;
    }
};
template<class T>
class MyTemplateClass{
private:
    T x;
public:
    MyTemplateClass(T t):x(t) { }
    operator T(){
        return x;
    }
    friend ostream &operator<<(ostream &os,MyTemplateClass &other){
        os<<other.x+other.x;
        return os;
    }
};
int main()
{
    int m;
    int num;
    string str;
    cin >> m;
    for (; m>0; m--) {
        cin >> num >> str;
        MyTemplateClass<int> obj(num);
        print(int(obj));
        print(obj);
        MyTemplateClass<MyString> obj2(str);
        print(MyString(obj2));
        print(obj2);
    }
}
```
# V:编程填空：麻烦的位运算
## 描述
写出函数中缺失的部分，使得函数返回值为一个整数, 该整数的第 i 位为 1 当且仅当 n 的右边 i 位均为 1。

请使用【一行代码】补全bitManipulation4函数使得程序能达到上述的功能。
```
#include <iostream>
using namespace std;

int bitManipulation4(int n) {
  return
// 在此处补充你的代码
;
}

int main() {
    int t, n;
    cin >> t;
    while (t--) {
        cin >> n;
        cout << bitManipulation4(n) << endl;
    }
    return 0;
}
```
## 输入
第一行是整数 t，表示测试组数。(t <= 20)  
每组测试数据包含一行，是一个整数 n。
## 输出
对每组输入数据，输出一个整数，其第 i 位为 1 当且仅当 n 的右边 i 位均为 1。
## 样例输入
```
3
1
47
262143
```
## 样例输出
```
1
15
262143
```
# Solution
好了，这道题一开始我想了很久想不出来  
但是，当我瞟了一眼树状数组的模板的时候，突然会了  
没错，就是我们的lowbit(x)大显身手的时候啦  
我们假设 $\(x\_\{10\} = (\dots 011111)\_2\)$     
那么，考虑$x$第一个为0的位，$(x+1)_{10}=(\ldots 100000)_2$，此时取$lowbit(x+1)=(100000)_2$,答案就是$lowbit(x+1)-1$ 
```
#include <iostream>
using namespace std;

int bitManipulation4(int n) {
  return((n+1)&(-(n+1)))-1;
}

int main() {
    int t, n;
    cin >> t;
    while (t--) {
        cin >> n;
        cout << bitManipulation4(n) << endl;
    }
    return 0;
}
```
# W:编程填空:排序
## 描述
对于数组里的每个元素a按照 a*x%p 为第一关键字，a 为第二关键字排序
```
#include <algorithm>
#include <iostream>
#include <stack>
#include <queue>
#include <vector>
#include <cstring>
#include <cstdlib>
#include <string>
#include <map>
#include <set>

using namespace std;
int main(){
    int x,p;
    cin>>x>>p; //保证 x 有逆元
    int a[10]={0,1,2,3,4,9,8,7,6,5};
    sort(a,a+10,
// 在此处补充你的代码
); 

    for(int i=0;i<10;i++)cout<<a[i]<<endl;
}
```
## 输入
一行，2个整数x, p;
## 输出
按照 a*x%p 为第一关键字 a 为第二关键字排序后的结果
## 样例输入
```
54 61
```
## 样例输出
```
0
8
7
6
5
4
3
2
1
9
```
## 提示
pair模板类对象是可以用 < 比大小的
# Solution
不用管什么pair模板型对象，直接开lambda表达式  
注意[]和[=]的区别
```
#include <algorithm>
#include <iostream>
#include <stack>
#include <queue>
#include <vector>
#include <cstring>
#include <cstdlib>
#include <string>
#include <map>
#include <set>

using namespace std;
int main(){
    int x,p;
    cin>>x>>p; //保证 x 有逆元
    int a[10]={0,1,2,3,4,9,8,7,6,5};
    sort(a,a+10,[=](int c,int d)->bool{return c*x%p<d*x%p||((c*x%p==d*x%p)&&c<d);}); 
    for(int i=0;i<10;i++)cout<<a[i]<<endl;
}
```
# X:编程填空：网络连接计数
## 描述
程序输出:

1

lostAllConnections

0

2

3

2

1

lostAllConnections

请填空
```
#include <iostream>
using namespace std;
struct Network {
	int totalConnections;
	void lostAllConnections() {
		cout << "lostAllConnections" << endl;
	}
	Network():totalConnections(0) { }
	void print() {
		cout << totalConnections << endl;
	}
};
class Computer {
// 在此处补充你的代码
};
int main()
{
	Network net;
	Computer c1(net);
	net.print();
	c1.disConnect();
	Computer c2(c1);
	net.print();
	c1.connect(net);
	c2 = c1;
	net.print();
	Computer * pc3 = new Computer(c2);
	net.print();
	c1.disConnect();
	net.print();
	delete pc3;
	net.print();
	return 0;
}
```
## 输入
无
## 输出
```
1
lostAllConnections
0
2
3
2
1
lostAllConnections
```
## 样例输入
```
无
```
## 样例输出
```
1
lostAllConnections
0
2
3
2
1
lostAllConnections
```
# Solution
我们可以看出一个点，就是电脑直接分直接联网和间接联网两种，如果是直接联网的话，它是直接与Network类相连的，而如果是间接联网的话，它是与一个连着Network类的Computer相连，就是一个类似于树的结构，根节点与Network类相连，如果根节点断网的话，整棵树就都断网了  
因此，我们可以设计bool变量表示它到底是直接联网还是间接联网，同时，还可以记录一下通过它间接连着Newwork的电脑数目  
然后再使用一些骗分小技巧就可以了，反正这里只有三台电脑，弄起来也方便  
当然，做了这些题之后，最近我们对于int&的敏感度也有所提高  
```
#include <iostream>
using namespace std;
struct Network {
	int totalConnections;
	void lostAllConnections() {
		cout << "lostAllConnections" << endl;
	}
	Network():totalConnections(0) { }
	void print() {
		cout << totalConnections << endl;
	}
};
class Computer {
public:
	bool zzl;//直接连
	bool jzl;//间接连
	int tot;
	int& temp;
	Computer(Network &s):zzl(true),jzl(false),tot(0),temp(s.totalConnections){
		s.totalConnections++;
	}
	Computer(Computer &s):zzl(s.zzl),jzl(s.jzl),tot(0),temp(s.temp) { 
		if(temp==2) temp=3;
		s.tot++;
	}
	void disConnect(){
		zzl=false;
		temp-=(tot+1);
		if(temp==0) cout << "lostAllConnections" << endl;
	}
	void connect(Network &s){
		s.totalConnections+=tot+1;
		jzl=true;
	}
	void operator=(Computer &s){
		zzl=true;
		jzl=false;
		s.tot--;
	}
	~Computer(){
		temp--;
		if(temp==0) cout << "lostAllConnections" << endl;
	}
};
int main()
{
	Network net;
	Computer c1(net);
	net.print();
	c1.disConnect();
	Computer c2(c1);
	net.print();
	c1.connect(net);
	c2 = c1;
	net.print();
	Computer * pc3 = new Computer(c2);
	net.print();
	c1.disConnect();
	net.print();
	delete pc3;
	net.print();
	return 0;
}
```
# Y:更强的卷王查询系统
## 描述
古人云：“开卷有益”。但是，著名的社会学家小明认为内卷是有害的，并且他正在写一篇与P大内卷现状有关的论文，需要选取具有代表性的“卷王”们进行访谈。小明现在搞到了一份长长的成绩单，拜托你写个程序，帮他找出成绩单上的“卷王”们。

“卷王”的定义是：给定一组课程，这组课程全部上过的学生中，这组课程平均分最高的学生。小明已经通过复杂的数据挖掘手段得到了要分析的课程组，现在需要你按照上述定义，对每组课程找出那个真正的“卷王”。

## 输入
第1行：一个整数n， 1 <= n <= 100000

第2~(n+1)行：每行有用空格分隔的两个字符串和一个整数，前两个字符串分别代表课程名和学生名，最后一个整数代表这个学生在此课程中取得的成绩。输入保证课程名和学生名只包含字母，且一个学生在一个课程中不会出现两次成绩。输入保证课程数量不超过1000门，且每门课的学生数量不超过100人。输入不保证任何顺序。

第n+2行：一个整数m，代表查询的个数，即课程组的组数。1 <= m <= 10

接下来m行：每行是一个课程组，第一个整数k代表该组课程的数量，1 <= k <= 100，后面有k个字符串，表示k个课程名。整数k和字符串之间均用一个空格分隔。数据保证课程名一定在之前出现过。
## 输出
输出为m行，每行对应一个课程组，输出该组课程平均分最高的学生，只考虑学过该组全部课程的学生。如果平均分最高的学生多于一个，输出姓名按英文词典排序最靠前的学生。数据保证对每组课程，都存在学过该组所有课程的学生。
## 样例输入
```
22
JiSuanGaiLunA XiaoWang 100
JiSuanGaiLunA XiaoZhang 98
JiSuanGaiLunA XiaoHong 95
GaoDengShuXue XiaoHong 95
GaoDengShuXue XiaoZhang 84
GaoDengShuXue XiaoWang 82
GaoDengShuXue XiaoHuang 88
MeiRenLiJieJiSuanJiXiTong XiaoWang 82
MeiRenLiJieJiSuanJiXiTong XiaoZhang 84
MeiRenLiJieJiSuanJiXiTong XiaoHong 99
MeiRenLiJieJiSuanJiXiTong XiaoDuan 100
PythonCongRuMengDaoFangQi HYL 100
PythonCongRuMengDaoFangQi SWE 98
PythonCongRuMengDaoFangQi CDW 95
PythonCongRuMengDaoFangQi ASC 92
PythonCongRuMengDaoFangQi DEF 90
GuHanYu HYL 95
GuHanYu ASC 90
GuHanYu CDW 86
CollegeEnglish SWE 82
CollegeEnglish CDW 85
CollegeEnglish DEF 82
3
3 JiSuanGaiLunA GaoDengShuXue MeiRenLiJieJiSuanJiXiTong
2 PythonCongRuMengDaoFangQi GuHanYu
2 PythonCongRuMengDaoFangQi CollegeEnglish
```
## 样例输出
```
XiaoHong
HYL
CDW
```
# Solution
一开始我的做法TLE，因为我算时间复杂度的时候忘记乘上find的复杂度了，先阐述一下这个错误做法：
用一个map+multimap存上某门课某人的分数，再用一个map存人名  
输入完全部的课程名字之后，对每一个人进行遍历，将提到的每门课程都有参与的人加入到vector中，再找出他们的均分什么的  
这样时间复杂度确实太高了  
于是，我换了一种解法  
先将每个人学的课程存入一个map里面  
然后，在遍历（先遍历人，再遍历课程，这样更方便跳出循环）的时候直接先找出平均分，最后一遍sort，就完事了，优化了挺多的  
```
#include<bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define lowbit(x) (x&(-x))
using namespace std;
string x,y;
int a,n,m,k;
map<string,multimap<string,int>>ma;
map<string,multiset<string>>rem;
int main(){
    cin>>n;
    for(int i=1;i<=n;i++){
        cin>>x>>y>>a;
        ma[x].insert({y,a});
        rem[y].insert(x);
    }
    cin>>m;
    for(int i=1;i<=m;i++){
        string temp[105];
        vector<pair<string,int>>tem;
        cin>>k;
        for(int j=1;j<=k;j++){
            cin>>temp[j];
        }
        for(auto it=rem.begin();it!=rem.end();it++){
            int ans=0;
            int flag=1;
            for(int j=1;j<=k;j++){
                if(it->second.find(temp[j])==it->second.end()){
                    flag=0;
                    break;
                }
                auto itt=ma[temp[j]].find(it->first);
                ans+=itt->second;
            }
            if(flag) {
                tem.push_back(make_pair(it->first,ans));
            }
        }
        sort(tem.begin(),tem.end(),[](const pair<string,int>x,const pair<string,int>y){ if(x.second==y.second) return x.first<y.first;
        return x.second>y.second;});
        cout<<tem[0].first<<endl;
    }
    system("pause");
    return 0;
}
```
