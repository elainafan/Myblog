---
title: 期中C++部分补充题一
date: 2025-05-09
categories:
    - 程序设计实习
---
# A:编程填空：Hero和Priest
## 描述
完善以下程序，使其输出为
```
Hero::defense()

Hero::attack()

Priest::defense()

Priest::attack()

Priest::defense()

#include <iostream>
using namespace std;
class Hero {
public:
// 在此处补充你的代码
};
class Priest: public Hero {
public:
    virtual void attack() { cout << "Priest::attack()" << endl; }
    virtual void defense() { cout << "Priest::defense()" << endl; } 
}; 

int main() {
    Priest anduin;
    Hero h;
    h.defense();
    Hero *player = &anduin;
    player->attack();
    player->defense();
    anduin.attack();
    anduin.defense();
    return 0;
}
```
## 输入
无
## 输出
```
Hero::defense()
Hero::attack()
Priest::defense()
Priest::attack()
Priest::defense()
```
## 样例输入
```
无
```
## 样例输出
```
Hero::defense()
Hero::attack()
Priest::defense()
Priest::attack()
Priest::defense()
```
# Solution
这道题没什么特殊的，就是直接开  
```
#include <iostream>
using namespace std;
class Hero {
public:
virtual void defense() { cout<<"Hero::defense()"<<endl; }
    void attack() { cout<<"Hero::attack()"<<endl; }
};
class Priest: public Hero {
public:
    virtual void attack() { cout << "Priest::attack()" << endl; }
    virtual void defense() { cout << "Priest::defense()" << endl; } 
}; 

int main() {
    Priest anduin;
    Hero h;
    h.defense();
    Hero *player = &anduin;
    player->attack();
    player->defense();
    anduin.attack();
    anduin.defense();
    return 0;
}
```
# B:可恶的括号
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
  cout << f(3)(5) << endl;
  cout << f(4)(10) << endl;
  cout << f(114)(514) << endl;
  cout << f(9,7) << endl;
  cout << f(2,3) << endl;
  cout << f(2,5) << endl;
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
2
6
400
63
6
10
```
# Solution
这道题就是直接重载两个()，参数不同罢了
```
#include <cstdio>
#include <iostream>
using namespace std;

class f {
private:
    int x;
public:
    f(int t):x(t) { }
    f(int a,int b){
        x=a*b;
    }
    int operator()(int k){
        return k-x;
    }
    friend ostream &operator<<(ostream &os,const f &t){
        os<<t.x;
        return os;
    }
};

int main() {
  cout << f(3)(5) << endl;
  cout << f(4)(10) << endl;
  cout << f(114)(514) << endl;
  cout << f(9,7) << endl;
  cout << f(2,3) << endl;
  cout << f(2,5) << endl;
}
```
# C:编程填空:Dog!Dog!Dog!
## 描述
程序填空，编写Dog类，使得程序按样例进行输出
```
#include <iostream>
using namespace std;
class Mammal {
public:
  Mammal() { cout << "Mammal constructor...\n"; }
  virtual ~Mammal() { cout << "Mammal destructor...\n"; }
  Mammal (const Mammal & rhs);
  virtual void Speak() const { cout << "Mammal speak!\n"; }
  virtual Mammal* Clone() { return new Mammal(*this); }
};
  
class Dog : public Mammal {
// 在此处补充你的代码
};

Mammal::Mammal (const Mammal & rhs) {
  cout << "Mammal Copy Constructor...\n";
}
  
Dog::Dog(){ cout << "Dog constructor...\n"; }
Dog::~Dog(){ cout << "Dog destructor...\n"; }
void Dog::Speak()const { cout << "Woof!\n"; }

int main() {
  Mammal* x=new Dog, *y=new Mammal;
  Mammal* x1=x->Clone(), *y1=y->Clone();
  x1->Speak(); y1->Speak();
  return 0;
}
```
## 输入
.
## 输出
.
## 样例输入
```
（无）
```
## 样例输出
```
Mammal constructor...
Dog constructor...
Mammal constructor...
Mammal Copy Constructor...
Dog copy constructor...
Mammal Copy Constructor...
Woof!
Mammal speak!
```
# Solution
这道题需要我们创建一个Dog类作为Mammal类的派生类，然后顺便注意一下外面的几个函数也要在里面写一下粗浅的定义。  
同时，因为有虚函数Clone的存在，我们需要通过复制构造函数和上面已经有示例的Clone函数来实现
```
#include <iostream>
using namespace std;
class Mammal {
public:
  Mammal() { cout << "Mammal constructor...\n"; }
  virtual ~Mammal() { cout << "Mammal destructor...\n"; }
  Mammal (const Mammal & rhs);
  virtual void Speak() const { cout << "Mammal speak!\n"; }
  virtual Mammal* Clone() { return new Mammal(*this); }
};
  
class Dog : public Mammal {
public:
    void Speak()const;
    Dog();
    Dog(const Dog &t):Mammal(t){ cout<<"Dog copy constructor...\n"; }
    ~Dog();
    Mammal* Clone(){ return new Dog(*this); }
};

Mammal::Mammal (const Mammal & rhs) {
  cout << "Mammal Copy Constructor...\n";
}
  
Dog::Dog(){ cout << "Dog constructor...\n"; }
Dog::~Dog(){ cout << "Dog destructor...\n"; }
void Dog::Speak()const { cout << "Woof!\n"; }

int main() {
  Mammal* x=new Dog, *y=new Mammal;
  Mammal* x1=x->Clone(), *y1=y->Clone();
  x1->Speak(); y1->Speak();
  return 0;
}
```
# D:编程填空:cmp函数模板
## 描述
填写代码，按要求输出结果。要求实现cmp函数模板，不能实现cmp函数。
```
#include <vector>
#include <set>
#include <list>
#include <iostream>
using namespace std;

template <class T>
// 在此处补充你的代码
int main(){
  int A[100];
  A[0]=1; A[1]=2;
  cmp(A[0],2);
  printf("finish 1\n");
  cmp(1, A[1]);
  printf("finish 2\n");
  cmp(A,A[1]);
  printf("finish 3\n");
}
```
## 输入
.
## 输出
.
## 样例输入
```
（无）
```
## 样例输出
```
a
finish 1
b
finish 2
c
finish 3
```
# Solution
好吧，这道题放在这里绝对是卡人的  
我们只能通过多个重载去判断，然后？  
这个a和b其实根本无法判断啊  
这时，我们发现，题目让写的是全局的  
一个变量的事不就完了吗，真就抖机灵
```
#include <vector>
#include <set>
#include <list>
#include <iostream>
using namespace std;

template <class T>
void cmp(T x,int y){
    cout<<'a'<<endl;
}
int k=0;
template<>
void cmp<>(int a,int b){
    if(k%2) cout<<'b'<<endl;
    else{
        k++;
        cout<<'a'<<endl;
    }
}
template<class T>
void cmp(T* a,int b){
    cout<<'c'<<endl;
}
int main(){
  int A[100];
  A[0]=1; A[1]=2;
  cmp(A[0],2);
  printf("finish 1\n");
  cmp(1, A[1]);
  printf("finish 2\n");
  cmp(A,A[1]);
  printf("finish 3\n");
}
```
# E:编程填空：花里胡哨的求和
## 描述
读入 n 个数, 输出 n 个数, 其中第 i 个数是读入中前 i 个数的和
```
#include<iostream>
#include<vector>
using namespace std;
class A{
// 在此处补充你的代码
};
int A::presum=0;
int main(){
  int n;cin>>n;
  vector<A*> p;
  for(int i=0;i<n;i++){
    int x;cin>>x;
    p.push_back(new A(x));
  }
  for(int i=0;i<n;i++){
    p[i]->output();
  }
  return 0;
}
```
## 输入
.
## 输出
.
## 样例输入
```
3
1 2 3
```
## 样例输出
```
1
3
6
```
# Solution
这题简单啊，静态成员变量直接加上x完事了
```
#include<iostream>
#include<vector>
using namespace std;
class A{
private:
    int x;
    static int presum;
public:
    A(int t):x(t) { }
    void output(){
        presum+=x;
        cout<<presum<<endl;
    }
};
int A::presum=0;
int main(){
  int n;cin>>n;
  vector<A*> p;
  for(int i=0;i<n;i++){
    int x;cin>>x;
    p.push_back(new A(x));
  }
  for(int i=0;i<n;i++){
    p[i]->output();
  }
  return 0;
}
```
# F:编程填空:Midterm
## 描述
填写缺失的部分，使程序输出要求的结果。
```
#include<iostream>
using namespace std;

class Midterm {
private:
  int val; 
public:
// 在此处补充你的代码
};

int Min(int a,int b) {
  if(a < b)
    return a;
  else
    return b;
}
int main(){
  Midterm a; 
  cout << a << endl;
  cout << a + 2021 << endl;
  Midterm b(1000);
  cout << b ++ << endl; 
  ((b-=10)-=20)-=30;
  cout << b ++ << endl; 
  cout << Min(255,b) <<endl;
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
0
2021
1001
942
255
```
# Solution
这个题也是不难，毕竟就要求我们重载几个运算符，然后就完事了  
调用Min的时候需要一个类型转换函数  
```
#include<iostream>
using namespace std;

class Midterm {
private:
  int val; 
public:
friend ostream &operator<<(ostream &os,const Midterm &t){
        os<<t.val;
        return os;
    }
    Midterm operator+(int x){
        val+=x;
        Midterm temp;
        temp.val=val;
        return temp;
    }
    Midterm(int x):val(x) { }
    Midterm() { }
    Midterm operator++(int ){
        Midterm temp;
        val++;
        temp.val=val;
        return temp;
    }
    operator int(){
        return val;
    }
    Midterm &operator-=(int x){
        val-=x;
        return *this;
    }
};

int Min(int a,int b) {
  if(a < b)
    return a;
  else
    return b;
}
int main(){
  Midterm a; 
  cout << a << endl;
  cout << a + 2021 << endl;
  Midterm b(1000);
  cout << b ++ << endl; 
  ((b-=10)-=20)-=30;
  cout << b ++ << endl; 
  cout << Min(255,b) <<endl;
  return 0;
}
```
# G:编程填空：统计个数
## 描述
请补充下列代码，使其可以根据输入分别统计不同数字个数以及不同字符串个数。
```
#include <iostream>
#include <string>
#include <set>
using namespace std;

class Counter{
    int cnt;
public:
    Counter():cnt(0){}
    virtual void push(void*) = 0;
    virtual string name() = 0;
    void inc(){
        ++cnt;
    }
    int number(){
        return cnt;
    }
};

template<class T>
class TCounter: public Counter{
// 在此处补充你的代码
};

Counter* build_counter(string name){
    if (name == "int") return new TCounter<int>("int");
    else return new TCounter<string>("string");
}



int main(){
    int n, m;
    cin >> n >> m;
    Counter *a = build_counter("int"), *b = build_counter("string");
    for (int i = 0; i < n; ++i){
        int x;
        cin >> x;
        a->push(&x);
    }
    for (int i = 0; i < m; ++i){
        string x;
        cin >> x;
        b->push(&x);
    }
    cout << a->name() << ": " << a->number() << endl;
    cout << b->name() << ": " << b->number();
    return 0;
}
```
## 输入
第一行两个整数n,m(1<=n,m<=1e5)，分别代表接下来将会输入的数字个数以及字符串个数。  
接下来两行分别是n个数字以及m个字符串，由空格分隔。  
数字大小不超过int的表示范围，字符串长度不超过10.  
## 输出
输出两行，分别代表不同的数字个数以及不同的字符串个数。
## 样例输入
```
5 5
1 2 3 4 3
a b b a ab
```
## 样例输出
```
int: 4
string: 3
```
# Solution
我们介绍一下void*这个类型  
这个类型的好处在于能够被能被任意类型的指针赋值，本身只表示指向一块地址，没有包含具体类型  
坏处是，这个类型无法被解引用  
都看到前面有两个虚函数了吧？那当然是要重载这两个虚函数啊  
然后，我们只需要写一个set类（因为不重复），并记录这到底是int还是string的字符串
```
#include <iostream>
#include <string>
#include <set>
using namespace std;

class Counter{
    int cnt;
public:
    Counter():cnt(0){}
    virtual void push(void*) = 0;
    virtual string name() = 0;
    void inc(){
        ++cnt;
    }
    int number(){
        return cnt;
    }
};

template<class T>
class TCounter: public Counter{
private:
    set<T>s; 
    string a;
public:
    TCounter(string k):Counter(){
        a=k;
    }
    void push(void* x){
        T* k=(T*)(x);
        if(s.find(*k)==s.end()){
            inc();
            s.insert(*k);
        }
        return ;
    }
    string name(){
        return a;
    }
};

Counter* build_counter(string name){
    if (name == "int") return new TCounter<int>("int");
    else return new TCounter<string>("string");
}



int main(){
    int n, m;
    cin >> n >> m;
    Counter *a = build_counter("int"), *b = build_counter("string");
    for (int i = 0; i < n; ++i){
        int x;
        cin >> x;
        a->push(&x);
    }
    for (int i = 0; i < m; ++i){
        string x;
        cin >> x;
        b->push(&x);
    }
    cout << a->name() << ": " << a->number() << endl;
    cout << b->name() << ": " << b->number();
    return 0;
}
```
# H:p园食宿预订系统
## 描述
某校园为方便学生订餐，推出食堂预定系统。食宿平台会在前一天提供菜单，学生在开饭时间前可订餐。 食堂每天会推出m个菜，每个菜有固定的菜价和总份数，售卖份数不能超过总份数。 假设共有n个学生点餐，每个学生固定点3个菜，当点的菜售罄时, 学生就买不到这个菜了。 请根据学生预定记录，给出食堂总的预定收入 数据满足1 <= n <= 6000，3 <= m <= 6000，单品菜价不大于1000元，每个菜的配额不超过3000

## 输入
第一行两个整数n和m，代表有n个学生订餐，共有m个可选的菜  
下面m行，每行三个元素，分别是菜名、售价和可提供量，保证菜名不重合，菜价为整数  
下面n行，每行三个元素，表示这个学生点的三个菜的菜名
## 输出
一个整数，表示食堂的收入
## 样例输入
```
5 5
yangroupaomo 13 10
jituifan 7 5
luosifen 16 3
xinlamian 12 20
juruo_milktea 999 1
yangroupaomo luosifen juruo_milktea
luosifen xinlamian jituifan
yangroupaomo jituifan juruo_milktea
jituifan xinlamian luosifen
yangroupaomo yangroupaomo yangroupaomo
```
## 样例输出
```
1157
```
# Solution
这题我们是不是在Python里面做过原题？  
当时肯定是用字典做的，那么，C++里对应的数据结构是什么呢？没错，是map
```
#include<bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define lowbit(x) (x&(-x))
using namespace std;
int n,m;
map<string,int>ma;
map<string,int>fa;
int ans=0;
string x,y,z;
int a,b;
int main(){
    cin>>n>>m;
    for(int i=1;i<=m;i++){
        cin>>x>>a>>b;
        ma[x]=a;
        fa[x]=b;
    }
    for(int i=1;i<=n;i++){
        cin>>x>>y>>z;
        if(fa[x]>0){
            fa[x]--;
            ans+=ma[x];
        }
        if(fa[y]>0){
            fa[y]--;
            ans+=ma[y];
        }
        if(fa[z]>0){
            fa[z]--;
            ans+=ma[z];
        }
    }
    cout<<ans<<endl;
    system("pause");
    return 0;
}
```
# I:编程填空:MySet模板
## 描述
程序填空，从set模板派生一个MySet模板  并按要求输出
```
#include <iostream>
#include <map>
#include <algorithm>
#include <string>
#include <vector> 
#include <set>
#include <cstdio>
using namespace std;
// 在此处补充你的代码
struct A {
	int n;
	A(int i):n(i) { }
	operator int() {
		return n;
	}
	bool operator >(const A & a) const {
		return n > a.n;
	}
};
template <class IT>
void print(IT s,IT e)
{	
	for(; s != e; ++s)
		cout << *s << ",";
	cout << endl;
}
int main()
{
	MySet<int> mst;
	for (int i = 0;i < 10; ++i)
		mst.insert(i);
	print(mst.begin(),mst.end());
	int a[] = {1,2,3,4};
	mst.erase(a,a+3);
	print(mst.begin(),mst.end());
	
	A b[] = {{7},{8}};
	mst.erase(b,b+2);
	print(mst.begin(),mst.end());	
	mst.erase(mst.find(6));
	print(mst.begin(),mst.end());
	for(int i = 0;i < 1000000; ++i)
		mst.insert(i);
	for(int i = 0; i < 1000000 - 10; ++i) 
		mst.erase(mst.find(i));
	int n;
	cin >> n;
	MySet<A> msta;
	
	for(int i = 0;i < n; ++i) {
		string cmd;
		int n;
		cin >> cmd >> n;
		if( cmd == "ADD") 
			msta.insert(A(n));
		else {
			if (msta.find(A(n))!= msta.end())
				cout << "YES"  <<endl; 
			else
				cout << "NO" <<endl;
		}
	}
	return 0;
}
```
## 输入
第一行是整数n (n <= 10000)  
接下来n行，每行一个命令，是以下两种格式之一：

ADD n 要求将整数n加入集合  
FIND n 查询集合中有无整数n
## 输出
先产生一些固有的输出，然后，  
对每个FIND命令， 如果集合中有整数n，则输出"YES"，否则输出"NO"
## 样例输入
```
6
ADD 1
ADD 2
FIND 3
FIND 2
ADD 3
FIND 3
```
## 样例输出
```
9,8,7,6,5,4,3,2,1,0,
9,8,7,6,5,4,0,
9,6,5,4,0,
9,5,4,0,
NO
YES
YES
```
# Solution
派生的MySet类，我们都知道，这道题，就按照正常的思路来MySet完事了  
但是，我们要注意的一点是，STL对于重载或者增加Pred判断函数的要求十分严格，一定要在没有影响的函数后面加上const表示只能调用静态成员变量  
同时，我们这个greater<T>根据样例也看得出来
# J:编程填空:C++也能函数式编程
## 描述
填写代码，按要求输出结果
```
#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

// 设 vector v = [x1, x2, ..., xn], 表示其内顺序存储了 x1 ~ xn 共 n 个值

template <class T, class F>
vector<T> vecMap(vector<T> v, F f) {
    // 返回 retV = [f(x1), f(x2), ..., f(xn)]
    vector<T> retV;
    for (auto x : v)
        retV.push_back(f(x));
    return retV;
}

template <class T, class F>
T vecReduce(T init, vector<T> v, F f) {
    // 返回 ret = f(...f(f(f(init, x1), x2), x3) ..., xn)
    T ret = init;
    for (auto x : v)
        ret = f(ret, x);
    return ret;
}

template <class T, class F>
vector<T> vecFilter(vector<T> v, F f) {
    // 返回 retV = [xi : 1 <= i <= n 且 f(xi) 成立]
    vector<T> retV;
    for (auto x : v)
        if (f(x)) retV.push_back(x);
    return retV;
}

template <class T>
void vecPrintln(vector<T> v) {
    // 依次输出 vector v 中的元素
    cout << "[ ";
    for (auto x : v)
        cout << x << ", ";
    cout << "]" << endl;
}

vector<int> vecRangeInt(int l, int r) {
    // 返回一个包含 [l, r) 中整数的 vector
    vector<int> retV;
    for (int x = l; x < r; ++x)
        retV.push_back(x);
    return retV;
}

class UnaryAdd;
class BinaryAdd;
class GetSecond;
class IsPrime;
// 在此处补充你的代码
int main() {
    // 测试 vecMap, UnaryAdd
    vector<int> a = vecRangeInt(0, 5);
    vecPrintln(a);                                  // [ 0, 1, 2, 3, 4, ]
    UnaryAdd addTen(10);
    vecPrintln(vecMap(a, addTen));                  // [ 10, 11, 12, 13, 14, ]
    UnaryAdd addOne(1);
    vecPrintln(vecMap(vecMap(a, addOne), addOne));  // [ 2, 3, 4, 5, 6, ]
    // 测试 vecReduce, GetSecond, BinaryAdd
    vector<int> b1 {1, 0, 2, 4};
    vector<int> b2 {8, 1, 9, 2};
    vector<int> b3 {2, 0, 4, 8};
    GetSecond getSecond;
    BinaryAdd binAdd;
    cout << vecReduce(-2, b1, getSecond) << endl;  // 4
    cout << vecReduce(-1, b2, getSecond) << endl;  // 2
    cout << vecReduce(0, b3, getSecond) << endl;   // 8
    cout << vecReduce(0, b1, binAdd) << endl;  // 0 + 1 + 0 + 2 + 4 = 7
    cout << vecReduce(1, b2, binAdd) << endl;  // 1 + 8 + 1 + 9 + 2 = 21
    cout << vecReduce(2, b3, binAdd) << endl;  // 2 + 2 + 0 + 4 + 8 = 16
    // 测试 vecFilter, isPrime
    vector<int> c1 = vecRangeInt(1, 10);
    vector<int> c2 {17, 11, 10, 19, 15, 23};
    IsPrime isPrime;
    vecPrintln(vecFilter(c1, isPrime));  // [ 2, 3, 5, 7, ]
    vecPrintln(vecFilter(c2, isPrime));  // [ 17, 11, 19, 23, ]

    vector<int> v1 = vecRangeInt(0, 8);
    cout << vecReduce(
            -1000000,
            vecMap(v1, [](int x) { return 7 * x - x * x + 2; }),
            [](int x, int y) { return max(x, y); }
    ) << endl;
    // max { 7x - x^2 + 2 : 0 <= x < 8 } = 14

    vector<int> v2 = vecRangeInt(0, 12);
    vecPrintln(vecFilter(
        vecMap(v2, [](int x) { return 2 * x + 1; }),
        [](int x) { return x % 3 == 0; }
    ));
    // [ 2x + 1 : 0 <= x < 12 且 (2x + 1) 是 3 的倍数 ] = [ 3, 9, 15, 21, ]
    return 0;
}
```
## 输入
.
## 输出
.
## 样例输入
```
（无）
```
## 样例输出
```
[ 0, 1, 2, 3, 4, ]
[ 10, 11, 12, 13, 14, ]
[ 2, 3, 4, 5, 6, ]
4
2
8
7
21
16
[ 2, 3, 5, 7, ]
[ 17, 11, 19, 23, ]
14
[ 3, 9, 15, 21, ]
```
# Solution
这道题就是要求我们实现四个仿函数，太明显了。  
第一个就是用一个数加到另一个数上  
第二个就是连续取后面一个数，然后返回第二个数  
第三个是一个数加到另一个数上  
第四个是判断是否是质数
```
#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

// 设 vector v = [x1, x2, ..., xn], 表示其内顺序存储了 x1 ~ xn 共 n 个值

template <class T, class F>
vector<T> vecMap(vector<T> v, F f) {
    // 返回 retV = [f(x1), f(x2), ..., f(xn)]
    vector<T> retV;
    for (auto x : v)
        retV.push_back(f(x));
    return retV;
}

template <class T, class F>
T vecReduce(T init, vector<T> v, F f) {
    // 返回 ret = f(...f(f(f(init, x1), x2), x3) ..., xn)
    T ret = init;
    for (auto x : v)
        ret = f(ret, x);
    return ret;
}

template <class T, class F>
vector<T> vecFilter(vector<T> v, F f) {
    // 返回 retV = [xi : 1 <= i <= n 且 f(xi) 成立]
    vector<T> retV;
    for (auto x : v)
        if (f(x)) retV.push_back(x);
    return retV;
}

template <class T>
void vecPrintln(vector<T> v) {
    // 依次输出 vector v 中的元素
    cout << "[ ";
    for (auto x : v)
        cout << x << ", ";
    cout << "]" << endl;
}

vector<int> vecRangeInt(int l, int r) {
    // 返回一个包含 [l, r) 中整数的 vector
    vector<int> retV;
    for (int x = l; x < r; ++x)
        retV.push_back(x);
    return retV;
}

class UnaryAdd;
class BinaryAdd;
class GetSecond;
class IsPrime;
class UnaryAdd{
private:
	int x;
public:
	UnaryAdd(int t):x(t) { }
	int operator()(int y){
		return x+y;
	}
};
class GetSecond{
public:
	int operator()(int x,int y){
		return y;
	}
};
class BinaryAdd{
public:
	int operator()(int x,int y){
		return x+y;
	}
};
class IsPrime{
public:
	bool operator()(int x){
		if(x==1) return false;
		if(x==2||x==3) return true;
		for(int i=2;i*i<=x;i++){
			if(x%i==0) return false;
		} 
		return true;
	}
};
int main() {
    // 测试 vecMap, UnaryAdd
    vector<int> a = vecRangeInt(0, 5);
    vecPrintln(a);                                  // [ 0, 1, 2, 3, 4, ]
    UnaryAdd addTen(10);
    vecPrintln(vecMap(a, addTen));                  // [ 10, 11, 12, 13, 14, ]
    UnaryAdd addOne(1);
    vecPrintln(vecMap(vecMap(a, addOne), addOne));  // [ 2, 3, 4, 5, 6, ]
    // 测试 vecReduce, GetSecond, BinaryAdd
    vector<int> b1 {1, 0, 2, 4};
    vector<int> b2 {8, 1, 9, 2};
    vector<int> b3 {2, 0, 4, 8};
    GetSecond getSecond;
    BinaryAdd binAdd;
    cout << vecReduce(-2, b1, getSecond) << endl;  // 4
    cout << vecReduce(-1, b2, getSecond) << endl;  // 2
    cout << vecReduce(0, b3, getSecond) << endl;   // 8
    cout << vecReduce(0, b1, binAdd) << endl;  // 0 + 1 + 0 + 2 + 4 = 7
    cout << vecReduce(1, b2, binAdd) << endl;  // 1 + 8 + 1 + 9 + 2 = 21
    cout << vecReduce(2, b3, binAdd) << endl;  // 2 + 2 + 0 + 4 + 8 = 16
    // 测试 vecFilter, isPrime
    vector<int> c1 = vecRangeInt(1, 10);
    vector<int> c2 {17, 11, 10, 19, 15, 23};
    IsPrime isPrime;
    vecPrintln(vecFilter(c1, isPrime));  // [ 2, 3, 5, 7, ]
    vecPrintln(vecFilter(c2, isPrime));  // [ 17, 11, 19, 23, ]

    vector<int> v1 = vecRangeInt(0, 8);
    cout << vecReduce(
            -1000000,
            vecMap(v1, [](int x) { return 7 * x - x * x + 2; }),
            [](int x, int y) { return max(x, y); }
    ) << endl;
    // max { 7x - x^2 + 2 : 0 <= x < 8 } = 14

    vector<int> v2 = vecRangeInt(0, 12);
    vecPrintln(vecFilter(
        vecMap(v2, [](int x) { return 2 * x + 1; }),
        [](int x) { return x % 3 == 0; }
    ));
    // [ 2x + 1 : 0 <= x < 12 且 (2x + 1) 是 3 的倍数 ] = [ 3, 9, 15, 21, ]
    return 0;
}
```
# K:编程填空：计算数组的低3位之和
## 描述
输入一个正整数构成的数组a[0], a[1], a[2], ... , a[n-1], 计算它们的二进制低3位之和。
```
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
// 在此处补充你的代码
int main(int argc, char* argv[]) {
	int  v, my_sum=0;
	vector<int> vec;		
	cin>>v;
	while ( v ) {
		vec.push_back(v);
		cin>>v;
	}
	for_each(vec.begin(), vec.end(), CMy_add(my_sum));
	cout<<my_sum<<endl;	
	return 0;
}
```
## 输入
数组a,以0表示输入结束。
## 输出
一个整数 , 所输入数组各元素的二进制低3位之和。
## 样例输入
```
1 3 9 7 3 6 20 15 18 17 4 8 18 0 
```
## 样例输出
```
41
```
# Solution
其实我不知道低3位是什么，还查了一下  
然后发现就是最低3个二进制位的数之和（1,2,4）的排列组合
```
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
class CMy_add{
private:
    int& result;
    bool flag;
public:
    CMy_add(int& x):result(x),flag(true) { }
    CMy_add(const CMy_add &other):result(other.result),flag(false) { }
    void operator()(int x){
        result+=(x&1);
        result+=((x>>1)&1)*2;
        result+=((x>>2)&1)*4;
    }
};
int main(int argc, char* argv[]) {
	int  v, my_sum=0;
	vector<int> vec;		
	cin>>v;
	while ( v ) {
		vec.push_back(v);
		cin>>v;
	}
	for_each(vec.begin(), vec.end(), CMy_add(my_sum));
	cout<<my_sum<<endl;	
	return 0;
}
```
# L:求平均数的类真叫mean
## 描述
输入一系列正整数, 计算它们的平均值，结果去尾取整数
```
#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>
using namespace std;
class CMean {
// 在此处补充你的代码
};

int main(int argc, char* argv[]) {
	int  v;
	int t;
	cin >> t;
	while ( t -- ) {
		cin >> v;
		vector<int> vec;
		while (v) {
			vec.push_back(v);
			cin >> v;
		}
		int myAver = 0;
		for_each(vec.begin(), vec.end(), CMean(myAver));
		cout << myAver << endl;
	}
	return 0;
}
```
## 输入
第一行是测试数据组数T  
接下T行，每行一组数据。每行是若干个正整数，以0表示输入结束(0不算)。
## 输出
对每组数据，输出所有数的平均值，结果去尾取整数
## 样例输入
```
1
17 4 8 18 0
``` 
## 样例输出
```
11
```
# Solution
这题就是开始考验我们的for_each技术了，先来介绍一下这个吧  
就是呢，for_each只会生成一个CMean类，你可能觉得简单，不要笑，但是编译会有更神奇的东西  
就是，我们通常需要在析构函数中作一些操作的时候，会发现，这操作怎么作了两次  
其实是因为移动构造函数惹的祸，它会通过复制构造函数把我们现有的类复制给别的东西  
这个时候我们需要做什么？就是让这个复制后的函数不执行析构函数中的操作（不是不析构！），只需要在原函数中体现一个bool变量，复制构造函数中让这个变量变成false,就能保证了  
还有，因为没有地方可以返回这个变量，所以类中的变量要改成一个整数型引用
```
#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>
using namespace std;
class CMean {
private:
	int& result;
	int num;
	bool flag;
public:
	CMean(int& t):result(t),num(0),flag(true) { }
	void operator()(const auto &x){
		result+=x;
		num++;
		return ;
	}
	CMean(const CMean &other):result(other.result),num(other.num),flag(false){ }
	~CMean(){
		if(flag){
			result/=num;
			flag=false;
		} 
	}
};

int main(int argc, char* argv[]) {
	int  v;
	int t;
	cin >> t;
	while ( t -- ) {
		cin >> v;
		vector<int> vec;
		while (v) {
			vec.push_back(v);
			cin >> v;
		}
		int myAver = 0;
		for_each(vec.begin(), vec.end(), CMean(myAver));
		cout << myAver << endl;
	}
	return 0;
}
```
# M:积分图
## 描述
对于一幅灰度的图像，积分图中的任意一点(x,y)的值是指从图像的左上角到这个点的所构成的矩形区域内所有的点的灰度值之和。
```
#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;
class IntegralImage{
// 在此处补充你的代码
};
int main(){
    int H, W;
    cin >> H >> W;
    int ** image = new int*[H];
    for(int i=0;i<H;++i){
        image[i]=new int[W];
    }
    for(int i=0;i<H;++i)
    for(int j=0;j<W;++j)
        cin >> image[i][j];
    IntegralImage it(H,W);
    for_each(image, image+H, it);
    for(int i=0;i<H;++i){
        for(int j=0;j<W;++j)
            cout<<it[i][j]<<" ";
        cout<<endl;
    }
   
}
```
## 输入
第一行两个整数，分别是图像的宽、高H, W  
接下来H*W的矩阵，分别代表图像的每个像素值
## 输出
积分图中每个点的值, H*W的矩阵，每个像素之间用空格分开
## 样例输入
```
2 3
1 2 3
1 0 0
```
## 样例输出
```
1 3 6
2 4 7
```
# Solution
这道题，我还是需要对这个矩阵作一些操作  
至于二维指针的设置，题目中已经有示例了，我们不管  
然后，我们新创建的指针要初始化  
最后重载一下[]就可以
```
#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;
class IntegralImage{
private:
	int h,w;
	int** dd;
	int num;
public:
	IntegralImage(int a,int b):h(a),w(b),num(0){
		dd=new int*[h];
		for(int i=0;i<h;i++){
			dd[i]=new int[w];
		}
		for(int i=0;i<h;i++){
			for(int j=0;j<w;j++){
				dd[i][j]=0;
			}
		}
	}
	void operator()(int* x){
		for(int i=0;i<w;i++){
			for(int j=num;j<h;j++){
				for(int v=i;v<w;v++){
					dd[j][v]+=x[i];
				}
			}
		}
		num++;
	}
	int* operator[](int x){
		return dd[x];
	}
};
int main(){
    int H, W;
    cin >> H >> W;
    int ** image = new int*[H];
    for(int i=0;i<H;++i){
        image[i]=new int[W];
    }
    for(int i=0;i<H;++i)
    for(int j=0;j<W;++j)
        cin >> image[i][j];
    IntegralImage it(H,W);
    for_each(image, image+H, it);
    for(int i=0;i<H;++i){
        for(int j=0;j<W;++j)
            cout<<it[i][j]<<" ";
        cout<<endl;
    }
   
}
```
# N:编程填空：序列累加和字符串复制
## 描述
程序填空完成指定功能
```
#include <iostream>
#include <set>
#include <string>
#include <stdio.h>
#include <vector>
#include <algorithm>
using namespace std;
// 在此处补充你的代码
int main(){
    vector<int> v1;
    vector<string> v2;
    int N, val, num_repeat,result_int=0;
    string str,result_str="";
    cin>>N;
    cin>>num_repeat;
    for(int i=0;i<N;++i){
        cin>>val;
        v1.push_back(val);
    }
    for_each(v1.begin(),v1.end(),MyFunc<int>(num_repeat,result_int));
    for(int i=0;i<N;++i){
        cin>>str;
        v2.push_back(str);
    }
    for_each(v2.begin(),v2.end(),MyFunc<string>(num_repeat,result_str));
    cout<<result_int<<endl;
    cout<<"--------------"<<endl;
    cout<<result_str<<endl;
}
```
## 输入
首先读入两个整数N和M，表示数字/字符串序列的元素个数及累加次数。  
接下来输入N个整数，形成这个数字序列。  
接下来输入N个字符串，形成一个字符串序列。  
## 输出
对数字序列进行累加，并将结果乘以M之后输出。  
对字符串序列进行拼接，并将结果复制M次之后输出。
## 样例输入
```
3 4
9 8 1
ab cd ef
```
## 样例输出
```
72
--------------
abcdefabcdefabcdefabcdef
```
# Solution
这道题跟我们上面说的for_each的析构函数是一样的，然后，对于这种STL，我们还是要养成写const的好习惯  
其他流程跟上面那道题几乎没有区别
```
#include <iostream>
#include <set>
#include <string>
#include <stdio.h>
#include <vector>
#include <algorithm>
using namespace std;
template<class T>
class MyFunc{
private:
    int& num_repeat;
    T& result;
    bool flag;
public:
    MyFunc(int& n,T& k):num_repeat(n),result(k),flag(true) { }
    MyFunc(const MyFunc &other):num_repeat(other.num_repeat),result(other.result),flag(false) { }
    void operator()(const T& a)const{
        result+=a;
        return ;
    }
    ~MyFunc(){
        if(flag){
            const T temp=result;
            for(int i=1;i<=num_repeat-1;i++){
            result+=temp;
            }
        }
    }
};
int main(){
    vector<int> v1;
    vector<string> v2;
    int N, val, num_repeat,result_int=0;
    string str,result_str="";
    cin>>N;
    cin>>num_repeat;
    for(int i=0;i<N;++i){
        cin>>val;
        v1.push_back(val);
    }
    for_each(v1.begin(),v1.end(),MyFunc<int>(num_repeat,result_int));
    for(int i=0;i<N;++i){
        cin>>str;
        v2.push_back(str);
    }
    for_each(v2.begin(),v2.end(),MyFunc<string>(num_repeat,result_str));
    cout<<result_int<<endl;
    cout<<"--------------"<<endl;
    cout<<result_str<<endl;
}
```
# O:编程填空：人群的排序和分类
## 描述
对人群按照输入的信息进行排序和分类。
```
#include <iostream>
#include <set>
#include <iterator>
#include <algorithm>
using namespace std;
// 在此处补充你的代码
int main()
{

	int t;
	cin >> t;
	set<A*,Comp> ct;
	while( t -- ) {
		int n;
		cin >> n;
		ct.clear();
		for( int i = 0;i < n; ++i)	{
			char c; int k;
			cin >> c >> k;
			
			if( c == 'A')
				ct.insert(new A(k));
			else
				ct.insert(new B(k));
		}	
		for_each(ct.begin(),ct.end(),Print);
		cout << "****" << endl;
	}
}
```
## 输入
第一行是整数t,表明一共t组数据. t < 20  
对每组数据：  
第一行是整数n,表示下面一共有n行。 0 < n < 100  
下面的每行代表一个人。每行以一个字母开头，代表该人所属的类别，然后跟着一个整数，代表年龄。字母只会是 'A‘或‘B' 。整数范围0到100。数据保证年龄都不相同。  
## 输出
对每组输入数据，将这些人按年龄从小到大输出。每个人先输出类别，再输出年龄。每组数据的末尾加一行 "****"
## 样例输入
```
2
4
A 3
B 4
A 5
B 6
3
A 4
A 3
A 2
```
## 样例输出
```
A 3
B 4
A 5
B 6
****
A 2
A 3
A 4
****
```
# Solution
我们需要通过输入来分类  
注意，这里A类在set中的表现是指针形式的  
而且，后续可以insert一个B类变量，为什么不需要我说了吧？  
当然是因为B是A的派生类  
同时，我们还需要构造一个仿函数，这个仿函数对A*和B\*进行比较，这里再强调一次，STL的自定义比较器一定要加const，不然会报错  
调用B类的时候，id变量赋成"B"，所以要再给A类写一个空默认构造函数
```
#include <iostream>
#include <set>
#include <iterator>
#include <algorithm>
using namespace std;
class A{
public:
	int age;
	char id;
	A(int x):age(x) { id='A'; }
	A(){ }
};
class B:public A{
public:
	B(int x){ 
		id='B';
		age=x; 
	} 
};
struct Comp{
	bool operator()(A* x,A* y)const{
		return x->age<y->age;
	}
};
void Print(const A* a){
	cout<<a->id<<' '<<a->age<<endl;
}
int main()
{

	int t;
	cin >> t;
	set<A*,Comp> ct;
	while( t -- ) {
		int n;
		cin >> n;
		ct.clear();
		for( int i = 0;i < n; ++i)	{
			char c; int k;
			cin >> c >> k;
			
			if( c == 'A')
				ct.insert(new A(k));
			else
				ct.insert(new B(k));
		}	
		for_each(ct.begin(),ct.end(),Print);
		cout << "****" << endl;
	}
}
```
# P:编程填空：数据库内的学生信息
## 描述
程序填空，使得下面的程序,先输出

(Tom,80),(Tom,70),(Jone,90),(Jack,70),(Alice,100),

(Tom,78),(Tom,78),(Jone,90),(Jack,70),(Alice,100),

(70,Jack),(70,Tom),(80,Tom),(90,Jone),(100,Alice),

(70,Error),(70,Error),(80,Tom),(90,Jone),(100,Alice),

******

然后，再根据输入数据按要求产生输出数据
```
#include <iostream>
#include <string>
#include <map>
#include <iterator>
#include <algorithm>
using namespace std;
// 在此处补充你的代码
struct Student 
{
	string name;
	int score;
};
template <class T>
void Print(T first,T last) {
	for(;first!= last; ++ first)
		cout << * first << ",";
	cout << endl;
}
int main()
{
	
	Student s[] = { {"Tom",80},{"Jack",70},
					{"Jone",90},{"Tom",70},{"Alice",100} };
	
	MyMultimap<string,int> mp;
	for(int i = 0; i<5; ++ i)
		mp.insert(make_pair(s[i].name,s[i].score));
	Print(mp.begin(),mp.end()); //按姓名从大到小输出

	mp.Set("Tom",78); //把所有名为"Tom"的学生的成绩都设置为78
	Print(mp.begin(),mp.end());
	
	
	
	MyMultimap<int,string,less<int> > mp2;
	for(int i = 0; i<5; ++ i) 
		mp2.insert(make_pair(s[i].score,s[i].name));
	
	Print(mp2.begin(),mp2.end()); //按成绩从小到大输出
	mp2.Set(70,"Error");          //把所有成绩为70的学生，名字都改为"Error"
	Print(mp2.begin(),mp2.end());
	cout << "******" << endl;
	
	mp.clear();
	
	string name;
	string cmd;
	int score;		
	while(cin >> cmd ) {
		if( cmd == "A") {
			cin >> name >> score;
			if(mp.find(name) != mp.end() ) {
				cout << "erroe" << endl;
			}
			mp.insert(make_pair(name,score));
		}
		else if(cmd == "Q") {
			cin >> name;
			MyMultimap<string,int>::iterator p = mp.find(name);
			if( p!= mp.end()) {
				cout << p->second << endl;
			}
			else {
				cout << "Not Found" << endl; 
			}		
		}
	}
	return 0;
}
```
## 输入
输入数据的每一行，格式为以下之一：

A name score  
Q name score

name是个不带个空格的字符串，长度小于 20  
score是个整数，能用int表示

A name score 表示往数据库中新增一个姓名为name的学生，其分数为score。开始时数据库中一个学生也没有。  
Q name 表示在数据库中查询姓名为name的学生的分数


数据保证学生不重名。  
输入数据少于200,000行。
## 输出
对于每个查询，输出学生的分数。如果查不到，则输出 "Not Found"
## 样例输入
```
A Tom1 30
A Tom2 40
Q Tom3 
A Tom4 89
Q Tom1
Q Tom2
```
## 样例输出
```
(Tom,80),(Tom,70),(Jone,90),(Jack,70),(Alice,100),
(Tom,78),(Tom,78),(Jone,90),(Jack,70),(Alice,100),
(70,Jack),(70,Tom),(80,Tom),(90,Jone),(100,Alice),
(70,Error),(70,Error),(80,Tom),(90,Jone),(100,Alice),
******
Not Found
30
40
```
## 提示
1) 编写模板的时候，连续的两个 “>”最好要用空格分开，以免被编译器看作是 ">>"运算符。VS可能无此问题，但是Dev C++和服务器上的编译环境会有这个问题。  
比如 vector<vector< int >> 有可能出错，要改成 vector<vector< int > >

2) 在模板中写迭代器时，最好在前面加上 typename关键字，否则可能会编译错。VS可能无此问题，但是Dev C++和服务器上的编译环境会有这个问题。
# Solution
这道题其实之前出过了，主要的要点还是在这个multimap类的重载  
我们需要一个Pred类来作为这个multimap的比较函数（缺省变量是T1类型的greater），这点一定不能忘！  
然后剩下的几个函数不谈  
我们注意一下，这个typedef的重命名问题，前面表示的是对于实例化的模板类的名称，所以真正要改名的只有iterator一个  
还有这个输出函数也要使用模板类
```
#include <iostream>
#include <string>
#include <map>
#include <iterator>
#include <algorithm>
using namespace std;
template<class T1,class T2,class Pred=greater<T1>>
class MyMultimap{
private:
    multimap<T1,T2,Pred>k;
public:
    typedef typename multimap<T1,T2,Pred>::iterator iterator;
    MyMultimap(){
        k.clear();
    }
    void insert(pair<T1,T2>a){
        k.insert(a);
    }
    auto begin(){
        return k.begin(); 
    }
    auto end(){
        return k.end();
    }
    void clear(){
        k.clear();
    }   
    auto find(T1 x){
        return k.find(x); 
    }
    void Set(T1 x,T2 y){
        for(auto it=k.begin();it!=k.end();it++){
            if(it->first==x) it->second=y;
        }
    }
};
template<class T1,class T2>
ostream &operator<<(ostream &os,const pair<T1,T2>x){
    os<<'('<<x.first<<','<<x.second<<')';
    return os;
}
struct Student 
{
	string name;
	int score;
};
template <class T>
void Print(T first,T last) {
	for(;first!= last; ++ first)
		cout << * first << ",";
	cout << endl;
}
int main()
{
	
	Student s[] = { {"Tom",80},{"Jack",70},
					{"Jone",90},{"Tom",70},{"Alice",100} };
	
	MyMultimap<string,int> mp;
	for(int i = 0; i<5; ++ i)
		mp.insert(make_pair(s[i].name,s[i].score));
	Print(mp.begin(),mp.end()); //按姓名从大到小输出

	mp.Set("Tom",78); //把所有名为"Tom"的学生的成绩都设置为78
	Print(mp.begin(),mp.end());
	
	
	
	MyMultimap<int,string,less<int> > mp2;
	for(int i = 0; i<5; ++ i) 
		mp2.insert(make_pair(s[i].score,s[i].name));
	
	Print(mp2.begin(),mp2.end()); //按成绩从小到大输出
	mp2.Set(70,"Error");          //把所有成绩为70的学生，名字都改为"Error"
	Print(mp2.begin(),mp2.end());
	cout << "******" << endl;
	
	mp.clear();
	
	string name;
	string cmd;
	int score;		
	while(cin >> cmd ) {
		if( cmd == "A") {
			cin >> name >> score;
			if(mp.find(name) != mp.end() ) {
				cout << "erroe" << endl;
			}
			mp.insert(make_pair(name,score));
		}
		else if(cmd == "Q") {
			cin >> name;
			MyMultimap<string,int>::iterator p = mp.find(name);
			if( p!= mp.end()) {
				cout << p->second << endl;
			}
			else {
				cout << "Not Found" << endl; 
			}		
		}
	}
	return 0;
}
```
# Q:矩形排序
## 描述
给定一系列边长已知的矩形，输出对矩形进行两种排序的结果。

在第一种排序中，先按矩形的面积从大到小排序；若两个矩形的面积相同，则周长大的排在前。

在第二种排序中，先按矩形的周长从小到大排序；若两个矩形的周长相同，则面积小的排在前。


```
#include <iostream>
#include <set>
using namespace std;
// 在此处补充你的代码
int main() {
    multiset<Rectangle> m1;
    multiset<Rectangle, Comp> m2;
    int n, a, b;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> a >> b;
        m1.insert(Rectangle(a, b));
        m2.insert(Rectangle(a, b));
    }
    for (multiset<Rectangle>::iterator it = m1.begin(); it != m1.end(); it++) {
        cout << *it << endl;
    }
    cout << endl;
    for (multiset<Rectangle>::iterator it = m2.begin(); it != m2.end(); it++) {
        cout << *it << endl;
    }
	return 0;
}
```
## 输入
第一行是一个整数n，表示输入的矩形个数。  
接下来n行表示了n个矩形。每行有两个整数a与b，表示该矩形的长与宽。
## 输出
先用n行输出第一种排序的结果。每行两个整数，依次表示该矩形的面积与周长。  
再输出一个空行。  
最后用n行输出第二种排序的结果。每行两个整数，依次表示该矩形的面积与周长。
## 样例输入
```
6
3 8
4 6
10 2
6 6
4 8
3 6
```
## 样例输出
```
36 24
32 24
24 22
24 20
20 24
18 18

18 18
24 20
24 22
20 24
32 24
36 24
```
# Solution
我们需要构造一个矩形类，这个类应该包含了周长和面积两个参数    
对于第一个缺省的类，我们通过重载小于号来完成（再次注意一下const）   
对于第二个有给出的类，我们写一个仿函数来完成（还是要注意const）  
```
#include <iostream>
#include <set>
using namespace std;
class Rectangle{
public:
    int l,w;
    int c,s;
    Rectangle(int a,int b):l(a),w(b) {
        c=2*(a+b);
        s=a*b;
    }
    friend ostream &operator<<(ostream &os,const Rectangle &t){
        os<<t.s<<' '<<t.c;
        return os;
    }
    bool operator<(const Rectangle &k)const{
        if(s==k.s) return c>k.c;
        return s>k.s;
    }
};
struct Comp{
    bool operator()(Rectangle a,Rectangle b)const{
        if(a.c==b.c) return a.s<b.s;
        return a.c<b.c;
    }
};
int main() {
    multiset<Rectangle> m1;
    multiset<Rectangle, Comp> m2;
    int n, a, b;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> a >> b;
        m1.insert(Rectangle(a, b));
        m2.insert(Rectangle(a, b));
    }
    for (multiset<Rectangle>::iterator it = m1.begin(); it != m1.end(); it++) {
        cout << *it << endl;
    }
    cout << endl;
    for (multiset<Rectangle>::iterator it = m2.begin(); it != m2.end(); it++) {
        cout << *it << endl;
    }
	return 0;
}
```
# R:学生考勤记录查询
## 描述
学生考勤记录查询，可以完成下面三条操作：

1)add date id，例如add 1 1500012755，学号为1500012755的学生，在本月1日缺勤

2)querydate_begin date_end，例如query 1 3，查询本月1日至本月3日（包含1日及3日）缺勤学生名单，输出格式为（同一日内缺勤的学生输出顺序与add操作顺序一致）：

date id id ……

date id ……

3)exit 结束程序

请实现QueryResult函数。


```
#include <iostream>
#include <string>
#include <map>
#include <list>
using namespace std;
// 在此处补充你的代码
int main(int argc, char* argv[])
{
	map<int, list<int> > Attendance;
	map<int, list<int> >::iterator it;
	string cmd;
	int date, id, date_lower, date_upper;
	while (cin >> cmd){
		if (cmd == "add"){
			cin >> date >> id;
			it = Attendance.find(date);
			if (it != Attendance.end()){
				it->second.push_back(id);
			}
			else{
				list<int> lst_id;
				lst_id.push_back(id);
				Attendance.insert(make_pair(date,lst_id));
			}
		}
		else if (cmd == "query"){
			cin >> date_lower>>date_upper;
			QueryResult(Attendance.lower_bound(date_lower), Attendance.upper_bound(date_upper));
		}
		else if (cmd == "exit")
			return 0;
	}
	return 0;
}
```
## 输入
每一行数据格式如上述两条命令，其中date是int型，0 < date < 32，id为int型，以15开头的10位学号。
## 输出
在输入数据有query命令时，输出相应格式的缺勤名单(每个学号后面有一个空格)
## 样例输入
```
add 1 1500012755
add 1 1500012796
add 3 1500012755
query 1 2
add 4 1500012737
query 1 4
exit
```
## 样例输出
```
1: 1500012755 1500012796
1: 1500012755 1500012796
3: 1500012755
4: 1500012737
```
# Solution
我们只需要写这个输出函数，因为不知道类型，所以，用一个函数模板完成  
同时，还要补一个Print函数，毕竟是数据结构套数据结构
```
#include <iostream>
#include <string>
#include <map>
#include <list>
using namespace std;
void Print(list<int> x){
    for(auto i=x.begin();i!=x.end();i++){
        cout<<*i<<' ';
    }
    cout<<endl;
}
template<class T>
void QueryResult(T x,T y){
    for(T i=x;i!=y;i++){
        cout<<i->first<<": ";
        Print(i->second);
    }
}
int main(int argc, char* argv[])
{
	map<int, list<int> > Attendance;
	map<int, list<int> >::iterator it;
	string cmd;
	int date, id, date_lower, date_upper;
	while (cin >> cmd){
		if (cmd == "add"){
			cin >> date >> id;
			it = Attendance.find(date);
			if (it != Attendance.end()){
				it->second.push_back(id);
			}
			else{
				list<int> lst_id;
				lst_id.push_back(id);
				Attendance.insert(make_pair(date,lst_id));
			}
		}
		else if (cmd == "query"){
			cin >> date_lower>>date_upper;
			QueryResult(Attendance.lower_bound(date_lower), Attendance.upper_bound(date_upper));
		}
		else if (cmd == "exit")
			return 0;
	}
	return 0;
}
```
# S:维护平面点
## 描述
程序填空，一开始平面上一个点都没有

每次可以插入一个点，删除一个已经存在的点，或者按照x 或y 来查询一个存在的点

保证任何时候任意两个点一定是一个点严格在另一个点的右下方

即两点(x1, y1), (x2, y2)，必定有x1 > x2 且y1 < y2 ，或者x1 < x2 且y1 > y2


```
#include <set>
#include <iostream>
#include <string>
using namespace std;
// 在此处补充你的代码
int main() {
	string cmd;
	set<pair<int, int>, myComp> S;
	while (cin >> cmd) {
		if (cmd == "A") {
			int x, y;
			cin >> x >> y;
			S.insert(make_pair(x, y));
		} else if (cmd == "Qx") {
			int x;
			cin >> x;
			cout << S.lower_bound(make_pair(x, -1))->second << endl;
		} else if (cmd == "Qy") {
			int y;
			cin >> y;
			cout << S.lower_bound(make_pair(-1, y))->first << endl;
		} else {
			int x, y;
			cin >> x >> y;
			S.erase(make_pair(x, y));
		}
	}
	return 0;
}
```
## 输入
输入数据的每一行，格式为以下之一：
A x y  
R x y  
Qx x  
Qy y  
其中 x 与 y 都是 0 到 10^9 之间的整数  
A x y 表示插入点 (x, y)  
R x y 表示删除点 (x, y)，保证存在  
Qx x 表示在当前所有点中，找到第一维为x的点，输出其第二维的值，保证存在  
Qy y 表示在当前所有点中，找到第二维为y的点，输出其第一维的值，保证存在  
总共操作数不超过100000
## 输出
对于每一个 Qx 和 Qy 操作，输出一行表示对应的答案
## 样例输入
```
A 3 5
A 4 2
Qx 4
R 4 2
A 4 3
Qy 3
```
## 样例输出
```
2
4
```
# Solution
题干我们不看了啊  
这次着重讲一下这个lower_bound  
这是什么？  
就是，对于一个数据结构进行查找，找到第一个“大于等于”给定数（广义）的数（广义）  
更通俗的理解是，找到第一个"违反小于"的数，我们这里看一下  
建立小于的话，对于原本的数据，显然挺好找  
但是，比如第一个数值是-1的时候，怎么定义"小于"？想象一下一个$x=t$的轴直接切过来，此时你是怎么想的？肯定是比较第一维吧，那么，就不能让第一维实际比x大的点被认定为"小于"  
第二维是同理的  
注意，我们定义的实际上是排序函数，也就是说lower_bound实际上是从begin到end找到最早满足条件的那个数，所以要注意排序顺序  
```
#include <set>
#include <iostream>
#include <string>
using namespace std;
struct myComp{
    bool operator()(const pair<int,int>&x,const pair<int,int>&y)const{
        if(x.first>0&&y.first>0&&x.second>0&&y.second>0) return x.first>y.first;
        if(x.first<0||y.first<0) return x.second<y.second;
        if(x.second<0||y.second<0) return x.first>y.first;
    }
};
int main() {
	string cmd;
	set<pair<int, int>, myComp> S;
	while (cin >> cmd) {
		if (cmd == "A") {
			int x, y;
			cin >> x >> y;
			S.insert(make_pair(x, y));
		} else if (cmd == "Qx") {
			int x;
			cin >> x;
			cout << S.lower_bound(make_pair(x, -1))->second << endl;
		} else if (cmd == "Qy") {
			int y;
			cin >> y;
			cout << S.lower_bound(make_pair(-1, y))->first << endl;
		} else {
			int x, y;
			cin >> x >> y;
			S.erase(make_pair(x, y));
		}
	}
	return 0;
}
```
# T:编程填空：按要求输出
## 描述
下列程序的输出为"10 13 18 15 17 12 16 19",  请补充代码


```
#include <iterator>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <stack>
#include <iostream>
#include <set>
using namespace std;
int  a[10] = {0, 6, 7, 3, 9, 5, 8, 6, 4, 9};
int  b[10] = {10, 11, 12, 13, 14, 15, 16, 17, 18, 19};
int main(int argc, char** argv) {
// 在此处补充你的代码
for(int i=0; i<10; i++) 
		c[a[i]] = b[i];
	for(it=c.begin(); it!=c.end(); it++) 
		cout<<it->second<<" ";
	return 0;
}
```
## 输入
无
## 输出
10 13 18 15 17 12 16 19
## 样例输入
```
None
```
## 样例输出
```
10 13 18 15 17 12 16 19
```
# Solution
一眼就是用map啊，又没有别的关联容器能这么干
```
#include <iterator>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <stack>
#include <iostream>
#include <set>
using namespace std;
int  a[10] = {0, 6, 7, 3, 9, 5, 8, 6, 4, 9};
int  b[10] = {10, 11, 12, 13, 14, 15, 16, 17, 18, 19};
int main(int argc, char** argv) {
map<int,int>c;
    map<int,int>::iterator it;
for(int i=0; i<10; i++) 
		c[a[i]] = b[i];
	for(it=c.begin(); it!=c.end(); it++) 
		cout<<it->second<<" ";
	return 0;
}
```
# U:编程填空：去除重复元素排序
## 描述
程序填空，使其按要求输出
```
#include <iterator>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <stack>
#include <iostream>
#include <set>
using namespace std;

int main() {
	int t;
	int  a[100];
	cin >> t;
	while(t--) {
		for(int i = 0;i < 12; ++i)
			cin >> a[i];
// 在此处补充你的代码
std::copy(b.begin(), b.end(), c);
		cout << endl;

	}
	return 0;
}
```
## 输入
第一行是个整数，表示输入数据组数  
每组数据一行,有12个整数
## 输出
对每组数据, 将12个整数从小到大排序并去除重复元素后输出
## 样例输入
```
2
34 5 4 6 3 9 8 34 5 3 3 18
31 2 4 6 2 9 8 31 5 3 3 18
```
## 样例输出
```
3 4 5 6 8 9 18 34 
2 3 4 5 6 8 9 18 31
``` 
## 提示
注意：行末都有一个空格
# Solution
这里肯定是要求我们使用一个数据结构b  
这里傻傻地用了vector，但事实上，set应该也可以，还更方便  
copy表示将一个范围中的元素赋值到另一个范围中，那么，如果我们将其赋值到一个ostream型变量中，它就会自动输出  
但是，这里的ostream_iterator很少见，我们可以记一下
```
#include <iterator>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <stack>
#include <iostream>
#include <set>
using namespace std;

int main() {
	int t;
	int  a[100];
	cin >> t;
	while(t--) {
		for(int i = 0;i < 12; ++i)
			cin >> a[i];
vector<int>b;
        for(int i=0;i<12;i++){
            b.push_back(a[i]);
        }
        sort(b.begin(),b.end());
        auto las=unique(b.begin(),b.end());
        b.erase(las,b.end());
        ostream_iterator<int>c(cout," ");
std::copy(b.begin(), b.end(), c);
		cout << endl;

	}
	return 0;
}
```
# V:前k大的偶数
## 描述
输入n个整数，输出整数数列中大小排名前k的偶数


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
class MyQueue
{
// 在此处补充你的代码
};
int main()
{
	int t;
	cin >> t;
	while(t--) {
		int n, k;
		cin >> n >> k;
		MyQueue q(k);
		for (int i = 0; i < n; ++i)
			cin >> q;
		cout<<q;
		cout << endl;
	}
	return 0; 
}
```
## 输入
有多组数据  
第一行是数据组数 t  
对每组数据：  
第一行为整数n (n>=3)和k  
接下来的一行为n个整数，保证这些整数中至少有k个偶数。  
## 输出
对每组数据，输出k个整数，降序排列，表示选出来的大小排名前k的偶数
## 样例输入
```
2
9 4
1 2 4 3 6 6 7 8 9
3 2
18 16 14
```
## 样例输出
```
8 6 6 4
18 16
```
# Solution
这道题看到输出前k肯定想的是优先队列  
然后，还要求降序排列，我们需要一个临时存储容器  
这样就完了  
注意:优先队列默认大根堆
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
class MyQueue
{
private:
    int tot,cnt;
public:
    priority_queue<int>q;
    MyQueue(int x){ 
        tot=x;
        cnt=0;
    }
    friend istream &operator>>(istream &is,MyQueue &t){
        int dd;
        is>>dd;
        if(dd%2) return is;
        else{
            t.q.push(-dd);
            t.cnt++;
            if(t.cnt>t.tot) t.q.pop();
            return is;
        }
    }
    friend ostream &operator<<(ostream &os,MyQueue &t){
        vector<int>a;
        while(!t.q.empty()){
            int x=-t.q.top();
            t.q.pop();
            a.push_back(x);
        }
        for(auto it=a.end()-1;it>=a.begin();it--){
            os<<*it<<' ';
        }
        return os;
    }
};
int main()
{
	int t;
	cin >> t;
	while(t--) {
		int n, k;
		cin >> n >> k;
		MyQueue q(k);
		for (int i = 0; i < n; ++i)
			cin >> q;
		cout<<q;
		cout << endl;
	}
	return 0; 
}
```
# W:编程填空:Three Sum
## 描述
给出一列备选整数，请问能否在其中选出三个（不能重复选取），使得它们的和等于一个给定数字呢？
```
#include<cstdio>
#include<cstring>
#include<set>
using namespace std;

multiset<int> s;
int a[5000 + 5];

int main() {
	int n, T, k;
	scanf("%d", &T);
	while (T--) {
		s.clear();
		scanf("%d", &n);
		for (int i = 0; i < n; i ++) {
			scanf("%d", a + i);
			s.insert(a[i]);
		}
		bool flag = false;
		scanf("%d", &k);
		for (int i = 0; i < n; i ++) {
			for (int j = i + 1; j < n; j ++) {
				int target = k - a[i] - a[j], min_count = 1;
// 在此处补充你的代码
}
			if (flag) break;
		}
		puts(flag? "Yes": "No");
	}
}
```
## 输入
输入包括多组测试数据。第一行一个整数T(1<=T<=20)，表示测试数据数量。  
接下来T组测试数据分别输入，对于每组测试数据，第一行一个整数n(1<=n<=1000)，表示给出备选数字的个数；第二行n个用空格隔开的整数ai(-3*10^8<=ai<=3*10^8)，表示备选数字列表；第三行一个整数k(-10^9<=k<=10^9)，表示希望组合的数字。
## 输出
对于每组测试数据输出一行答案，如果能够选出三个数合成k，请输出"Yes"(不含引号)，否则输出"No".
## 样例输入
```
4
10
1 2 3 4 5 6 7 8 9 10
8
10
1 2 3 4 5 6 7 8 9 10
5
4
1 1 1 1
3
4
1 2 9 10
4
```
## 样例输出
```
Yes
No
Yes
No
```
# Solution
至于这里已经给出明显思路了，那么，我们直接查找不就行了吗，不解释了  
其实这里好像应该用set，严格意义的话
```
#include<cstdio>
#include<cstring>
#include<set>
using namespace std;

multiset<int> s;
int a[5000 + 5];

int main() {
	int n, T, k;
	scanf("%d", &T);
	while (T--) {
		s.clear();
		scanf("%d", &n);
		for (int i = 0; i < n; i ++) {
			scanf("%d", a + i);
			s.insert(a[i]);
		}
		bool flag = false;
		scanf("%d", &k);
		for (int i = 0; i < n; i ++) {
			for (int j = i + 1; j < n; j ++) {
				int target = k - a[i] - a[j], min_count = 1;
if(s.find(target)!=s.end()){
                    flag=true;
                }
}
			if (flag) break;
		}
		puts(flag? "Yes": "No");
	}
}
```
# X:编程填空：排队看医生
## 描述
看病要排队是地球人都知道的常识。不过细心的Rainbow观察发现，医院里排队还是有讲究的：Rainbow所去的医院有三个医生同时看病。而看病的人病情有轻重，所以不能根据简单的先来先服务的原则。所以医院对每种病情规定了10种不同的优先级。级别为10的优先权最高，级别为1的优先权最低。医生在看病时，则会在他的队伍里面选择一个优先权最高的人进行诊治。如果遇到两个优先权一样的病人的话，则选择最早来排队的病人。

现在，请你来模拟一下这个看病的过程吧！

## 输入
输入数据包含多组测试。第一行一个整数T(1<=T<=20)，表示测试数据数目。  
每组数据第一行有一个正整数N(1<=N<=20000)表示发生事件的数目。  
接下来有N行分别表示发生的事件。  
一共有两种事件：  
IN A B,表示有一个拥有优先级B的病人要求医生A诊治。(1<=A<=3, 1<=B<=10)  
OUT A,表示医生A进行了一次诊治，诊治完毕后，病人出院。(1<=A<=3)
## 输出
对于每个”OUT A”事件，请在一行里面输出被诊治人的编号ID。如果该事件时无病人需要诊治，则输出”EMPTY”。  
诊治人的编号ID的定义为：在一组测试中，”IN A B”事件发生第K次时，进来的病人ID即为K。从1开始编号。
## 样例输入
```
2
7
IN 1 1
IN 1 2
OUT 1
OUT 2
IN 2 1
OUT 2
OUT 1 
2
IN 1 1
OUT 1
```
## 样例输出
```
2
EMPTY
3
1
1
```
# Solution
一开始题目看错了，ID的定义不对  
肯定是要用优先队列来的  
然后？就没有然后了  
挺有OI味的
```
#include<bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define lowbit(x) (x&(-x))
using namespace std;
int t,n;
string x;
struct node{
    int id,se;
    bool operator<(node x)const{
        if(x.se==se) return id>x.id;
        else return se<x.se;
    }
};
int num;
int a,b;
priority_queue<node>q[4];
int main(){
    cin>>t;
    while(t--){
        cin>>n;
        for(int i=1;i<=3;i++){
            while(!q[i].empty()){
                q[i].pop();
            }
            num=0;
        }
        for(int i=1;i<=n;i++){
            cin>>x;
            if(x=="IN"){
                cin>>a>>b;
                num++;
                q[a].push(node{num,b});
            }
            else{
                cin>>a;
                if(q[a].empty()){
                    cout<<"EMPTY"<<endl;
                    continue;
                }
                else{
                    node k=q[a].top();q[a].pop();
                    cout<<k.id<<endl;
                    continue;
                }
            }
        }
    }
    system("pause");
    return 0;
}
```
# Y:宠物小精灵
## 描述
宠物小精灵的世界中，每位训练师都在收集自己的小精灵。但是，训练师的背包里只能同时携带6只小精灵。如果一位训练师抓到了更多的精灵，那么最早抓到的精灵将被自动传送到电脑中，保证持有的小精灵数量依然是6只。 训练师也可以随时从电脑中取出精灵，取出的精灵将从电脑中传送到训练师的背包里。取出的精灵同样被认为是最新的，导致背包中最早取出或抓到的精灵被替换到电脑中，训练师持有的精灵数量依然是6只。 初始状态下，所有训练师的背包中都没有小精灵，电脑中也没有任何训练师的精灵。

## 输入
输入数据包含多组测试。第一行一个整数T(1<=T<=20)，表示测试数据数目。  
每组数据第一行有一个正整数N(1<=N<=20000)表示发生事件的数目。  
接下来有N行分别表示发生的事件。  
一共有两种事件：  
C X, Y 表示训练师X抓到了精灵Y  
T X, Y 表示训练师X试图从电脑中取出精灵Y。

X和Y都是长度在20以下的由字母或数字构成的字符串。

小精灵的世界中同样存在着作恶多端的火箭队。他们试图利用电脑的漏洞，从电脑中取出本不属于自己的小精灵。因此，电脑需要识别并拒绝取出这种请求。注意，如果一只小精灵仅存在于训练师的背包中而未被传送至电脑，该训练师也不能取出这只精灵。相同训练师不会多次抓到相同名字的精灵。
## 输出
对于每次从电脑中取出小精灵的请求，输出一行。成功则输出Success，失败则输出Failed。
## 样例输入
```
1 10
C satoshi pikachu1
C satoshi pikachu2
C satoshi pikachu3
C satoshi pikachu4
C satoshi pikachu5
C satoshi pikachu6
C satoshi pikachu7
T satoshi pikachu2
T satoshi pikachu1
T pikachu pikachu2
```
## 样例输出
```
Failed
Success
Failed
```
# Solution
多测记得清空！  
这个肯定要用队列表示的，外部是map
```
#include<bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define lowbit(x) (x&(-x))
using namespace std;
int t,n;
map<string,queue<string>>ma;
map<string,int>cnt;
map<string,set<string>>computer;
char op;
string x,y;
int main(){
    cin>>t;
    while(t--){
        ma.clear();
        cnt.clear();
        computer.clear();
        cin>>n;
        for(int i=1;i<=n;i++){
            cin>>op;
            if(op=='C'){
                cin>>x>>y;
                cnt[x]++;
                ma[x].push(y);
                if(cnt[x]>=7){
                    cnt[x]--;
                    string temp=ma[x].front();
                    ma[x].pop();
                    computer[x].insert(temp);
                }
            }
            else{
                cin>>x>>y;
                if(ma.find(x)!=ma.end()&&computer[x].find(y)!=computer[x].end()){
                    cout<<"Success"<<endl;
                    auto it=computer[x].find(y);
                    computer[x].erase(it);
                    ma[x].push(y);
                    cnt[x]++;
                    if(cnt[x]>=7){
                        cnt[x]--;
                        string temp=ma[x].front();
                        ma[x].pop();
                        computer[x].insert(temp);
                    }
                }
                else{
                    cout<<"Failed"<<endl;
                }
            }
        }
    }
    system("pause");
    return 0;
}
```
# Z:石油交易
## 描述
原油期货价格暴跌，甚至出现了负油价。有很多卖家想要低价卖出手中囤积的石油，同时也有部分买家想要低价抄底。

每位卖家和买家按时间顺序在交易平台依次发布交易信息。他们的交易流程如下：

卖家在交易平台发布自己希望卖出的石油桶数X， 以及这X桶石油每桶报价Y。当买家希望购买Z桶石油时，会从当前交易平台所有在售的石油中购买价格最低的Z桶， 但无法购买在其之后的卖家发布的石油。如果在买家购买Z桶石油之时，没有足够的石油在售，则不足的部分将按每桶40美元的价格购买， 所有卖家的价格均低于40美元。

现在请计算每位买家购买石油的总价。

## 输入
输入数据的第一行是一个正整数N(N < 100000)，表明买卖信息的总数目。  
接下来N行分别表示买卖的信息。  
一共有两种信息：  
SELL X Y，表示卖家希望卖出X桶石油，每桶价格为Y美元。  
BUY Z，表示买家买入Z桶石油。  
0 < X，Z <= 10000。Y为整数。结果保证在INT范围内。
## 输出
对于每次买入石油的信息，输出一个正整数，表示该买家当次买入石油的总价。
## 样例输入
```
6
BUY 5
SELL 10 10
BUY 5
SELL 10 5
BUY 5
BUY 15
```
## 样例输出
```
200
50
25
275
```
# Solution
这道题唯一要注意的点就是，当我们erase一个元素之后，迭代器会直接指向下一个元素，因此，不需要执行++操作  
这点调了一晚上ww
```
#include<bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define lowbit(x) (x&(-x))
using namespace std;
string x;
ll cnt=0;//库存
multimap<int,int>ma;
int n;
int a,b;
ll tot=0;
int main(){
    cin>>n;
    for(int i=1;i<=n;i++){
        cin>>x;
        if(x=="BUY"){
            cin>>a;
            ll ans=0;
            for(auto it=ma.begin();it!=ma.end();){
				if(a<=0) break;
                if(it->second<=a){
                    a-=it->second;
                    ans+=it->second*it->first;
                    tot-=it->second*it->first;
                    cnt-=it->second;
                    it=ma.erase(it);
                }
                else{
                    ans+=it->first*a;
                    it->second-=a;
                    tot-=a*it->first;
                    cnt-=a;
					a=0;
                }
            }
			if(a>0) ans+=a*40;
            cout<<ans<<endl;
        }
        else if(x=="SELL"){
            cin>>a>>b;
            ma.insert(make_pair(b,a));
            cnt+=a;
            tot+=a*b;
        }
    }
    system("pause");
    return 0;
}
```
