---
title: STL作业一
date: 2025-04-18
categories:
    - 程序设计实习
---
# A:goodcopy
## 描述
编写GoodCopy类模板，使得程序按指定方式输出
```
#include <iostream>
using namespace std;


template <class T>
struct GoodCopy {
// 在此处补充你的代码
};

int a[200];
int b[200];
string c[200];
string d[200];

template <class T>
void Print(T s,T e) {
	for(; s != e; ++s)
		cout << * s << ",";
	cout << endl;
}

int main()
{
	int t;
	cin >> t;
	while( t -- ) {
		int m ;
		cin >> m;
		for(int i = 0;i < m; ++i)
			cin >> a[i];
		GoodCopy<int>()(a,a+m,b);
		Print(b,b+m);
		GoodCopy<int>()(a,a+m,a+m/2);
		Print(a+m/2,a+m/2 + m);

		for(int i = 0;i < m; ++i)
			cin >> c[i];
		GoodCopy<string>()(c,c+m,d);
		Print(c,c+m);
		GoodCopy<string>()(c,c+m,c+m/2);
		Print(c+m/2,c+m/2 + m);
	}
	return 0;
}
```
## 输入
第一行是整数 t,表示数据组数  
每组数据：  
第一行是整数 n , n < 50  
第二行是 n 个整数  
第三行是 n 个字符串  
## 输出
将输入的整数原序输出两次，用","分隔  
然后将输入的字符串原序输出两次，也用 ","分隔  
## 样例输入
```
2
4
1 2 3 4
Tom Jack Marry Peking
1
0
Ted
```
## 样例输出
```
1,2,3,4,
1,2,3,4,
Tom,Jack,Marry,Peking,
Tom,Jack,Marry,Peking,
0,
0,
Ted,
Ted,
``` 
# Solution
我们定义了一个GoodCopy类（结构体，不用管public，自动public的），然后这个类用于生成一个函数（看下面）  
所以，只需要处理好迭代器的顺序，要从后往前，不然重叠的那块会先被迭代掉  
下面看代码:
```
#include <iostream>
using namespace std;


template <class T>
struct GoodCopy {
public:
    void operator()(T* a,T* b,T* c){
        for(int i=b-a-1;i>=0;i--){
            *(c+i)=*(a+i);
        }
    }
};

int a[200];
int b[200];
string c[200];
string d[200];

template <class T>
void Print(T s,T e) {
	for(; s != e; ++s)
		cout << * s << ",";
	cout << endl;
}

int main()
{
	int t;
	cin >> t;
	while( t -- ) {
		int m ;
		cin >> m;
		for(int i = 0;i < m; ++i)
			cin >> a[i];
		GoodCopy<int>()(a,a+m,b);
		Print(b,b+m);
		GoodCopy<int>()(a,a+m,a+m/2);
		Print(a+m/2,a+m/2 + m);

		for(int i = 0;i < m; ++i)
			cin >> c[i];
		GoodCopy<string>()(c,c+m,d);
		Print(c,c+m);
		GoodCopy<string>()(c,c+m,c+m/2);
		Print(c+m/2,c+m/2 + m);
	}
	return 0;
}
```
# B:按距离排序
## 描述
程序填空，输出指定结果
```
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
## 输入
多组数据，每组一行，是一个整数n和一个字符串s
## 输出
定义两个整数的距离为两个整数差的绝对值  
定义两个字符串的距离为两个字符串长度差的绝对值

对每组数据：  
对数组a按和n的距离从小到大排序后输出。距离相同的，值小的排在前面。  
然后对数组b，按照和s的距离从小到大输出。距离相同的，字典序小的排在前面  
## 样例输入
```
2 a123456
4 a12345
```
## 样例输出
```
1,3,0,4,7,8,9,10,15,20,
American,Peking,123456789,Jack,To,abcdefghijklmnop,
4,3,1,7,0,8,9,10,15,20,
Peking,American,Jack,123456789,To,abcdefghijklmnop,
```
# Solution
这里可以看到，Closer生成了一个匿名对象，用于sort的比较器  
这个匿名对象函数，肯定是需要接受两个对象，然后判断这两个对象从而给出一个bool对象  
不过，在本题中，这两个对象还需要通过引用原有函数进行进一步比较，上面的两个模板也暗示了我们，一个应该是题目所需的距离，另一个应该是判断函数  
这样就理得很清楚了  
```
#include <iostream>
#include <cmath>
#include <algorithm>
#include <string>
using namespace std;
template <class T1,class T2>
struct Closer {
    T1 val;
    T2 func;
    Closer(T1 val,T2 func):val(val),func(func){ }
    bool operator()(T1 a,T1 b){
        int c=func(a,val);
        int d=func(b,val);
        if(c!=d){
            return c<d;
        }
        return a<b;
    }
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
# C:很难蒙混过关的CArray3D三维数组模板类
## 描述
实现一个三维数组模版CArray3D，可以用来生成元素为任意类型变量的三维数组，输出指定结果
```
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
	for( int i = 0; i < 3; ++ i ) {
		a[i];
		for( int j = 0; j < 4; ++j ) {
			a[j][i];
			for( int k = 0; k < 5; ++k )
				a[i][j][k] = No ++;
			a[j][i][i];	
		}
	}
	PrintA();
	memset(a[1],-1 ,20*sizeof(int));	
	memset(a[1],-1 ,20*sizeof(int));
	PrintA(); 
	memset(a[1][1],0 ,5*sizeof(int));	
	PrintA();

	for( int i = 0; i < 3; ++ i )
		for( int j = 0; j < 2; ++j )
			for( int k = 0; k < 2; ++k )
				b[i][j][k] = 10.0/(i+j+k+1);
	PrintB();
	int n = a[0][1][2];
	double f = b[0][1][1];
	cout << "****" << endl;
	cout << n << "," << f << endl;
		
	return 0;
}
```
## 输入
```
无
```
## 输出
```
等同于样例
```
## 样例输入
```
无
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
5,6,7,8,9,
10,11,12,13,14,
15,16,17,18,19,
layer 1:
-1,-1,-1,-1,-1,
-1,-1,-1,-1,-1,
-1,-1,-1,-1,-1,
-1,-1,-1,-1,-1,
layer 2:
40,41,42,43,44,
45,46,47,48,49,
50,51,52,53,54,
55,56,57,58,59,
layer 0:
0,1,2,3,4,
5,6,7,8,9,
10,11,12,13,14,
15,16,17,18,19,
layer 1:
-1,-1,-1,-1,-1,
0,0,0,0,0,
-1,-1,-1,-1,-1,
-1,-1,-1,-1,-1,
layer 2:
40,41,42,43,44,
45,46,47,48,49,
50,51,52,53,54,
55,56,57,58,59,
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
7,3.33333
```
## 提示
建议做法：
1. a[i][j][k] 这个表达式的第一个[]返回一个内部类的对象，该内部类也重载了[],且返回值为指针。
2. 必要时需重载对象到指针的强制类型转换运算符
# Solution
这题是重头戏！  
感觉跟我之前写的那个，二元数组的实现有点像，这里我主要解释一下吧  
首先肯定要有三维的数据和一个T* 指针，分配出[x\*y\*z]大小的空间  
然后，考虑降维  
我们肯定要重载[]这个函数，而根据题目提示，最后一个[]直接从T*类变成T类了，所以只要在三维和二维各自重载一个[]就好  
然后，为什么要写这个operator T\*呢？  
我们为了迎合memset，要把CArray2D这个类转换成T* 类，从而完成任务！  
下面看代码:
```
#include <iostream>
#include <iomanip> 
#include <cstring>
using namespace std;
template <class T>
class CArray3D
{
public:
    int x,y,z;
    T* p;
    CArray3D(int x,int y,int z):x(x),y(y),z(z){
        p=new T[x*y*z];
    }
    class CArray2D{
    private:
        T* dd;
        int k;
    public:
        CArray2D(T* pd,int id):dd(pd),k(id){ }
        T* operator [](int index){
            T* ddg=dd+index*k;
            return ddg;
        }    
        operator T*(){
            return dd;
        }
    };
    CArray2D operator [](int index){
        T* dd=p+index*y*z;
        return CArray2D(dd,z);
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
	for( int i = 0; i < 3; ++ i ) {
		a[i];
		for( int j = 0; j < 4; ++j ) {
			a[j][i];
			for( int k = 0; k < 5; ++k )
				a[i][j][k] = No ++;
			a[j][i][i];	
		}
	}
	PrintA();
	memset(a[1],-1 ,20*sizeof(int));	
	memset(a[1],-1 ,20*sizeof(int));
	PrintA(); 
	memset(a[1][1],0 ,5*sizeof(int));	
	PrintA();

	for( int i = 0; i < 3; ++ i )
		for( int j = 0; j < 2; ++j )
			for( int k = 0; k < 2; ++k )
				b[i][j][k] = 10.0/(i+j+k+1);
	PrintB();
	int n = a[0][1][2];
	double f = b[0][1][1];
	cout << "****" << endl;
	cout << n << "," << f << endl;
		
	return 0;
}
```
# D:函数对象的过滤器
## 描述
程序填空输出指定结果
```
#include <iostream>
#include <vector>
using namespace std;


struct A {
	int v;
	A() { }
	A(int n):v(n) { };
	bool operator<(const A & a) const {
		return v < a.v;
	}
};
// 在此处补充你的代码
template <class T>
void Print(T s,T e)
{
	for(;s!=e; ++s)
		cout << *s << ",";
	cout << endl;
}
template <class T1, class T2,class T3>
T2 Filter( T1 s,T1 e, T2 s2, T3 op) 
{
	for(;s != e; ++s) {
		if( op(*s)) {
			* s2 = * s;
			++s2;
		}
	}
	return s2;
}

ostream & operator <<(ostream & o,A & a)
{
	o << a.v;
	return o;
}
vector<int> ia;
vector<A> aa; 
int main()
{
	int m,n;
	while(cin >> m >> n) {
		ia.clear();
		aa.clear(); 
		int k,tmp;
		cin >> k;
		for(int i = 0;i < k; ++i) {
			cin >> tmp; 
			ia.push_back(tmp);
			aa.push_back(tmp); 
		}
		vector<int> ib(k);
		vector<A> ab(k);
		vector<int>::iterator p =  Filter(ia.begin(),ia.end(),ib.begin(),FilterClass<int>(m,n));
		Print(ib.begin(),p);
		vector<A>::iterator pp = Filter(aa.begin(),aa.end(),ab.begin(),FilterClass<A>(m,n));
		Print(ab.begin(),pp);
		
	}
	return 0;
}
```
## 输入
多组数据  
每组数据两行

第一行是两个整数 m 和 n  
第二行先是一个整数k ,然后后面跟着k个整数
## 输出
对每组数据，按原顺序输出第二行的后k个整数中，大于m且小于n的数
输出两遍
数据保证一定能找到符合要求的整数
## 样例输入
```
1 3
1 2
2 8
5 1 2 3 4 9
```
## 样例输出
```
2,
2,
3,4,
3,4,
```
# Solution
本题需要我们实现一个FilterClass类，这个类，跟第二题差不多，还是生成一个op判断函数，那就完事了，只不过接收变量从一个变成两个了而已  
```
#include <iostream>
#include <vector>
using namespace std;


struct A {
	int v;
	A() { }
	A(int n):v(n) { };
	bool operator<(const A & a) const {
		return v < a.v;
	}
};
template<class T>
class FilterClass{
public:
    T m,n;
    FilterClass(T m,T n):m(m),n(n){ }
    bool operator()(T val){
        return (m<val)&&(val<n);
    }
};
template <class T>
void Print(T s,T e)
{
	for(;s!=e; ++s)
		cout << *s << ",";
	cout << endl;
}
template <class T1, class T2,class T3>
T2 Filter( T1 s,T1 e, T2 s2, T3 op) 
{
	for(;s != e; ++s) {
		if( op(*s)) {
			* s2 = * s;
			++s2;
		}
	}
	return s2;
}

ostream & operator <<(ostream & o,A & a)
{
	o << a.v;
	return o;
}
vector<int> ia;
vector<A> aa; 
int main()
{
	int m,n;
	while(cin >> m >> n) {
		ia.clear();
		aa.clear(); 
		int k,tmp;
		cin >> k;
		for(int i = 0;i < k; ++i) {
			cin >> tmp; 
			ia.push_back(tmp);
			aa.push_back(tmp); 
		}
		vector<int> ib(k);
		vector<A> ab(k);
		vector<int>::iterator p =  Filter(ia.begin(),ia.end(),ib.begin(),FilterClass<int>(m,n));
		Print(ib.begin(),p);
		vector<A>::iterator pp = Filter(aa.begin(),aa.end(),ab.begin(),FilterClass<A>(m,n));
		Print(ab.begin(),pp);
		
	}
	return 0;
}
```
# E:白给的list排序
## 描述
程序填空，产生指定输出
```
#include <cstdio>
#include <iostream>
#include <algorithm>
#include <list>
using namespace std;
int main()
{	
	double a[] = {1.2,3.4,9.8,7.3,2.6};
	list<double> lst(a,a+5);
	lst.sort(
// 在此处补充你的代码
);
	
	for(list<double>::iterator i  = lst.begin(); i != lst.end(); ++i) 
		cout << * i << "," ;
    return 0;
}
```
## 输入
```
无
```
## 输出
```
9.8,7.3,3.4,2.6,1.2,
```
## 样例输入
```
无
```
## 样例输出
```
同输入
```
# Solution 
这道题，就是考察课件内容  
五一还需要好好地把课件内容过一遍  
STL中给我们定义了一个比较函数  
greater<数据类型>()  
这个函数自动实现降序比较 那就完事了  
```
#include <cstdio>
#include <iostream>
#include <algorithm>
#include <list>
using namespace std;
int main()
{	
	double a[] = {1.2,3.4,9.8,7.3,2.6};
	list<double> lst(a,a+5);
	lst.sort(
greater<double>()
);
	
	for(list<double>::iterator i  = lst.begin(); i != lst.end(); ++i) 
		cout << * i << "," ;
    return 0;
}
```
# F:我自己的ostream_iterator
## 描述
程序填空输出指定结果
```
#include <iostream>
#include <list>
#include <string>
using namespace std;

template <class T1,class T2>
void Copy(T1 s,T1 e, T2 x)
{
	for(; s != e; ++s,++x)
		*x = *s;
}

 
template<class T>
class myostream_iteraotr
{
// 在此处补充你的代码
};


int main()
{	const int SIZE = 5;
	int a[SIZE] = {5,21,14,2,3};
	double b[SIZE] = { 1.4, 5.56,3.2,98.3,3.3};
	list<int> lst(a,a+SIZE);
	myostream_iteraotr<int> output(cout,",");
	Copy( lst.begin(),lst.end(),output); 
	cout << endl;
	myostream_iteraotr<double> output2(cout,"--");
	Copy(b,b+SIZE,output2);
	return 0;
}
```
## 输入
```
无
```
## 输出
```
5,21,14,2,3,
1.4--5.56--3.2--98.3--3.3--
```
## 样例输入
```
无
```
## 样例输出
```
同输入
```
# Solution
上次不是有个“山寨的istream_iterator”这道题嘛，提醒我们要去参考STL的原装代码  
然后我就去看了一下
```
	ostream_iterator& operator=(const _Ty& _Val) { // insert value into output stream, followed by delimiter
        *_Myostr << _Val;
        if (_Mydelim) {
            *_Myostr << _Mydelim;
        }

        return *this;
    }

    _NODISCARD ostream_iterator& operator*() noexcept /* strengthened */ {
        return *this;
    }

    ostream_iterator& operator++() noexcept /* strengthened */ {
        return *this;
    }

```
到这里一切都很明朗了，事实上本来就只需要重载'++'、'*'和'='三个符号，无非是重载方式调一下而已  
下面看代码:
```
#include <iostream>
#include <list>
#include <string>
using namespace std;

template <class T1,class T2>
void Copy(T1 s,T1 e, T2 x)
{
	for(; s != e; ++s,++x)
		*x = *s;
}

 
template<class T>
class myostream_iteraotr
{
private:
    ostream& ost;
    T n;
    string k;
public:
    myostream_iteraotr(ostream& ost,string x):ost(ost),k(x) { }
    myostream_iteraotr& operator++(){
        return *this;
    }
    myostream_iteraotr& operator*(){
        return *this;
    }
    void operator=(const T& other){
        ost<<other<<k;
    }
};


int main()
{	const int SIZE = 5;
	int a[SIZE] = {5,21,14,2,3};
	double b[SIZE] = { 1.4, 5.56,3.2,98.3,3.3};
	list<int> lst(a,a+SIZE);
	myostream_iteraotr<int> output(cout,",");
	Copy( lst.begin(),lst.end(),output); 
	cout << endl;
	myostream_iteraotr<double> output2(cout,"--");
	Copy(b,b+SIZE,output2);
	return 0;
}
```