---
title: 【程序设计实习】STL作业二
date: 2025-04-23
categories:
    - 程序设计实习
---
# A:List
## 描述
写一个程序完成以下命令：  
new id ——新建一个指定编号为id的序列(id < 10000)  
add id num——向编号为id的序列加入整数  
num merge id1 id2——如果id1等于id2,不做任何事，否则归并序列id1和id2中的数，并将id2清空  
unique id——去掉序列id中重复的元素  
out id ——从小到大输出编号为id的序列中的元素，以空格隔开  
## 输入
第一行一个数n，表示有多少个命令( n＜＝２０００００)。以后n行每行一个命令。
## 输出
按题目要求输出。
## 样例输入
```
16
new 1
new 2
add 1 1
add 1 2
add 1 3
add 2 1
add 2 2
add 2 3
add 2 4
out 1
out 2
merge 1 2
out 1
out 2
unique 1
out 1
```
## 样例输出
```
1 2 3 
1 2 3 4
1 1 2 2 3 3 4

1 2 3 4
```
# Solution
其实题目没有强求你用题干的数据结构就是了  
但是我们这题还是用list，虽然这题用multimap或者multiset也可以的  
那题目中的指令就变成:  
new 其实也没啥用  
add 就是push_back  
merge 就是merge  
unique 就是先sort后unique（有点像离散化？不过方便输出也是了  )
out 就是用迭代器输出 使用更方便的auto而不是iterator  
下面看代码:
```
#include<bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define maxn 200005
using namespace std;
int n;
list<int>ma[maxn];
string s;
int id,num;
int main(){
    scanf("%d",&n);
    for(int i=1;i<=n;i++){
        cin>>s;
        if(s[0]=='n'){
            cin>>id;
        }
        else if(s[0]=='a'){
            cin>>id>>num;
            ma[id].push_back(num);
        }
        else if(s[0]=='m'){
            cin>>id>>num;
            if(id==num) continue;
            else{
                ma[id].merge(ma[num]);
            }
        }
        else if(s[0]=='u'){
            cin>>id;
            ma[id].sort();
            ma[id].unique();
        }
        else if(s[0]=='o'){
            cin>>id;
            if(ma[id].empty()) cout<<endl;
            else{
                ma[id].sort();
                for(auto i=ma[id].begin();i!=ma[id].end();i++){
                    cout<<*i<<' ';
                }
                cout<<endl;
            }
        }
    }
    system("pause");
    return 0;
}
```
# B RPN Calculator
## 描述
逆波兰表示法（或简称 RPN），与相关的波兰表示法类似，波兰表示法是波兰数学家扬・武卡谢维奇（Jan Łukasiewicz）于 1920 年引入的一种前缀表示法。逆波兰表示法是一种数学表示法，其中每个运算符都紧跟在其所有操作数之后。它也被称为后缀表示法。  
在逆波兰表示法中，运算符紧跟在操作数之后；例如，要计算 3 加 4 ，应写成 “3 4 +”，而不是 “3 + 4”。如果有多个运算，运算符会紧跟在第二个操作数之后；所以常规中缀表示法下写成 “3 - 4 + 5” 的表达式，在逆波兰表示法中应写成 “3 4 - 5 +” ：先计算 3 减 4 ，然后再加上 5。逆波兰表示法的一个优点是它无需中缀表示法中所需的括号。“3 - 4 * 5” 也可以写成 “3 - (4 * 5)” ，但这与 “(3 - 4) * 5” 的含义截然不同，只有括号能区分这两种不同的含义。在后缀表示法中，前者应写成 “3 4 5 * -” ，它明确表示 “3 (4 5 *) -” 。  
你需要设计一个简单的逆波兰表示法计算器，该计算器需支持 “+”、“-”、“*”、“/”（除数的绝对值不小于 10⁻⁹ ）和 “^”（幂运算符，若底数 b≤0 ，指数 e 必须是不大于 10⁹ 的正整数 ）运算符。可以假设计算过程中的所有数字都可以用双精度浮点数表示。  
此外，我们的计算器有一定的内存。每次计算一个表达式时，内存中最小的数字将被删除，并替换为该表达式的值。  
## 输入
第一行包含一个整数 n，它是我们计算器的内存大小。  
从第二行开始，将给出 n 个数字，这些是内存的初始值。除最后一行外，每行将有 10 个数字。  
然后每行是一个有效的逆波兰表示法表达式，以 “=” 结尾，“=” 是计算命令。每个项的长度不超过 20 个字符。
## 输出
对于每个表达式，在一行中输出其值。  
然后输出一个空行，将两部分内容分隔开。  
最后，按升序输出内存中的所有数字，每行 10 个数字。  
每个数字应采用科学计数法格式，保留 6 位小数，指数部分占 2 位，类似于 C 语言中 printf () 函数的 “% e” 格式字符串。一行中的数字之间用空格分隔。  
## 样例输入
```
4
1e6 1e-6 0.001 1000
1 2 + 3 4 + * =
1 0.1 / 8 ^ =
```
## 样例输出
```
2.100000e+01
1.000000e+08

2.100000e+01 1.000000e+03 1.000000e+06 1.000000e+08
```
## 提示
Huge input, scanf() is recommended  
%e格式输出在windows环境下指数部分为3位，在系统的测试环境下为2位。
# Solution
逆波兰表达式的求法应该都会？用一个栈很简单  
然后，有什么要介绍的呢   
啊，就是这个atof(x.c_str())  
其中，c_str()指的是将string类型变量x转换成char*类型变量  
然后，atof()表示将char*型变量转换成双精度浮点数  
这部分来自网络代码  
下面看代码:
```
#include<bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define lowbit(x) (x&(-x))
using namespace std;
int n;
int main(){
    cin>>n;
    stack<double>ma;
    multiset<double>res;
    for(int i=1;i<=n;i++){
        double x;
        cin>>x;
        res.insert(x);
    }
    string x;
    while(cin>>x){
        if(x=="="){
            double s=ma.top();
            printf("%e\n",s);
            ma.pop();
            auto it=res.begin();
            res.erase(it);
            res.insert(s);
        }
        else if(x=="+"||x=="-"||x=="*"||x=="/"||x=="^"){
            double a,b,c;
            a=ma.top();
            ma.pop();
            b=ma.top();
            ma.pop();
            if(x=="+"){
                c=a+b;
            }
            else if(x=="-"){
                c=b-a;
            }
            else if(x=="*"){
                c=a*b;
            }
            else if(x=="/"){
                c=b/a;
            }
            else{
                c=pow(b,a);
            }
            ma.push(c);
        }
        else{
            double num;
            num=atof(x.c_str());
            ma.push(num);
        }
    }
    cout<<endl;
    int count=0;
    for(auto it=res.begin();it!=res.end();it++){
        count++;
        if(count%10==0){
            printf("%e\n",*it);
        }
        else{
            printf("%e ",*it);
        }
    }
    system("pause");
    return 0;
}
```
# C:Set
## 描述
现有一整数集（允许有重复元素），初始为空。我们定义如下操作：  
add x 把x加入集合  
del x 把集合中所有与x相等的元素删除  
ask x 对集合中元素x的情况询问  
对每种操作，我们要求进行如下输出。  
add 输出操作后集合中x的个数  
del 输出操作前集合中x的个数  
ask 先输出0或1表示x是否曾被加入集合（0表示不曾加入），再输出当前集合中x的个数，中间用空格格开。  
## 输入
第一行是一个整数n，表示命令数。0<=n<=100000。  
后面n行命令，如Description中所述。
## 输出
共n行，每行按要求输出。
## 样例输入
```
7
add 1
add 1
ask 1
ask 2
del 2
del 1
ask 1
```
## 样例输出
```
1
2
1 2
0 0
0
2
1 0
```
## 提示
Please use STL’s set and multiset to finish the task
# Solution
由于题目中需要我们删除重复元素，所以必须用到multiset 然后，我们用set来记录x是否被加入过集合就可以  
至于删除操作，我们用一个循环find就能实现  
下面看代码:
```
#include<bits/stdc++.h>
#define ll long long
#define ull unsigned long long
using namespace std;
int n;
multiset<int>ma;
set<int>k;
string s;
int x;
int main(){
    scanf("%d",&n);
    for(int i=1;i<=n;i++){
        cin>>s>>x;
        if(s[1]=='d'){
            ma.insert(x);
            k.insert(x);
            cout<<ma.count(x)<<endl;
        }
        else if(s[1]=='e'){
            cout<<ma.count(x)<<endl;
            auto it=ma.find(x);
            while(it!=ma.end()){
                ma.erase(it);
                it=ma.find(x);
            }
        }
        else{
            if(k.find(x)!=k.end()) cout<<1<<' ';
            else cout<<0<<' ';
            cout<<ma.count(x)<<endl;
        }
    }
    system("pause");
    return 0;
}
```
# D:字符串操作
## 描述
给定n个字符串（从1开始编号），每个字符串中的字符位置从0开始编号，长度为1-500，现有如下若干操作：

copy N X L：取出第N个字符串第X个字符开始的长度为L的字符串。  
add S1 S2：判断S1，S2是否为0-99999之间的整数，若是则将其转化为整数做加法，若不是，则作字符串加法，返回的值为一字符串。  
find S N：在第N个字符串中从左开始找寻S字符串，返回其第一次出现的位置，若没有找到，返回字符串的长度。  
rfind S N：在第N个字符串中从右开始找寻S字符串，返回其第一次出现的位置，若没有找到，返回字符串的长度。  
insert S N X：在第N个字符串的第X个字符位置中插入S字符串。  
reset S N：将第N个字符串变为S。  
print N：打印输出第N个字符串。  
printall：打印输出所有字符串。  
over：结束操作。  
其中N，X，L可由find与rfind操作表达式构成，S，S1，S2可由copy与add操作表达式构成。

## 输入
第一行为一个整数n（n在1-20之间）


接下来n行为n个字符串，字符串不包含空格及操作命令等。


接下来若干行为一系列操作，直到over结束。

## 输出
根据操作提示输出对应字符串。

## 样例输入
```
3
329strjvc
Opadfk48
Ifjoqwoqejr
insert copy 1 find 2 1 2 2 2
print 2
reset add copy 1 find 3 1 3 copy 2 find 2 2 2 3
print 3
insert a 3 2
printall
over
```
## 样例输出
```
Op29adfk48
358
329strjvc
Op29adfk48
35a8
```
## 提示
推荐使用string类中的相关操作函数。
# Solution
我们要明确的一点是，这道题可能存在嵌套的函数，所以应该使用没有参数值的函数来实现，因为如果有参数值确实不好处理这个东西的类型，写模版确实麻烦多了  
这道题思路有参考网络  
其中，stoi表示将string型变量转成int型变量  
to_string表示将int型变量转成string型变量  
npos通常用于表示查找失败或者末尾  
下面看代码:
```
#include<bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define lowbit(x) (x&(-x))
#define maxn 25
using namespace std;
string Copy();
string Add();
bool isnum(string x);
int Find();
int Rfind();
string Insert();
string Reset();
void Print(int x);
void Printall();
int n0;
string str[maxn];
int tot;
string Copy(){
    string N,X,L;
    int n,x,l;
    cin>>N;
    if(N=="find"){
        n=Find();
    }
    else if(N=="rfind"){
        n=Rfind();
    }
    else n=stoi(N);
    cin>>X;
    if(X=="find"){
        x=Find();
    }
    else if(X=="rfind"){
        x=Rfind();
    }
    else x=stoi(X);
    cin>>L;
    if(L=="find"){
        l=Find();
    }
    else if(L=="rfind"){
        l=Rfind();
    }
    else l=stoi(L);
    string temp=str[n].substr(x,l);
    return temp;
}
string Add(){
    string S1,S2,s1,s2;
    cin>>S1;
    if(S1=="copy"){
        s1=Copy();
    }
    else if(S1=="add"){
        s1=Add();
    }
    else s1=S1;
    cin>>S2;
    if(S2=="copy"){
        s2=Copy();
    }
    else if(S2=="add"){
        s2=Add();
    }
    else s2=S2;
    if(isnum(s1)&&isnum(s2)){
        int a=stoi(s1),b=stoi(s2);
        return to_string(a+b);
    }
    else return s1+s2;
}
bool isnum(string x){
    int l=x.length();
    if(l>=5) return false;
    bool flag=true;
    for(int i=0;i<=l-1;i++){
        if(!(x[i]>='0'&&x[i]<='9')){
            flag=false;
            break;
        }
    }
    return flag;
}
int Find(){
    string S,N,s;
    int n;
    cin>>S;
    if(S=="copy"){
        s=Copy();
    }
    else if(S=="add"){
        s=Add();
    }
    else s=S;
    cin>>N;
    if(N=="find"){
        n=Find();
    }
    else if(N=="rfind"){
        n=Rfind();
    }
    else n=stoi(N);
    int temp;
    if(str[n].find(s)!=string::npos){
        temp=str[n].find(s);
    }
    else temp=str[n].size();
    return temp;
}
int Rfind(){
    string S,s,N;
    int n;
    cin>>S;
    if(S=="copy"){
        s=Copy();
    }
    else if(S=="add"){
        s=Add();
    }
    else s=S;
    cin>>N;
    if(N=="find"){
        n=Find();
    }
    else if(N=="rfind"){
        n=Rfind();
    }
    else n=stoi(N);
    int temp;
    if(str[n].rfind(s)!=string::npos){
        temp=str[n].rfind(s);
    }
    else temp=str[n].size();
    return temp;
}
string Insert(){
    string N,X,S,s;
    int n,x;
    cin>>S;
    if(S=="copy"){
        s=Copy();
    }
    else if(S=="add"){
        s=Add();
    }
    else s=S;
    cin>>N;
    if(N=="find"){
        n=Find();
    }
    else if(N=="rfind"){
        n=Rfind();
    }
    else{
        n=stoi(N);
    }
    cin>>X;
    if(X=="find"){
        x=Find();
    }
    else if(X=="rfind"){
        x=Rfind();
    }
    else x=stoi(X);
    string temp=str[n].insert(x,s);
    return temp;
}
string Reset(){
    string S,s,N;
    int n;
    cin>>S;
    if(S=="copy"){
        s=Copy();
    }
    else if(S=="add"){
        s=Add();
    }
    else s=S;
    cin>>N;
    if(N=="find"){
        n=Find();
    }
    else if(N=="rfind"){
        n=Rfind();
    }
    else n=stoi(N);
    swap(str[n],s);
    return str[n];
}
void Print(int x){
    cout<<str[x]<<endl;
    return ;
}
void Printall(){
    for(int i=1;i<=n0;i++){
        cout<<str[i]<<endl;
    }
    return ;
}
int main(){
    cin>>n0;
    for(int i=1;i<=n0;i++){
        cin>>str[i];
    }
    while(1){
        string op;
        cin>>op;
        if(op=="over") break;
        else if(op=="copy"){
            Copy();
        }
        else if(op=="add"){
            Add();
        }
        else if(op=="find"){
            Find();
        }
        else if(op=="rfind"){
            Rfind();
        }
        else if(op=="insert"){
            Insert();
        }
        else if(op=="reset"){
            Reset();
        }
        else if(op=="print"){
            int x;
            cin>>x;
            Print(x);
        }
        else if(op=="printall"){
            Printall();
        }
    }
    system("pause");
    return 0;
}
```
# E:热血格斗场
## 描述
为了迎接08年的奥运会，让大家更加了解各种格斗运动，facer新开了一家热血格斗场。格斗场实行会员制，但是新来的会员不需要交入会费，而只要同一名老会员打一场表演赛，证明自己的实力。

我们假设格斗的实力可以用一个正整数表示，成为实力值。另外，每个人都有一个唯一的id，也是一个正整数。为了使得比赛更好看，每一个新队员都会选择与他实力最为接近的人比赛，即比赛双方的实力值之差的绝对值越小越好，如果有两个人的实力值与他差别相同，则他会选择比他弱的那个（显然，虐人必被虐好）。

不幸的是，Facer一不小心把比赛记录弄丢了，但是他还保留着会员的注册记录。现在请你帮facer恢复比赛纪录，按照时间顺序依次输出每场比赛双方的id。

## 输入
第一行一个数n(0 < n <=100000)，表示格斗场新来的会员数（不包括facer）。以后n行每一行两个数，按照入会的时间给出会员的id和实力值。一开始，facer就算是会员，id为1，实力值1000000000。输入保证两人的实力值不同。

## 输出
N行，每行两个数，为每场比赛双方的id，新手的id写在前面。

## 样例输入
```
3
2 1
3 3
4 2
```
## 样例输出
```
2 1
3 2
4 2
```
# Solution
本题要求我们匹配比赛记录  
那么，我们可以采用multimap  
为什么是multimap?因为这道题其实用multiset好像也可以，但是就直接用multimap吧，因为可能有的数的power是一样的  
代码实现还是不难的  
下面看代码:
```
#include<bits/stdc++.h>
#define ll long long
#define ull unsigned long long
using namespace std;
int n;
int id,p;
multimap<int,int>lst;
int main(){
    scanf("%d",&n);
    lst.insert(make_pair(1000000000,1));
    for(int i=1;i<=n;i++){
        cin>>id>>p;
        auto it=lst.insert(make_pair(p,id));
        cout<<id<<' ';
        if(it!=lst.begin()&&it!=--lst.end()){
            auto it_1=it;
            auto it_2=it;
            it_1--;
            it_2++;
            if(abs(it_1->first-p)<=abs(it_2->first-p)){
                cout<<it_1->second<<endl;
            }
            else cout<<it_2->second<<endl;
        }   
        else if(it==lst.begin()){
            cout<<(++it)->second<<endl;
        }
        else if(it==--lst.end()){
            cout<<(--it)->second<<endl;
        }
    }
    system("pause");
    return 0;
}
```
# F:冷血格斗场
## 描述
为了迎接08年的奥运会，让大家更加了解各种格斗运动，facer新开了一家冷血格斗场。格斗场实行会员制，但是新来的会员不需要交入会费，而只要同一名老会员打一场表演赛，证明自己的实力。

我们假设格斗的实力可以用一个非负整数表示，称为实力值，两人的实力值可以相同。另外，每个人都有一个唯一的id，也是一个正整数。为了使得比赛更好看，每一个新队员都会选择与他实力最为接近的人比赛，即比赛双方的实力值之差的绝对值越小越好，如果有多个人的实力值与他差别相同，则他会选择id最小的那个。

不幸的是，Facer一不小心把比赛记录弄丢了，但是他还保留着会员的注册记录。现在请你帮facer恢复比赛纪录，按照时间顺序依次输出每场比赛双方的id。

## 输入
第一行一个数n(0 < n <=100000)，表示格斗场新来的会员数（不包括facer）。以后n行每一行两个数，按照入会的时间给出会员的id和实力值。一开始，facer就算是会员，id为1，实力值1000000000。

## 输出
N行，每行两个数，为每场比赛双方的id，新手的id写在前面。

## 样例输入
```
3
2 3
3 1
4 2
```
## 样例输出
```
2 1
3 2
4 2
```
# Solution
本题的重点在于，如果有多个人的实力值和他相同，那么，它会选择id最小的那个  
意思是，对于后输入的，如果后输入的id比前面的小，那么前面的就没有意义了（有点像优先队列？）  
所以，我们只需维护一个map，因为在上述说法下不会存在冲突  
下面看代码:
```
#include<bits/stdc++.h>
#define ll long long
#define ull unsigned long long
using namespace std;
int n,id,p;
map<int,int>ma;
int main(){
    scanf("%d",&n);
    ma[1000000000]=1;
    for(int i=1;i<=n;i++){
        cin>>id>>p;
        cout<<id<<' ';
        auto it=ma.find(p);
        if(it!=ma.end()) {
            cout<<ma[p]<<endl;
            ma[p]=min(id,ma[p]);
            continue;
        }
        else ma[p]=id;
        it=ma.find(p);
        if(it!=ma.begin()&&it!=--ma.end()){
            auto it_1=it;
            auto it_2=it;
            it_1--;
            it_2++;
            if(abs(it_1->first-p)<abs(it_2->first-p)){
                cout<<it_1->second<<endl;
            }
            else if(abs(it_1->first-p)==abs(it_2->first-p)){
                cout<<min(it_1->second,it_2->second)<<endl;
            }
            else cout<<it_2->second<<endl;
        }
        else if(it==ma.begin()){
            cout<<(++it)->second<<endl;
        }
        else if(it==--ma.end()){
            cout<<(--it)->second<<endl;
        }
    }
    system("pause");
    return 0;
}
```
# G:Priority_queue 练习题
## 描述
我们定义一个正整数a比正整数b优先的含义是：
*a的质因数数目（不包括自身）比b的质因数数目多；  
*当两者质因数数目相等时，数值较大者优先级高。  

现在给定一个容器，初始元素数目为0，之后每次往里面添加10个元素，每次添加之后，要求输出优先级最高与最低的元素，并把该两元素从容器中删除。

## 输入
第一行: num (添加元素次数，num <= 30)

下面10*num行，每行一个正整数n（n < 10000000).

## 输出
每次输入10个整数后，输出容器中优先级最高与最低的元素，两者用空格间隔。

## 样例输入
```
1
10 7 66 4 5 30 91 100 8 9
```
## 样例输出
```
66 5
```
# Solution
本题没叫你用优先队列，那你可以不用啊哈哈  
所以我们用set来完成 虽然multiset也可以，但是set可以去除不必要的元素，所以使用set  
同样，这里要说明的是，我们到目前使用仿函数还是比较少的，所以这里要注意一下  
然后就是仿函数类这里要注意，要加上一个const 因为新版本编译器要求更为严格，需要cmp通过静态函数变量形式被调用，所以不加const会报错  
```
#include<bits/stdc++.h>
#define ll long long
#define ull unsigned long long
#define lowbit(x) (x&(-x))
using namespace std;
bool isprime(int x){
    if(x==1) return false;
    if(x==2) return true;
    for(int i=2;i*i<=x;i++){
        if(x%i==0) return false;
    }
    return true;
} 
int count(int x){
    int ans=0;
    for(int i=1;i<x;i++){
        if(x%i!=0) continue;
        if(isprime(i)) ans++;
    }
    return ans;
}
struct node{
    int num,rnum;
};
struct cmp{
    bool operator()(const node a,const node b)const{
        if(a.rnum==b.rnum) return a.num<b.num;
        return a.rnum<b.rnum;
    }
};
int main(){
    int n,k;
    cin>>n;
    set<node,cmp>queue;
    for(int i=1;i<=n;i++){
        for(int j=1;j<=10;j++){
            cin>>k;
            node a;
            a.num=k;
            a.rnum=count(k);
            queue.insert(a);
        }
        auto it=queue.end();it--;
        cout<<(*it).num<<' ';
        auto it_2=queue.begin();
        cout<<(*it_2).num<<endl;
        queue.erase(it);queue.erase(it_2);
    }
    system("pause");
    return 0;
}
```
# H:编程填空：数据库内的学生信息
## 描述
程序填空，使得下面的程序,先输出
```
(Tom,80),(Tom,70),(Jone,90),(Jack,70),(Alice,100),

(Tom,78),(Tom,78),(Jone,90),(Jack,70),(Alice,100),

(70,Jack),(70,Tom),(80,Tom),(90,Jone),(100,Alice),

(70,Error),(70,Error),(80,Tom),(90,Jone),(100,Alice),

******
```

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
比如 vector<vector<int>> 有可能出错，要改成 vector<vector<int> >

2) 在模板中写迭代器时，最好在前面加上 typename关键字，否则可能会编译错。VS可能无此问题，但是Dev C++和服务器上的编译环境会有这个问题。  
# Solution
我们通过报错可以发现，这题需要我们定义一个模板类了，但是，对于pred（谓词，返回一个bool型变量），前面是有缺省的，所以我们需要一个greater来顶一下  
剩下的其实要说的不多，还有就是，这个public的第一行是因为，下面代码中的iterator类缺少了定义，我们需要把它称作一个新的名字  
然后，这个输出函数要写在外面，因为输出的应该是对于外部函数而言的，而不是类变量  
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
	multimap<T1,T2,Pred>ma;
public:
	typedef typename multimap<T1,T2,Pred>::iterator iterator;
	MyMultimap(){
		ma.clear();
	}
	void insert(pair<T1,T2>x){
		ma.insert(x);
	}
	auto begin(){
		return ma.begin();
	}
	auto end(){
		return ma.end();
	}
	void Set(T1 x,T2 y){
		for(auto it=ma.begin();it!=ma.end();it++){
			if(it->first==x) it->second=y;
		}
	}
	void clear(){
		ma.clear();
	}
	auto find(T1 x){
		return ma.find(x);
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