---
title: 从零开始的C++11高级特性
date: 2025-04-30
categories:
    - 程序设计实习
slug: 从零开始的c11高级特性
hidden: true
seriesOrder: 19
---
## 高阶函数F(x)
### 描述
Lisp 语言中有高阶函数的概念，即函数可以作为函数的参数，也可以作为函数的返回值。例如:

```lisp
(define (f n)   (lambda (x) (+ x n)))
```

定义了一个函数 `f`，该函数的返回值是另一个函数，假定称为 `g`，即 `(lambda (x) (+ x n))`。此函数功能是参数为 `x`，返回值为 `x + n`。 

于是 `((f 7) 9)` 如下执行：

1. `(f 7)` 以参数 `7` 调用 `f`，`f` 的返回值是 `g`，`n` 的值为 `7`。

2. `((f 7) 9)` 等价于 `(g 9)`，即以参数 `9` 调用 `g`。 因 `n = 7`, `x = 9`，因此 `(g 9)` 返回值为 `16`。

编写一个C++的通用函数模板 `f`，使之能完成类似于 Lisp 函数 `f` 的功能，并能输出对应输出。

```cpp
#include <iostream>
using namespace std;
// 在此处补充你的代码
int main()
{
   cout << f<int,int>(7)(9) << endl;   //16
   cout << f<string,string> (" hello!")("world")  <<endl; // world hello!
   cout << f<char,string> ('!')("world") << endl;
   
   
   return 0;    //world!
}
```
### 输入
```
None
```
### 输出
16
world hello!
world!

### 提示
C++函数模板实例化时，也可以通过在``<>``中指定类型参数所对应的具体类型来实现。
### Solution
题目给的背景不够通俗易懂，简单来说，就是函数可以返回函数，也就是在Python中经常见到的。

但是原生C++是没有这种功能的，因此可以考虑将代码中的``f<int,int>(7)(9)``看成先将``7``用转换构造函数实例化，再重载``()``使用仿函数即可。

```cpp
#include <iostream>
using namespace std;
// 在此处补充你的代码
template <class T1, class T2>
class f {
private:
    T1 x;

public:
    f(T1 k) : x(k) {}
    T2 operator()(T2 k) { return k + x; }
};
int main() {
    cout << f<int, int>(7)(9) << endl;                      // 16
    cout << f<string, string>(" hello!")("world") << endl;  // world hello!
    cout << f<char, string>('!')("world") << endl;
    system("pause");
    return 0;  // world!
}
```
## 高阶函数Combine
### 描述
Lisp 语言中有高阶函数的概念，即函数可以作为函数的参数，也可以作为函数的返回值。例如:

```lisp
(define (square x) (* x x)); 定义了一个求 x 的平方的函数

(define (inc x) (+ x 1)); 定义了一个求 x+1 的函数

(define (combine f g) (lambda (x) (f (+ (f x) (g x)))))
```

`(combine f g)` 返回函数 `k`， $k(x) = f(f(x) + g(x))$。

因此 `((combine square inc) 3)` 的返回值就是 $169$。

此处：
$$
\begin{aligned}
f(x) &= x^2 \\
g(x) &= x + 1 \\
k(x) &= (x^2 + x + 1)^2
\end{aligned}
$$

`((combine square inc) 3)` 即是 $k(3)$。

因此返回值为 $169$。用 C++ 实现类似的 `combine` 函数模板，使得程序能够输出对应输出。

```cpp
#include <iostream>
using namespace std;
// 在此处补充你的代码
int main()
{
    auto Square = [] (double a) { return a * a; };
    auto Inc = [] (double a) { return a + 1; };
    cout << combine<decltype(Square),decltype(Inc),int>(Square,Inc)(3) << endl;
    cout << combine<decltype(Inc),decltype(Square),double>(Inc,Square)(2.5) << endl;

    return 0;
}
```
### 输入
```
None
```
### 输出
```
169
10.75
```
### 提示
C++函数模板实例化时，也可以通过在``<>``中指定类型参数所对应的具体类型来实现。
### Solition
首先要解释的是，这里为什么要用``decltype``？

由于这里``lambda``表达式的特性，编译器只知道它有一个唯一的、未命名的类型，而当然不能用它去自动实例化模板类，因此此时需要通过``decltype``去推导它的类型，这里为函数指针，并进行实例化。

随后，跟上题类似，还是使用模板类的仿函数，重载``()``运算符，以达成高阶函数效果。

```cpp
#include <iostream>
using namespace std;
// 在此处补充你的代码
template <class T1, class T2, class T3>
class combine {
private:
    T1 a;
    T2 b;

public:
    combine(T1 x, T2 y) : a(x), b(y) {}
    T3 operator()(T3 x) { return a(a(x) + b(x)); }
};
int main() {
    auto Square = [](double a) { return a * a; };
    auto Inc = [](double a) { return a + 1; };
    cout << combine<decltype(Square), decltype(Inc), int>(Square, Inc)(3) << endl;
    cout << combine<decltype(Inc), decltype(Square), double>(Inc, Square)(2.5) << endl;
    system("pause");
    return 0;
}
```
## 自己实现bitset
### 描述
程序填空，实现一个类似STL bitset的 MyBitset, 输出指定结果。
```cpp
#include <iostream>
#include <cstring>
using namespace std;
template <int bitNum>
struct MyBitset 
{
	char a[bitNum/8+1];
	MyBitset() { memset(a,0,sizeof(a));};
	void Set(int i,int v) {
		char & c = a[i/8];
		int bp = i % 8;
		if( v ) 
			c |= (1 << bp);
		else 
			c &= ~(1 << bp);
	}
// 在此处补充你的代码
void Print() {
		for(int i = 0;i < bitNum; ++i) 
			cout << (*this) [i];
		cout << endl;
	}

};

int main()
{
	int n;
	int i,j,k,v;
	while( cin >>  n) {
		MyBitset<20> bs;
		for(int i = 0;i < n; ++i) {
			int t;
			cin >> t;
			bs.Set(t,1);
		}
		bs.Print();
		cin >> i >> j >> k >> v;
		bs[k] = v;
		bs[i] = bs[j] = bs[k];
		bs.Print();
		cin >> i >> j >> k >> v;
		bs[k] = v;
		(bs[i] = bs[j]) = bs[k];
		bs.Print();
	}
	return 0;
}
```
### 输入
多组数据，每组数据：  

第一行是整数 $n , 1 \leq n < 20$;  

第二行是 $n$ 个整数 $k_1,k_2,\ldots,k_n$,$ 均在范围 $[0,19]$ 内。  

第三行是四个整数 $i_1,j_1,k_1,v_1, 0 \leq i_1,j_1,k_1 \leq 19, v_1$ 值为 $0$ 或 $1$ 。 

第三行是四个整数 $i_2,j_2,k_2,v_2, 0 \leq i_2,j_2,k_2 \leq 19, v_2$ 值为 $0$ 或 $1$ 。

```
4
0 1 2 8
7 19 0 1
7 2 8 0
1
1
1 1 1 0
1 1 1 1
```
### 输出
对每组数据，共输出3行，每行20位，每位为1或者0。最左边称为第0位。

第一行： 第 $k_1,k_2,\ldots, k_n$ 位为1，其余位为0。  

第二行： 将第一行中的第 $i_1,j_1,k_1$ 位变为 $v_1$ ，其余位不变。
第三行： 将第二行中的第 $i_2$ 位和 $k_2$ 位变为 $v_2$ ，其余位不变 。

```
11100000100000000000
11100001100000000001
11100000000000000001
01000000000000000000
00000000000000000000
01000000000000000000
```
### 提示
推荐使用内部类，内部类中使用引用成员。引用成员要在构造函数中初始化。
### Solution
观察代码，发现这里只需要重载``[]``运算符返回引用。

有一种很巧妙的方法，就是将一开始传入的数组，第一次要修改的时候直接将其完整展开为一个``int``数组，后续每次在这个数组中修改，然后因为重载的是``[]``，也不会影响``Print``函数。

但是需要注意的是，需要在第一次初始化之前，记录一个是否初始化过的成员``bool``型变量。

```cpp
#include <cstring>
#include <iostream>

using namespace std;
template <int bitNum>
struct MyBitset {
    char a[bitNum / 8 + 1];
    MyBitset() { memset(a, 0, sizeof(a)); };
    void Set(int i, int v) {
        char &c = a[i / 8];
        int bp = i % 8;
        if (v)
            c |= (1 << bp);
        else
            c &= ~(1 << bp);
    }
    int myb[20];
    bool flag = false;
    void transform() {
        memset(myb, 0, sizeof(myb));
        for (int i = 0; i <= bitNum / 8 + 1; i++) {
            int temp = i * 8;
            int num = (unsigned char)(a[i]);
            while (num > 0) {
                if (num % 2) myb[temp]++;
                temp++;
                num /= 2;
            }
        }
        flag = true;
    }
    int &operator[](int x) {
        if (!flag) transform();
        return myb[x];
    }
    // 在此处补充你的代码
    void Print() {
        for (int i = 0; i < bitNum; ++i) cout << (*this)[i];
        cout << endl;
    }
};

int main() {
    int n;
    int i, j, k, v;
    while (cin >> n) {
        MyBitset<20> bs;
        for (int i = 0; i < n; ++i) {
            int t;
            cin >> t;
            bs.Set(t, 1);
        }
        bs.Print();
        cin >> i >> j >> k >> v;
        bs[k] = v;
        bs[i] = bs[j] = bs[k];
        bs.Print();
        cin >> i >> j >> k >> v;
        bs[k] = v;
        (bs[i] = bs[j]) = bs[k];
        bs.Print();
    }
    system("pause");
    return 0;
}
```