---
title: "2023 广东省大学生程序设计竞赛"
slug: gdcpc-2023
date: 2023-05-14
seriesOrder: 1
encrypt: false
hidden: true
image: "/images/anime-diary/5.png"
---

## 23GDCPC A
出处：[23GDCPC A](https://codeforces.com/gym/104369/problem/A)

题目大意：

数据范围：

思路：

```cpp
void solve() {
    ll x, n, y;
    cin >> x >> n;
    vl a(n);
    rep(i, 0, n - 1) cin >> a[i];
    cin >> y;
    ranges::sort(a);
    int tem = ranges::upper_bound(a, y) - a.begin();
    cout << y - x + 1 - tem << endl;
    return;
}
```

## 23GDCPC B
出处：[23GDCPC B](https://codeforces.com/gym/104369/problem/B)

题目大意：

数据范围：

思路：

```cpp
void solve() {
    ll n, m, x, y;
    cin >> n;
    vl a(n + 1);
    rep(i, 1, n) cin >> a[i];
    cin >> m;
    vl mx(n + 1, 0);
    rep(i, 1, m) {
        cin >> x >> y;
        mx[y] = max(mx[y], x);
    }
    vl dp(n + 1, LLONG_MAX / 3);
    deque<int> q;
    q.push_back(0);
    dp[0] = 0;
    ll l = 0;
    rep(i, 1, n) {
        l = max(l, mx[i - 1]);
        while (!q.empty() && q.front() < l) q.pop_front();
        dp[i] = dp[q.front()] + a[i];
        while (!q.empty() && dp[q.back()] >= dp[i]) q.pop_back();
        q.push_back(i);
    }
    l = max(l, mx[n]);
    while (!q.empty() && q.front() < l) q.pop_front();
    cout << dp[q.front()] << endl;
    return;
}
```

## 23GDCPC C
出处：[23GDCPC C](https://codeforces.com/gym/104369/problem/C)

题目大意：

数据范围：

思路：

```cpp
void solve() {
    ll n;
    cin >> n;
    vector<pll> ma(n);
    rep(i, 0, n - 1) cin >> ma[i].first >> ma[i].second;
    sort(all(ma), [&](const pll& x, const pll& y) { return x.first < y.first; });
    int l = 0, r = n - 1;
    ll ans = 0;
    while (l < r) {
        if (ma[l].second < ma[r].second) {
            ans += (ma[r].first - ma[l].first) * ma[l].second;
            ma[r].second -= ma[l].second;
            l++;
        } else if (ma[l].second == ma[r].second) {
            ans += (ma[r].first - ma[l].first) * ma[l].second;
            l++;
            r--;
        } else if (ma[l].second > ma[r].second) {
            ans += (ma[r].first - ma[l].first) * ma[r].second;
            ma[l].second -= ma[r].second;
            r--;
        }
    }
    cout << ans << endl;
    return;
}
```

## 23GDCPC D
出处：[23GDCPC D](https://codeforces.com/gym/104369/problem/D)

题目大意：

数据范围：

思路：

```cpp
void solve() {
    ll n, m;
    cin >> n >> m;
    vector<pll> ma(n);
    rep(i, 0, n - 1) cin >> ma[i].first >> ma[i].second;
    if (n == 1) {
        cout << ma[0].second << endl;
        return;
    }
    ll ans = 0;
    rep(i, 0, n - 1) ans += ma[i].first;
    sort(all(ma), [&](const pll& x, const pll& y) { return x.second - x.first > y.second - y.first; });
    ll ans2 = ans;
    ll pre = 0;
    rep(i, 0, n - 1) {
        pre += ma[i].second - ma[i].first;
        if (i == n - 2) continue;
        if (0 <= i && i <= n - 3 && m >= n + i + 1) ans2 = max(ans2, ans + pre);
        if (i == n - 1 && m >= 2 * n - 1) ans2 = max(ans2, ans + pre);
    }
    cout << ans2 << endl;
    return;
}
```

## 23GDCPC E
出处：[23GDCPC E](https://codeforces.com/gym/104369/problem/E)

题目大意：

数据范围：

思路：

```cpp
void solve() {
    int n, k;
    cin >> n >> k;
    vector<string> ma(n);
    rep(i, 0, n - 1) cin >> ma[i];
    ranges::sort(ma);
    vector<string> ma2;
    auto lcp = [&](const string& x, const string& y) -> string {
        int tem = min(sz(x), sz(y));
        int cnt = 0;
        while (cnt < tem && x[cnt] == y[cnt]) cnt++;
        return x.substr(0, cnt);
    };
    ma2.push_back("");
    rep(i, 1, n - 1) { ma2.push_back(lcp(ma[i], ma[i - 1])); }
    ranges::sort(ma2);
    ma2.erase(unique(all(ma2)), ma2.end());
    int m = sz(ma2);
    int l = 0, r = m - 1, mid, ans = 0;
    auto check = [&](int mid) -> bool {
        int cnt = 0;
        int tem = 0;
        while (tem < n) {
            cnt++;
            if (cnt >= k) return true;
            if (ma[tem] <= ma2[mid]) {
                tem++;
                continue;
            }
            int tem2 = 0;
            int tem3 = min(sz(ma[tem]), sz(ma2[mid]));
            while (tem2 < tem3 && ma[tem][tem2] == ma2[mid][tem2]) tem2++;
            string tem4 = ma[tem].substr(0, tem2 + 1);
            int tem5 = ranges::lower_bound(ma, tem4 + (char)(127)) - ma.begin();
            tem = tem5;
        }
        return false;
    };
    while (l <= r) {
        mid = (l + r) / 2;
        if (check(mid)) {
            ans = mid;
            r = mid - 1;
        } else
            l = mid + 1;
    }
    cout << (ans == 0 ? "EMPTY" : ma2[ans]) << endl;
    return;
}
```

## 23GDCPC F
出处：[23GDCPC F](https://codeforces.com/gym/104369/problem/F)

题目大意：

数据范围：

思路：

```cpp
ull splitmix64(ull x) {
    x += 0x9e3779b97f4a7c15;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9;
    x = (x ^ (x >> 27)) * 0x94d049bb133111eb;
    return x ^ (x >> 31);
}

struct custom_hash {
    static const ull FIXED_RANDOM;

    size_t operator()(ull x) const { return splitmix64(x + FIXED_RANDOM); }
};
const ull custom_hash::FIXED_RANDOM = chrono::steady_clock::now().time_since_epoch().count();
struct Info {
    umap<int, int, custom_hash> ma;
    int len = 0;
    Info(int c = -1) {
        if (c != -1) {
            ma[c]++;
            len = 1;
        }
    }
    bool check(const vi& ma2) const {
        int tem = 0;
        rep(i, 0, sz(ma2) - 1) {
            if (!ma.count(ma2[i])) continue;
            tem += ma.find(ma2[i])->second;
        }
        return tem == len;
    }
};
Info operator+(const Info& a, const Info& b) {
    Info c;
    c.len = a.len + b.len;
    for (auto& [x, y] : a.ma) c.ma[x] += y;
    for (auto& [x, y] : b.ma) c.ma[x] += y;
    return c;
}
template <typename T>
class SegmentTree {
    int n;
    vector<T> tree;
    T merge_val(T a, T b) const { return a + b; }  // 合并子树

    void maintain(int node) {  // 维护整棵树
        tree[node] = merge_val(tree[node * 2], tree[node * 2 + 1]);
    }

    void build(const vector<T>& a, int node, int l, int r) {
        if (l == r) {
            tree[node] = a[l];
            return;
        }
        int m = (l + r) / 2;
        build(a, node * 2, l, m);
        build(a, node * 2 + 1, m + 1, r);
        maintain(node);
    }  // 建树

    void update(int node, int l, int r, int i, int val, int val2) {
        tree[node].ma[val]--;
        if (tree[node].ma[val] == 0) tree[node].ma.erase(tree[node].ma.find(val));
        tree[node].ma[val2]++;
        if (l == r) return;
        int m = (l + r) / 2;
        if (i <= m)
            update(node * 2, l, m, i, val, val2);
        else
            update(node * 2 + 1, m + 1, r, i, val, val2);
    }  // 更新i处的值为val

    T query(int node, int l, int r, int ql, int qr) const {
        if (ql <= l && r <= qr) return tree[node];
        int m = (l + r) / 2;
        if (qr <= m) return query(node * 2, l, m, ql, qr);
        if (ql > m) return query(node * 2 + 1, m + 1, r, ql, qr);
        T l_res = query(node * 2, l, m, ql, qr);
        T r_res = query(node * 2 + 1, m + 1, r, ql, qr);
        return merge_val(l_res, r_res);
    }  // 查询[ql,qr]的值

    int find_first(int node, int l, int r, int ql, int qr, const vi& val) const {
        if (r < ql || l > qr) return -1;
        if (ql <= l && r <= qr && tree[node].check(val)) return -1;
        if (l == r) return l;
        int m = (l + r) >> 1;
        int res = find_first(node << 1, l, m, ql, qr, val);
        if (res != -1) return res;
        return find_first(node << 1 | 1, m + 1, r, ql, qr, val);
    }
    // 若固定左端点，需要记录前缀分段最大值，并加被待求区间完全覆盖的剪枝

    int find_last(int node, int l, int r, int ql, int qr, const vi& val) const {
        if (r < ql || l > qr) return -1;
        if (ql <= l && r <= qr && tree[node].check(val)) return -1;
        if (l == r) return l;
        int m = (l + r) >> 1;
        int res = find_last(node << 1 | 1, m + 1, r, ql, qr, val);
        if (res != -1) return res;
        return find_last(node << 1, l, m, ql, qr, val);
    }

public:
    SegmentTree(int n, T init_val) : SegmentTree(vector<T>(n, init_val)) {}

    // 传入一个数组维护
    SegmentTree(const vector<T>& a) : n(a.size()), tree(2 << bit_width(a.size() - 1)) { build(a, 1, 0, n - 1); }

    void update(int i, int val, int val2) { update(1, 0, n - 1, i, val, val2); }  // 更新i的值为val

    T query(int ql, int qr) const { return query(1, 0, n - 1, ql, qr); }  // 查询[ql,qr]的值

    T get(int i) const { return query(1, 0, n - 1, i, i); }  // 取出i处的值

    // 查询[ql,qr]中第一个满足条件的下标
    int find_first(int ql, int qr, const vi& val) const { return find_first(1, 0, n - 1, ql, qr, val); }

    // 查询[ql,qr]中最后一个满足条件的下标
    int find_last(int ql, int qr, const vi& val) const { return find_last(1, 0, n - 1, ql, qr, val); }
};
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
    int n, q, op, x, y;
    cin >> n >> q;
    vi c(n);
    rep(i, 0, n - 1) cin >> c[i];
    vl v(n);
    rep(i, 0, n - 1) cin >> v[i];
    Tree tree(v);
    vector<Info> init(n);
    rep(i, 0, n - 1) init[i] = Info(c[i]);
    SegmentTree<Info> tree2(init);
    rep(i, 0, q - 1) {
        cin >> op >> x;
        x--;
        if (op == 1) {
            cin >> y;
            tree2.update(x, c[x], y);
            c[x] = y;
        } else if (op == 2) {
            cin >> y;
            tree.add(x, y - v[x]);
            v[x] = y;
        } else {
            cin >> y;
            vi tem(y);
            rep(j, 0, y - 1) cin >> tem[j];
            int L = tree2.find_last(0, x - 1, tem);
            int R = tree2.find_first(x + 1, n - 1, tem);
            if (R == -1) R = n;
            cout << tree.query(L + 1, R - 1) << endl;
        }
    }
    return;
}
```

## 23GDCPC I
出处：[23GDCPC I](https://codeforces.com/gym/104369/problem/I)

题目大意：

数据范围：

思路：

```cpp
void solve() {
    ll n, m;
    cin >> n >> m;
    vvl ma(n, vl(m));
    rep(i, 0, n - 1) { rep(j, 0, m - 1) cin >> ma[i][j]; }
    vector<pll> ma2(m * n);
    rep(i, 0, n - 1) { rep(j, 0, m - 1) ma2[ma[i][j]] = make_pair(i, j); }
    int cnt = 0;
    set<pii> s;
    rep(i, 0, n * m - 1) {
        auto [x, y] = ma2[i];
        auto it = s.lower_bound({x, y});
        if (it != s.end()) {
            if (y > it->second) {
                cout << i << endl;
                return;
            }
        }
        if (it != s.begin()) {
            auto pre = prev(it);
            if (pre->second > y) {
                cout << i << endl;
                return;
            }
        }
        s.insert({x, y});
    }
    cout << m * n << endl;
    return;
}
```

## 23GDCPC K
出处：[23GDCPC K](https://codeforces.com/gym/104369/problem/K)

题目大意：

数据范围：

思路：

```cpp
int dx[5] = {0, 1, -1, 0, 0};
int dy[5] = {0, 0, 0, 1, -1};
void solve() {
    ll n, m, k, x, y;
    cin >> n >> m >> k;
    ll tem = 0;
    auto check = [&](int x, int y) -> int { return x * m + y; };
    rep(i, 0, k - 1) {
        cin >> x >> y;
        x--, y--;
        tem |= (1LL << check(x, y));
    }
    map<ll, int> ma;
    auto dfs = [&](this auto&& dfs, ll tem2) -> int {
        if (ma.count(tem2)) return ma[tem2];
        ll res = popcount((ull)tem2);
        rep(i, 0, n - 1) {
            rep(j, 0, m - 1) {
                int tem = check(i, j);
                if (((tem2 >> tem) & 1) == 0) continue;
                rep(v, 1, 4) {
                    int ax = i + dx[v], ay = j + dy[v];
                    int bx = i + 2 * dx[v], by = j + 2 * dy[v];
                    if (ax < 0 || ax >= n || ay < 0 || ay >= m) continue;
                    if (bx < 0 || bx >= n || by < 0 || by >= m) continue;
                    int tem3 = check(ax, ay);
                    int tem4 = check(bx, by);
                    if (((tem2 >> tem3) & 1) == 1 && ((tem2 >> tem4) & 1) == 0) {
                        res = min(res, 1LL * dfs(tem2 ^ (1LL << tem) ^ (1LL << tem3) ^ (1LL << tem4)));
                    }
                }
            }
        }
        ma[tem2] = res;
        return res;
    };
    cout << dfs(tem) << endl;
    return;
}
```

## 23GDCPC M
出处：[23GDCPC M](https://codeforces.com/gym/104369/problem/M)

题目大意：

数据范围：

思路：

```cpp
void solve() {
    int n;
    cin >> n;
    vector<pll> ma(n);
    rep(i, 0, n - 1) cin >> ma[i].first >> ma[i].second;
    auto dis = [&](const pll& x, const pll& y) -> ll {
        return (x.first - y.first) * (x.first - y.first) + (x.second - y.second) * (x.second - y.second);
    };
    auto cro = [&](const pll& x, const pll& y) -> ll { return x.first * y.second - x.second * y.first; };
    vl pre(2 * n + 1);
    rep(i, 0, 2 * n - 1) pre[i + 1] = pre[i] + cro(ma[i % n], ma[(i + 1) % n]);
    vvl dp(n, vl(n + 1));
    rep(i, 2, n) {
        rep(j, 0, n - 1) { dp[j][i] = max({dp[j][i - 1], dp[(j + 1) % n][i - 1], dis(ma[j], ma[(j + i - 1) % n])}); }
    }
    ll ans = LLONG_MAX;
    rep(i, 0, n - 1) {
        rep(j, 1, n - 1) {
            if (pre[i + j] - pre[i] + cro(ma[(i + j) % n], ma[i % n]) == 0) continue;
            if (pre[i + n] - pre[i + j] + cro(ma[(i + n) % n], ma[(i + j) % n]) == 0) continue;
            ans = min(ans, dp[i][j + 1] + dp[(i + j) % n][n - j + 1]);
        }
    }
    cout << ans << endl;
    return;
}
```
