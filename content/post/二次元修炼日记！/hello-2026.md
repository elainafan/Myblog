---
title: "Hello 2026"
slug: hello-2026
date: 2026-01-07
seriesOrder: 0
encrypt: false
hidden: true
image: "/images/anime-diary/5.png"
---

## A
题目大意：

数据范围：

思路：

```cpp
void solve() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i <= n - 1; i++) cin >> a[i];
    int cnt0 = 0;
    int cnt1 = 0;
    int tem = 0;
    for (int i = 0; i <= n - 1; i++) {
        if (a[i] == 1) tem++;
        if (a[i] == 0) {
            if (tem > 0) cnt1++;
            tem = 0;
        }
        if (i == n - 1 && tem > 0) cnt1++;
    }
    tem = 0;
    for (int i = 0; i <= n - 1; i++) {
        if (a[i] == 0) tem++;
        if (a[i] == 1) {
            if (tem > 0) cnt0++;
            tem = 0;
        }
        if (i == n - 1 && tem > 0) cnt0++;
    }
    if (cnt1 >= cnt0)
        cout << "Alice" << endl;
    else
        cout << "Bob" << endl;
    return;
}
```

## B
题目大意：

数据范围：

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
题目大意：

数据范围：

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
题目大意：

数据范围：

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
题目大意：

数据范围：

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
题目大意：

数据范围：

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
