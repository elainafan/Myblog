---
title: 欧拉反演与莫比乌斯反演
date: 2026-05-07
encrypt: false
image: "/images/13.jpg"
categories:
    - 算法
---

## 前言

其实不想更新，本期来自bupt算法皇后、本硕acm兼推理加速第一人、数据结构专家、华为天之骄子L女士的催更。

之前写 [CF1900D Small GCD](https://codeforces.com/problemset/problem/1900/D) 的时候，做到一半就卡住了，属于是看着式子发呆了三分钟，呜呜。

题目本身看起来只是一个很普通的 $\gcd$ 贡献，排序之后也很自然地可以变成

$$
\sum\limits_{i=2}^{n}(n-i)\sum\limits_{j=1}^{i-1}\gcd(a_j,a_i)
$$

好了，到这里就不会了，我开始宕机，脑袋上仿佛出现了一个“Loading...”的小气泡。

因为如果直接枚举前面的 $j$，显然是 $O(n^2)$，而这题的 $\sum n$ 是 $8\cdot 10^4$，肯定不可能这样写。于是启动补题模式，介绍一种求公因数贡献和的常见方法：欧拉反演。

顺便也把莫比乌斯反演放在一起整理一下。它们两个经常一起出现，但在 CF 里的手感其实不太一样：欧拉反演更常用来算 $\gcd$ 的值，莫比乌斯反演更常用来把“倍数统计”还原成“恰好统计”。

## 欧拉反演

首先要知道一个非常经典的式子，看起来有点像小魔法，不过它其实还挺乖的：

$$
\sum\limits_{d\mid n}\phi(d)=n
$$

其中 $\phi(d)$ 是欧拉函数，表示 $1\sim d$ 中与 $d$ 互质的数的个数。

这个式子的证明也比较自然。对于 $1\sim n$ 中的每一个数 $x$，设 $\gcd(x,n)=g$，那么可以写成 $x=gk$，并且 $\gcd(k,\frac{n}{g})=1$。因此对于每一个 $\frac{n}{g}$，会贡献 $\phi(\frac{n}{g})$ 个数，加起来刚好就是 $n$。

不过做题的时候更重要的是，把 $n$ 替换成 $\gcd(x,y)$，于是有，真正好用的地方要来了：

$$
\gcd(x,y)
=\sum\limits_{d\mid \gcd(x,y)}\phi(d)
=\sum\limits_{d\mid x, d\mid y}\phi(d)
$$

也就是说，两个数的最大公因数，可以看成它们所有公共因子的欧拉函数贡献和。

这个东西就非常好用了，因为 $d\mid x$ 这样的条件可以通过枚举因子或者枚举倍数维护，而 $\gcd(x,y)$ 本身不好在线统计。也就是说，把不太听话的 $gcd$ 拆成一堆乖乖排队的因子，事情就突然好做起来了。

## [CF1900D Small GCD](https://codeforces.com/problemset/problem/1900/D)

题目大意：

给定一个长度为 $n$ 的数组 $a$，对于所有三元组 $(i,j,k)$，求三元组中较小两个数的 $\gcd$ 之和。

数据范围：

$3\leq n$，$\sum n\leq 8\cdot 10^4$，$1\leq a_i\leq 10^5$。

思路：

首先考虑排序。排序之后，如果固定 $a_i$ 作为三元组中的第二小值，那么左边选择一个 $a_j$，右边选择一个比它大的数即可。

因此它的贡献为

$$
(n-i)\sum\limits_{j=1}^{i-1}\gcd(a_j,a_i)
$$

这里下标按照 $1$ 开始写，代码里当然是 $0$ 开始，注意不要被自己绕晕了。

那么问题就变成了，枚举到 $a_i$ 的时候，怎么快速计算

$$
\sum\limits_{j=1}^{i-1}\gcd(a_j,a_i)
$$

使用欧拉反演展开：

$$
\begin{aligned}
\sum\limits_{j=1}^{i-1}\gcd(a_j,a_i)
&=\sum\limits_{j=1}^{i-1}\sum\limits_{d\mid a_j, d\mid a_i}\phi(d)\\\\
&=\sum\limits_{d\mid a_i}\phi(d)\sum\limits_{j=1}^{i-1}[d\mid a_j]
\end{aligned}
$$

于是只需要维护 $cnt_d$，表示前面已经出现过的数里，有多少个可以被 $d$ 整除。

那么对于当前的 $a_i$，枚举它的所有因子 $d$，答案加上

$$
(n-i)\cdot \phi(d)\cdot cnt_d
$$

然后再把 $a_i$ 的所有因子对应的 $cnt_d$ 加一即可。

这里其实就是把“枚举前面的数”换成了“枚举当前数的因子”，因为 $a_i\leq 10^5$，所以因子个数不会很多，放心放心。

代码：

```cpp
constexpr int MX = 1e5 + 1;
int phi[MX];

auto init = [] {
    auto Phi = [](int n) -> int {
        int res = n;
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                res = res / i * (i - 1);
                while (n % i == 0) {
                    n /= i;
                }
            }
        }
        if (n > 1) res = res / n * (n - 1);
        return res;
    };
    rep(i, 1, MX - 1) { phi[i] = Phi(i); }
    return 0;
}();

vector<int> divisors[MX];
auto init2 = [] {
    for (int i = 1; i < MX; i++) {
        for (int j = i; j < MX; j += i) {
            divisors[j].push_back(i);
        }
    }
    return 0;
}();

void solve() {
    int n;
    cin >> n;
    vi a(n);
    rep(i, 0, n - 1) cin >> a[i];

    ll ans = 0;
    ranges::sort(a);
    vi cnt(MX + 1);

    rep(i, 0, n - 1) {
        for (int& p : divisors[a[i]]) {
            ans += 1LL * (n - 1 - i) * phi[p] * cnt[p];
        }
        for (int& p : divisors[a[i]]) {
            cnt[p]++;
        }
    }
    cout << ans << endl;
}
```

总的时间复杂度大概是 $O(V\log V+n\sqrt V)$，不过实际上因为枚举的是预处理出的因子，跑得还是很舒服的。

这道题最核心的一步就是

$$
\gcd(x,y)=\sum\limits_{d\mid x, d\mid y}\phi(d)
$$

只要把这个式子看出来，后面基本就是维护计数了，算是很典型的 $gcd$ 贡献题。第一次见可能会觉得“这怎么想到的”，但是见多了就会发现它真的经常在门口等着你，就好像玲奈子在外面被xxx回家看到遥奈一样（什么比喻）。

## 莫比乌斯反演

然后我们介绍莫比乌斯反演。

莫比乌斯函数定义为

$$
\mu(n)=
\begin{cases}
1,&n=1,\\\\
0,&n\text{ 含有平方因子},\\\\
(-1)^k,&n\text{ 为 }k\text{ 个不同质数的乘积}.
\end{cases}
$$

它最重要的性质是

$$
\sum\limits_{d\mid n}\mu(d)=[n=1]
$$

于是可以得到一个判断互质的式子：

$$
[\gcd(x,y)=1]
=\sum\limits_{d\mid \gcd(x,y)}\mu(d)
=\sum\limits_{d\mid x, d\mid y}\mu(d)
$$

这个式子经常用于“统计互质数对”。

另一种更常见的形式是，假设 $F(d)$ 表示 $\gcd$ 恰好为 $d$ 的数对个数，$G(d)$ 表示 $\gcd$ 是 $d$ 的倍数的数对个数，那么显然有

$$
G(d)=\sum\limits_{k\geq 1}F(kd)
$$

于是可以反演得到

$$
F(d)=\sum\limits_{k\geq 1}\mu(k)G(kd)
$$

当然在写代码的时候，我一般不会真的把这个式子写出来，而是倒着枚举倍数：

$$
F(d)=G(d)-\sum\limits_{k\geq 2}F(kd)
$$

这样写更像容斥，也更不容易写挂。毕竟显式写 $\mu$ 的时候，我很容易把下标看反，然后开始 debug 到怀疑人生。

## [CF1884D Counting Rhyme](https://codeforces.com/problemset/problem/1884/D)

题目大意：

给定一个数组 $a_1,\ldots,a_n$，统计有多少对 $(i,j)$ 满足不存在某个数组中的数 $a_k$，使得 $a_k\mid \gcd(a_i,a_j)$。

数据范围：

$1\leq a_i\leq n$，$\sum n\leq 10^6$。

思路：

首先设

$$
C(d)=|\{i:d\mid a_i\}|
$$

那么 $\gcd(a_i,a_j)$ 是 $d$ 的倍数的数对数量为

$$
G(d)=\binom{C(d)}{2}
$$

接着，我们想求 $\gcd(a_i,a_j)$ 恰好等于 $d$ 的数量 $F(d)$。因为

$$
G(d)=\sum\limits_{k\geq 1}F(kd)
$$

所以倒着枚举 $d$，把倍数的贡献扣掉即可。

其中 $cnt[d]$ 表示数组中有多少个数是 $d$ 的倍数。这个小数组看起来朴素，但是在倍数题里非常能干，属于默默搬砖型选手。

然后考虑哪些 $d$ 是不合法的。如果存在一个数组中的数 $x$，满足 $x\mid d$，那么所有 $\gcd$ 恰好为 $d$ 的数对都不合法。

于是枚举出现过的 $x$，标记它的所有倍数即可。

最后答案就是所有数对数量，减去不合法的 $F(d)$。

整体放进 `solve()` 里大概长这样：

```cpp
void solve() {
    int n;
    cin >> n;
    vector<int> a(n);
    vector<int> freq(n + 1), cnt(n + 1), exact(n + 1);
    vector<int> bad(n + 1);

    for (int& x : a) {
        cin >> x;
        freq[x]++;
    }

    for (int d = 1; d <= n; d++) {
        for (int x = d; x <= n; x += d) {
            cnt[d] += freq[x];
        }
    }

    for (int d = n; d >= 1; d--) {
        exact[d] = 1LL * cnt[d] * (cnt[d] - 1) / 2;
        for (int k = d + d; k <= n; k += d) {
            exact[d] -= exact[k];
        }
    }

    for (int x = 1; x <= n; x++) {
        if (!freq[x]) continue;
        for (int y = x; y <= n; y += x) {
            bad[y] = true;
        }
    }

    ll ans = 1LL * n * (n - 1) / 2;
    for (int d = 1; d <= n; d++) {
        if (bad[d]) ans -= exact[d];
    }
    cout << ans << endl;
}
```

这道题的主要感觉就是：先把“$gcd$ 是 $d$ 的倍数”统计出来，再反演出“$gcd$ 恰好等于 $d$”。这和 Small GCD 里的欧拉反演不太一样，Small GCD 是在算 $\gcd$ 的权值，而这题是在分离每一个 $\gcd$ 值对应的数对。

## 两个东西怎么区分

最后简单总结一下，防止下次又忘了。

如果题目要求的是很多个 $\gcd$ 的和，比如

$$
\sum \gcd(x,y)
$$

那么优先考虑欧拉反演：

$$
\gcd(x,y)=\sum\limits_{d\mid x, d\mid y}\phi(d)
$$

如果题目要求的是互质、$\gcd$ 恰好等于某个值，或者要从倍数统计还原精确统计，那么优先考虑莫比乌斯反演：

$$
[\gcd(x,y)=1]=\sum\limits_{d\mid x, d\mid y}\mu(d)
$$

或者写成倒着枚举倍数的形式：

$$
F(d)=G(d)-\sum\limits_{k\geq 2}F(kd)
$$

顺便一提，欧拉函数本身也可以用莫比乌斯函数写出来：

$$
\phi(n)=\sum\limits_{d\mid n}d\cdot \mu\left(\frac{n}{d}\right)
$$

所以这两个东西并不是完全分开的，只是做题时的切入点不同。

总的来说，看到 $\gcd$ 贡献题，先不要急着枚举数对，先想一下能不能枚举因子；看到“恰好”和“互质”，就想一下能不能先统计倍数，再用莫比乌斯反演容斥回来。

这里先记到这里。感觉数论题很多时候就是这样，第一次看很玄学，第二次看有点板，第三次就开始怀疑自己为什么第一次没看出来了。好吧，先和反演和解一下，下次再见到 $gcd$ 就不要装作不认识它了。

鸣谢：赛博Elainafan替身与丘比