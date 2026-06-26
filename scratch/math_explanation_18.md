# 射影行列 $P_X = X^T (X X^T)^{-1} X$ とその性質の解説

レポートの式 (4.533):

$$
\|\bm{\beta} - X^T (X X^T)^{-1} X \bm{\beta}\|^2 = \bm{\beta}^T \left( I_p - X^T (X X^T)^{-1} X \right) \bm{\beta}
$$

の変形において、**射影行列**と呼んでいるのは以下の行列 $P_X$ です。

$$
P_X = X^T (X X^T)^{-1} X \quad (\in \mathbb{R}^{p \times p})
$$

この $P_X$ は、入力行列 $X$ の行空間（Row Space）への**直交射影行列**になります。以下にその定義、対称性、べき等性（2乗しても自分自身に戻る性質）および式変形の詳細を示します。

---

### 1. 射影行列 $P_X$ の性質

行列 $P$ が直交射影行列であるためには、**「対称性」**と**「べき等性」**の2つの条件を満たす必要があります。$P_X$ がこれらを満たすことを確認します。

#### ① 対称性 ($P_X^T = P_X$)
転置の公式 $(ABC)^T = C^T B^T A^T$ を用いて計算します：

$$
\begin{aligned}
P_X^T &= \left( X^T (X X^T)^{-1} X \right)^T \\
&= X^T \left( (X X^T)^{-1} \right)^T (X^T)^T
\end{aligned}
$$

ここで、$(X^T)^T = X$ であり、また積行列 $X X^T$ は対称行列（$(X X^T)^T = X X^T$）なので、その逆行列も対称行列となります。したがって：

$$
\left( (X X^T)^{-1} \right)^T = (X X^T)^{-1}
$$

となり、以下が成り立ちます：

$$
P_X^T = X^T (X X^T)^{-1} X = P_X \quad (\text{対称行列})
$$

#### ② べき等性 ($P_X^2 = P_X$)
自分自身を2回掛け合わせます：

$$
\begin{aligned}
P_X^2 &= \left( X^T (X X^T)^{-1} X \right) \left( X^T (X X^T)^{-1} X \right) \\
&= X^T (X X^T)^{-1} \underbrace{(X X^T) (X X^T)^{-1}}_{I_n} X \\
&= X^T (X X^T)^{-1} X \\
&= P_X
\end{aligned}
$$

これにより、2乗しても値が変わらない性質（べき等性）が示されました。これは「同じ空間へ2回続けて射影しても、1回目の射影と結果は同じである」という射影の性質を数式で表したものです。

---

### 2. 補空間への射影行列 $I_p - P_X$ の性質

$P_X$ が「$X$ の行空間への射影行列」であるとき、**$I_p - P_X$ は「$X$ の零空間（行空間と直交する空間）への射影行列」**になります。
$I_p - P_X$ も同様に、対称性とべき等性を持ちます。

* **対称性**:
  $$ (I_p - P_X)^T = I_p^T - P_X^T = I_p - P_X $$
* **べき等性**:
  $$ (I_p - P_X)^2 = I_p - 2P_X + P_X^2 = I_p - 2P_X + P_X = I_p - P_X $$

---

### 3. 式 (4.533) の具体的な変形ステップ

この性質を使って、レポートの二乗ノルム $\|\bm{\beta} - P_X \bm{\beta}\|^2$ を展開します。

まず、共通の $\bm{\beta}$ でくくります：

$$
\|\bm{\beta} - P_X \bm{\beta}\|^2 = \|(I_p - P_X) \bm{\beta}\|^2
$$

ベクトルの L2 ノルムの二乗は、自分自身の転置との積になります（$\|\bm{v}\|^2 = \bm{v}^T \bm{v}$）：

$$
\begin{aligned}
\|(I_p - P_X) \bm{\beta}\|^2 &= \left( (I_p - P_X) \bm{\beta} \right)^T \left( (I_p - P_X) \bm{\beta} \right) \\
&= \bm{\beta}^T (I_p - P_X)^T (I_p - P_X) \bm{\beta}
\end{aligned}
$$

ここで、**対称性** $(I_p - P_X)^T = I_p - P_X$ を用いると：

$$
= \bm{\beta}^T (I_p - P_X) (I_p - P_X) \bm{\beta}
$$

さらに、**べき等性** $(I_p - P_X)(I_p - P_X) = I_p - P_X$ を用いると、2つの行列が1つに縮約されます：

$$
= \bm{\beta}^T (I_p - P_X) \bm{\beta}
$$

最後に、$P_X = X^T (X X^T)^{-1} X$ を元に戻すと：

$$
= \bm{\beta}^T \left( I_p - X^T (X X^T)^{-1} X \right) \bm{\beta}
$$

となり、式 (4.533) が導かれます。
