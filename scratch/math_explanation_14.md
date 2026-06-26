# ノイズ共分散 $E[\bm{\epsilon}\bm{\epsilon}^T] = \sigma^2 I_n$ の解説

線形回帰モデルにおいて、各観測データに加わるノイズベクトル $\bm{\epsilon} \in \mathbb{R}^{n \times 1}$ は以下のように定義されています。

$$
\bm{\epsilon} = \begin{pmatrix}
\epsilon_1 \\
\epsilon_2 \\
\vdots \\
\epsilon_n
\end{pmatrix}
$$

ここで、モデルの仮定から、ノイズの各成分 $\epsilon_i$ はそれぞれ独立に平均 $0$、分散 $\sigma^2$ の正規分布に従う（i.i.d.）とされています：

$$
\epsilon_i \sim N(0, \sigma^2)
$$

### 1. 各成分の期待値と分散・共分散
この仮定から、以下の統計的性質が得られます。

* **平均（期待値）が 0**:
  $$ E[\epsilon_i] = 0 \quad (\forall i) $$
* **分散が $\sigma^2$**:
  $$ V[\epsilon_i] = E[\epsilon_i^2] - (E[\epsilon_i])^2 = E[\epsilon_i^2] = \sigma^2 \quad (\forall i) $$
* **互いに独立（無相関）**:
  異なる観測に対するノイズ $\epsilon_i$ と $\epsilon_j$ ($i \neq j$) は独立であるため、その共分散は 0 になります。
  $$ E[\epsilon_i \epsilon_j] = E[\epsilon_i] E[\epsilon_j] = 0 \quad (i \neq j) $$

---

### 2. ベクトルの外積と期待値 $E[\bm{\epsilon}\bm{\epsilon}^T]$
$\bm{\epsilon}\bm{\epsilon}^T$ は列ベクトルと行ベクトルの外積（テンソル積）であり、以下のような $n \times n$ の正方行列になります。

$$
\bm{\epsilon}\bm{\epsilon}^T = \begin{pmatrix}
\epsilon_1 \\
\epsilon_2 \\
\vdots \\
\epsilon_n
\end{pmatrix}
\begin{pmatrix}
\epsilon_1 & \epsilon_2 & \dots & \epsilon_n
\end{pmatrix}
= \begin{pmatrix}
\epsilon_1^2 & \epsilon_1 \epsilon_2 & \dots & \epsilon_1 \epsilon_n \\
\epsilon_2 \epsilon_1 & \epsilon_2^2 & \dots & \epsilon_2 \epsilon_n \\
\vdots & \vdots & \ddots & \vdots \\
\epsilon_n \epsilon_1 & \epsilon_n \epsilon_2 & \dots & \epsilon_n^2
\end{pmatrix}
$$

行列の期待値は各成分の期待値を取ることに等しいため、以下のようになります。

$$
E[\bm{\epsilon}\bm{\epsilon}^T] = \begin{pmatrix}
E[\epsilon_1^2] & E[\epsilon_1 \epsilon_2] & \dots & E[\epsilon_1 \epsilon_n] \\
E[\epsilon_2 \epsilon_1] & E[\epsilon_2^2] & \dots & E[\epsilon_2 \epsilon_n] \\
\vdots & \vdots & \ddots & \vdots \\
E[\epsilon_n \epsilon_1] & E[\epsilon_n \epsilon_2] & \dots & E[\epsilon_n^2]
\end{pmatrix}
$$

ここで、先ほどの統計的性質（対角成分は $E[\epsilon_i^2] = \sigma^2$、非対角成分は $E[\epsilon_i \epsilon_j] = 0$）を代入すると：

$$
E[\bm{\epsilon}\bm{\epsilon}^T] = \begin{pmatrix}
\sigma^2 & 0 & \dots & 0 \\
0 & \sigma^2 & \dots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \dots & \sigma^2
\end{pmatrix}
= \sigma^2 \begin{pmatrix}
1 & 0 & \dots & 0 \\
0 & 1 & \dots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \dots & 1
\end{pmatrix}
= \sigma^2 I_n
$$

ここで、$I_n$ は $n \times n$ の単位行列（Identity Matrix）です。

---

### 3. 共分散行列 $\text{Cov}[\hat{\bm{\beta}}]$ への代入
推定量 $\hat{\bm{\beta}}$ の共分散行列の計算式：

$$
\text{Cov}[\hat{\bm{\beta}}] = X^+ E[\bm{\epsilon}\bm{\epsilon}^T] (X^+)^T
$$

に $E[\bm{\epsilon}\bm{\epsilon}^T] = \sigma^2 I_n$ を代入すると、以下のようになります。

$$
\text{Cov}[\hat{\bm{\beta}}] = X^+ (\sigma^2 I_n) (X^+)^T
$$

$\sigma^2$ はスカラー値であるため、行列積の前に出すことができます。また、単位行列 $I_n$ を掛けても行列は変化しません ($X^+ I_n = X^+$)。

$$
\text{Cov}[\hat{\bm{\beta}}] = \sigma^2 X^+ I_n (X^+)^T = \sigma^2 X^+ (X^+)^T
$$

これにより、レポートの式 (4.56):

$$
\text{Cov}[\hat{\bm{\beta}}] = \sigma^2 X^+ (X^+)^T
$$

が導かれます。
