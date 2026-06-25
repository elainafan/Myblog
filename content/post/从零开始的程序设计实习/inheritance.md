---
title: 从零开始的继承
date: 2025-03-05
categories:
    - 程序设计实习
slug: 从零开始的继承
hidden: true
seriesOrder: 3
---
## 全面的MyString
### 描述
根据输出完善程序。
```cpp
#include <cstdlib>
#include <iostream>
using namespace std;
int strlen(const char * s) 
{	int i = 0;
	for(; s[i]; ++i);
	return i;
}
void strcpy(char * d,const char * s)
{
	int i = 0;
	for( i = 0; s[i]; ++i)
		d[i] = s[i];
	d[i] = 0;
		
}
int strcmp(const char * s1,const char * s2)
{
	for(int i = 0; s1[i] && s2[i] ; ++i) {
		if( s1[i] < s2[i] )
			return -1;
		else if( s1[i] > s2[i])
			return 1;
	}
	return 0;
}
void strcat(char * d,const char * s)
{
	int len = strlen(d);
	strcpy(d+len,s);
}
class MyString
{
// 在此处补充你的代码
};


int CompareString( const void * e1, const void * e2)
{
	MyString * s1 = (MyString * ) e1;
	MyString * s2 = (MyString * ) e2;
	if( * s1 < *s2 )
	return -1;
	else if( *s1 == *s2)
	return 0;
	else if( *s1 > *s2 )
	return 1;
}
int main()
{
	MyString s1("abcd-"),s2,s3("efgh-"),s4(s1);
	MyString SArray[4] = {"big","me","about","take"};
	cout << "1. " << s1 << s2 << s3<< s4<< endl;
	s4 = s3;
	s3 = s1 + s3;
	cout << "2. " << s1 << endl;
	cout << "3. " << s2 << endl;
	cout << "4. " << s3 << endl;
	cout << "5. " << s4 << endl;
	cout << "6. " << s1[2] << endl;
	s2 = s1;
	s1 = "ijkl-";
	s1[2] = 'A' ;
	cout << "7. " << s2 << endl;
	cout << "8. " << s1 << endl;
	s1 += "mnop";
	cout << "9. " << s1 << endl;
	s4 = "qrst-" + s2;
	cout << "10. " << s4 << endl;
	s1 = s2 + s4 + " uvw " + "xyz";
	cout << "11. " << s1 << endl;
	qsort(SArray,4,sizeof(MyString),CompareString);
	for( int i = 0;i < 4;i ++ )
	cout << SArray[i] << endl;
	//s1的从下标0开始长度为4的子串
	cout << s1(0,4) << endl;
	//s1的从下标5开始长度为10的子串
	cout << s1(5,10) << endl;
	return 0;
}
```
### 输入
```
None
```
### 输出
```
1. abcd-efgh-abcd-
2. abcd-
3.
4. abcd-efgh-
5. efgh-
6. c
7. abcd-
8. ijAl-
9. ijAl-mnop
10. qrst-abcd-
11. abcd-qrst-abcd- uvw xyz
about
big
me
take
abcd
qrst-abcd-
```
### Solution
一种奇技淫巧是，输入vscode按照报错模拟即可。

还是正经解释一下代码怎么填的。

首先，从主函数可以观察到``MyString``类需要实现字符串类型的转换构造函数和拷贝构造函数，而它的成员变量自然还是一个字符指针。

随后，需要重载右操作数分别为``MyString``类对象和``字符指针``类型的赋值运算符，以及两个``MyString``类对象的加法运算符（注意此时返回的是临时对象）。

接着，需要实现对``MyString``类对象元素的随机访问，即重载``[]``运算符，可以由字符指针直接实现，注意应该返回的是引用，因为有``s1[2]='A``这一行。

然后，需要重载``输出运算符``和``左操作数为字符串、右操作数为MyString类对象``的加法运算符，在[elainafan-从零开始的运算符重载](https://www.elainafan.one/p/%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84%E8%BF%90%E7%AE%97%E7%AC%A6%E9%87%8D%E8%BD%BD/)中有讲到它们都需要使用友元函数，如果忘记了可以回顾一下。

再往下看，需要重载``+=``运算符和``左操作数为MyString类对象、右操作数为字符串``的加法运算符，注意前者需要返回引用，而后者由于是临时变量，只需要返回对象。

然后是一个``qsort``，注意它传入的比较函数是``CompareString``，而其中使用了大于号、等于号和小于号，因此这三个符号都需要重载，可以使用已经实现的``strcmp``函数进行实现。

最后，则是需要重载``()``运算符，利用``strcpy``函数进行实现即可，在所有的函数中，都需要注意指针空间的释放与分配。

这题看上去跟继承没有任何关系，但是其实老师的目的就是在于将这道题与下面那道题进行对比，从而能更深层地理解继承的用法。

```cpp
#include <cstdlib>
#include <iostream>
using namespace std;
int strlen(const char *s) {
    int i = 0;
    for (; s[i]; ++i);
    return i;
}
void strcpy(char *d, const char *s) {
    int i = 0;
    for (i = 0; s[i]; ++i) d[i] = s[i];
    d[i] = 0;
}
int strcmp(const char *s1, const char *s2) {
    for (int i = 0; s1[i] && s2[i]; ++i) {
        if (s1[i] < s2[i])
            return -1;
        else if (s1[i] > s2[i])
            return 1;
    }
    return 0;
}
void strcat(char *d, const char *s) {
    int len = strlen(d);
    strcpy(d + len, s);
}
class MyString {
private:
    char *p;

public:
    MyString() { p = NULL; }
    MyString(const char *s) {
        p = new char[strlen(s) + 1];
        strcpy(p, s);
    }
    ~MyString() {
        if (p) delete[] p;
    }
    MyString(const MyString &s) {
        if (s.p == NULL)
            p = NULL;
        else {
            p = new char[strlen(s.p) + 1];
            strcpy(p, s.p);
        }
    }
    MyString &operator=(const MyString &s) {
        if (p) delete[] p;
        if (s.p == NULL) {
            p = NULL;
            return *this;
        } else {
            p = new char[strlen(s.p) + 1];
            strcpy(p, s.p);
            return *this;
        }
    }
    MyString &operator=(const char *s) {
        if (p) delete[] p;
        if (s == NULL) {
            p = NULL;
            return *this;
        } else {
            p = new char[strlen(s) + 1];
            strcpy(p, s);
            return *this;
        }
    }
    char &operator[](int l) { return p[l]; }
    friend MyString operator+(const MyString &a, const MyString &b) {
        MyString ans;
        ans.p = new char[strlen(a.p) + strlen(b.p) + 1];
        strcpy(ans.p, a.p);
        strcat(ans.p, b.p);
        return ans;
    }
    MyString &operator+=(const char *c) {
        MyString temp(c);
        *this = *this + temp;
        return *this;
    }
    bool operator<(const MyString s) { return (strcmp(p, s.p) == -1); }
    bool operator==(const MyString s) { return (strcmp(p, s.p) == 0); }
    bool operator>(const MyString s) { return (strcmp(p, s.p) == 1); }
    char *operator()(int start, int len) {
        char *temp = new char[len + 1];
        for (int i = start; i < start + len; i++) {
            temp[i - start] = p[i];
        }
        temp[len] = '\0';
        return temp;
    }
    friend ostream &operator<<(ostream &o, const MyString &s) {
        if (s.p == NULL)
            return o;
        else {
            o << s.p;
            return o;
        }
    }
};
int CompareString(const void *e1, const void *e2) {
    MyString *s1 = (MyString *)e1;
    MyString *s2 = (MyString *)e2;
    if (*s1 < *s2)
        return -1;
    else if (*s1 == *s2)
        return 0;
    else if (*s1 > *s2)
        return 1;
}
int main() {
    MyString s1("abcd-"), s2, s3("efgh-"), s4(s1);
    MyString SArray[4] = {"big", "me", "about", "take"};
    cout << "1. " << s1 << s2 << s3 << s4 << endl;
    s4 = s3;
    s3 = s1 + s3;
    cout << "2. " << s1 << endl;
    cout << "3. " << s2 << endl;
    cout << "4. " << s3 << endl;
    cout << "5. " << s4 << endl;
    cout << "6. " << s1[2] << endl;
    s2 = s1;
    s1 = "ijkl-";
    s1[2] = 'A';
    cout << "7. " << s2 << endl;
    cout << "8. " << s1 << endl;
    s1 += "mnop";
    cout << "9. " << s1 << endl;
    s4 = "qrst-" + s2;
    cout << "10. " << s4 << endl;
    s1 = s2 + s4 + " uvw " + "xyz";
    cout << "11. " << s1 << endl;
    qsort(SArray, 4, sizeof(MyString), CompareString);
    for (int i = 0; i < 4; i++) cout << SArray[i] << endl;
    // s1的从下标0开始长度为4的子串
    cout << s1(0, 4) << endl;
    // s1的从下标5开始长度为10的子串
    cout << s1(5, 10) << endl;
    system("pause");
    return 0;
}
```
## 继承自string的MyString
### 描述
根据输出完善程序。
```cpp
#include <cstdlib>
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;
class MyString:public string
{
// 在此处补充你的代码
};


int main()
{
	MyString s1("abcd-"),s2,s3("efgh-"),s4(s1);
	MyString SArray[4] = {"big","me","about","take"};
	cout << "1. " << s1 << s2 << s3<< s4<< endl;
	s4 = s3;
	s3 = s1 + s3;
	cout << "2. " << s1 << endl;
	cout << "3. " << s2 << endl;
	cout << "4. " << s3 << endl;
	cout << "5. " << s4 << endl;
	cout << "6. " << s1[2] << endl;
	s2 = s1;
	s1 = "ijkl-";
	s1[2] = 'A' ;
	cout << "7. " << s2 << endl;
	cout << "8. " << s1 << endl;
	s1 += "mnop";
	cout << "9. " << s1 << endl;
	s4 = "qrst-" + s2;
	cout << "10. " << s4 << endl;
	s1 = s2 + s4 + " uvw " + "xyz";
	cout << "11. " << s1 << endl;
        sort(SArray,SArray+4);
	for( int i = 0;i < 4;i ++ )
	cout << SArray[i] << endl;
	//s1的从下标0开始长度为4的子串
	cout << s1(0,4) << endl;
	//s1的从下标5开始长度为10的子串
	cout << s1(5,10) << endl;
	return 0;
}
```
### 输入
```
None
```
### 输出
```
1. abcd-efgh-abcd-
2. abcd-
3.
4. abcd-efgh-
5. efgh-
6. c
7. abcd-
8. ijAl-
9. ijAl-mnop
10. qrst-abcd-
11. abcd-qrst-abcd- uvw xyz
about
big
me
take
abcd
qrst-abcd-
```
### 提示
提示 1：如果将程序中所有 "MyString" 用 "string" 替换，那么除了最后两条红色的语句编译无法通过外，其他语句都没有问题，而且输出和前面给的结果吻合。也就是说，MyString 类对 string 类的功能扩充只体现在最后两条语句上面。

提示 2: string 类有一个成员函数 string substr(int start,int
length);能够求从 start 位置开始，长度为 length 的子串。

提示 3: C++中，派生类的对象可以赋值给基类对象，因为，一个派生类对象，也可看作是一个基类对象（大学生是学生）。反过来则不行（学生未必是大学生） 同样，调用需要基类对象作参数的函数时，以派生类对象作为实参，也是没有问题的。
### Solution
注意本题中导入了标准库``string``和``algorithm``，前者在计概中学过就是字符串类型``string``的实现，后者主要用于``sort``。

回想起本题标题，继承自``string``的``MyString``，同时上题中的``strcpy``等等一车函数在``string``类中也有实现，而代码中也写了``class MyString:public string``，表示它能访问``String``类的公有对象。

因此，只需要重载``MyString``类的默认构造函数和转换构造函数，而同时调用``string``类的构造函数，注意传入的对象需要作为``String``类对象的构造变量。

以及，最后需要重载``String``类中没有的``()``运算符就可以了，而显然地，调用``string``类的``substr``函数即可实现。
```cpp
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <string>

using namespace std;
class MyString : public string {
public:
    MyString() : string() {}
    MyString(const string s) : string(s) {}
    MyString(const char *s) : string(s) {}
    string operator()(int start, int len) { return substr(start, len); }
};
int main() {
    MyString s1("abcd-"), s2, s3("efgh-"), s4(s1);
    MyString SArray[4] = {"big", "me", "about", "take"};
    cout << "1. " << s1 << s2 << s3 << s4 << endl;
    s4 = s3;
    s3 = s1 + s3;
    cout << "2. " << s1 << endl;
    cout << "3. " << s2 << endl;
    cout << "4. " << s3 << endl;
    cout << "5. " << s4 << endl;
    cout << "6. " << s1[2] << endl;
    s2 = s1;
    s1 = "ijkl-";
    s1[2] = 'A';
    cout << "7. " << s2 << endl;
    cout << "8. " << s1 << endl;
    s1 += "mnop";
    cout << "9. " << s1 << endl;
    s4 = "qrst-" + s2;
    cout << "10. " << s4 << endl;
    s1 = s2 + s4 + " uvw " + "xyz";
    cout << "11. " << s1 << endl;
    sort(SArray, SArray + 4);
    for (int i = 0; i < 4; i++) cout << SArray[i] << endl;
    // s1的从下标0开始长度为4的子串
    cout << s1(0, 4) << endl;
    // s1的从下标5开始长度为10的子串
    cout << s1(5, 10) << endl;
    system("pause");
    return 0;
}
```