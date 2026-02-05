---
title: 从零开始的上机(5)
date: 2025-04-13
categories:
    - 程序设计实习
---
本次上机涉及内容：类与对象、运算符重载、继承、多态
## Hero和Priest
### 描述
根据输出完善程序。

```cpp
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

### 输入

```
None
```

### 输出

```
Hero::defense()
Hero::attack()
Priest::defense()
Priest::attack()
Priest::defense()
```

### Solution


## 统计动物数量
### 描述
根据输出完善程序。

```cpp
#include <iostream>
using namespace std;
// 在此处补充你的代码
void print() {
	cout << Animal::number << " animals in the zoo, " << Dog::number << " of them are dogs, " << Cat::number << " of them are cats" << endl;
}

int main() {
	print();
	Dog d1, d2;
	Cat c1;
	print();
	Dog* d3 = new Dog();
	Animal* c2 = new Cat;
	Cat* c3 = new Cat;
	print();
	delete c3;
	delete c2;
	delete d3;
	print();
}
```
## 输入
```
无
```
## 输出
```
0 animals in the zoo, 0 of them are dogs, 0 of them are cats
3 animals in the zoo, 2 of them are dogs, 1 of them are cats
6 animals in the zoo, 3 of them are dogs, 3 of them are cats
3 animals in the zoo, 2 of them are dogs, 1 of them are cats
```
### Solution
有一点要注意，因为太久没写忘了  
就是基类的析构函数要写成虚函数形式，这样，在delete派生类对象的时候才会先执行派生类析构函数，再执行基类的析构函数，消得干净  
这里我们都会写 但是通过C++的报错可以得知一个点  
print函数中引用的Animal::number这个东西，它是引用的Animal类（划重点）的number成员变量  
这个时候就必须写成静态形式，因为如果不写成的话，编译器不知道你调用的是哪个Animal类对象的成员变量  
这个也是因为太久没写忘了  
下面看代码:
```cpp
#include <iostream>
using namespace std;
class Animal{
public:
    static int number;
	Animal(){
		number+=1;
	}
	virtual ~Animal(){
		number--;
	}
};
class Dog:public Animal{
public:
	static int number;
	Dog(){
		number+=1;
	}
	~Dog(){
		number--;
	}
};
class Cat:public Animal{
public:
	static int number;
	Cat(){
		number+=1;
	}
	~Cat(){
		number--;
	}
};
int Animal::number=0;
int Dog::number=0;
int Cat::number=0;
// 在此处补充你的代码
void print() {
	cout << Animal::number << " animals in the zoo, " << Dog::number << " of them are dogs, " << Cat::number << " of them are cats" << endl;
}

int main() {
	print();
	Dog d1, d2;
	Cat c1;
	print();
	Dog* d3 = new Dog();
	Animal* c2 = new Cat;
	Cat* c3 = new Cat;
	print();
	delete c3;
	delete c2;
	delete d3;
	system("pause");
	print();
}
```

## 还是Fun和Do
### 描述
根据输出完善代码

```cpp
#include <iostream> 
using namespace std;

class A { 
	public: 
		virtual void Fun() { 
			cout << "A::Fun" << endl; 
		}; 
		virtual void Do() { 
			cout << "A::Do" << endl; 
		} 
};
// 在此处补充你的代码
{ 
	p.Fun(); 
	p.Do(); 
} 

void Call2(B p) {
	p.Fun();
	p.Do();
}



int main() { 
	C c;
	B b;
	Call1(b);
	Call1(c); 
	Call2(c);
	return 0;
}
```

### 输入

```
None
```

### 输出

```
A::Fun
B::Do
C::Fun
C::Do
A::Fun
B::Do
```

### Solution

## 多态
### 描述
根据输出完善代码。
```cpp
#include <iostream>
using namespace std;

class Base {
public:
   virtual Base& fun() { cout << "base fun" << endl; return *this; }
   virtual Base& foo() { cout << "base foo" << endl; return *this; }
};

class Derived: public Base {
public:
   Base& fun() { cout << "derived fun" << endl; return *this; }
   Base& foo() { cout << "derived foo" << endl; return *this; }
};

Base& foo();
Base& fun();
// 在此处补充你的代码
int main() {
   foo().fun().foo();
   fun().foo().fun();
   return 0;
}
```
### 输入
```
None
```
### 输出
```
derived foo
derived fun
derived foo
base fun
base foo
base fun
```
### Solution
这道题花的时间最长   
估计是因为函数的写了不调用形式没怎么见到（以及python写太久了，C++有所淡忘）  
就是那个Base& foo();  
这个表示这是个函数 但是啥都没声明  
所以，题目就是需要我们声明一下两个函数是什么  
然后呢？我们看一下这个函数的返回值类型  
当时就是因为没注意到这个，所以好长时间没做出来  
我们以第二个函数fun为例  
它声明一个Base类对象b 首先，为什么要静态？  
因为这个静态对象只能创建一次，并且在函数结束后不会被销毁  
然后return b.fun();  
这句的意思是执行一次b的fun（Base类）函数，再返回一个b对象的拷贝  
而Derived类和Base类中的foo/fun成员函数同理  
所以才会输出三次一样的  
下面看代码:
```cpp
#include <iostream>
using namespace std;

class Base {
public:
   virtual Base& fun() { cout << "base fun" << endl; return *this; }
   virtual Base& foo() { cout << "base foo" << endl; return *this; }
};

class Derived: public Base {
public:
   Base& fun() { cout << "derived fun" << endl; return *this; }
   Base& foo() { cout << "derived foo" << endl; return *this; }
};

Base& foo();
Base& fun();
Base& foo(){
   static Derived d;
   return d.foo();
}
Base& fun(){
   static Base b;
   return b.fun();
}
// 在此处补充你的代码
int main() {
   foo().fun().foo();
   fun().foo().fun();
   system("pause");
   return 0;
}
```

## 变来变去的数
### 描述
根据输出完善代码。
```cpp
#include <iostream>
using namespace std;

class myobject {
public:
// 在此处补充你的代码
};

class producer : public myobject {
public:
	virtual void work() {
		counter = counter + 5;
		print_avaliable();
	}
};

int myobject::counter = 0;

int main(){
	producer *pro = new producer();
	myobject *con = new myobject();
	pro->work(); pro->work(); cout << endl;
	con->work(); con->work(); con->work(); cout << endl;
	pro->work(); cout << endl;
	con->work(); con->work(); cout << endl;
}
```
### 输入
```
None
```
### 输出
```
5 10
6 2 2
7
3 3
```
### Solution
这里其实没有啥要看清的  
就是抖机灵 在A的函数里写上counter大于等于4就减一这种解法  
- ### 笔者注:此题后得知可不用特判解出，本解法仅供参考
下面看代码：
```cpp
#include <iostream>
using namespace std;

class myobject {
public:
    static int counter;
    void work(){
        if(counter>=4) counter-=4;
        cout<<counter<<' ';
    }
    void print_avaliable(){
        cout<<counter<<' ';
    }
// 在此处补充你的代码
};

class producer : public myobject {
public:
	virtual void work() {
		counter = counter + 5;
		print_avaliable();
	}
};

int myobject::counter = 0;

int main(){
	producer *pro = new producer();
	myobject *con = new myobject();
	pro->work(); pro->work(); cout << endl;
	con->work(); con->work(); con->work(); cout << endl;
	pro->work(); cout << endl;
	con->work(); con->work(); cout << endl;
    system("pause");
    return 0;
}
```
## MyClass
### 描述
根据输出完善代码。
```cpp
#include <iostream>
using namespace std;
class CMyClassA {
	int val;
public:
	CMyClassA(int);
	void virtual print();
};
CMyClassA::CMyClassA(int arg) {
	val = arg;
	printf("A:%d\n", val);
}
void CMyClassA::print() {
	printf("%d\n", val);
	return;
}
// 在此处补充你的代码
int main(int argc, char** argv) {
	CMyClassA a(3), *ptr;
	CMyClassB b(5);
	ptr = &a; ptr->print();
	a = b;
	a.print();
	ptr = &b; ptr->print();
	return 0;
}
```
### 输入
```
None
```

### 输出
```
A:3
A:15
B:5
3
15
5
```
### Solution
别的不说，就说一个  
这里的派生类的构造函数如何调用基类构造函数？  
做的时候忘记了  
下面看代码:
```cpp
#include <iostream>
using namespace std;
class CMyClassA {
	int val;
public:
	CMyClassA(int);
	void virtual print();
};
CMyClassA::CMyClassA(int arg) {
	val = arg;
	printf("A:%d\n", val);
}
void CMyClassA::print() {
	printf("%d\n", val);
	return;
}
class CMyClassB:public CMyClassA{
public:
    int val;
    CMyClassB(int x):CMyClassA(3*x){
        val=x;
        printf("B:%d\n",val);
    }
    void print(){
        printf("%d\n",val);
    }
};
// 在此处补充你的代码
int main(int argc, char** argv) {
	CMyClassA a(3), *ptr;
	CMyClassB b(5);
	ptr = &a; ptr->print();
	a = b;
	a.print();
	ptr = &b; ptr->print();
    system("pause");
	return 0;
}
```

## 输出指定结果二
### 描述
根据输出完善程序

```cpp
#include <iostream>
#include <map>
using namespace std;
// 在此处补充你的代码
int A::count = 0;
void func(B b) {  }
int main()
{
	A a1(5),a2;
	cout << A::count << endl;
	B b1(4);
	cout << A::count << endl;
	func(b1);
	cout << A::count << endl;
	A * pa = new B(4);
	cout << A::count << endl;
	delete pa;
	cout << A::count << endl;
	return 0;
}
```

### 输入

```
None
```

### 输出

```
2
3
B::destructor
A::destructor
3
4
B::destructor
A::destructor
3
B::destructor
A::destructor
A::destructor
A::destructor
```

### Solution


## 构造与析构
### 描述
根据输出完善程序。

```cpp
#include<cstdio>
#include<iostream>
#include<algorithm>
#include<cstring>
using namespace std;
// 在此处补充你的代码
int main(){
	int n;
	cin >> n;
	for (int i = 1; i<=n; i++) {
		int x;
		cin >> x;
		if (x == 0) {
			A *a = new A();
			delete a;
		}else {
			A *a = new B();
			delete a;
		}
	}
	return 0;	
}
```

### 输入

```
3
1 0 1
```

### 输出

```
New A
New B
Delete B
Delete A
New A 
Delete A
New A
New B
Delete B
Delete A
```

### Solution


## 卖肉付牛肉
### 描述
根据输出完善程序。

```cpp
#include<bits/stdc++.h>
using namespace std;

class Food {
public:
// 在此处补充你的代码
};

class Meat : public Food {
public:
	void Buy() { cout << "Buy Meat" << endl; }
	virtual void Pay() { cout << "Pay Meat" << endl; }
};

class Beef : public Meat {
public:
	void Buy() { cout << "Buy Beef" << endl; }
	void Pay() { cout << "Pay Beef" << endl; }
};
int main() {
	Beef bf;
	Meat* pmt = &bf;
	Food* pfd = &bf;

	pfd->Buy();
	pfd->Pay();
	pmt->Buy();
	pmt->Pay();
	return 0;
}
```

### 输入

```
None
```

### 输出

```
Buy Nothing
Pay Beef
Buy Meat
Pay Beef
```

### Solution