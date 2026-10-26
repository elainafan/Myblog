---
title: 2026CCPC Reg长春
slug: ccpc-2026-reg-changchun
date: 2026-10-26
encrypt: false
seriesOrder: 1
hidden: true
image: "/images/my-internet-addiction/cover.png"
categories:
    - 算法
    - 数学
---
## A
题目大意：给定一个 $n$ 行 $m$ 列的矩阵 $a_{ij}$ ，可以进行若干次的以下操作：选择 $1 \leq l \leq r \leq m$ ，然后选择 $1 \leq p_l \leq p_{l+1} \ldots p_r \leq m$ ，将矩阵中坐标为 $(p_l),(p_{l+1},l+1),\ldots,(p_r,r)$ 的元素减一，请求出将整个矩阵归零的最少操作次数。

数据范围： $1 \leq \sum(mn) \leq 10^6$

思路：猜猜的签到题。首先考虑到一个元素能被减一，其贡献当且仅当其左上角能被贡献的次数，否则要以它为起点重新开始减，于是考虑左边能剩下多少，不难发现，左边能减到它的次数，至多为它左侧一列上方的前缀和，于是取这列的最大的最大值，也就是需要从这列开始减的最大值，然后加上即可。

```cpp
void solve() {
    ll n, m;
    cin >> n >> m;
    vvl ma(n, vl(m));
    rep(i, 0, n - 1) { rep(j, 0, m - 1) cin >> ma[i][j]; }
    vvl pre(n, vl(m));
    ll ans = 0;
    pre[0][0] = ma[0][0];
    rep(i, 1, n - 1) pre[i][0] = pre[i - 1][0] + ma[i][0];
    ans = pre[n - 1][0];
    rep(j, 1, m - 1) {
        pre[0][j] = ma[0][j];
        ll mx = max(0LL, pre[0][j] - pre[0][j - 1]);
        rep(i, 1, n - 1) {
            pre[i][j] = pre[i - 1][j] + ma[i][j];
            mx = max(mx, pre[i][j] - pre[i][j - 1]);
        }
        ans += mx;
    }
    cout << ans << endl;
    return;
}
```

## C
题目大意：首先，选择某个长度为 $k$ 的数组 $a$ ，使得 $a$ 是 $[1,2,\ldots,k]$ 的某个循环位移，接着将这段数组一直重复，截取前 $n$ 个元素得到数组 $b$ ，现在给定 $b'$ 跟 $k$ ， $b'$ 是 $b$ 通过将任意下标上元素修改为任意数字进行若干次后得出的，请求出从 $b$ 到 $b'$ 的最小可能修改次数。

数据范围： $2 \leq k \leq n \leq 2 \cdot 10^5, 1 \leq b'_i \leq 10^9$

思路：签到题。可以考虑枚举未被修改的元素，它们的偏移量相同，使用一个大小为 $k$ 的桶计数即可，最后考虑取出最多的未被修改元素数即可。

```cpp
void solve() {
    ll n, k;
    cin >> n >> k;
    vl a(n);
    rep(i, 0, n - 1) cin >> a[i], a[i]--;
    vl cnt(k);
    rep(i, 0, n - 1) {
        if (a[i] >= k) continue;
        cnt[(a[i] - i % k + k) % k]++;
    }
    cout << n - *max_element(all(cnt)) << endl;
    return;
}
```

## E
题目大意：给定 $n$ 和 $a_1,a_2,a_3,a_1+a_2+a_3=n-1$ ，请构造一个排列 $p$ 跟一棵树 ，使得 $p$ 中， 树上 $dis({p_i},p_{i+1})$ 为 $k=1,2,3$ 的 $p_i$ 数分别为 $a_1,a_2,a_3$ 。

数据范围： $8 \leq n \leq 2 \cdot 10^5,0 \leq a_1,a_2,a_3 \leq n-1, a_1+a_2+a_3=n-1$

思路：自己补的时候没有做出来，果然 adhoc 里还是最不会构造题。

这题考察一种常用思路，就是考虑归纳法，也就是说，考虑从 $n$ 变为 $n+1$ 的变化。

首先发现，如果存在一条长度为 $2$ 的链，记为 $x-y-z,x$ 是最新的节点 ，那么此时新来了一个 $1$ ，就把新节点接在 $x$ 上，随后更新 $x,y,z$ 为 $u,x,y$ ，如果新来了一个 $2$ ，就把新节点接在 $y$ 上，随后更新 $x,y,z$ 为 $u,y,x$ ，如果新来了一个 $3$ ，就把新节点接在 $z$ 上，随后更新 $x,y,z$ 为 $u,z,y$ ，就这样。

然后就是一堆繁琐的讨论了，这里不讲。

```cpp
void solve() {
    ll n;
    cin >> n;
    vl a(3);
    rep(i, 0, 2) cin >> a[i];
    if (a[0] == 0 && a[1] == n - 1 && a[2] == 0) {
        cout << -1 << endl;
        return;
    }
    vector<pll> edges;
    ll x, y, z;
    vl p;
    if (a[0] >= 2) {
        edges.emplace_back(1, 2), edges.emplace_back(2, 3);
        p.emplace_back(1), p.emplace_back(2), p.emplace_back(3);
        a[0] -= 2;
        x = 3, y = 2, z = 1;
    } else if (a[0] >= 1 && a[1] >= 1) {
        edges.emplace_back(1, 2), edges.emplace_back(1, 3);
        p.emplace_back(1), p.emplace_back(2), p.emplace_back(3);
        a[0]--, a[1]--;
        x = 3, y = 1, z = 2;
    } else if (a[1] >= 2) {
        edges.emplace_back(1, 2), edges.emplace_back(2, 3), edges.emplace_back(3, 4);
        p.emplace_back(2), p.emplace_back(4), p.emplace_back(1), p.emplace_back(3);
        a[1] -= 2, a[2]--;
        x = 3, y = 2, z = 1;
    } else if (a[0] == 1) {
        edges.emplace_back(1, 2), edges.emplace_back(1, 3), edges.emplace_back(3, 4), edges.emplace_back(1, 5);
        edges.emplace_back(2, 6);
        p.emplace_back(2), p.emplace_back(4), p.emplace_back(5), p.emplace_back(6), p.emplace_back(3), p.emplace_back(1);
        a[0]--, a[2] -= 4;
        x = 1, y = 3, z = 4;
    } else if (a[1] == 1) {
        edges.emplace_back(1, 2), edges.emplace_back(1, 3), edges.emplace_back(3, 4), edges.emplace_back(1, 5);
        edges.emplace_back(2, 6), edges.emplace_back(2, 7);
        p.emplace_back(2), p.emplace_back(4), p.emplace_back(5), p.emplace_back(6), p.emplace_back(3), p.emplace_back(7), p.emplace_back(1);
        a[1]--, a[2] -= 5;
        x = 1, y = 2, z = 7;
    } else {
        edges.emplace_back(1, 2), edges.emplace_back(1, 3), edges.emplace_back(3, 4), edges.emplace_back(1, 5), edges.emplace_back(2, 6);
        edges.emplace_back(2, 7), edges.emplace_back(6, 8);
        p.emplace_back(2), p.emplace_back(4), p.emplace_back(5), p.emplace_back(6), p.emplace_back(3), p.emplace_back(7), p.emplace_back(8), p.emplace_back(1);
        a[2] -= 7;
        x = 1, y = 2, z = 6;
    }
    rep(i, 0, 2) {
        rep(j, 0, a[i] - 1) {
            auto cx = x, cy = y, cz = z;
            if (i == 0) {
                edges.emplace_back(sz(p) + 1, x);
                x = sz(p) + 1, y = cx, z = cy;
            } else if (i == 1) {
                edges.emplace_back(sz(p) + 1, y);
                x = sz(p) + 1, y = cy, z = cx;
            } else {
                edges.emplace_back(sz(p) + 1, z);
                x = sz(p) + 1, y = cz, z = cy;
            }
            p.emplace_back(sz(p) + 1);
        }
    }
    for (auto& [x, y] : edges) cout << x << ' ' << y << endl;
    rep(i, 0, n - 1) cout << p[i] << ' ';
    cout << endl;
    return;
}
```

## G

题目大意：给定两个长度为 $n$ 的二进制字符串 $A,B$ ，以及 $m$ 个区间 $[l_i,r_i]$ ，现在给定 $k$ ，每次禁用区间 $[l_k,r_k]$ ，问是否能通过翻转其他未被禁用的区间，使得 $A$ 能变成 $B$ ？ 请分别求出 $k=1,2\ldots,m$ 时的答案。

数据范围： $1 \leq n,m \leq 2 \cdot 10^5$

思路：首先，很显然地，区间变化可以转化为差分。

然后，由于 $A$ 只需要变为 $B$ 即可，因此只关注 $a_i \oplus b_i$ 的结果，记为 $c_i$ ，考虑在 $c_i$ 上做差分。

由于最后的条件要求是 $c$ 全为 $0$ ，因此转化为 $c_0=0$ ，以及差分项全为 $0$ 。

接着由于这里只改变 $diff_l$ 和 $diff_{r+1}$ ，因此可以将他们连边，而一次操作相当于，将两个相连的点上的元素全部翻转。

如果没有禁用，直接问全部的话，那思路就是很 trivial 的，也就是说，每个连通块里的 $1$ 数量都是偶数，可以想一下为什么这个是对的。

然后，遮掉一条边，这时候最容易想到的就是割边，然后考虑边双。如果删掉的边是割边，那么连通块就会分为两个，此时需要考虑两边是否仍然保持 $1$ 数量为偶数这个条件，而边双可以转化为桥树，然后割边分割后，就形成一棵树的子树与它的残余部分，记录一下信息判断即可。如果不是割边，那显然不影响连通性，因此直接判断即可，当然，所有的大条件都是，原图的各个连通块内 $1$ 数量是偶数。

维护比较麻烦就是了。

```cpp
// 边双连通分量 Edge-BCC，无向图，点 0-based
// 依赖 1.cpp 中的宏：rep, sz, vi, vvi, pii
// 思路：先找桥，再忽略桥 DFS 染色。
struct EBCC {
    int n, m, tim, tot;
    vector<vector<pii>> g;  // {to, edge_id}
    vector<pii> edges;      // edges[id] = {u, v}
    vi dfn, low, is_bridge, bel;
    vvi comps;  // comps[i] 是第 i 个边双里的点

    EBCC(int n = 0) { init(n); }

    void init(int n_) {
        n = n_;
        m = tim = tot = 0;
        g.assign(n, vector<pii>());
        edges.clear();
        dfn.assign(n, 0);
        low.assign(n, 0);
        is_bridge.clear();
        bel.assign(n, -1);
        comps.clear();
    }

    int add_edge(int u, int v) {
        edges.push_back({u, v});
        is_bridge.push_back(0);
        g[u].push_back({v, m});
        g[v].push_back({u, m});
        return m++;
    }

    void tarjan(int u, int pe) {
        dfn[u] = low[u] = ++tim;
        for (int i = 0; i < sz(g[u]); i++) {
            int v = g[u][i].first;
            int id = g[u][i].second;
            if (id == pe) continue;
            if (!dfn[v]) {
                tarjan(v, id);
                low[u] = min(low[u], low[v]);
                if (low[v] > dfn[u]) is_bridge[id] = 1;
            } else {
                low[u] = min(low[u], dfn[v]);
            }
        }
    }

    void dfs_comp(int u) {
        bel[u] = tot;
        comps.back().push_back(u);
        for (int i = 0; i < sz(g[u]); i++) {
            int v = g[u][i].first;
            int id = g[u][i].second;
            if (bel[v] != -1 || is_bridge[id]) continue;
            dfs_comp(v);
        }
    }

    vi work() {
        rep(i, 0, n - 1) {
            if (!dfn[i]) tarjan(i, -1);
        }
        rep(i, 0, n - 1) {
            if (bel[i] == -1) {
                comps.push_back(vi());
                dfs_comp(i);
                tot++;
            }
        }
        return bel;
    }

    // 建桥树，要求先 work()
    vvi build_tree() {
        vvi tree(tot);
        rep(id, 0, m - 1) {
            if (!is_bridge[id]) continue;
            int a = bel[edges[id].first];
            int b = bel[edges[id].second];
            tree[a].push_back(b);
            tree[b].push_back(a);
        }
        return tree;
    }

    // 建带原图边编号的桥树，tree[u] 中元素为 {v, edge_id}
    vector<vector<pii>> build_tree_with_edge_id() {
        vector<vector<pii>> tree(tot);
        rep(id, 0, m - 1) {
            if (!is_bridge[id]) continue;
            int a = bel[edges[id].first];
            int b = bel[edges[id].second];
            tree[a].push_back({b, id});
            tree[b].push_back({a, id});
        }
        return tree;
    }
};

// 用法：
// EBCC ebcc(n);
// int id = ebcc.add_edge(u, v); // 无向边，id 是边编号
// vi bel = ebcc.work();         // bel[u] 是 u 所在边双编号
// ebcc.is_bridge[id];           // 这条边是否为桥
// ebcc.comps;                   // 每个边双的点集
// vvi tree = ebcc.build_tree(); // 桥树
// vector<vector<pii>> tree_id = ebcc.build_tree_with_edge_id(); // {to_bcc, 原图边编号}
// 注意：重边不会被误判成桥，因为每条无向边都有独立 edge_id。
void solve() {
    ll n, m, l, r;
    cin >> n >> m;
    string a, b;
    cin >> a >> b;
    vl diff(n + 1);
    vl c(n);
    rep(i, 0, n - 1) c[i] = (a[i] != b[i]);
    diff[0] = c[0];
    rep(i, 1, n) diff[i] = (c[i] ^ c[i - 1]);
    diff[n] = c[n - 1];
    EBCC ebcc(n + 1);
    rep(i, 0, m - 1) {
        cin >> l >> r;
        l--, r--;
        ebcc.add_edge(l, r + 1);
    }
    ebcc.work();
    auto ma = ebcc.build_tree_with_edge_id();
    vl cnt(ebcc.tot), res(m, 1);
    vector<bool> vis(ebcc.tot, false);
    rep(i, 0, n) cnt[ebcc.bel[i]] ^= diff[i];
    auto dfs = [&](this auto&& dfs, int x, int pa) -> void {
        vis[x] = true;
        for (auto& [p, id] : ma[x]) {
            if (p == pa) continue;
            dfs(p, x);
            cnt[x] ^= cnt[p];
            if (cnt[p]) res[id] = 0;
        }
        return;
    };
    bool flag = true;
    rep(i, 0, ebcc.tot - 1) {
        if (vis[i]) continue;
        dfs(i, -1);
        if (cnt[i]) flag = false;
    }
    if (!flag) ranges::fill(res, 0);
    rep(i, 0, m - 1) cout << res[i];
    cout << endl;
    return;
}
```

## I

题目大意：这是一道通信题。

给定一个长度为 $n$ 的二进制字符串，需要把它加密为一个长度不超过 $\lfloor \frac{3}{2}n \rfloor$ 的二进制字符串，其中不能有连续三个字符相同，同时需要保证，能通过新字符串解码出原来的字符串。

数据范围： $1 \leq n \leq 5 \cdot 10^5$

思路：首先很自然地想到，这个条件提醒我们去使用当前字符串中较少的那个字符，随后联想到，把较少的字符编码为两个连续相同字符，较多的字符编码为一个字符，但是此时会发现无法编码哪个是较少，哪个是较多，于是只需通过第一个字符的编码来查看它是较少还是较多。

然后，为了满足三个不相同条件，只需让第一个字符不变，然后后续按照奇偶位分组转化即可，解码也很简单。

```cpp
void solve1() {
    ll n;
    cin >> n;
    string s;
    cin >> s;
    ll cnt0 = 0, cnt1 = 0;
    rep(i, 0, n - 1) {
        if (s[i] == '0')
            cnt0++;
        else
            cnt1++;
    }
    ll idx = 0;
    if (cnt0 < cnt1) idx = 1;
    string res = "";
    ll base = s[0] - '0';
    rep(i, 0, n - 1) {
        if (s[i] == '0' + idx) {
            if (i % 2 == 0)
                res.push_back((char)s[0]);
            else
                res.push_back((char)('0' + (base ^ 1)));
        } else {
            if (i % 2 == 0)
                res.push_back((char)s[0]), res.push_back((char)s[0]);
            else
                res.push_back((char)('0' + (base ^ 1))), res.push_back((char)('0' + (base ^ 1)));
        }
    }
    cout << sz(res) << endl;
    cout.flush();
    cout << res << endl;
    cout.flush();
    return;
}
void solve2() {
    ll n;
    cin >> n;
    string s;
    cin >> s;
    vl tem;
    ll i = 0;
    while (i <= n - 1) {
        ll j = i;
        while (j <= n - 1 && s[j] == s[i]) j++;
        tem.push_back(j - i);
        i = j;
    }
    ll base = s[0] - '0';
    ll m = sz(tem);
    string res = "";
    rep(i, 0, m - 1) {
        if (tem[i] != tem[0])
            res.push_back((char('0' + (base ^ 1))));
        else
            res.push_back(s[0]);
    }
    cout << sz(res) << endl;
    cout.flush();
    cout << res << endl;
    cout.flush();
    return;
}
void solve() {
    int t, q;
    cin >> t >> q;
    while (t--) {
        if (q == 1)
            solve1();
        else
            solve2();
    }
    return;
}
```


## J
题目大意：现在有一个秘密数列 $a$ ，满足 $\forall i, 1 \leq i \leq n, 0 \leq a_i \leq 2^w-1$ ，给出 $m$ 个询问的结果，第 $i$ 个问题的答案为 $a_{x_i} \& a_{y_i}=z_i$ ，需要判断，满足以上询问的数列是否存在，如果存在，它的元素之和的最小可能值是多少。

数据范围： $1 \leq n \leq 2 \cdot 10^5, 0 \leq m \leq 2 \cdot 10^5, 1 \leq w \leq 30$

思路：猜猜的签到，只需知道与条件能提供每个数都有 $z_i$ 这些位，也就是做一下或运算，然后倒回去验证是否满足所有询问，最后由于最小条件不需要引入额外位，所以直接加起来即可。

```cpp
void solve() {
    ll n, m, k, x, y, z;
    cin >> n >> m >> k;
    vector<array<ll, 3>> queries;
    vl a(n);
    rep(i, 0, m - 1) {
        cin >> x >> y >> z;
        x--, y--;
        queries.push_back({x, y, z});
        a[x] |= z, a[y] |= z;
    }
    for (auto& [x, y, z] : queries) {
        if ((a[x] & a[y]) != z) {
            cout << -1 << endl;
            return;
        }
    }
    ll ans = 0;
    rep(i, 0, n - 1) ans += a[i];
    cout << ans << endl;
    return;
}
```


## K
题目大意：有一条长度为 $n$ 的纸带，初始的时候每个格子都是空白的。现在有 $m$ 次操作，每次操作由 $(op,x)$ 表示。对于第 $i$ 次操作，当 $op=0$ 时，将 $[1,x]$ 内的格子都涂成颜色 $i$ ，否则将 $[x,n]$ 内的格子都涂成颜色 $i$ 。

现在有 $q$ 次查询，每次查询给出 $l,r$ ，请求出，从空白纸带开始，只进行 $l,l+1,\ldots,r$ 操作，最后纸带上剩下的颜色数。

数据范围： $1 \leq n \leq 10^9, 1 \leq m,q \leq 10^5$

思路：这题做的时候也没做出来，果然数据结构是一生之敌。

首先，不难想到，当一个颜色 $i$ 能存活，当且仅当后续的所有 $l$ 都小于 $r+1$ ，且视 $op$ 而定还需要考虑什么 $r<\max(r)$ 之类的条件，这样做应该使用单调栈二分也能做，就是比较难写。

事实上，这题也考察了一个比较 trivial 的思路，就是，注意到一个颜色在图中始终维持一整段，且他死后不会复生，因此可以使用一个单调队列维护当前从头到尾的各个颜色段。

同时，还有就是，对于颜色 $i$ ， $[1,i]$ 的操作，必然对它没有影响，因此当查询 $r \gt i$ 时，完全可以查询 $[1,r]$ 下，它是否活着，这就使得我们可以使用树状数组维护前缀和中颜色是否活着，以及把询问挂到 $r$ 上，进行离线询问，于是做完了。

```cpp
template <typename T = long long>
class Tree {
    vector<T> tree;

public:
    // 构造函数：初始化大小为 n 的树状数组，初始所有元素值为 val（外部表现为 0-based）
    Tree(int n, T val = 0) : tree(n + 1) {
        for (int i = 1; i <= n; i++) {
            tree[i] += val;
            int nxt = i + (i & -i);
            if (nxt <= n) {
                tree[nxt] += tree[i];
            }
        }
    }

    // 构造函数：使用给定的 vector 在 O(N) 时间内快速初始化建树
    Tree(const vector<T>& data) {
        int n = data.size();
        tree.resize(n + 1);
        for (int i = 1; i <= n; i++) {
            tree[i] += data[i - 1];  // data是 0-based
            int nxt = i + (i & -i);
            if (nxt <= n) {
                tree[nxt] += tree[i];
            }
        }
    }

    // 单点修改：将 0-based 下标 i 处的元素增加 val
    void add(int i, T val = 1) {
        for (++i; i < sz(tree); i += i & (-i)) {
            tree[i] += val;
        }
    }

    // 前缀求和：计算 0-based 下标区间 [0, i] 内的所有元素之和
    T pre(int i) const {
        T res = 0;
        for (++i; i > 0; i &= i - 1) {
            res += tree[i];
        }
        return res;
    }

    // 区间求和：计算 0-based 下标区间 [l, r] 内的所有元素之和
    T query(int l, int r) const {
        if (r < l) {
            return 0;
        }
        return pre(r) - pre(l - 1);  // 当 l=0 时, pre(-1) 会合理地返回 0
    }

    // 树上二分查找：返回满足前缀和 >= val 的最小 0-based 下标
    int lower_bound(T val) const {
        int w = bit_width(tree.size() - 1);
        int res = 0;
        T s = 0;
        for (int i = w - 1; i >= 0; i--) {
            int nxt = res + (1 << i);
            if (nxt < tree.size() && tree[nxt] + s < val) {
                res += (1 << i);
                s += tree[nxt];
            }
        }
        return res;  // 返回 0-based 下标：内部 1-based 下标为 res + 1，因此 0-based 为 res
    }
};
void solve() {
    ll n, m, q, l, r;
    cin >> n >> m >> q;
    vl res(q);
    vector<pll> ma(m);
    rep(i, 0, m - 1) cin >> ma[i].first >> ma[i].second, ma[i].second--;
    vector<vector<pll>> queries(m);
    rep(i, 0, q - 1) {
        cin >> l >> r;
        l--, r--;
        queries[r].emplace_back(l, i);
    }
    Tree<ll> bit(m);
    deque<trl> dq;
    dq.emplace_back(0, n - 1, -1);
    rep(i, 0, m - 1) {
        auto [op, x] = ma[i];
        if (op == 0) {
            while (!dq.empty() && get<1>(dq.front()) <= x) {
                auto [L, R, id] = dq.front();
                if (id != -1) bit.add(id, -1);
                dq.pop_front();
            }
            if (!dq.empty()) get<0>(dq.front()) = x + 1;
            dq.emplace_front(0, x, i);
        } else {
            while (!dq.empty() && get<0>(dq.back()) >= x) {
                auto [L, R, id] = dq.back();
                if (id != -1) bit.add(id, -1);
                dq.pop_back();
            }
            if (!dq.empty()) get<1>(dq.back()) = x - 1;
            dq.emplace_back(x, n - 1, i);
        }
        bit.add(i, 1);
        for (auto& [l, id] : queries[i]) {
            res[id] = bit.query(l, i);
        }
    }
    for (auto& p : res) cout << p << endl;
    return;
}
```

## M
题目大意：给定数组 $a_1,a_2,\ldots,a_n$ ，定义 $f(l,r,m)=1$ 当且仅当 $a_l,a_{l+1}...a_r$ 在模 $m$ 意义下为回文数组。给定 $M$ ，请求出 $\sum\limits_{1 \leq l \lt r \leq n}\sum\limits_{2 \leq m \leq M}f(l,r,m)$ 。

数据范围： $1 \leq n \leq 8000,2 \leq M \leq 10^6,0 \leq a_i \leq M$ 。

思路：简单题。首先注意到，一个数组是回文数组，那么必然满足 $m \mid abs(a_l-a_r) \ldots$ ，也就是说， $m | gcd(abs(a_l-a_r),\ldots)$ ，从而，可以预处理出，每个 $gcd$ 可以贡献出多少 $m$ ，然后采用中心拓展法，可以在 $O(n^2)$ 复杂度下求出，注意一下预处理时 $0$ 的贡献数。

```cpp
void solve() {
    ll n, m;
    cin >> n >> m;
    vl a(n);
    rep(i, 0, n - 1) cin >> a[i];
    vl cnt(m + 1);
    cnt[0] = m - 1;
    rep(i, 2, m) {
        for (ll j = i; j <= m; j += i) cnt[j]++;
    }
    ll ans = 0;
    rep(i, 0, n - 1) {
        ll cur = 0;
        for (ll l = i - 1, r = i + 1; l >= 0 && r <= n - 1; l--, r++) {
            cur = __gcd(cur, abs(a[l] - a[r]));
            ans += cnt[cur];
            if (cur == 1) break;
        }
    }
    rep(i, 0, n - 1) {
        ll cur = 0;
        for (ll l = i, r = i + 1; l >= 0 && r <= n - 1; l--, r++) {
            cur = __gcd(cur, abs(a[l] - a[r]));
            ans += cnt[cur];
            if (cur == 1) break;
        }
    }
    cout << ans << endl;
    return;
}
```