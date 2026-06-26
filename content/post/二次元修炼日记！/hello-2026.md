---
title: "Hello 2026"
slug: hello-2026
date: 2026-01-07
seriesOrder: 0
encrypt: false
hidden: true
image: "/images/anime-diary/5.png"
---

## B
题目大意：给定一个长度为 $n$ 的数组 $a$，以及一个整数 $k$。令 $f(l, r)$ 表示 $\operatorname{mex}(a_l,a_{l+1},\ldots,a_r)$ $^\text{∗}$ 的值。需要进行如下操作 $n-k+1$ 次： - 设当前序列长度为 $|a|$。需要找到一个长度为 $k$ 的区间 $[l, r]$，使得 $\operatorname{max}_{i=1}^{|a|-k+1} f(i, i+k-1) = f(l, r)$。换句话说，需要在所有长度为 $k$ 的窗口中，选择一个 $\operatorname{mex}$ 最大的窗口 $[l, r]$。如果有多个符合条件的区间 $[l, r]$，可以任选其一。

数据范围：$1 \le t \le 10^4$，$2\leq k \leq n \leq 2\cdot 10^5$，$0\leq a_i \leq n$，$\sum n \le 2\cdot 10^5$。

思路：

```cpp
void solve() {
    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    for (int i = 0; i <= n - 1; i++) cin >> a[i];
    map<int, int> ma;
    for (int p : a) ma[p]++;
    int cnt = 0;
    if (!ma.count(0)) {
        cout << 0 << endl;
        return;
    }
    for (auto [x, y] : ma) {
        if (x == cnt)
            cnt++;
        else
            break;
        if (cnt == k - 1) break;
    }
    cout << cnt << endl;
    return;
}
```

## C
题目大意：战争爆发了！你作为国家的最高将领，必须制定战略部署你的军队。有 $n$ 个基地排成一行，第 $k$ 个基地是你的主基地。最开始，只有一个士兵驻扎在第 $k$ 个基地。每天按照如下顺序发生： - 你下达命令，选择一个基地 $i$（$1 \leq i \leq n$），并选择该基地内任意数量的士兵（可以为 $0$，也可以为该基地全部士兵），然后命令这些士兵全部向相同方向移动：要么移动到 $i-1$ 号基地，要么移动到 $i+1$ 号基地。没有士兵能够移动到 $1$ 号基地的左侧或 $n$ 号基地的右侧。- 之后，会有一名新的士兵加入到第 $k$ 个基地。这名士兵不能被当天的命令调动。不过时间紧迫，距离敌军进攻只剩下 $m$ 天。

数据范围：$1 \le t \le 10^4$，$1 \leq k \leq n \leq 10^5$，$1 \leq m \leq 10^9$，$\sum n \le 2 \cdot 10^5$。

思路：

```cpp
void solve() {
    int n, m, k;
    cin >> n >> m >> k;
    int l = k - 1, r = n - k;
    if (l > r) swap(l, r);
    if (max(2 * r - 1 + l, l + 2 * r - 1) <= m) {
        cout << n << endl;
        return;
    }
    int tem = 0;
    int tem2 = 0;
    int t = min(l, (m + 1) / 3);
    tem = t + 1 + min(r, (m + 1 - t) / 2);
    cout << tem << endl;
    return;
}
```

## D1
题目大意：这是本题的 Easy 版本，两个版本的区别在于本版本只要求你求出最小操作次数。只有当你解决了所有版本后才能进行 Hack。给定一棵以 $1$ 号点为根的树 $^{\text{∗}}$，共 $n$ 个顶点，编号为 $1$ 到 $n$，每个顶点初始都是白色。定义 $d_i$ 为 $i$ 号顶点到根节点的距离。你可以执行任意次如下操作： 1. 选择一个白色顶点的子集 $S$，满足子集中没有两个节点有边直接连接，且没有两个节点到 $1$ 号节点的距离相等。形式化地说，对于 $S$ 中任意 $x,y$ 且 $x\ne y$，有 $d_x\ne d_y$，且 $x$ 和 $y$ 之间没有边直接连接。2. 将 $S$ 中的所有顶点染成黑色。

数据范围：$1\le t\le 10^4$，$2\le n\le 2\cdot 10^5$，$1\le u_i,v_i\le n$，$\sum n \le 2\cdot 10^5$。

思路：

```cpp
void solve() {
    int n;
    cin >> n;
    int x, y;
    vector<vector<int>> ma(n);
    for (int i = 0; i < n - 1; i++) {
        cin >> x >> y;
        ma[x - 1].push_back(y - 1);
        ma[y - 1].push_back(x - 1);
    }
    map<int, int> s;
    int maxx2 = INT_MIN;
    auto dfs = [&](this auto&& dfs, int x, int pa, int d) -> void {
        s[d]++;
        if (x == 0)
            maxx2 = max(maxx2, (int)ma[0].size() + 1);
        else
            maxx2 = max(maxx2, (int)ma[x].size());
        for (auto p : ma[x]) {
            if (p == pa) continue;
            dfs(p, x, d + 1);
        }
        return;
    };
    dfs(0, -1, 0);
    int maxx = INT_MIN;
    for (auto [x, y] : s) {
        maxx = max(maxx, y);
    }
    cout << max(maxx2, maxx) << endl;
    return;
}
```

## D2
题目大意：这是该问题的 Hard 版本。不同之处在于，本题中你不仅需要求出最少操作次数，还需要输出一种达到该次数的染色方案。只有在你完成了所有版本的题目的情况下，才可以进行 Hack。给定一棵 $n$ 个顶点的有根树 $^{\text{∗}}$，顶点编号为 $1$ 到 $n$，根节点编号为 $1$，所有顶点初始时均为白色。定义 $d_i$ 为根到第 $i$ 个顶点的距离。你可以进行如下操作任意多次： 1. 选择一组白色顶点组成的集合 $S$，要求集合内任意两个节点都不通过边相连，且到根节点的距离均不相同。即对任意 $x, y \in S$ 且 $x \neq y$，有 $d_x \neq d_y$ 且 $x$ 和 $y$ 间没有直接的边相连。

数据范围：$1 \leq t \leq 10^4$，$2 \leq n \leq 2 \cdot 10^5$，$1 \leq u_i,v_i \leq n$，$\sum n \le 2 \cdot 10^5$。

思路：

```cpp
void solve() {
    int n, x, y;
    cin >> n;
    vvi ma(n);
    rep(i, 1, n - 1) {
        cin >> x >> y;
        ma[x - 1].push_back(y - 1);
        ma[y - 1].push_back(x - 1);
    }
    map<int, int> s;
    map<int, map<int, vi>> s2;
    int maxx = INT_MIN;
    vector<pii> tem(n);
    vi depth(n);
    auto dfs = [&](this auto&& dfs, int x, int pa, int d) -> void {
        s[d]++;
        depth[x] = d;
        int cnt = 0;
        tem[x].first = pa;
        for (int& p : ma[x]) {
            if (p == pa) continue;
            cnt++;
            dfs(p, x, d + 1);
        }
        if (s.count(d + 1) && cnt == s[d + 1])
            maxx = max(maxx, cnt + 1);
        else
            maxx = max(maxx, cnt);
        return;
    };
    dfs(0, -1, 0);
    for (auto& [x, y] : s) {
        maxx = max(maxx, y);
    }
    cout << maxx << endl;
    int md = sz(s);
    vvi ma2(md);
    rep(i, 0, n - 1) ma2[depth[i]].push_back(i);
    tem[0].second = 0;
    rep(i, 1, md - 1) {
        sort(all(ma2[i]), [&](const int& x, const int& y) { return tem[tem[x].first].second < tem[tem[y].first].second; });
        vector<bool> vis(maxx, false);
        rep(j, 0, sz(ma2[i]) - 1) { vis[(tem[tem[ma2[i][j]].first].second - j + maxx) % maxx] = true; }
        int idx = 0;
        while (vis[idx]) idx++;
        rep(j, 0, sz(ma2[i]) - 1) { tem[ma2[i][j]].second = (j + idx + maxx) % maxx; }
    }
    vvi res(maxx);
    rep(i, 0, n - 1) { res[tem[i].second].push_back(i); }
    for (auto& p : res) {
        cout << sz(p) << endl;
        for (auto& q : p) cout << q + 1 << ' ';
        cout << endl;
    }
    return;
}
```

## E
题目大意：给定一个长度为 $n$ 的序列 $a$ 和一个正整数 $m$。序列 $a$ 的每个元素都是 $[0, m]$ 范围内的整数。当且仅当以下两个条件都满足时，序列 $a$ 被认为是好的： - $a_1 < a_2 < a_3 < \ldots < a_n$； - $\frac{1}{\operatorname{lcm}(a_1,a_2)}+\frac{1}{\operatorname{lcm}(a_2,a_3)}+\ldots+ \frac{1}{\operatorname{lcm}(a_{n-1},a_n)}+{\color{red}\frac{1}{\operatorname{lcm}(a_n,a_1)}}\ge 1$。

数据范围：$1 \le t \le 1000$，$2 \le n \le m \le 3000$，$0 \le a_i \le m$，$\sum m \le 3000$。

思路：

```cpp
constexpr int MOD = 998244353;
constexpr int MX = 1e5 + 1;
ll F[MX];      // 预处理阶乘
ll INV_F[MX];  // 预处理逆元
ll qpow(ll x, int n) {
    ll res = 1;
    for (; n; n >>= 1) {
        if (n % 2) res = res * x % MOD;
        x = x * x % MOD;
    }
    return res;
}
auto init = [] {
    F[0] = 1;
    for (int i = 1; i < MX; i++) F[i] = F[i - 1] * i % MOD;  // 预处理阶乘
    INV_F[MX - 1] = qpow(F[MX - 1], MOD - 2);
    for (int i = MX - 1; i; i--) {
        INV_F[i - 1] = INV_F[i] * i % MOD;
    }  // 预处理逆元
    return 0;
}();
// 计算C(n,m),即从n个数中取m个数
ll comb(int n, int m) { return m < 0 || m > n ? 0 : F[n] * INV_F[m] % MOD * INV_F[n - m] % MOD; }
void solve() {
    int n, m;
    cin >> n >> m;
    auto lcm = [&](int x, int y) {
        int tem = __gcd(x, y);
        return x / tem * y;
    };
    vi a(n);
    rep(i, 0, n - 1) cin >> a[i];
    if (a[0] != 0 && a[0] != 1) {
        cout << 0 << endl;
        return;
    }
    if (a[1] != 0 && a[1] != 2) {
        cout << 0 << endl;
        return;
    }
    a[0] = 1;
    a[1] = 2;
    vvi dp(n, vi(m + 1));
    ll ans = 0;
    dp[0][1] = 1;
    dp[1][2] = 1;
    rep(i, 2, n - 1) {
        if (a[i] == 0) {
            rep(j, 1, m) {
                for (int k = 1; (k + 1) * j <= m; k++) {
                    dp[i][(k + 1) * j] += dp[i - 1][k * j] % MOD;
                    dp[i][(k + 1) * j] %= MOD;
                }
            }
        } else {
            rep(j, 1, a[i] - 1) {
                if (__gcd(a[i], j) == a[i] - j) {
                    dp[i][a[i]] += dp[i - 1][j] % MOD;
                    dp[i][a[i]] %= MOD;
                }
            }
        }
    }
    rep(i, 1, m) {
        ans += dp[n - 1][i] % MOD;
        ans %= MOD;
    }
    cout << ans << endl;
    return;
}
```
