# 課題3（Kullback-Leibler情報量）の数学的解説

このファイルでは、課題3の各小問に対する数学的な定義、導出、および統計力学的解釈を整理しています。
数式が正しく表示されるよう、Markdown Preview (`Cmd + Shift + V` on macOS) を起動してご覧ください。

---

## 3.1 情報エントロピーと KL ダイバージェンスの定義

離散確率分布を想定し、確率分布 $p(x)$ および $q(x)$ に対する各定義を記述します。

### 1. 情報エントロピー（Shannon Entropy） $S(p)$
確率分布 $p(x)$ が持つ情報の不確実性を表す尺度です。
$$S(p) = - \sum_{x} p(x) \log p(x)$$
（連続分布の場合は $S(p) = - \int p(x) \log p(x) dx$）

### 2. カルバック・ライブラー情報量（Kullback-Leibler Divergence） $\text{KL}(p \parallel q)$
2つの確率分布 $p(x)$ と $q(x)$ の間の「差異」を測定する非負の尺度（情報損失量）です。
$$\text{KL}(p \parallel q) = \sum_{x} p(x) \log \frac{p(x)}{q(x)}$$
（連続分布の場合は $\text{KL}(p \parallel q) = \int p(x) \log \frac{p(x)}{q(x)} dx$）
※ $\text{KL}(p \parallel q) \ge 0$ であり、$p(x) = q(x)$ のときに限り等号が成立しますが、対称性 $\text{KL}(p \parallel q) \neq \text{KL}(q \parallel p)$ や三角不等式を満たさないため、数学的な意味での「距離（metric）」ではありません。

---

## 3.2 ボルツマン分布の代入と自由エネルギーの差分への整理

KLダイバージェンス $\text{KL}(q \parallel p)$ において、基準となる分布 $p(x)$ にボルツマン分布：
$$p(x) = \frac{\exp(-\beta E(x))}{Z} \quad \left(Z = \sum_{x} \exp(-\beta E(x))\right)$$
を代入します。ここで、$\beta = \frac{1}{k_B T}$ は逆温度、$E(x)$ は状態 $x$ のエネルギー、$Z$ は分配関数です。

### 導出プロセス：
$$\text{KL}(q \parallel p) = \sum_{x} q(x) \log \frac{q(x)}{p(x)}$$
$$\text{KL}(q \parallel p) = \sum_{x} q(x) \log q(x) - \sum_{x} q(x) \log p(x)$$

第1項は情報エントロピーの定義より $-S(q)$ です。
$$- S(q) = \sum_{x} q(x) \log q(x)$$

第2項にボルツマン分布 $p(x)$ の対数を代入します。
$$\log p(x) = -\beta E(x) - \log Z$$
これより、
$$- \sum_{x} q(x) \log p(x) = - \sum_{x} q(x) \left( -\beta E(x) - \log Z \right)$$
$$= \beta \sum_{x} q(x) E(x) + \log Z \sum_{x} q(x)$$

ここで、確率の規格化条件 $\sum_{x} q(x) = 1$、および分布 $q(x)$ の下でのエネルギーの期待値（平均エネルギー）を $\langle E \rangle_q = \sum_{x} q(x) E(x)$ と書くと、
$$- \sum_{x} q(x) \log p(x) = \beta \langle E \rangle_q + \log Z$$

これらをまとめると、次の関係式が得られます。
$$\text{KL}(q \parallel p) = \beta \langle E \rangle_q - S(q) + \log Z$$

両辺を $\beta$ で割ります（$k_B T$ を掛けることに相当）。
$$\frac{1}{\beta} \text{KL}(q \parallel p) = \langle E \rangle_q - \frac{1}{\beta} S(q) + \frac{1}{\beta} \log Z$$

### 自由エネルギーの導入：
1. 熱平衡状態 $p$ における（ヘルムホルツ）自由エネルギー $F(p)$：
   $$F(p) = - \frac{1}{\beta} \log Z$$
2. 任意の非平衡分布 $q$ に対する変分自由エネルギー（Gibbs 自由エネルギー） $F(q)$：
   $$F(q) = \langle E \rangle_q - \frac{1}{\beta} S(q)$$

これらを用いると、上の式は次のように極めてシンプルな「自由エネルギーの差分」の形に整理されます。
$$\frac{1}{\beta} \text{KL}(q \parallel p) = F(q) - F(p)$$

---

## 3.3 KL ダイバージェンスの非負性の証明

$\text{KL}(p \parallel q) \ge 0$ であることを、対数関数の凸性（あるいはイェンセンの不等式）を用いて示します。

### イェンセンの不等式を用いた証明：
任意の確率分布 $p(x), q(x)$ について、定義より：
$$-\text{KL}(p \parallel q) = -\sum_{x} p(x) \log \frac{p(x)}{q(x)} = \sum_{x} p(x) \log \frac{q(x)}{p(x)}$$

対数関数 $f(t) = \log(t)$ は上に凸（concave）な関数です。
確率の重み $p(x)$ （$\sum_{x} p(x) = 1$, $p(x) \ge 0$）に対するイェンセンの不等式：
$$E[f(T)] \le f(E[T])$$
を適用すると、次が成り立ちます。
$$\sum_{x} p(x) \log \left( \frac{q(x)}{p(x)} \right) \le \log \left( \sum_{x} p(x) \frac{q(x)}{p(x)} \right)$$

右辺の対数の中身を簡略化します。
$$\sum_{x} p(x) \frac{q(x)}{p(x)} = \sum_{x} q(x) = 1$$
（※ $q(x)$ も規格化された確率分布であるため、和は 1 になります）

したがって、
$$-\text{KL}(p \parallel q) \le \log(1) = 0$$
両辺に $-1$ を掛けることで、非負性が示されます。
$$\text{KL}(p \parallel q) \ge 0$$

### 等号成立条件：
$\log(t)$ は厳密に凸（strictly concave）な関数であるため、等号が成立するのは確率変数 $\frac{q(x)}{p(x)}$ が確率 1 で定数となるときのみです。
すなわち、すべての $x$ に対して $q(x) = c p(x)$ となるときであり、両辺の和が 1 であることから定数 $c=1$ となり、
$$p(x) = q(x) \quad (\forall x)$$
のときに限り等号 $\text{KL}(p \parallel q) = 0$ が成立します。

---

## 3.4 統計力学的な解釈

3.2 と 3.3 の結果を組み合わせることで、統計力学的な重要な物理的意味が導かれます。

$$\text{KL}(q \parallel p) \ge 0 \quad \text{かつ} \quad \frac{1}{\beta} \text{KL}(q \parallel p) = F(q) - F(p)$$
これより、
$$F(q) \ge F(p)$$
が任意の状態分布 $q$ に対して成り立ち、等号は $q = p$（熱平衡分布）のときにのみ成立します。

### 解釈：
1. **自由エネルギー最小化の原理（変分原理）**
   温度 $T$ の熱浴と接している熱力学系が取り得るあらゆる確率状態分布 $q$ のうち、ヘルムホルツ自由エネルギー $F(q)$ を最小にする唯一の分布は、ボルツマン分布 $p$（熱平衡状態）であることを意味します。
2. **第二法則と非平衡状態の損失（自由エネルギーの散逸）**
   系が非平衡状態 $q$ にあるとき、平衡状態に比べて余分な自由エネルギー $F(q) - F(p) \ge 0$ を保持しています。この差分は「非平衡状態から平衡状態に遷移する過程で、最大で系から取り出し可能な自由エネルギー（または熱力学的な無駄・散逸）」に相当し、KLダイバージェンスが情報論的・統計力学的に「非平衡度（平衡からのズレ）」を直接測定する物理量であることを示しています。
