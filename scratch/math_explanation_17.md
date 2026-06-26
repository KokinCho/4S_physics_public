# 最小ノルム解（$n < p$ の場合）の導出と幾何学的解釈

パラメータ数 $p$ がデータ数 $n$ より大きい超決定不足系（Underdetermined System, $n < p$）において、誤差をゼロにする解（$X\bm{\beta} = \bm{y}$ を満たす解）が無数に存在する中で、なぜ L2 ノルム $\|\bm{\beta}\|$ を最小化する解が一意に以下の形になるのか：

$$
\hat{\bm{\beta}} = X^T (X X^T)^{-1} \bm{y}
$$

を、「ラグランジュの未定乗数法による導出」と「線形代数（幾何学）によるアプローチ」の2つの方法で詳しく解説します。

---

### アプローチ1：ラグランジュの未定乗数法による導出

この問題は、以下の制約付き最適化問題として定式化されます：

* **目的関数（最小化したいもの）**:
  $$ f(\bm{\beta}) = \frac{1}{2} \|\bm{\beta}\|^2 = \frac{1}{2} \bm{\beta}^T \bm{\beta} $$
* **制約条件（満たさなければならない方程式）**:
  $$ X\bm{\beta} = \bm{y} $$
  （※ $X$ がフルローランク $\text{rank}(X) = n$ であるため、連立方程式 $X\bm{\beta} = \bm{y}$ を完全に満たす解が必ず存在します）

#### 1. ラグランジュ関数の定義
未定乗数ベクトル $\bm{\lambda} = (\lambda_1, \dots, \lambda_n)^T \in \mathbb{R}^{n \times 1}$ を導入し、ラグランジュ関数 $L(\bm{\beta}, \bm{\lambda})$ を以下のように定義します：

$$
L(\bm{\beta}, \bm{\lambda}) = \frac{1}{2} \bm{\beta}^T \bm{\beta} - \bm{\lambda}^T (X\bm{\beta} - \bm{y})
$$

#### 2. 各変数での微分と極値条件
この関数を $\bm{\beta}$ について微分し、$\bm{0}$ と置きます：

$$
\frac{\partial L}{\partial \bm{\beta}} = \bm{\beta} - X^T \bm{\lambda} = \bm{0} \implies \bm{\beta} = X^T \bm{\lambda}
$$

この式は、**「最小ノルム解 $\bm{\beta}$ は、入力行列 $X$ の行ベクトルの線形結合（すなわち $X$ の行空間 $\text{Row}(X)$）に含まれていなければならない」**という重要な性質を示しています。

#### 3. 制約条件への代入と $\bm{\lambda}$ の決定
得られた $\bm{\beta} = X^T \bm{\lambda}$ を、制約条件 $X\bm{\beta} = \bm{y}$ に代入します：

$$
X (X^T \bm{\lambda}) = \bm{y} \implies (X X^T) \bm{\lambda} = \bm{y}
$$

ここで、$X \in \mathbb{R}^{n \times p}$ は $n < p$ であり、フルローランク（$\text{rank}(X) = n$）と仮定しています。したがって、積行列 $X X^T \in \mathbb{R}^{n \times n}$ もフルランクであり、正則（可逆）行列です。
よって、両辺に左から逆行列 $(X X^T)^{-1}$ を掛けることで、$\bm{\lambda}$ が一意に定まります：

$$
\bm{\lambda} = (X X^T)^{-1} \bm{y}
$$

#### 4. 最小ノルム解 $\hat{\bm{\beta}}$ の決定
求めた $\bm{\lambda}$ を $\bm{\beta} = X^T \bm{\lambda}$ に戻すと、最小ノルム推定量が得られます：

$$
\hat{\bm{\beta}} = X^T (X X^T)^{-1} \bm{y}
$$

---

### アプローチ2：幾何学的アプローチ（直交分解）

線形代数の射影と零空間（カーネル）の概念を用いると、この式の直感的な意味が非常によく分かります。

任意の解 $\bm{\beta} \in \mathbb{R}^p$ は、**「$X$ の行空間（直交補空間を含む）」**の成分 $\bm{\beta}_R$ と、**「$X$ の零空間（カーネル）」**の成分 $\bm{\beta}_N$ に直交分解（直和分解）できます：

$$
\bm{\beta} = \bm{\beta}_R + \bm{\beta}_N
$$

ここで、
* $\bm{\beta}_R \in \text{Row}(X)$
* $\bm{\beta}_N \in \text{Null}(X)$（すなわち $X\bm{\beta}_N = \bm{0}$）
* $\bm{\beta}_R \perp \bm{\beta}_N$（互いに直交する）

#### 1. 制約条件の分解
この分解を制約条件 $X\bm{\beta} = \bm{y}$ に適用します：

$$
X\bm{\beta} = X(\bm{\beta}_R + \bm{\beta}_N) = X\bm{\beta}_R + X\bm{\beta}_N = X\bm{\beta}_R + \bm{0} = X\bm{\beta}_R = \bm{y}
$$

これより、**「制約条件 $X\bm{\beta} = \bm{y}$ は、行空間の成分 $\bm{\beta}_R$ のみによって決定され、零空間の成分 $\bm{\beta}_N$ には一切依存しない」**ことが分かります。

#### 2. L2ノルムの最小化
このとき、パラメータの L2 ノルムの二乗は、三平方の定理（直交性）より次のように表されます：

$$
\|\bm{\beta}\|^2 = \|\bm{\beta}_R + \bm{\beta}_N\|^2 = \|\bm{\beta}_R\|^2 + \|\bm{\beta}_N\|^2
$$

制約条件をクリアするために $\|\bm{\beta}_R\|^2$ は変更できません（$X\bm{\beta}_R = \bm{y}$ という固定の拘束があるため）。
したがって、全体のノルム $\|\bm{\beta}\|^2$ を最小化するためには、**もう一方の自由度である零空間の成分を $\bm{\beta}_N = \bm{0}$ と選ぶほかありません**。

よって、最小ノルム解は **「零空間成分を一切持たず、行空間（$\text{Row}(X)$）に完全に含まれる解」**、すなわち：

$$
\hat{\bm{\beta}} = \bm{\beta}_R
$$

となります。$\hat{\bm{\beta}}$ が行空間に含まれるということは、あるベクトル $\bm{\lambda} \in \mathbb{R}^n$ を用いて $\hat{\bm{\beta}} = X^T \bm{\lambda}$ と書けることを意味し、アプローチ1と同様に $X(X^T\bm{\lambda}) = \bm{y} \implies \hat{\bm{\beta}} = X^T(XX^T)^{-1}\bm{y}$ が導かれます。
