---
title: 图
date: 2025-09-14
categories:
    - 算法
slug: 数算-图
hidden: true
seriesOrder: 7
---

## 图的表示

图由顶点集合和边集合组成

$$
G=(V,E)
$$

无向图的边是一对无序顶点，有向图的边则有明确的起点和终点。边还可以携带距离、费用或容量等权值。

无向图中，与顶点关联的边数称为度。所有顶点的度数之和满足握手定理

$$
\sum_{v\in V}\deg(v)=2|E|
$$

有向图把度分为入度和出度，全部顶点的入度之和与出度之和都等于边数。

顶点序列 $v_0,v_1,\ldots,v_k$ 若满足相邻顶点之间均有边，就构成一条路径。除首尾外不重复经过顶点的路径称为简单路径，首尾相同的简单路径构成环。有向无环图简称 DAG。

无向图中任意两点之间都存在路径时，图是连通的；极大连通子图称为连通分量。有向图中任意两点能够互相到达时，它们强连通；极大强连通子图称为强连通分量。

简单图不含自环和重边。含 $n$ 个顶点的无向简单图至多有 $n(n-1)/2$ 条边，有向简单图至多有 $n(n-1)$ 条边。边数接近这个上界时称为稠密图，远小于平方级时称为稀疏图；这个区分会影响存储结构和算法实现。

图的抽象操作除了增加、删除顶点和边，还要支持枚举邻接点、读取边权和修改标记。算法若只通过这些接口访问图，邻接矩阵与邻接表便可以替换；实际复杂度仍取决于接口在具体表示下的成本。

### 邻接矩阵

含 $n$ 个顶点的图可以用 $n\times n$ 矩阵保存。无权图用零和一表示边是否存在，带权图在对应位置保存边权，并用无穷大或额外标志表示无边。

邻接矩阵始终占用 $O(n^2)$ 空间。检查一条边、增加边和删除边都是 $O(1)$ 时间；枚举一个顶点的所有邻居需要扫描一整行，时间为 $O(n)$ 。

无向图的邻接矩阵关于主对角线对称。有向图中第 $i$ 行的非零项对应顶点 $i$ 的出边，第 $j$ 列的非零项对应顶点 $j$ 的入边。

### 邻接表

邻接表为每个顶点保存一组出边。无向边会在两个端点的表中各出现一次，因此无向图占用 $O(|V|+2|E|)$ 空间，有向图占用 $O(|V|+|E|)$ 空间。

```cpp
struct Edge {
    int to;
    long long weight;
};

using Graph = std::vector<std::vector<Edge>>;
```

邻接表适合稀疏图，可以在与顶点度数成正比的时间内枚举邻居。检查指定两点之间是否有边则需要搜索边表，最坏时间与起点的出度成正比。

十字链表同时串联有向边的入边关系和出边关系，适合频繁沿两个方向遍历的动态图。实际程序中也可以直接同时维护原图和反图，以更简单的代码换取边记录的重复存储。

有向图的十字链表让每条边结点同时出现在起点的出边链和终点的入边链中。边记录至少保存起点、终点、下一条同起点边和下一条同终点边。删除一条边时，两条链都要解除链接。

无向图可以使用邻接多重表。每条边只保存一次，却分别带有连接两个端点边链的指针。它减少了无向边的重复记录，但结构与修改逻辑都比普通邻接表复杂。只需遍历的静态图通常仍直接保存两条有向边。

## 图的遍历

### 深度优先搜索

深度优先搜索（Depth First Search，DFS）沿未访问的边尽量深入，无法继续时回溯。访问标记既能避免环导致的死循环，也能保证每个顶点只被处理一次。

```cpp
void dfs(const Graph& graph, int u, std::vector<bool>& visited) {
    visited[u] = true;
    visit(u);

    for (const Edge& edge : graph[u]) {
        if (!visited[edge.to]) {
            dfs(graph, edge.to, visited);
        }
    }
}
```

图不连通时，仅从一个起点执行 DFS 无法覆盖全部顶点。需要依次检查所有顶点，对每个未访问顶点重新启动搜索。由此得到的多棵 DFS 树共同组成 DFS 森林。

邻接表中每个顶点和每条边只被检查常数次，DFS 的时间复杂度为 $O(|V|+|E|)$ 。邻接矩阵版本需要为每个顶点扫描整行，时间为 $O(|V|^2)$ 。

DFS 的递归进入与退出时间还能描述边的关系。无向图中，遇到已访问且不是父亲的邻居说明存在环。有向图使用三色标记时，指向递归栈中灰色顶点的边称为回边，它同样证明存在有向环。

DFS 森林中的树边记录了第一次发现顶点的来源。若为每个顶点保存进入时间和退出时间，顶点 $u$ 是 $v$ 的祖先当且仅当 $u$ 的时间区间包含 $v$ 的时间区间。这类信息可以继续用于拓扑排序、强连通分量和离线祖先查询。

### 广度优先搜索

广度优先搜索（Breadth First Search，BFS）使用队列保存已发现但尚未展开的顶点。它先访问距离起点一条边的顶点，再访问两条边的顶点，因此能求无权图中的最短路。

```cpp
std::vector<int> bfsDistance(const Graph& graph, int source) {
    std::vector<int> distance(graph.size(), -1);
    std::queue<int> pending;

    distance[source] = 0;
    pending.push(source);

    while (!pending.empty()) {
        int u = pending.front();
        pending.pop();

        for (const Edge& edge : graph[u]) {
            int v = edge.to;
            if (distance[v] != -1) continue;
            distance[v] = distance[u] + 1;
            pending.push(v);
        }
    }

    return distance;
}
```

BFS 与 DFS 的渐近时间相同，区别在于访问次序和保存的边界。DFS 的栈保存一条搜索路径，BFS 的队列保存当前层与下一层的边界。

若还要恢复最短路径，应在顶点第一次入队时记录前驱。目标不可达时距离保持为 `-1`；可达时沿前驱从目标走回源点，再反转序列。

```cpp
std::vector<int> restorePath(
    int source,
    int target,
    const std::vector<int>& previous) {
    if (previous[target] == -1) return {};

    std::vector<int> path;
    for (int vertex = target;; vertex = previous[vertex]) {
        path.push_back(vertex);
        if (vertex == source) break;
    }
    std::reverse(path.begin(), path.end());
    return path;
}
```

BFS 只保证边数最少。边权不同时，经过边更少的路径可能总权值更大，不能继续使用普通队列求带权最短路。

## 有向无环图

### 拓扑排序

DAG 的拓扑序是一个顶点排列，使每条有向边的起点都出现在终点之前。课程依赖、工程先后关系和编译任务都可以表示为拓扑排序问题。

Kahn 算法维护所有当前入度为零的顶点。取出一个顶点后，删除它的出边；某个邻居入度降为零时，再把邻居加入容器。

```cpp
std::vector<int> topologicalSort(const Graph& graph) {
    std::vector<int> indegree(graph.size());
    for (const auto& edges : graph) {
        for (const Edge& edge : edges) {
            ++indegree[edge.to];
        }
    }

    std::queue<int> ready;
    for (int i = 0; i < static_cast<int>(graph.size()); ++i) {
        if (indegree[i] == 0) ready.push(i);
    }

    std::vector<int> order;
    while (!ready.empty()) {
        int u = ready.front();
        ready.pop();
        order.push_back(u);

        for (const Edge& edge : graph[u]) {
            if (--indegree[edge.to] == 0) {
                ready.push(edge.to);
            }
        }
    }

    if (order.size() != graph.size()) return {};
    return order;
}
```

若最后输出的顶点少于 $|V|$ ，剩余子图中每个顶点都有入边，说明图中存在有向环。

把普通队列换成小根堆，可以得到字典序最小的拓扑序。拓扑序不一定唯一；某一步若同时有多个入度为零的顶点，它们之间没有被现有边约束，选择顺序可能产生不同合法结果。若每一步都只有一个可选顶点，拓扑序才唯一。

DFS 也能生成拓扑序。一个顶点的全部后继处理完毕后再把它加入序列，最后将序列反转。此时需要三色标记区分未访问、正在递归栈中和已经完成的顶点；遇到指向“正在访问”顶点的边，就是检测到了环。

### AOE 网与关键路径

活动在边上（Activity On Edge，AOE）的网络用顶点表示事件，用有向边表示活动，边权表示活动持续时间。事件只有在所有入边对应活动完成后才能发生，因此 AOE 网必须是 DAG。

从源事件到汇事件的最长路径长度决定整个工程最早何时结束，这条最长路径称为关键路径。这里求最长路不会遇到一般图中的正环问题，因为拓扑序保证所有边只从前向后。

按拓扑序计算事件最早发生时间 $ve$ 。源点时间为零，每条边 $u\to v$ 的持续时间为 $w$ 时执行

$$
ve[v]=\max(ve[v],ve[u]+w)
$$

汇点的 $ve$ 就是工程最短工期。再按逆拓扑序计算事件最迟发生时间 $vl$ ，所有值先设为工期，并执行

$$
vl[u]=\min(vl[u],vl[v]-w)
$$

对活动边 $u\to v$ ，最早开工时间为 $ve[u]$ ，在不延误总工期的前提下最迟开工时间为 $vl[v]-w$ 。二者相等的活动没有机动时间，属于关键活动。

```cpp
std::vector<std::pair<int, int>> criticalActivities(
    const Graph& graph,
    const std::vector<int>& order) {
    int n = graph.size();
    std::vector<long long> earliest(n);

    for (int u : order) {
        for (const Edge& edge : graph[u]) {
            earliest[edge.to] = std::max(
                earliest[edge.to], earliest[u] + edge.weight
            );
        }
    }

    long long duration = *std::max_element(earliest.begin(), earliest.end());
    std::vector<long long> latest(n, duration);

    for (auto it = order.rbegin(); it != order.rend(); ++it) {
        int u = *it;
        for (const Edge& edge : graph[u]) {
            latest[u] = std::min(
                latest[u], latest[edge.to] - edge.weight
            );
        }
    }

    std::vector<std::pair<int, int>> answer;
    for (int u = 0; u < n; ++u) {
        for (const Edge& edge : graph[u]) {
            if (earliest[u] == latest[edge.to] - edge.weight) {
                answer.push_back({u, edge.to});
            }
        }
    }
    return answer;
}
```

关键活动可能组成多条关键路径。缩短一条关键活动不一定缩短总工期，因为另一条等长关键路径仍可能决定汇点时间。

## 最短路

### 单源最短路

设 `dist[v]` 表示当前已知的源点到 $v$ 的最短距离上界。沿边 $(u,v,w)$ 尝试改进距离的操作称为松弛

$$
dist[v]\leftarrow\min(dist[v],dist[u]+w)
$$

Dijkstra 算法适用于边权非负的图。它反复选取尚未确定且距离最小的顶点 $u$ ，把 $u$ 标记为已确定，再松弛它的所有出边。

![Dijkstra 算法的距离与前驱迭代过程](assets/07-dijkstra-iterations.png)

```cpp
std::vector<long long> dijkstra(const Graph& graph, int source) {
    const long long inf = std::numeric_limits<long long>::max() / 4;
    std::vector<long long> distance(graph.size(), inf);

    using State = std::pair<long long, int>;
    std::priority_queue<State, std::vector<State>, std::greater<State>> heap;

    distance[source] = 0;
    heap.push({0, source});

    while (!heap.empty()) {
        auto [currentDistance, u] = heap.top();
        heap.pop();
        if (currentDistance != distance[u]) continue;

        for (const Edge& edge : graph[u]) {
            long long candidate = currentDistance + edge.weight;
            if (candidate >= distance[edge.to]) continue;
            distance[edge.to] = candidate;
            heap.push({candidate, edge.to});
        }
    }

    return distance;
}
```

优先队列中可能同时保留同一顶点的多个旧距离。弹出后与 `distance[u]` 比较即可丢弃过期记录，不必实现堆内修改键值。邻接表配合二叉堆的时间复杂度为

$$
O((|V|+|E|)\log |V|)
$$

非负边权保证最小未确定距离不会在以后被改小。只要存在负权边，这个贪心不变量就可能失效，即使图中没有负环也不能继续使用 Dijkstra。含负权边时可以使用 Bellman-Ford；存在从源点可达的负环时，相关顶点不存在有限最短距离。

Dijkstra 确定顶点 $u$ 时，所有尚未确定顶点的暂定距离都不小于 $dist[u]$ 。任何以后才被发现的替代路径必须先经过某个未确定顶点，非负边权使这条路径不可能再降到 $dist[u]$ 以下。这个不变量正是负权边会破坏的部分。

恢复路径时，在每次成功松弛后令 `previous[v] = u`。优先队列中的旧记录可以丢弃，但前驱数组只对应当前最短距离，不能在未改进距离时覆盖。

### 任意两点最短路

Floyd-Warshall 使用动态规划计算所有点对之间的最短距离。令 $d^{(k)}[i][j]$ 表示只允许编号不超过 $k$ 的顶点作为中间点时，从 $i$ 到 $j$ 的最短距离。最短路径要么不经过顶点 $k$ ，要么由经过 $k$ 的两段路径组成

$$
d^{(k)}[i][j]=\min\left(d^{(k-1)}[i][j],d^{(k-1)}[i][k]+d^{(k-1)}[k][j]\right)
$$

状态可以原地压缩成一个二维矩阵

```cpp
void floydWarshall(std::vector<std::vector<long long>>& distance,
                   long long infinity) {
    int n = distance.size();
    for (int k = 0; k < n; ++k) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (distance[i][k] == infinity ||
                    distance[k][j] == infinity) {
                    continue;
                }
                distance[i][j] = std::min(
                    distance[i][j],
                    distance[i][k] + distance[k][j]
                );
            }
        }
    }
}
```

实现时需要避免无穷大参与加法导致溢出。Floyd-Warshall 的时间复杂度为 $O(|V|^3)$ ，空间复杂度为 $O(|V|^2)$ 。它允许负权边；若最终出现 $distance[i][i]<0$ ，说明存在可从 $i$ 到达并返回的负环。

路径恢复可以额外保存 `next[i][j]`，表示从 $i$ 前往 $j$ 的最短路第一步。当经过 $k$ 得到更短路径时，令 `next[i][j] = next[i][k]`。之后从 $i$ 开始反复跳到 `next[current][j]`，直到到达 $j$ 。

外层循环必须枚举中间点 $k$ 。若把 $i$ 或 $j$ 放到最外层，原地数组中已经更新与尚未更新的状态会混在一起，不再对应“只允许前 $k$ 个中间点”的动态规划阶段。

## 最小生成树

连通无向图的生成树包含全部顶点，并用恰好 $|V|-1$ 条边保持连通。边权总和最小的生成树称为最小生成树（Minimum Spanning Tree，MST）。

MST 与最短路径解决的是不同问题。最短路径要求某些点对之间的路线最短，MST 只要求全图连通时总边权最小，树中两点之间的路径不一定是原图最短路。

Prim 算法从任意起点建立一棵树。每一步选择连接“树内顶点”和“树外顶点”的最小边，把新顶点并入。它与 Dijkstra 的框架相似，但优先级保存的是新顶点到当前树的最小边权，不累加源点距离。

Kruskal 算法把所有边按权值升序处理。若一条边的两个端点位于不同连通分量，就选择这条边并合并两个分量；若端点已经连通，加入它会形成环，因此跳过。并查集可以高效维护这些分量。

![Kruskal 算法跳过会形成环的较重边](assets/07-kruskal-cycle.png)

```cpp
struct WeightedEdge {
    int from;
    int to;
    long long weight;
};

long long kruskal(int vertexCount, std::vector<WeightedEdge> edges) {
    std::sort(edges.begin(), edges.end(), [](const auto& a, const auto& b) {
        return a.weight < b.weight;
    });

    DisjointSet sets(vertexCount);
    long long total = 0;
    int chosen = 0;

    for (const WeightedEdge& edge : edges) {
        if (!sets.unite(edge.from, edge.to)) continue;
        total += edge.weight;
        ++chosen;
    }

    if (chosen != vertexCount - 1) {
        throw std::runtime_error("graph is disconnected");
    }
    return total;
}
```

Kruskal 的主要成本是排序，时间复杂度为 $O(|E|\log |E|)$ 。Prim 使用邻接表和堆时为 $O(|E|\log |V|)$ ；使用邻接矩阵并线性寻找最小边时为 $O(|V|^2)$ ，在稠密图上反而可能更合适。

两种算法都依赖割性质：任意把顶点划分为两个非空集合，跨越这道割的最轻边一定可以出现在某棵最小生成树中。若所有边权互不相同，最小生成树唯一；存在相同边权时，可能有多棵权值相同的最小生成树。

Kruskal 当前选中的边把顶点划分成若干连通分量。下一条连接不同分量的最轻边跨越某道割，按割性质可以安全加入。Prim 则始终只维护“已选顶点集合”与其补集这一道割。

图不连通时不存在覆盖全部顶点的生成树。分别在每个连通分量上运行算法会得到最小生成森林，边数为 $|V|-c$ ，其中 $c$ 是连通分量数。
