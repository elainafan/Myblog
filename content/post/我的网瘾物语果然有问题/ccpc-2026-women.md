---
title: 2026CCPC女生赛
slug: ccpc-2026-women
date: 2026-11-04
encrypt: false
seriesOrder: 3
hidden: true
image: "/images/my-internet-addiction/cover.jpg"
categories:
    - 算法
    - 数学
---
## A

八百签到，不讲。

## B
题目大意：给定数组 $a_1,\ldots,a_n$ ，定义某个子序列的不平衡指数为，大于它的均值的数所占的比例，对于整个数组，请输出它所有长度不小于 $2$ 的子序列的不平衡指数的最大值和最小值。

数据范围： $2 \leq n \leq 5 \cdot 10^5$

思路：首先注意到，子序列跟原数组中的顺序完全没有关系。

再发现，当不平衡指数最大，则它必然含有一个原数组中的最小值，当它最小，则必然含有一个原数组中的最大值，而剩下选出来的必然是一个连续段，然后双指针即可。

```cpp
void solve() {
    ll n;
    cin >> n;
    vl a(n);
    rep(i, 0, n - 1) cin >> a[i];
    map<ll, ll> ma;
    rep(i, 0, n - 1) ma[a[i]]++;
    ranges::sort(a);
    vl pre(n + 1);
    rep(i, 1, n) pre[i] = pre[i - 1] + a[i - 1];
    ll l = 1;
    ll ans = 0;
    rep(r, 1, n - 1) {
        while (l <= r && (pre[r + 1] - pre[l] - (r - l + 1) * a[l] >= a[l] - a[0])) l++;
        ans = max(ans, r - l + 1);
    }
    cout << ans << "/" << ans + 1 << ' ';
    for (auto& [x, y] : ma) {
        if (y >= 2) {
            cout << 0 << '/' << 1 << endl;
            return;
        }
    }
    ans = 0;
    l = 0;
    rep(r, 0, n - 2) {
        while (l <= r && (r - l + 1) * a[r] - (pre[r + 1] - pre[l]) > a[n - 1] - a[r]) l++;
        ans = max(ans, r - l + 1);
    }
    cout << 1 << '/' << ans + 1 << endl;
    return;
}
```

## C

题目大意：给定一张 $n$ 个点 $m$ 条边的无向图，并给定 $q$ 次变化，每次在 $x,y$ 之间新增一条边，或者删除它们之间的边，每次变化后，会进行一次以下规则的模拟，请求出模拟代价的期望值。

每次模拟时，先删除当前度数为 $0$ 的点，然后花费 $1$ 代价从存活的点中随机选取一个点，删除它与它相连的边。

数据范围： $2 \leq n,m \leq 2 \cdot 10^5,1 \leq q \leq 2 \cdot 10^5$

思路：首先考虑将 $x$ 拆成示性函数，也就是 $E(x_1+\ldots+x_n)=E(x_1)+\ldots +E(x_n)$ ，然后考虑 $P(x_i=1)$ 时的条件，也就是 $1-P(x_i=0)$ ，而 $P(x_i=0)$ 当且仅当与它相连的所有点都先被删了，那就是 $\frac{1}{deg_i+1}$ ，因此 $E(X_i)=\frac{deg_i}{deg_i+1}$ ，这就一目了然了。

```cpp
constexpr ll INF = LLONG_MAX / 3;
constexpr ll MOD = 998244353;
ll mul(ll x, ll y) { return x * y % MOD; }
ll qpow(ll x, ll y) {
    ll z = 1;
    while (y > 0) {
        if (y & 1) z = mul(z, x);
        x = mul(x, x);
        y >>= 1;
    }
    return z;
}  // 求x**y%MOD

// 注意：当MOD为质数时， (x/y)%MOD=(x*(y**(MOD-2)))%MOD，即y在模MOD意义下的逆元为b^{-1} \equiv b^{p-2} mod p
void solve() {
    ll n, m, q, x, y;
    char op;
    cin >> n >> m >> q;
    vvl ma(n);
    vl deg(n);
    ll ans = 0;
    rep(_, 0, m - 1) {
        cin >> x >> y;
        ma[x - 1].push_back(y - 1), ma[y - 1].push_back(x - 1);
        deg[x - 1]++, deg[y - 1]++;
    }
    rep(i, 0, n - 1) ans = (ans + mul(deg[i], qpow(deg[i] + 1, MOD - 2))) % MOD;
    rep(_, 0, q - 1) {
        cin >> op >> x >> y;
        x--, y--;
        ll oldx = mul(deg[x], qpow(deg[x] + 1, MOD - 2)), oldy = mul(deg[y], qpow(deg[y] + 1, MOD - 2));
        ans = (ans - oldx + MOD) % MOD, ans = (ans - oldy + MOD) % MOD;
        if (op == '+')
            deg[x]++, deg[y]++;
        else
            deg[x]--, deg[y]--;
        ans = (ans + mul(deg[x], qpow(deg[x] + 1, MOD - 2))) % MOD, ans = (ans + mul(deg[y], qpow(deg[y] + 1, MOD - 2))) % MOD;
        cout << ans << endl;
    }
    return;
}
```

## D

题目大意：给定数组 $a_1,a_2,\ldots,a_n$ ，现在定义，一个区间 $[l,r]$ 内若存在三个数 $a_i,a_j,a_k$ 能构成三角形，则称其为三角形区间，现在给定 $q$ 个操作，每个操作将 $a_x$ 改为 $y$ ，或者查询 $[l,r]$ 之内的三角形区间个数。

数据范围： $1 \leq n \leq 10^6, 1 \leq q \leq 2 \cdot 10^4, 1 \leq a_i \leq 10^{18}$

思路：这题没有完全做出来，借助了 gpt 大人。

首先注意到，你要三角形，那么必然是把当前数组内元素排序后，考虑相邻的三个。然后如果不存在三角形，则必然有 $a_{i+2} \geq a_{i+1}+a_i$ ，也就是 $a_{i+2} \geq 2 \times a_i$ ，于是结合值域，得到一个等比关系，从而，长度大于等于 88 的区间必然是三角形区间。

然后，我们可以知道，令 $x \lt y \lt z$ 是三角形的三个下标，那么对于 $l \leq x, z \leq r$ ， $[l,r]$ 必然是三角形区间，因此，可以设 $f(l)=\min \{r | [l,r]\text{是三角形区间} \}$ ，从而可以得出， $f(l)$ 是一个阶梯式的上升函数，那么静态查找时，完全可以二分找到 $f(x) \leq r$ 的最大 $x$ ，然后直接推式子算贡献即可。

那么，带修怎么处理呢？联想到上面长度大于等于 $88$ 的区间必然是三角形区间，那么，此时最多只需要修改 88 个 $f(l)$ ，考虑暴力处理，并在树状数组上进行修改，因为后面需要动态查区间和。

好了，到现在，你也许会了，但是还有个问题，这里的暴力初始化跟暴力处理，究竟是怎么个暴力法？其实由于单调性考虑双指针就行，用 multiset 模拟一下当前排好序的数组，然后每次插入只会影响至多两个前驱跟后缀的三元组，另外维护写里面三角形的个数，就是不太好写。

```cpp
constexpr ll INF = LLONG_MAX / 3;
constexpr ll MOD = 998244353;
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
        for (++i; i < tree.size(); i += i & (-i)) {
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
    ll n, q, op, x, y;
    cin >> n >> q;
    vl a(n);
    rep(i, 0, n - 1) cin >> a[i];
    multiset<ll> s;
    ll r = -1;
    vl val(n);
    ll cnt = 0;
    auto add = [&](ll x) -> void {
        auto it = s.lower_bound(x);
        auto l1 = (it == s.begin()) ? s.end() : prev(it);
        auto l2 = (l1 == s.end() || l1 == s.begin() ? s.end() : prev(l1));
        auto r1 = it, r2 = (it == s.end() ? s.end() : next(it));
        if (l2 != s.end() && r1 != s.end()) cnt -= (*l2 + *l2 > *r1);
        if (l1 != s.end() && r2 != s.end()) cnt -= (*l1 + *r1 > *r2);
        if (l2 != s.end()) cnt += (*l2 + *l1 > x);
        if (l1 != s.end() && r1 != s.end()) cnt += (*l1 + x > *r1);
        if (r2 != s.end()) cnt += (x + *r1 > *r2);
        s.insert(it, x);
    };
    auto del = [&](ll x) -> void {
        auto it = s.find(x);
        auto l1 = it == s.begin() ? s.end() : prev(it);
        auto l2 = l1 == s.end() || l1 == s.begin() ? s.end() : prev(l1);
        auto r1 = next(it), r2 = r1 == s.end() ? s.end() : next(r1);
        if (l2 != s.end()) cnt -= (*l2 + *l1 > x);
        if (l1 != s.end() && r1 != s.end()) cnt -= (*l1 + x > *r1);
        if (r2 != s.end()) cnt -= (x + *r1 > *r2);
        if (l2 != s.end() && r1 != s.end()) cnt += (*l2 + *l1 > *r1);
        if (l1 != s.end() && r2 != s.end()) cnt += (*l1 + *r1 > *r2);
        s.erase(it);
    };
    rep(l, 0, n - 1) {
        while (r <= n - 2 && !cnt) add(a[++r]);
        val[l] = (cnt ? r : n);
        del(a[l]);
    }
    Tree<ll> bit(val);
    rep(_, 0, q - 1) {
        cin >> op >> x >> y;
        if (op == 1) {
            x--, a[x] = y;
            s.clear(), cnt = 0;
            ll L = max(0LL, x - 87), R = L - 1;
            rep(i, L, x) {
                while (R <= n - 2 && !cnt) add(a[++R]);
                ll cur = (cnt ? R : n);
                bit.add(i, cur - val[i]);
                val[i] = cur;
                del(a[i]);
            }
        } else {
            x--, y--;
            ll pos = upper_bound(val.begin() + x, val.begin() + y + 1, y) - val.begin() - 1;
            if (pos < x)
                cout << 0 << endl;
            else
                cout << (pos - x + 1) * (y + 1) - bit.query(x, pos) << endl;
        }
    }
    return;
}
```

## E

题目大意：给定 $a_1,\ldots,a_n$ ，满足 $3 \times a_i \leq a_{i+1}$ ，有 $q$ 次询问，每次给出一个整数 $v$ ，问是否存在 $\sum\limits_{i=1}^{n}a_i \cdot c_i=q,c_i \in \{-1,0,1\}$ ，如有，请求出 $c_i$ ，否则请输出 NO。

数据范围： $1 \leq n \leq 50, 1 \leq a_i \leq 10^{18},\sum(q \times n) \leq 5 \times 10^5$

思路：你都给出 $O(nq)$ 了，那显然是某种暴力贪心吧。

观察到，这里的三倍条件跟 $c$ 的取值范围，完全符合三进制下的高位被固定条件，从而从高位开始贪心即可。

```cpp
void solve() {
    ll n, q, x;
    cin >> n;
    vl a(n);
    rep(i, 0, n - 1) cin >> a[i];
    cin >> q;
    rep(i, 0, q - 1) {
        cin >> x;
        vl res(n);
        frep(j, n - 1, 0) {
            if (2 * abs(x) > a[j]) {
                res[j] = (x < 0 ? -1 : 1);
                x -= res[j] * a[j];
            }
        }
        if (x != 0)
            cout << "NO" << endl;
        else {
            cout << "YES" << endl;
            for (auto& p : res) cout << p << ' ';
            cout << endl;
        }
    }
    return;
}
```

## F

八百签到，不讲。

## G

题目大意：给定一个数组 $a_1,a_2,\ldots,a_n$ ，定义一个数组的潮汐值为，找出它的最大值 $M$ ，然后 $A,B$ 分别是 $M$ 在它里面最早出现跟最晚出现的位置，则它的潮汐值为 $M \times (B-A)$ ，现在给出 $q$ 个询问，对于每个询问 $[l,r]$ ，请你求出 $[l,r]$ 中，潮汐值最大的子数组的潮汐值，注意本题要求**强制在线**。

数据范围： $1 \leq n \leq 5 \cdot 10^5, 1 \leq q \leq 3 \cdot 10^6$

思路：出题人的冯呢？从来没见过 $q \leq 3 \cdot 10^6$ 的数据范围，好不容易想出来还他妈卡我常。

首先一开始我考虑的是，一种类似后缀非严格最大值的结构，然后死活想不出来。

接着想到，对于一个数组的话，它的两边必然是要大于等于中间的所有值的，然后再细想，要达到最优，完全就是将原数组分为多个满足两边大于等于中间所有值的分组，也就是按照值来分组，这样的组最多有 $O(n)$ 个，然后按照 $pos[a[i]]$ 来预处理。

然后，考虑以下情况，一种是 $pos[a[i]][1] \lt l \leq r \lt pos[a[i][-1]$ ，这种就可以通过二分 $[l,r]$ 里面的 $pos[a[i]]$ 来查出来了，另外，注意到此时 $a[i]=M$ ，所以只有一种情况，使用线段树维护一下动态最大值即可。

接着，考虑 $l \leq pos[a[i]][1]$ 的情况，由于此时对于 $a[i]$ ，可以将其分为 $pos[a[i]][1],pos[a[i]][2]$ 等等，也就是转化为 $l \leq pos[a[i]][j] \leq pos[a[i]][k] \leq r$ ，然后求 $a[i] \times (pos[a[i]][k]-pos[a[i]][j])$ 的最大值，但是注意到，由于此时 $j=1$ 跟 $k=-1$ 必然有一个成立，否则转化为上面的情况，因此可以在预处理组的时候，将这个值直接挂在右边的 $pos[a[i]][k]$ 上，然后就转化为强制在线求 $l \leq pos[a[i]][j] \leq pos[a[i]][k] \leq r$ 的挂的值的最大值，这就是一个可持久化线段树典了， $pos[a[i]][-1] \leq r$ 的情况同理。

好了，上面的方法会被卡常，正解是四个 st 表，谁能想出来谁做去，反正我不会数据结构。

```cpp
// 可持久化线段树：保留所有历史版本，支持从任意版本分叉、单点赋值和区间查询。
// 数组下标为 0-indexed，区间均为闭区间 [l, r]，0 号版本是初始数组。

struct Info {
    ll mx = 0;

    Info(ll x = 0) : mx(x) {}
};

Info operator+(const Info& a, const Info& b) { return {max(a.mx, b.mx)}; }  // 按顺序合并左右子树

bool operator<(const Info& a, const Info& b) { return a.mx < b.mx; }

template <typename Info>
class PersistentSegmentTree {
    struct Node {
        int left, right;
        Info val;
    };

    int n;
    vector<Node> tree;
    vi root;

    Info merge_val(const Info& a, const Info& b) const { return a + b; }

    int new_node(int left, int right, const Info& val) {
        tree.push_back({left, right, val});
        return sz(tree) - 1;
    }

    int build(const vector<Info>& a, int l, int r) {
        if (l == r) return new_node(0, 0, a[l]);
        int m = (l + r) >> 1;
        int left = build(a, l, m);
        int right = build(a, m + 1, r);
        return new_node(left, right, merge_val(tree[left].val, tree[right].val));
    }

    int build(int l, int r, const Info& init_val) {
        if (l == r) return new_node(0, 0, init_val);
        int m = (l + r) >> 1;
        int left = build(l, m, init_val);
        int right = build(m + 1, r, init_val);
        return new_node(left, right, merge_val(tree[left].val, tree[right].val));
    }

    int update(int old, int l, int r, int p, const Info& val) {
        if (l == r) return new_node(0, 0, val);
        int m = (l + r) >> 1;
        int left = tree[old].left;
        int right = tree[old].right;
        if (p <= m)
            left = update(left, l, m, p, val);
        else
            right = update(right, m + 1, r, p, val);
        return new_node(left, right, merge_val(tree[left].val, tree[right].val));
    }  // 沿根到叶子复制一条链

    Info query(int node, int l, int r, int ql, int qr) const {
        if (ql <= l && r <= qr) return tree[node].val;
        int m = (l + r) >> 1;
        if (qr <= m) return query(tree[node].left, l, m, ql, qr);
        if (ql > m) return query(tree[node].right, m + 1, r, ql, qr);
        return merge_val(query(tree[node].left, l, m, ql, qr), query(tree[node].right, m + 1, r, ql, qr));
    }

    template <typename F>
    int find_first(int node, int l, int r, int ql, int qr, F& check) const {
        if (r < ql || qr < l || !check(tree[node].val)) return -1;
        if (l == r) return l;
        int m = (l + r) >> 1;
        int res = find_first(tree[node].left, l, m, ql, qr, check);
        if (res != -1) return res;
        return find_first(tree[node].right, m + 1, r, ql, qr, check);
    }

    template <typename F>
    int find_last(int node, int l, int r, int ql, int qr, F& check) const {
        if (r < ql || qr < l || !check(tree[node].val)) return -1;
        if (l == r) return l;
        int m = (l + r) >> 1;
        int res = find_last(tree[node].right, m + 1, r, ql, qr, check);
        if (res != -1) return res;
        return find_last(tree[node].left, l, m, ql, qr, check);
    }

    int nodes_per_update() const { return bit_width((unsigned)n - 1) + 1; }

    void reserve_memory(int max_updates) {
        tree.reserve((size_t)2 * n - 1 + (size_t)max_updates * nodes_per_update());
        root.reserve((size_t)max_updates + 1);
    }

public:
    // 维护长度为 n、初值均为 init_val 的数组；n > 0，max_updates >= 0。
    PersistentSegmentTree(int size, const Info& init_val = Info(), int max_updates = 0) : n(size) {
        reserve_memory(max_updates);
        root.push_back(build(0, n - 1, init_val));
    }

    // 维护初始数组 a；max_updates >= 0 且仅用于预留内存，不影响正确性。
    PersistentSegmentTree(const vector<Info>& a, int max_updates = 0) : n(sz(a)) {
        reserve_memory(max_updates);
        root.push_back(build(a, 0, n - 1));
    }

    // 从 version 版本分叉，令 a[p] = val，返回新版本编号。
    int update(int version, int p, const Info& val) {
        root.push_back(update(root[version], 0, n - 1, p, val));
        return versions() - 1;
    }

    // 从最新版本分叉，令 a[p] = val，返回新版本编号。
    int update(int p, const Info& val) { return update(latest_version(), p, val); }

    // 均摊 O(1) 复制 version 为一个新版本，不新建线段树节点。
    int copy_version(int version) {
        root.push_back(root[version]);
        return versions() - 1;
    }

    // 查询 version 版本的 [ql, qr]。
    Info query(int version, int ql, int qr) const { return query(root[version], 0, n - 1, ql, qr); }

    Info query(int ql, int qr) const { return query(latest_version(), ql, qr); }  // 查询最新版本的 [ql, qr]

    Info get(int version, int p) const { return query(version, p, p); }  // 查询 version 版本的 a[p]

    Info get(int p) const { return get(latest_version(), p); }  // 查询最新版本的 a[p]

    Info query_all(int version) const { return tree[root[version]].val; }  // O(1) 查询 version 版本的整个数组

    Info query_all() const { return query_all(latest_version()); }  // 查询最新版本的整个数组

    template <typename F>
    int find_first(int version, int ql, int qr, F&& check) const {
        return find_first(root[version], 0, n - 1, ql, qr, check);
    }  // 查询 [ql, qr] 中第一个令叶子 Info 通过 check 的位置

    template <typename F>
    int find_first(int ql, int qr, F&& check) const {
        return find_first(latest_version(), ql, qr, check);
    }

    template <typename F>
    int find_last(int version, int ql, int qr, F&& check) const {
        return find_last(root[version], 0, n - 1, ql, qr, check);
    }  // 查询 [ql, qr] 中最后一个令叶子 Info 通过 check 的位置

    template <typename F>
    int find_last(int ql, int qr, F&& check) const {
        return find_last(latest_version(), ql, qr, check);
    }

    int versions() const { return sz(root); }

    int latest_version() const { return versions() - 1; }

    // 已经建树后才知道修改数时，可手动为后续修改预留内存。
    void reserve_updates(int max_updates) {
        tree.reserve(tree.size() + (size_t)max_updates * nodes_per_update());
        root.reserve(root.size() + (size_t)max_updates);
    }
};

template <typename T = long long>
class MaxTree {
    vector<T> tree;
    T identity;

public:
    // 构造函数：初始化大小为 n 的树状数组（外部表现为 0-based）
    explicit MaxTree(int n, T identity = numeric_limits<T>::lowest()) : tree(n + 1, identity), identity(identity) {}

    // 构造函数：使用给定的 vector 在 O(N) 时间内快速初始化建树
    explicit MaxTree(const vector<T>& data, T identity = numeric_limits<T>::lowest()) : tree(data.size() + 1, identity), identity(identity) {
        int n = data.size();
        for (int i = 1; i <= n; i++) {
            tree[i] = max(tree[i], data[i - 1]);  // data 是 0-based
            int nxt = i + (i & -i);
            if (nxt <= n) {
                tree[nxt] = max(tree[nxt], tree[i]);
            }
        }
    }

    // 单点修改：将 0-based 下标 i 处的值与 val 取最大值（只支持值变大）
    void chmax(int i, T val) {
        for (++i; i < tree.size(); i += i & -i) {
            tree[i] = max(tree[i], val);
        }
    }

    // 前缀最大值：计算 0-based 下标区间 [0, i] 内的最大值
    T pre(int i) const {
        T res = identity;
        for (++i; i > 0; i &= i - 1) {
            res = max(res, tree[i]);
        }
        return res;
    }
};
// ST 表：静态区间查询，0-based 闭区间；预处理和空间 O(n log n)，查询 O(1)。
// 默认维护最大值；merge_val 需满足结合律和幂等性，即合并重复信息不影响结果。
template <typename T = ll>
class STTable {
    vector<vector<T>> st;

    T merge_val(const T& a, const T& b) const { return max(a, b); }  // 可改为 min(a,b)、gcd(a,b)、a&b、a|b；不能直接改为求和或异或

public:
    STTable(const vector<T>& a) {
        int n = sz(a);
        int lg = bit_width(unsigned(n));
        st.resize(lg);
        if (!n) return;
        st[0] = a;
        rep(j, 1, lg - 1) {
            int len = 1 << j;
            st[j].resize(n - len + 1);
            rep(i, 0, n - len) { st[j][i] = merge_val(st[j - 1][i], st[j - 1][i + (len >> 1)]); }
        }
    }  // st[j][i] 维护 [i,i+2^j-1]

    T query(int l, int r) const {
        int k = bit_width(unsigned(r - l + 1)) - 1;
        return merge_val(st[k][l], st[k][r - (1 << k) + 1]);
    }  // 要求 0 <= l <= r < n；用两段长度为 2^k 的区间覆盖 [l,r]，允许重叠
};
void solve() {
    ll n, q, l, r;
    cin >> n >> q;
    vl a(n);
    rep(i, 0, n - 1) cin >> a[i];
    auto sorted = a;
    ranges::sort(sorted);
    sorted.erase(unique(all(sorted)), sorted.end());
    ll m = sz(sorted);
    vvl pos(m);
    vl id(n);
    rep(i, 0, n - 1) {
        id[i] = ranges::lower_bound(sorted, a[i]) - sorted.begin();
        pos[id[i]].push_back(i);
    }
    STTable st(a);
    vector<vector<pll>> cand(n);
    rep(i, 0, m - 1) {
        ll j = 0;
        while (j <= sz(pos[i]) - 1) {
            ll v = j + 1;
            while (v <= sz(pos[i]) - 1 && st.query(pos[i][v - 1], pos[i][v]) == sorted[i]) v++;
            rep(k, j + 1, v - 1) cand[pos[i][k]].emplace_back(pos[i][j], sorted[i] * (pos[i][k] - pos[i][j]));
            rep(k, j + 1, v - 2) cand[pos[i][v - 1]].emplace_back(pos[i][k], sorted[i] * (pos[i][v - 1] - pos[i][k]));
            j = v;
        }
    }
    PersistentSegmentTree<Info> pseg(n, Info(0), 2 * n);
    vl ver(n);
    rep(r, 0, n - 1) {
        for (auto& [l, val] : cand[r]) {
            pseg.update(l, Info(val));
        }
        ver[r] = pseg.latest_version();
    }
    ll las = 0, res = 0;
    cin >> l >> r;
    rep(i, 0, q - 1) {
        if (i != 0) {
            ll a = (l + las * 37) % n + 1, b = (l + r + las * 53) % n + 1;
            l = min(a, b), r = max(a, b);
        }
        ll mx = st.query(l - 1, r - 1);
        ll idx = ranges::lower_bound(sorted, mx) - sorted.begin();
        auto pos1 = ranges::lower_bound(pos[idx], l - 1) - pos[idx].begin();
        auto pos2 = ranges::upper_bound(pos[idx], r - 1) - pos[idx].begin() - 1;
        ll ans = mx * (pos[idx][pos2] - pos[idx][pos1]);
        ans = max(ans, pseg.query(ver[r - 1], l - 1, n - 1).mx);
        las = ans;
        res = res ^ (ans + i + 1);
    }
    cout << res << endl;
    return;
}
```

## H
题目大意：现在有一条网络流，给定源点 $S$ 跟汇点 $T$ ，现在有 $n$ 个点，每个点可以从 $k$ 个类型中选一个，第 $i$ 个点选择第 $j$ 个类型，会使得 $(S,i)$ 的容量变为 $a_{ij}$ ， $(i,T)$ 的容量变为 $b_{ij}$ ， $(i,i+1)$ 的容量变为 $c_{ij}$ ，请你计算出所有可能取法下，最大流的最小值。

数据范围： $2 \leq n \leq 10^5,1 \leq k \leq 5$

思路：看到这个数据范围还觉得这是网络流的，那没救了，肯定是套皮的网络流题目。

考虑最大流，最大流想来想去都想不到能怎么做，于是开始猜，把最大流转化为最小割，然后求最小割的可能最小值，又因为这个数据范围，怎么看怎么像 DP，于是考虑 $O(nk^2)$ 的 DP 。

从最小割的定义出发，设 $dp[i][j][k]$ 为遍历到点 $i$ ， $j=0 \Leftrightarrow i\text{属于源点}，j=1 \Leftrightarrow i\text{属于汇点}$ ， $k$ 表示当前状态，的最小割容量最小值，于是对于 $j=0$ ，由于此时跟 $i-1$ 无关，直接 $dp[i][0][k]=\min(b[i][j]+dp[i-1][op][v])$ ，而对于 $j=1$ ，当 $op=0$ 时， $dp[i][1][k]=\min(a[i][j]+dp[i-1][op][v]+c[i-1][v])$ ，否则 $dp[i][1][k]=\min(a[i][j]+dp[i-1][op][v])$ 。

```cpp
void solve() {
    ll n, k;
    cin >> n >> k;
    vvl a(n, vl(k)), b(n, vl(k)), c(n, vl(k));
    vector<vvl> dp(n, vvl(2, vl(k, INF)));
    rep(i, 0, n - 1) { rep(j, 0, k - 1) cin >> a[i][j]; }
    rep(i, 0, n - 1) { rep(j, 0, k - 1) cin >> b[i][j]; }
    rep(i, 0, n - 2) { rep(j, 0, k - 1) cin >> c[i][j]; }
    rep(i, 0, k - 1) dp[0][0][i] = b[0][i], dp[0][1][i] = a[0][i];
    rep(i, 1, n - 1) {
        rep(j, 0, k - 1) {
            rep(v, 0, k - 1) {
                rep(op, 0, 1) {
                    dp[i][0][j] = min(dp[i][0][j], b[i][j] + dp[i - 1][op][v]);
                    dp[i][1][j] = min(dp[i][1][j], a[i][j] + dp[i - 1][op][v] + (op == 0 ? c[i - 1][v] : 0));
                }
            }
        }
    }
    cout << min(*min_element(all(dp[n - 1][0])), *min_element(all(dp[n - 1][1]))) << endl;
    return;
}
```

## J

题目大意：给定一棵有根树， $0$ 为树根，每条边 $(pa_i,i)$ 都有双重权值 $(d_i,e_i)$ ，考虑对于每个点，定义它的 $f(i)=\min\limits_{j\text{是}i\text{的祖先}}(a_j+\sum\limits_{v\text{在}i\text{j}的路径上}d_v\sum\limits_{v\text{在}i\text{j}的路径上}e_v)$ ， $g(i)=\max\limits_{j\text{是}i\text{的祖先}}f(j)$ ，请求出对于每个点 $i$ 的 $g(i)$ ，注意，给定的树中最多只有 $10$ 个叶子。

数据范围： $2 \leq n \leq 3 \cdot 10^5$

思路：首先很容易转化为两个前缀和之积，然后转化为最大化某个式子，但是这个式子是二元的，所以就不会了。

不过，此时注意到，这里好像对于一条链的情况，存在决策单调性，也就是说，如果一个节点作为最优解被更深的节点打擂台干掉了，那么它不可能回到最优解的位置（事实上前面推的式子也有四边形不等式的味道），那么对于一条链就可以通过决策单调性求解。

又由于给定的树中最多只有 $10$ 个叶子，因此直接拆成十条从根到叶子的链进行决策单调性即可。

```cpp
constexpr ll INF = LLONG_MAX / 3;
constexpr ll MOD = 998244353;
void solve() {
    ll n, x, y;
    cin >> n;
    vvl ma(n);
    vl pa(n), d(n), e(n);
    rep(i, 1, n - 1) {
        cin >> pa[i] >> d[i] >> e[i];
        pa[i]--;
        ma[pa[i]].push_back(i);
        ma[i].push_back(pa[i]);
    }
    vl a(n);
    rep(i, 0, n - 1) cin >> a[i];
    vl pred(n), pree(n);
    auto dfs = [&](this auto&& dfs, int x, int pa) -> void {
        if (pa != -1) pred[x] = pred[pa] + d[x], pree[x] = pree[pa] + e[x];
        for (auto& p : ma[x]) {
            if (p == pa) continue;
            dfs(p, x);
        }
        return;
    };
    dfs(0, -1);
    vvl path;
    vl used;
    auto dfs2 = [&](this auto&& dfs2, int x, int pa, vl& used) {
        used.push_back(x);
        if (sz(ma[x]) == 1 && pa != -1) {
            path.push_back(used);
            used.pop_back();
            return;
        }
        for (auto& p : ma[x]) {
            if (p == pa) continue;
            dfs2(p, x, used);
        }
        used.pop_back();
        return;
    };
    dfs2(0, -1, used);
    vl res(n, INF);
    for (auto& p : path) {
        ll m = sz(p);
        auto calc = [&](ll x, ll y) -> ll { return a[p[x]] + (pred[p[y]] - pred[p[x]]) * (pree[p[y]] - pree[p[x]]); };
        auto dfs = [&](this auto&& dfs, ll l, ll r, ll opl, ll opr) -> void {
            if (l > r) return;
            ll idx = -1, mid = (l + r) / 2;
            ll mn = INF;
            rep(j, opl, min(mid, opr)) {
                ll val = calc(j, mid);
                if (val <= mn) {
                    mn = val, idx = j;
                }
            }
            res[p[mid]] = mn;
            dfs(l, mid - 1, opl, idx);
            dfs(mid + 1, r, idx, opr);
            return;
        };
        dfs(0, m - 1, 0, m - 1);
    }
    rep(i, 1, n - 1) res[i] = max(res[i], res[pa[i]]);
    for (auto& p : res) cout << p << endl;
    cout << endl;
    return;
}
```

## K

题目大意：现在有一些弓箭塔和一些魔法塔，它们各自位于 $(x_i,y_i)$ ，并且有攻击力 $a_i$ 和半径 $r_i$ ，现在所有弓箭塔可以发动最多 $k_a$ 次技能，而所有魔法塔可以发动最多 $k_m$ 次技能，每次发动技能，弓箭塔会使它半径内的所有塔（包括自身）的半径变为 $2$ 倍，而魔法塔会使它半径内的所有塔（包括自身）的攻击力变为 $2$ 倍，每座塔只能发动一次技能。现在请你合理安排使用技能的顺序，求出 $\sum\limits_{i=1}^{n}a_i r_i^2$ 的最大值。

数据范围： $1 \leq n \leq 20, 0 \leq k_a \leq 5,0 \leq k_m \leq 5$

思路：首先很显然，你把所有的弓箭塔都放在最前面，肯定是最优的。

然后，你发现不同弓箭塔使用技能的顺序也有关系，因此状压 DP 就不行了，而数据结构这么小，那么就是暴搜，暴搜！接着再用状压 DP 看看魔法塔要使用哪些即可，因为魔法塔跟使用顺序是没有关系的，因为你的 $r$ 不会再变。

```cpp
constexpr ll INF = LLONG_MAX / 3;
constexpr ll MOD = 998244353;
void solve() {
    ll n, ka, km, x, y, a, r, op;
    cin >> n >> ka >> km;
    vector<array<ll, 4>> ma;
    vector<array<ll, 4>> mp;
    rep(_, 0, n - 1) {
        cin >> op >> x >> y >> r >> a;
        if (op == 1)
            ma.push_back({x, y, a, r});
        else
            mp.push_back({x, y, a, r});
    }
    ll m1 = sz(ma), m2 = sz(mp);
    ka = min(ka, m1), km = min(km, m2);
    ll ans = -INF;
    vector<bool> vis(m1, false);
    vl used;
    auto dfs = [&](this auto&& dfs, int pos) -> void {
        if (pos == ka) {
            auto v = mp;
            for (auto& p : ma) v.push_back(p);
            for (auto& p : used) {
                ll id = p + m2;
                ll r = v[id][3];
                rep(i, 0, n - 1) {
                    if ((v[i][0] - v[id][0]) * (v[i][0] - v[id][0]) + (v[i][1] - v[id][1]) * (v[i][1] - v[id][1]) <= r * r) v[i][3] *= 2;
                }
            }
            vl mask(n);
            rep(i, 0, m2 - 1) {
                rep(j, 0, n - 1) {
                    if ((v[i][0] - v[j][0]) * (v[i][0] - v[j][0]) + (v[i][1] - v[j][1]) * (v[i][1] - v[j][1]) <= v[i][3] * v[i][3]) mask[j] |= (1 << i);
                }
            }
            rep(i, 0, (1 << m2) - 1) {
                if (popcount((unsigned)i) != km) continue;
                ll tot = 0;
                rep(j, 0, n - 1) {
                    ll cnt = popcount((unsigned)(mask[j] & i));
                    tot += v[j][2] * v[j][3] * v[j][3] * (1LL << cnt);
                }
                ans = max(ans, tot);
            }
            return;
        }
        rep(i, 0, m1 - 1) {
            if (vis[i]) continue;
            vis[i] = true;
            used.push_back(i);
            dfs(pos + 1);
            used.pop_back();
            vis[i] = false;
        }
        return;
    };
    dfs(0);
    cout << ans << endl;
    return;
}
```

## L

八百签到，不讲。
