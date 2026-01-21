---
title: 二次元修炼日记！
date: 2026-01-21
encrypt: true
image: 5.png
categories: 
    - 算法
    - 动漫
---
## 前言
这里是一个二次元的堕落之路啦，虽然窝觉得也没人能看到这里~

看番的口味从奇幻到党争到百合再到萌豚，说明越来越躺平摆烂了，事情实在太多，有时候腾出点时间写写博客就是莫大的消遣了。

好吧，也许ICS的笔记应该排除在外，不过谁会拒绝可爱的二次元纸片人呢哈哈哈，光是看着就很治愈耶~

那么进入正题，为什么要开始写这一篇长期更新的博文？

众所周知，Codeforces的题目，思维要求非常灵活，并且目前我所在的分段，刚好就是拼Div2前几道题的思维与手速。

因此，进行复盘是非常必要的，包括我之前板刷的时候，不时会发现自己赛时会做但是第二次不会的情况。

希望在未来一年里Rating能有所进步，加油加油！

- By Elainafan，2025.11.29，写于发烧之时

## 看番日记
| Date       | Round      | div    | id   | sol | rk   | perf | A   | B   | C   | D   | E   | F   | G   | H   | I   |
| ---------- | ---------- | ------ | ---- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025.10.12 | R1058      | div2   | 2160 | 3   | vp   | vp   | √   | √   | √   |     |     |     |     |     |     |  |
| 2025.10.19 | R1060      | div2   | 2154 | 3   | 3145 | 1536 | √   | √   | √   |     |     |     |     |     |     |  |
| 2025.10.25 | R1061      | div2   | 2156 | 2   | 9898 | 1033 | √   | √   | B   |     |     |     |     |     |     |  |
| 2025.10.28 | R1062      | div4   | 2167 | 5   | vp   | vp   | √   | √   | √   | √   |     |     | √   |     |     |  |
| 2025.11.10 | R1063      | div2   | 2163 | 2   | 2470 | 1582 | √   |     | √   |     |     |     |     |     |     |  |
| 2025.11.14 | Edu184     | edu    | 2169 | 3   | 4838 | 1333 | H   | √   | √   | √   |     |     |     |     |     |  |
| 2025.11.20 | R1065      | div3   | 2171 | 5   | 2504 | 1474 | √   | √   | √   | √   | √   |     | B   |     |     |  |
| 2025.11.28 | Edu185     | edu    | 2170 | 3   | 1885 | 1658 | √   | √   | √   |     |     |     |     |     |     |  |
| 2025.11.29 | R1067      | div2   | 2158 | 3   | 2812 | 1490 | √   | √   | √   |     |     |     |     |     |     |  |
| 2025.12.03 | R1064      | div1/2 | 2166 | 3   | vp   | 1483 | √   | √   | √   |     |     |     |     |     |     |  |
| 2025.12.05 | R1068      | div2   | 2173 | 3   | 2748 | 1532 | √   | √   | √   |     |     |     |     |     |     |  |
| 2025.12.06 | R1069      | div1/2 | 2175 | 3   | 934  | 1728 | √   | √   | √   | B   |     |     |     |     |     |  |
| 2025.12.11 | R1070      | div2   | 2176 | 3   | 2051 | 1611 | √   | √   | √   | B   |     |     |     |     |     |  |
| 2025.12.17 | GR30       | div1+2 | 2164 | 3   | vp   | 1521 | √   | √   | √   |     |     |     |     |     |     |  |
| 2025.12.19 | GR31       | div1+2 | 2180 | 3   | 1870 | 1800 | √   | √   | √   | B   |     |     |     |     |     |  |
| 2025.12.23 | R1071      | div3   | 2179 | 5   | 1266 | 1758 | √   | √   | √   | √   | √   | B   |     |     |     |  |
| 2025.12.29 | Edu186     | edu    | 2182 | 3   | 5418 | 1256 | √   | √   | √   | B   | B   |     |     |     |     |  |
| 2026.01.07 | Gb 2025    | div1+2 | 2178 | 4   | vp   | 1642 | √   | √   | √   | √   | B   |     |     |     |     |  |
| 2026.01.07 | Hello 2026 | div1+2 | 2183 | 4   | 1989 | 1786 | √   | √   | √   | √   |     |     |     |     |     |  |
| 2026.01.12 | R1072      | div3   | 2184 | 6   | 822  | 1921 | √   | √   | √   | √   | √   | √   | B   |     |     |  |
| 2026.01.17 | R1073      | div1/2 | 2191 | 4   | 4312 | 1330 | √   | √   | √   | √   |     |     |     |     |     |  |
| 2025.01.18 | R1074      | div4   | 2185 | 7   | 679  | 1997 | √   | √   | √   | √   | √   | √   | √   |     |     |  |

## Codeforces Round #1072(Div.3)
第一次在d3做出六道题，事实上G理论也能出，只是AB花太多时间了，唉唉我的AK。

也是第一次写这样的博文，瞎写的，多多见谅~
### C Huge Pile
题目大意： 有一堆大小为 $n$ 的苹果，每次可以对一堆苹果进行操作，将其分为大小为 $\lfloor \frac{n}{2} \rfloor$ 和 $\lceil \frac{n}{2} \rceil$ 的两堆，问能否得到大小为 $k$ 的一堆，若能请给出最少操作次数。

数据范围： $1 \leq n,k \leq 10^9$

思路：就是裸的DFS啊，这个时间复杂度绝对不会爆的，放心放心~

```cpp
void solve() {
    ll n, k;
    cin >> n >> k;
    if (n < k) {
        cout << -1 << endl;
        return;
    }
    int ans = INT_MAX;
    map<ll, int> ma;
    auto dfs = [&](this auto&& dfs, ll x, int t) {
        if (ma.count(x)) return;
        if (x < k) return;
        ma[x]++;
        if (x == k) {
            ans = min(ans, t);
            return;
        }
        if (x % 2 == 0)
            dfs(x / 2, t + 1);
        else {
            dfs(x / 2, t + 1);
            dfs(x / 2 + 1, t + 1);
        }
        return;
    };
    dfs(n, 0);
    if (ans == INT_MAX)
        cout << -1 << endl;
    else
        cout << ans << endl;
    return;
}
```

### D Unfair Game
题目大意：Alice跟Bob玩游戏，Alice每次可以进行两种操作中的其中一种，即将当前数减一或者将当前数除以2（必须是偶数时才能进行），当Alice将这个数变为0时，她就获胜了。给出 $n=2^d$ ，Bob需要求出 $1 \sim n$ 中，作为初始值无法使Alice在 $k$ 个回合内获胜的个数。

数据范围： $1 \leq n,k \leq 10^9$

思路：考虑最高位为第 $i$ 位时，在 $1 \sim (i-1)$ 位共有 $j$ 位为0，则低位共有 $i-1-j$ 个1，每个1提供2步的容错，每个0跟最高位1提供1步的容错，因此一共需要 $2*(i-1-j)+j+1=2*i-j-1$ 步，考虑当其 $>k$ 时的组合数即可，注意组合数初始化的方法。

```cpp
ll cn[32][32];
void init() {
    for (int i = 0; i <= 31; i++) {
        cn[i][0] = cn[i][i] = 1;
        for (int j = 1; j < i; j++) {
            cn[i][j] = cn[i - 1][j - 1] + cn[i - 1][j];
        }
    }
}
void solve() {
    int n, k;
    cin >> n >> k;
    int tem = __lg(n);
    tem++;
    ll ans = 0;
    for (int i = 1; i <= tem - 1; i++) {
        if (2 * i - 1 <= k) continue;
        for (int j = 0; j <= i - 1; j++) {
            if (2 * i - j - 1 > k) ans += cn[i - 1][j];
        }
    }
    if (tem > k) ans++;
    cout << ans << endl;
    return;
}
```

### E Exquisite Array
题目大意：如果一个数组至少有两个元素，且其中任意相邻元素至少相差 $k$ ，称其为 $k-$ 数组。给定一个 $1 \sim n$ 的排列 ，请求出从 $k \in \{1 \sim n-1\}$ 的 $k-$ 子数组个数。

数据范围： $2 \leq n \leq 10^5$

思路：首先预处理出所有相邻元素之间的差值。考虑贡献法，先用单调栈处理出某个差值作为子数组最小值对应的贡献，倒着遍历 $n-1 \sim 1$ ，如果当前差值刚好等于 $i$ ，则考虑其作为子数组最小元素的贡献，并累加到总值中即可，注意相邻差值若相等，两侧预处理时一侧有等号一侧没有等号，算是比较板的题。

```cpp
void solve() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i <= n - 1; i++) cin >> a[i];
    vector<int> res(n - 1);
    vector<int> diff(n - 1);
    for (int i = 0; i < n - 1; i++) diff[i] = abs(a[i + 1] - a[i]);
    vector<int> r(n - 1, n - 1);
    vector<int> l(n - 1, -1);
    stack<int> s;
    vector<vector<int>> ma(n);
    for (int i = 0; i < n - 1; i++) ma[diff[i]].push_back(i);
    for (int i = n - 2; i >= 0; i--) {
        while (!s.empty() && diff[s.top()] >= diff[i]) s.pop();
        if (!s.empty()) r[i] = s.top();
        s.push(i);
    }
    while (!s.empty()) s.pop();
    for (int i = 0; i <= n - 2; i++) {
        while (!s.empty() && diff[s.top()] > diff[i]) s.pop();
        if (!s.empty()) l[i] = s.top();
        s.push(i);
    }
    vector<ll> ans(n);
    ll cnt = 0;
    for (int i = n - 1; i >= 1; i--) {
        for (int p : ma[i]) {
            cnt += 1LL * (r[p] - p) * (p - l[p]);
        }
        ans[i] = cnt;
    }
    for (int i = 1; i <= n - 1; i++) cout << ans[i] << ' ';
    cout << endl;
    return;
}
```

注：本题似乎还存在并查集+链表的做法，放一个朋友的提交链接在这里[Kita3's submission](https://codeforces.com/contest/2184/submission/357673035)。

### F Cherry Tree
题目大意：给一棵顶点编号为 $1 \sim n$ 的有根树，树根默认为1。每个叶子都有一颗樱桃，每次操作可以选择某个节点使以其为根的子树的所有叶子的樱桃掉落，若某个叶子的樱桃已经掉落则不能被摇动第二次，问是否能使摇动次数为3的倍数？

数据范围： $2 \leq n \leq 2 \cdot 10^5$ 

思路：一眼树上状态机，如果难点可以出树上背包？可以作为思考题。首先，需要知道的是对于某个非根节点，摇动它能节省的次数就是（以它为根子树的叶子数-1），然后就可以对每个节点维护，以其为根的子树中是否存在节省操作数模3的余数为1或为2的状态，逐步回传即可。

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
    int ans = 0;
    for (int i = 0; i <= n - 1; i++) {
        if (ma[i].size() == 1 && i != 0) ans++;
    }
    if (ans % 3 == 0) {
        cout << "YES" << endl;
        return;
    }
    int r = ans % 3;
    bool flag = false;
    vector<int> mt(n);
    auto dfs = [&](this auto&& dfs, int x, int pa) -> int {
        if (ma[x].size() == 1 && pa != -1) return 1;
        int cnt = 0;
        int cnt1 = 0, cnt2 = 0;
        for (int p : ma[x]) {
            if (p == pa) continue;
            cnt += dfs(p, x);
        }
        mt[x] = cnt;
        if ((cnt + 2) % 3 == r) flag = true;
        return cnt;
    };
    auto dfs2 = [&](this auto&& dfs2, int x, int pa) -> pair<bool, bool> {
        if (ma[x].size() == 1 && pa != -1) return {false, false};
        bool pd1 = false, pd2 = false;
        for (int p : ma[x]) {
            if (p == pa) continue;
            auto tem = dfs2(p, x);
            if (pd1 == true && tem.first) pd2 = true;
            if (pd2 == true && tem.second) pd1 = true;
            pd1 = pd1 | tem.first;
            pd2 = pd2 | tem.second;
        }
        if (r == 1 && pd1) flag = true;
        if (r == 2 && pd2) flag = true;
        if (mt[x] % 3 == 2) pd1 = true;
        if (mt[x] % 3 == 0) pd2 = true;
        return {pd1, pd2};
    };
    dfs(0, -1);
    dfs2(0, -1);
    if (flag)
        cout << "YES" << endl;
    else
        cout << "NO" << endl;
    return;
}
```

### G Nastiness of Segments
题目大意：给定编号为 $1 \sim n$ 的 $n$ 个元素 $a_1,a_2,\ldots,a_n$ ，定义 $[l,r](1 \leq l \leq r \leq n)$ 的恶心度为满足 $\mathrm{min}(a_l,a_{l+1},\ldots,a_{l+d})=d, 0 \leq d \leq r-l$ 的 $d$ 的个数。

现在给定 $q$ 个查询，分别为操作1和操作2，操作1把 $a[idx]$ 改为 $x$ ，操作2查询 $[l,r]$ 的恶心度。

数据范围： $1 \leq n,q \leq 2 \cdot 10^5, 1 \leq a_i \leq 2 \cdot 10^5, 1 \leq x \leq 2 \cdot 10^5$

思路：首先，注意到 $\mathrm{min}(a_l,\ldots,a_{l+d})$ 为单调递减函数，而 $d$ 为严格单调递增函数，因此它们的交点至多只有一个。

一种显然的思路是，用线段树动态维护区间最小值，同时在 $[l,r]$ 上二分，线段树的查询复杂度为 $O(logn)$ ，因此总的时间复杂度为 $O(q logn logn)$

```cpp
template <typename T>
class SegmentTree {
    int n;
    vector<T> tree;
    T merge_val(T a, T b) const { return min(a, b); }  // 合并子树

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

    void update(int node, int l, int r, int i, T val) {
        if (l == r) {
            tree[node] = val;
            return;
        }
        int m = (l + r) / 2;
        if (i <= m)
            update(node * 2, l, m, i, val);
        else
            update(node * 2 + 1, m + 1, r, i, val);
        maintain(node);
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

    int find_first(int node, int l, int r, int ql, int qr, T val) const {
        if (r < ql || l > qr) return -1;
        if (tree[node] < val) return -1;
        if (l == r) return l;
        int m = (l + r) >> 1;
        int res = find_first(node << 1, l, m, ql, qr, val);
        if (res != -1) return res;
        return find_first(node << 1 | 1, m + 1, r, ql, qr, val);
    } 

    int find_last(int node, int l, int r, int ql, int qr, T val) const {
        if (r < ql || l > qr) return -1;
        if (tree[node] < val) return -1;
        if (l == r) return l;
        int m = (l + r) >> 1;
        int res = find_last(node << 1 | 1, m + 1, r, ql, qr, val);
        if (res != -1) return res;
        return find_last(node << 1, l, m, ql, qr, val);
    }

public:
    SegmentTree(int n, T init_val) : SegmentTree(vector<T>(n, init_val)) {}

    SegmentTree(const vector<T>& a) : n(a.size()), tree(2 << bit_width(a.size() - 1)) { build(a, 1, 0, n - 1); }  // 传入一个数组维护

    void update(int i, T val) { update(1, 0, n - 1, i, val); }  // 更新i的值为val

    T query(int ql, int qr) const { return query(1, 0, n - 1, ql, qr); }  // 查询[ql,qr]的值

    T get(int i) const { return query(1, 0, n - 1, i, i); }  // 取出i处的值

    int find_first(int ql, int qr, T val) const { return find_first(1, 0, n - 1, ql, qr, val); } // 查询[ql,qr]中第一个满足条件的下标

    int find_last(int ql, int qr, T val) const { return find_last(1, 0, n - 1, ql, qr, val); } // 查询[ql,qr]中最后一个满足条件的下标
};
void solve() {
    int n, q, op, x, y;
    cin >> n >> q;
    vector<int> a(n);
    for (int i = 0; i <= n - 1; i++) cin >> a[i];
    SegmentTree tree(a);
    auto check = [&](this auto&& check, int l, int mid) -> bool {
        int tem = tree.query(l, mid);
        if (tem <= mid - l) return true;
        return false;
    };
    for (int i = 1; i <= q; i++) {
        cin >> op;
        if (op == 1) {
            cin >> x >> y;
            tree.update(x - 1, y);
        } else {
            cin >> x >> y;
            int sl = --x, sr = --y;
            int l = sl, r = sr, mid;
            while (l + 1 < r) {
                mid = (l + r) / 2;
                if (check(sl, mid))
                    r = mid;
                else
                    l = mid;
            }
            if (tree.query(sl, r) == r - sl)
                cout << 1 << endl;
            else
                cout << 0 << endl;
        }
    }
    return;
}
```

但是，这种做法并不是最优的，是否能直接进行线段树二分，把复杂度降到 $O(qlogn)$ ？ 这里先瞎放张图。

![](4.png)

当然，上面是普通的线段树二分流程，而这题固定了左端点，就要考虑怎么求右端点了。

回想起线段树有个性质，即某个节点的左子树必然先于其右子树被遍历到，因此，到遍历到某个 $[l,r]$ ，则 $[1,l]$ 必然都被遍历过，因此若遍历到被 $[ql,qr]$ 完全包裹的区间 $[l,r]$ ，则代表之前所有的 $[ql,l)$ 都被遍历过了，而且都是以完全包裹的形式，因此可以使用一个全局变量（或者直接在查找时传引用），当完全包裹并且不行的时候就进行更新（因为如果行那么直接接着二分，直到不行被更新或者得到一个点）。

```cpp
template <typename T>
class SegmentTree {
    int n;
    vector<T> tree;
    T merge_val(T a, T b) const { return min(a, b); }  // 合并子树

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

    void update(int node, int l, int r, int i, T val) {
        if (l == r) {
            tree[node] = val;
            return;
        }
        int m = (l + r) / 2;
        if (i <= m)
            update(node * 2, l, m, i, val);
        else
            update(node * 2 + 1, m + 1, r, i, val);
        maintain(node);
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

    int find_first(int node, int l, int r, int ql, int qr, T& val) const {
        if (r < ql || l > qr) return -1;
        if (ql <= l && r <= qr && min(tree[node], val) > r - ql) {
            val = min(tree[node], val);
            return -1;
        }
        if (l == r) return l;
        int m = (l + r) >> 1;
        int res = find_first(node << 1, l, m, ql, qr, val);
        if (res != -1) return res;
        return find_first(node << 1 | 1, m + 1, r, ql, qr, val);
    }

    int find_last(int node, int l, int r, int ql, int qr, T val) const {
        if (r < ql || l > qr) return -1;
        if (tree[node] < val) return -1;
        if (l == r) return l;
        int m = (l + r) >> 1;
        int res = find_last(node << 1 | 1, m + 1, r, ql, qr, val);
        if (res != -1) return res;
        return find_last(node << 1, l, m, ql, qr, val);
    }

public:
    SegmentTree(int n, T init_val) : SegmentTree(vector<T>(n, init_val)) {}

    SegmentTree(const vector<T>& a) : n(a.size()), tree(2 << bit_width(a.size() - 1)) { build(a, 1, 0, n - 1); }  // 传入一个数组维护

    void update(int i, T val) { update(1, 0, n - 1, i, val); }  // 更新i的值为val

    T query(int ql, int qr) const { return query(1, 0, n - 1, ql, qr); }  // 查询[ql,qr]的值

    T get(int i) const { return query(1, 0, n - 1, i, i); }  // 取出i处的值

    int find_first(int ql, int qr, T& val) const { return find_first(1, 0, n - 1, ql, qr, val); }  // 查询[ql,qr]中第一个满足条件的下标

    int find_last(int ql, int qr, T val) const { return find_last(1, 0, n - 1, ql, qr, val); }  // 查询[ql,qr]中最后一个满足条件的下标
};
void solve() {
    int n, q, op, x, y;
    cin >> n >> q;
    vector<int> a(n);
    for (int i = 0; i <= n - 1; i++) cin >> a[i];
    SegmentTree tree(a);
    for (int i = 1; i <= q; i++) {
        cin >> op;
        if (op == 1) {
            cin >> x >> y;
            tree.update(x - 1, y);
        } else {
            cin >> x >> y;
            int sl = --x, sr = --y;
            int cur = INT_MAX;
            int tem = tree.find_first(sl, sr, cur);
            if (tem != -1 && tree.query(sl, tem) == tem - sl)
                cout << 1 << endl;
            else
                cout << 0 << endl;
        }
    }
    return;
}
```

最后是灵神的点评：

![](3.jpg)

## Codeforces Round #1074(Div.4) 
D脑子抽了WA了五发，H不是我能做出来的，赛时出A-G差不多了，反正是Unr。

### D OutOfMemoryError
题目大意： 给定 $a_1,a_2,\ldots,a_n$ ，进行 $m$ 次操作，每次 $a_{b_i}+=c_i$ ，当任意元素大于 $h$ 时，所有元素重置回初始值，请求出最后的结果数。

数据范围： $1 \leq n,m \leq 2 \cdot 10^5,1 \leq h \leq 10^9$ ，其中 $n,m$ 的和不超过 $2 \cdot 10^5$ 。

思路：一开始想的就是模拟，但是没想到d4D就能上强度，直接吃了一发TLE，随后脑子有点蠢，一直想着二分最后一次重置或者倒序遍历，但是注意到重置只和顺序遍历有关，倒序或者二分会丢失这一信息，因此还是顺序遍历。

于是，顺序遍历怎么优化呢？由于每个数组的变化是稀疏的，因此完全可以用一个数组存储上次重置到这次的所有变化而不更新原数组，每次检测到重置则直接清空数组，最终用存储的变化更新原来数组就是最终结果，时间复杂度为 $O(N+M)$ 。

```cpp
void solve() {
    int n, m, h;
    cin >> n >> m >> h;
    vector<int> a(n);
    for (int i = 0; i <= n - 1; i++) cin >> a[i];
    vector<int> b(m);
    vector<int> c(m);
    vector<int> diff(n);
    vector<int> re;
    for (int i = 0; i <= m - 1; i++) {
        cin >> b[i] >> c[i];
        diff[b[i] - 1] += c[i];
        re.push_back(i);
        if (diff[b[i] - 1] + a[b[i] - 1] > h) {
            for (int p : re) {
                diff[b[p] - 1] = 0;
            }
            re.clear();
        }
    }
    for (int i = 0; i <= n - 1; i++) cout << a[i] + diff[i] << ' ';
    cout << endl;
    return;
}
```

### E The Robotic Rush
题目大意：在一条数轴上有 $n$ 个机器人和 $m$ 个障碍物，机器人走到障碍物上就会死。现在给定长度为 $k$ 的字符串，其为``L``则代表机器人全部往左走一步，反之全部往右走一步，问对于所有的 $i (1 \leq i \leq k)$ ，给出第 $i$ 步后活着的机器人数量。

数据范围： $1 \leq n,m,k \leq 2 \cdot 10^5$ ，它们的和不超过 $2 \cdot 10^5$

思路：注意到机器人如果死，必然是走到左右的障碍物死的，因此可以预处理轨迹的时间点，再预处理左右的距离，得到每个时间点死去的机器人数量，最后使用差分即可。

```cpp
void solve() {
    int n, m, k;
    cin >> n >> m >> k;
    vector<int> a(n);
    vector<int> b(m);
    for (int i = 0; i <= n - 1; i++) cin >> a[i];
    for (int i = 0; i <= m - 1; i++) cin >> b[i];
    ranges::sort(b);
    string s;
    cin >> s;
    vector<int> mo(k + 1);
    vector<int> l(n, INT_MIN);
    vector<int> r(n, INT_MAX);
    vector<int> die(k + 1, 0);
    map<int, int> ma;
    for (int i = 1; i <= k; i++) {
        if (s[i - 1] == 'L')
            mo[i] = mo[i - 1] - 1;
        else
            mo[i] = mo[i - 1] + 1;
        if (!ma.count(mo[i])) ma[mo[i]] = i;
    }
    for (int i = 0; i <= n - 1; i++) {
        auto x = ranges::lower_bound(b, a[i]);
        if (x == b.end()) {
            l[i] = *(--x) - a[i];
            if (ma.count(l[i])) die[ma[l[i]]]++;
        } else if (x == b.begin()) {
            r[i] = *x - a[i];
            if (ma.count(r[i])) die[ma[r[i]]]++;
        } else {
            r[i] = *x - a[i];
            l[i] = *(--x) - a[i];
            int tem = INT_MAX;
            if (ma.count(l[i])) tem = min(tem, ma[l[i]]);
            if (ma.count(r[i])) tem = min(tem, ma[r[i]]);
            if (tem != INT_MAX) die[tem]++;
        }
    }
    for (int i = 2; i <= k; i++) die[i] += die[i - 1];
    for (int i = 1; i <= k; i++) {
        cout << n - die[i] << ' ';
    }
    cout << endl;
    return;
}
```

### F BattleCows
题目大意：现在给定 $2^n$ 头牛，它们有自己的技能等级 $a_i$ 并各自属于自己的一个栈，每个栈的总技能等级记为其中所有牛技能等级的异或和，现在会重复进行以下过程：奇数位置的栈与右边的栈进行战斗，技能等级较高的栈赢得比赛，若平局则奇数位置的赢得比赛。赢家会把自己的栈堆叠到输家上面，形成新的栈，如此直至最后只剩一个栈。

现有 $q$ 次查询，每次查询将牛 $b$ 的技能等级改变为 $c$ （注意是模拟改变，不是永久改变）， 问最终时有多少头牛在它上面。

数据范围： $1 \leq n \leq 18, 1 \leq q \leq 2 \cdot 10^5, 1 \leq a_i \leq 2^{30}, 1 \leq b \leq 2^n, 1 \leq c \leq 2^{30}$

思路：由于是动态查询和动态修改，很容易想到线段树。而整个过程就是类似二叉树自底向上的一个过程，只需要每次模拟需要查询的牛的所在位置，并用贡献法统计它周围栈比赛会跑到它上面的牛数量即可，经过估算发现复杂度为 $O(qn^2)$ ，显然是可以过的。

```cpp
template <typename T>
class SegmentTree {
    int n;
    vector<T> tree;
    T merge_val(T a, T b) const { return a ^ b; }  // 合并子树

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

    void update(int node, int l, int r, int i, T val) {
        if (l == r) {
            tree[node] = val;
            return;
        }
        int m = (l + r) / 2;
        if (i <= m)
            update(node * 2, l, m, i, val);
        else
            update(node * 2 + 1, m + 1, r, i, val);
        maintain(node);
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

    int find_first(int node, int l, int r, int ql, int qr, T val) const {
        if (r < ql || l > qr) return -1;
        if (tree[node] < val) return -1;
        if (l == r) return l;
        int m = (l + r) >> 1;
        int res = find_first(node << 1, l, m, ql, qr, val);
        if (res != -1) return res;
        return find_first(node << 1 | 1, m + 1, r, ql, qr, val);
    }  // 若遇到固定左端点的情况，需要使用全局变量（或者传入引用）记录前缀分段最大值，加一个被待求区间完全覆盖的剪枝

    int find_last(int node, int l, int r, int ql, int qr, T val) const {
        if (r < ql || l > qr) return -1;
        if (tree[node] < val) return -1;
        if (l == r) return l;
        int m = (l + r) >> 1;
        int res = find_last(node << 1 | 1, m + 1, r, ql, qr, val);
        if (res != -1) return res;
        return find_last(node << 1, l, m, ql, qr, val);
    }

public:
    SegmentTree(int n, T init_val) : SegmentTree(vector<T>(n, init_val)) {}

    SegmentTree(const vector<T>& a) : n(a.size()), tree(2 << bit_width(a.size() - 1)) { build(a, 1, 0, n - 1); }  // 传入一个数组维护

    void update(int i, T val) { update(1, 0, n - 1, i, val); }  // 更新i的值为val

    T query(int ql, int qr) const { return query(1, 0, n - 1, ql, qr); }  // 查询[ql,qr]的值

    T get(int i) const { return query(1, 0, n - 1, i, i); }  // 取出i处的值

    int find_first(int ql, int qr, T val) const { return find_first(1, 0, n - 1, ql, qr, val); }  // 查询[ql,qr]中第一个满足条件的下标

    int find_last(int ql, int qr, T val) const { return find_last(1, 0, n - 1, ql, qr, val); }  // 查询[ql,qr]中最后一个满足条件的下标
};
void solve() {
    int n, q, b, c;
    cin >> n >> q;
    vector<int> a((1 << n));
    for (int i = 0; i <= (1 << n) - 1; i++) cin >> a[i];
    SegmentTree tree(a);
    for (int i = 1; i <= q; i++) {
        cin >> b >> c;
        b--;
        int tem = a[b];
        tree.update(b, c);
        int tem2 = b;
        int ans = 0;
        for (int j = 0; j <= n - 1; j++) {
            int tem3 = tem2 >> j;
            if (tem3 & 1) {
                int pre = tree.query(tem3 << j, (tem3 << j) + (1 << j) - 1);
                int pre2 = tree.query((tem3 - 1) << j, (tem3 << j) - 1);
                if (pre <= pre2) ans += (1 << j);
            } else {
                int pre = tree.query(tem3 << j, (tem3 << j) + (1 << j) - 1);
                int pre2 = tree.query((tem3 + 1) << j, ((tem3 + 1) << j) + (1 << j) - 1);
                if (pre < pre2) ans += (1 << j);
            }
        }
        tree.update(b, tem);
        cout << ans << endl;
    }
    return;
}
```

### G Mixing MEXes
题目大意： 给定 $n$ 个数组 $a_1,a_2,\ldots,a_n$ ，每个数组的长度为 $l_1,l_2,\ldots,l_n$ ，现在只进行**一次**以下操作，即选择 $1 \leq i \leq n$ 与 $1 \leq j \leq l_i$ ，将 $a_{ij}$ 添加到 $a_k ( k\not ={i})$ 中，求对于所有有序对 $(i,j,k)$ ， $\sum\limits_{i=1}^{n} \mathrm{MEX}(a_i)$ 。

数据范围： $2 \leq n \leq 2 \cdot 10^5, 1 \leq l_i \leq 10^5, 0 \leq a_i \leq 10^6$ ， $l_i$ 之和不超过 $2 \cdot 10^5$ 。

思路：看到这里肯定考虑贡献法，首先判断取出的数会不会影响当前数组的MEX，即它是否在MEX的范围内，且是否有替代，同时考虑加入的数组中会不会影响该数组的MEX，注意加入的数不一定是让当前数组的MEX+1，完全可能是连接上两段不相干的数，因此需要预处理原始MEX和可能存在的缝合一次后的MEX，并计算贡献。

```cpp
void solve() {
    int n;
    cin >> n;
    vector<int> l(n);
    vector<vector<int>> a(n);
    for (int i = 0; i <= n - 1; i++) {
        cin >> l[i];
        a[i].resize(l[i]);
        for (int j = 0; j < l[i]; j++) {
            cin >> a[i][j];
        }
    }
    vector<int> mex(n, 0);
    ll tot = 0;
    ll ans = 0;
    vector<map<int, int>> ma(n);
    map<int, int> ma2;
    for (int i = 0; i <= n - 1; i++) {
        int cnt = 0;
        for (int& p : a[i]) ma[i][p]++;
        while (ma[i].count(cnt)) cnt++;
        mex[i] = cnt;
        tot += 1LL * cnt;
        int cnt2 = cnt + 1;
        while (ma[i].count(cnt2)) cnt2++;
        ma2[cnt] += cnt2 - cnt;
    }
    for (int i = 0; i <= n - 1; i++) {
        for (int j = 0; j <= l[i] - 1; j++) {
            if (a[i][j] <= mex[i]) {
                int tem = ma2[a[i][j]];
                if (ma[i][a[i][j]] >= 2) {
                    ans += (n - 1) * tot + 1LL * tem;
                } else {
                    ans += (n - 1) * tot + 1LL * tem;
                    ans -= 1LL * (n - 1) * (mex[i] - a[i][j]);
                }
            } else {
                int tem = ma2[a[i][j]];
                ans += (n - 1) * tot + 1LL * tem;
            }
        }
    }
    cout << ans << endl;
    return;
}
```