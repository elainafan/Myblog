---
title: 2026ICPC Reg成都
slug: icpc-2026-reg-chengdu
date: 2026-11-01
encrypt: false
seriesOrder: 2
hidden: true
image: "/images/my-internet-addiction/cover.jpg"
categories:
    - 算法
    - 数学
---
## C
题目大意：给定两个整数 $n,m$ ，令 $pre_i=a_1+\ldots +a_i$ ， 给定 $m$ 个限制，要求 $pre_{m_i}=s_i$ ，同时要求 $a_1=0,0 \le a_{i+1}-a_i \le 1$ ，问能构造出的 $a$ 个数，由于答案可能很大，请对 $998244353$ 取模。

数据范围： $1 \leq t \leq 10^4, 1 \leq n \leq 100, 0 \leq m \leq n$ ，注意没有对 $\sum(m)$ 和 $\sum(n)$ 的限制。

思路：简单题。很显然地，会想到对 $pre$ 进行 DP，然后考虑相邻 $pre$ 之间的转移，不难发现只要记录前面一个 $pre$ 的结尾的数，就可以抽象为，在 $1,2...j-i$ 之间选 $r$ 个数，使得其和为 $pre_j-pre_i-(j-i) \times x$ ，这里 $x$ 是 $pre_i$ 结尾的数，而很显然这个是可以预处理的，所以直接枚举即可，视奸复杂度 $O(n^2)$ ，最后还要考虑 $pre_{m_i}$ 后面的数的方案数。

```cpp
constexpr ll INF = LLONG_MAX / 3;
constexpr ll MOD = 998244353;
int f[101][101][5051];
int pw[101];
auto init = [] {
    f[0][0][0] = 1;
    rep(i, 1, 100) {
        rep(j, 0, i) {
            rep(v, 0, i * (i + 1) / 2) {
                f[i][j][v] = f[i - 1][j][v];
                if (j > 0 && v >= i) {
                    f[i][j][v] = (f[i][j][v] + f[i - 1][j - 1][v - i]) % MOD;
                }
            }
        }
    }
    pw[0] = 1;
    rep(i, 1, 100) pw[i] = pw[i - 1] * 2 % MOD;
    return 0;
}();
void solve() {
    ll n, m, x, y;
    cin >> n >> m;
    vector<pll> pre(m + 1);
    pre[0] = make_pair(1, 0);
    rep(i, 1, m) cin >> pre[i].first >> pre[i].second;
    vl dp(n + 1);
    dp[0] = 1;
    rep(i, 1, m) {
        vl ndp(n + 1);
        ll tot = pre[i].second - pre[i - 1].second, l = pre[i].first - pre[i - 1].first;
        rep(j, 0, pre[i - 1].first - 1) {
            if (!dp[j]) continue;
            if (tot - l * j < 0 || tot - l * j > l * (l + 1) / 2) continue;
            rep(v, 0, l) ndp[j + v] = (ndp[j + v] + dp[j] * f[l][v][tot - l * j] % MOD) % MOD;
        }
        dp = ndp;
    }
    ll ans = 0;
    rep(i, 0, pre[m].first - 1) ans = (ans + dp[i]) % MOD;
    cout << ans * pw[n - pre[m].first] % MOD << endl;
    return;
}
```

## D
题目大意：有两个观者，给定他们的起始生命值 $h_a,h_b$ 和起始攻击力 $a,b$ ，如果一个人的生命值降低到 $0$ 及以下，那么他就死了。每个人可以选择在当前回合进入愤怒模式，此时他造成的伤害跟受到的伤害都变为原来的两倍，请问，在所有可能的情况下，观者 $A$ 是否都比观者 $B$ 晚死？请注意，同时死亡不算数。

数据范围： $1 \leq a,b,h_a,h_b \leq 10^{18}$

思路：签到题。很显然，考虑 $\lceil \frac{h_a}{b} \rceil$ 和 $\lceil \frac{h_b}{a} \rceil$ ，显然至少需要 $\lceil \frac{h_a}{b} \rceil \gt \lceil \frac{h_b}{a} \rceil+3$ ，因为最后一回合可能是差 $3$ 倍 ，注意此题会爆 long long，使用 Python。

```python
def solve():
    a, b, ha, hb = mii()
    res = (hb + a - 1) // a
    mx = res + 3
    print("YES" if mx * b < ha else "NO")
    return
```

## E
题目大意：平面直角坐标系上有 $n$ 个点， $P_1,P_2,\ldots,P_n$ ，现在有 $q$ 个询问，每个询问给出一个点 $x$ ，请问，是否可以在 $P_1,\ldots,P_n$ 中选出最少数量的点，使得 $x$ 严格位于这些点构成的四边形（可以是凹四边形或者凸四边形）内？ 如有，请给出这些点的编号，如果没有，请输出 $-1$ 。

数据范围： $3 \leq n \leq 10^5, 1 \leq q \leq 10^5,-10^9 \leq x,y \leq 10^9$

思路：计算几何，不会，问了gpt大人，好像是金牌题？

首先猜答案，考虑到如果一个点不位于所有点构成的四边形内，那么显然需要考虑所有点构成的凸包，因此先 $O(n\log n)$ 求出所有点的凸包，然后用到的点注意维护一下原始编号而不是新编号，如果不在凸包内则返回 $-1$ 。

接着猜答案，由于 $x$ 在凸包内，不难猜出答案只可能是 $3$ 或者 $4$ ，因此如果它位于 $h_0,h_{l},h_{l+1}$ 内的话，那就是三个，否则可能位于对角线上，那么取对角线跟周围两个点，就是四个，因此如果仅使用凸包内的点的话，就至多需要四个。

但是，如果在对角线上，可能可以通过刚才没有用来求出凸包的点来凑出三角形，所以要暂时先放后面考虑。

首先，使用凸包二分，如果 $x$ 在 $h_0,h_{l},h_{l+1}$ 内部，那显然是 $3$ 个，直接输出即可，否则， $x$ 落在对角线 $(h_0,h_{l})$ 上，考虑 $h_0,h_{l-1},h_l,h_{l+1}$ 形成的四边形，如果 $x$ 无法确定的话，那么只有一种情况，那就是 $x$ 是两条对角线 $(h_0,h_l)$ 跟 $(h_{l-1},h_{l+1})$ 的交点。

现在就要确定一下了，也很简单，就是由于 $x$ 是对角线交点，那么此时考虑两条对角线把平面直角坐标系分成四份，然后只要有一个点严格位于某份中，就可以组成三角形。如果凸包大小大于等于 $5$ 的话，那么显然随便选一个其他的凸包节点即可，否则需要考虑 $O(n)$ 找一个不位于凸包内且不与对角线共线的点，然后直接暴力枚举候选点中的三元组即可，这是 $O(1)$ 的。

```cpp
struct PointI {
    i128 x = 0, y = 0;

    auto operator+(const PointI& p) const -> PointI { return {x + p.x, y + p.y}; }

    auto operator-(const PointI& p) const -> PointI { return {x - p.x, y - p.y}; }

    auto operator*(i128 k) const -> PointI { return {x * k, y * k}; }

    auto operator<(const PointI& p) const -> bool { return x != p.x ? x < p.x : y < p.y; }

    auto operator==(const PointI& p) const -> bool { return x == p.x && y == p.y; }
};

auto cross(const PointI& a, const PointI& b) -> i128 { return a.x * b.y - a.y * b.x; }

auto cross(const PointI& o, const PointI& a, const PointI& b) -> i128 { return cross(a - o, b - o); }

auto convexHull(vector<PointI>& p) -> vi {
    int n = sz(p);
    vi ord(n);
    rep(i, 0, n - 1) ord[i] = i;
    sort(all(ord), [&](const int& x, const int& y) { return p[x] < p[y]; });
    ord.erase(unique(all(ord), [&](const int& x, const int& y) { return p[x] == p[y]; }), ord.end());
    if (sz(ord) <= 1) return ord;
    int m = sz(ord);
    vi h(2 * m);
    int k = 0;
    for (auto& x : ord) {
        while (k >= 2 && cross(p[h[k - 2]], p[h[k - 1]], p[x]) <= 0) k--;
        h[k++] = x;
    }
    for (int i = sz(ord) - 2, t = k + 1; i >= 0; i--) {
        while (k >= t && cross(p[h[k - 2]], p[h[k - 1]], p[ord[i]]) <= 0) k--;
        h[k++] = ord[i];
    }
    h.resize(k - 1);
    return h;
};

int InConvex(const vector<PointI>& h, const PointI& p) {
    int n = sz(h);
    if (n < 3 || cross(h[0], h[1], p) <= 0 || cross(h[0], h[n - 1], p) >= 0) return -1;
    int l = 1, r = n - 2, ans = 0, mid;
    auto check = [&](int mid) -> bool { return cross(h[0], h[mid], p) >= 0; };
    while (l <= r) {
        mid = (l + r) / 2;
        if (check(mid)) {
            ans = mid;
            l = mid + 1;
        } else
            r = mid - 1;
    }
    if (cross(h[ans], h[ans + 1], p) <= 0) return -1;
    return ans;
};

bool inTriangle(const PointI& a, const PointI& b, const PointI& c, const PointI& d) {
    i128 x = cross(a, b, d), y = cross(b, c, d), z = cross(c, a, d);
    return (x < 0 && y < 0 && z < 0) || (x > 0 && y > 0 && z > 0);
};

void solve() {
    ll n, q, x, y;
    cin >> n >> q;
    vector<PointI> p;
    rep(i, 0, n - 1) {
        cin >> x >> y;
        p.emplace_back(x, y);
    }
    vi id = convexHull(p);
    int m = sz(id);
    vector<PointI> h;
    rep(i, 0, m - 1) h.push_back(p[id[i]]);
    int idx = -1;
    if (m == 4) {
        rep(i, 0, n - 1) {
            if (cross(h[0], h[2], p[i]) != 0 && cross(h[1], h[3], p[i]) != 0) {
                idx = i;
                break;
            }
        }
    }
    rep(_, 0, q - 1) {
        cin >> x >> y;
        PointI tem(x, y);
        int l = InConvex(h, tem);
        if (l == -1) {
            cout << -1 << endl;
            continue;
        }
        if (cross(h[0], h[l], tem) > 0) {
            cout << 3 << endl;
            cout << id[0] + 1 << ' ' << id[l] + 1 << ' ' << id[l + 1] + 1 << endl;
            continue;
        }
        vi cand = {id[0], id[l - 1], id[l], id[l + 1]};
        if (m >= 5)
            cand.push_back(id[(l == 2 ? 4 : 1)]);
        else if (m == 4 && idx != -1)
            cand.push_back(idx);
        bool flag = false;
        int m1 = sz(cand);
        for (int i = 0; i <= m1 - 1 && !flag; i++) {
            for (int j = i + 1; j <= m1 - 1 && !flag; j++) {
                for (int v = j + 1; v <= m1 - 1 && !flag; v++) {
                    if (inTriangle(p[cand[i]], p[cand[j]], p[cand[v]], tem)) {
                        cout << 3 << endl;
                        cout << cand[i] + 1 << ' ' << cand[j] + 1 << ' ' << cand[v] + 1 << endl;
                        flag = true;
                        break;
                    }
                }
            }
        }
        if (!flag) {
            cout << 4 << endl;
            rep(i, 0, 3) cout << cand[i] + 1 << ' ';
            cout << endl;
            continue;
        }
    }
    return;
}
```

## H
题目大意：这是一道交互题。

现在有 $a_1,\ldots,a_n$ ，每个元素可能是 $0,1,2$ ，每次询问可以询问 $a_i,a_j$ ，评测机将会给出 $a_i \gt a_j$ 是否为真的判定，请在 $2n-3$ 次询问内，给出一个 $1 \sim n$ 的排列 $p_1,\ldots,p_n$ ，使得 $a_{p_1} \leq a_{p_2} \leq \ldots \leq a_{p_n}$ 。

请注意，交互器是自适应的，但是当前情况的答案始终满足已询问的约束。

数据范围： $2 \leq n \leq 500$

思路：不简单的交互，很容易想歪，好像是金牌题？

首先我们会想，去动态维护最终的链，然后一步步插入（不然题目为啥给 $O(n^2)$ 的数据）。

其次，看到这个 $2 \times n-3$ ，会想到之前做过的一个 D2c，大概是这样子的，就是先用某种特殊手段简化前三个元素，使其少问一次，然后再对后面的其他元素进行统一处理。

接着，发现如果已经询问出 $a_i \lt a_j$ ，就能再用两次询问，询问出 $a_k$ 的情况，首先询问 $ask(k,i)$ ，如果 $a_k \gt a_i$ ，再次询问 $ask(k,j)$ ，如果 $a_k \gt a_j$ ，直接插到最后去，否则把 $a_k$ 插到 $a_j$ 前面。如果 $a_k \leq a_i$ ，那么此时取整条链的头部 $st$ ，询问 $ask(k,st)$ ，如果 $a_k \gt a_{st}$ ，那么把 $a_k$ 插到 $a_i$ 后面，否则插到 $a_st$ 前面。

然后，问题就在于如何找出 $a_i \lt a_j$ ，其实完全可以考虑，还是维护一条当前的链 $a_{st} \ldots a_{ed}$ ，其中每个 $a_i$ 之间都是小于等于关系，每次先询问 $ask(i,st)$ ，如果 $a_i \gt a_{st}$ ，那么再询问 $ask(i,ed)$ ，如果 $a_i \gt a_{ed}$ ，那么得到 $a_{st} \lt a_{i}$ ，化为上一种情况，否则直接插在 $a_{ed}$ 前面。如果 $a_i \leq a_{st}$ ，此时询问 $ask(st,i)$ ，如果 $a_{st} \gt a_i$ ，那么 $a_i \lt a_{ed}$ ，插到最前面，化为上一种情况，否则随便插一下。


```cpp
ll ask(ll l, ll r) {
    cout << "? " << l << ' ' << r << '\n';
    cout.flush();
    ll op;
    cin >> op;
    return op;
}
void report(vl& res) {
    cout << "! ";
    rep(i, 0, sz(res) - 1) cout << res[i] << ' ';
    cout << '\n';
    cout.flush();
    return;
}
void solve() {
    ll n;
    cin >> n;
    vl res;
    res.push_back(1), res.push_back(2);
    ll idx = -1;
    if (ask(1, 2)) {
        swap(res[0], res[1]), idx = 0;
    }
    rep(i, 3, n) {
        if (idx == -1) {
            ll st = res[0], ed = res[sz(res) - 1];
            if (ask(i, st)) {
                if (ask(i, ed)) {
                    idx = sz(res) - 1;
                    res.push_back(i);
                } else {
                    idx = sz(res) - 2;
                    res.insert(res.end() - 1, i);
                }
            } else {
                if (ask(st, i)) {
                    idx = 0;
                    res.insert(res.begin(), i);
                } else
                    res.insert(res.end() - 1, i);
            }
        } else {
            ll l = res[idx], r = res[idx + 1];
            if (ask(i, l)) {
                if (ask(i, r))
                    res.push_back(i);
                else
                    res.insert(res.begin() + idx + 1, i);
            } else {
                ll st = res[0], ed = res[sz(res) - 1];
                if (ask(i, st))
                    res.insert(res.begin() + idx + 1, i), idx++;
                else
                    res.insert(res.begin(), i), idx++;
            }
        }
    }
    report(res);
    return;
}
```

## I
题目大意：这是一道通信题。

给定一棵 $n$ 个节点， $m$ 条边的森林，现在 $A$ 需要给每个点 $0 \sim n-1$ 附上 $val_i$ ，并且 $1 \leq val_i \leq 2 \times n$ ，然后系统会自动打乱这些编号，使得编号信息被隐藏。随后， $B$ 会收到打乱后的 $val_0,\ldots,val_{n-1}$ ，现在 $B$ 需要还原这些 $val$ 对应的原来树中结构，只需要采用打乱后的下标即可。

数据范围： $1 \leq n \leq 2 \cdot 10^5$

思路：简单题。首先看到 $1 \sim 2 \times n$ ，很容易想到要使用欧拉序。

然后，我们想到，欧拉序分为 $t_{in}$ 和 $t_{out}$ ，如果要存两个信息肯定是不可行的，但是此时发现，如果我们已经知道所有的 $t_{in}$ ，剩下的就都是 $t_{out}$ ，然后就可以令 $val_i=t_{in}$ ，然后按照 $t_{in}$ 排序来模拟栈。

也就是说，对于 $1 \sim 2 \times n$ 遍历，如果遇到 $t_{in}$ ，那么当前栈顶就是它的父亲，把他俩连起来之后入栈，否则，直接弹出栈顶即可，这就做完了。

```cpp
void solve1() {
    ll n, m, x, y;
    cin >> n >> m;
    vvl ma(n);
    rep(_, 0, m - 1) {
        cin >> x >> y;
        ma[x - 1].push_back(y - 1);
        ma[y - 1].push_back(x - 1);
    }
    vector<bool> vis(n, false);
    vl res(n);
    ll cnt = 0;
    auto dfs = [&](this auto&& dfs, int x, int pa) -> void {
        vis[x] = true;
        res[x] = ++cnt;
        for (auto& p : ma[x]) {
            if (p == pa) continue;
            dfs(p, x);
        }
        cnt++;
        return;
    };
    rep(i, 0, n - 1) {
        if (!vis[i]) dfs(i, -1);
    }
    for (auto& p : res) cout << p << ' ';
    cout << endl;
    return;
}
void solve2() {
    ll n;
    cin >> n;
    vl a(n);
    rep(i, 0, n - 1) cin >> a[i];
    vector<pll> ma;
    rep(i, 0, n - 1) ma.emplace_back(a[i], i + 1);
    sort(all(ma), [&](const pll& x, const pll& y) { return x.first < y.first; });
    vector<pll> edges;
    stack<ll> s;
    rep(i, 0, n - 1) {
        if (i > 0) {
            rep(j, 1, ma[i].first - ma[i - 1].first - 1) s.pop();
        }
        if (!s.empty()) edges.emplace_back(s.top(), ma[i].second);
        s.push(ma[i].second);
    }
    cout << sz(edges) << endl;
    for (auto& [x, y] : edges) cout << x << ' ' << y << endl;
    return;
}
void solve() {
    int t;
    string s;
    cin >> s >> t;
    while (t--) {
        if (s == "cat")
            solve1();
        else
            solve2();
    }
    return;
}
```

## K
题目大意：给定数组 $a_1,a_2,\ldots,a_n$ ，满足 $a_1 \leq a_2 \leq \ldots \leq a_n$ ，现在需要你构造 $b_1,\ldots,b_n$ ，且满足限制 $|b_i-b_{i-1}| \geq l_i,\forall 2 \leq i \leq n$ ，请求出所有可能的构造中 $\max\limits_{i=1}^{n}|a_i-b_i|$ 的最小值，注意不用给出具体构造。

数据范围： $2 \leq n \leq 10^5,1 \leq a_i,l_i \leq 10^9$

思路：签到题。

很容易想到二分答案，此时考虑 $\max\limits_{i=1}^{n}|a_i-b_i| \leq mid$ ，于是可以转化为递推的区间，只需要维护上一个区间的可能取值，然后通过递推条件，比较这个区间是否存在满足条件的值即可。

```cpp
void solve() {
    ll n;
    cin >> n;
    vl a(n), b(n);
    rep(i, 0, n - 1) cin >> a[i];
    rep(i, 1, n - 1) cin >> b[i];
    ll l = 0, r = INF, mid, ans = 0;
    // there exists a b that every |bi-ai|<=mid
    auto check = [&](ll mid) -> bool {
        vector<pll> ma;
        rep(i, 0, n - 1) ma.emplace_back(a[i] - mid, a[i] + mid);
        ll L = ma[0].first, R = ma[0].second;
        rep(i, 1, n - 1) {
            ll l1 = ma[i].first, r1 = min(ma[i].second, R - b[i]);
            ll l2 = max(ma[i].first, L + b[i]), r2 = ma[i].second;
            if (l1 > r1 && l2 > r2) return false;
            if (l1 > r1) l1 = INF, r1 = -INF;
            if (l2 > r2) l2 = INF, r2 = -INF;
            L = min(l1, l2), R = max(r1, r2);
        }
        return true;
    };
    while (l <= r) {
        mid = (l + r) / 2;
        if (check(mid)) {
            ans = mid;
            r = mid - 1;
        } else
            l = mid + 1;
    }
    cout << ans << endl;
    return;
}
```

## M
题目大意：给定 $n$ 个闭区间 $[l_i,r_i]$ ，现在想要构造一个数列 $a_1,a_2,\ldots,a_n$ ，满足 $l_i \leq a_i \leq r_i$ ，定义 $a_i$ 为好的位置当且仅当 $a_i \gt a_j, \forall j<i$ ，请求出可能的最少好位置数。

数据范围： $1 \leq n \leq 10^6, -10^9 \leq l_i,r_i \leq 10^9$

思路：签到题。

首先发现，如果我钦定这个位置是最大值，那么为了让之后的不可能成为前缀最大，我肯定取 $r_i$ 。

然后看到这种数据范围，考虑从左到右遍历，不难发现如果当前位置无论如何都要成为前缀最大值，那么直接把前面没用过的前缀最大 $r$ 拿过来顶即可。

```cpp
constexpr ll INF = LLONG_MAX / 3;
constexpr ll MOD = 998244353;
void solve() {
    ll n;
    cin >> n;
    vector<pll> ma(n);
    rep(i, 0, n - 1) cin >> ma[i].first >> ma[i].second;
    ll las = -INF, mx = -INF;
    ll ans = 0;
    rep(i, 0, n - 1) {
        mx = max(mx, ma[i].second);
        if (ma[i].first > las) {
            las = mx, ans++;
        }
    }
    cout << ans << endl;
    return;
}
```
