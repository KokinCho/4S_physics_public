# 問題4の数学的導出 (線形回帰の理論誤差)

このドキュメントでは、機械学習概論レポート前半の問題4（線形回帰の理論誤差）に対する詳細な数学的導出を行います。

---

## 4.1 最小二乗推定量 $\hat{\bm{\beta}}$ の導出

最小二乗推定量は以下の最適化問題の解として定義されます。
$$ \hat{\bm{\beta}} = \arg\min_{\bm{\beta}} L(\bm{\beta}), \quad L(\bm{\beta}) := \|\bm{y} - X\bm{\beta}\|^2 $$

目的関数 $L(\bm{\beta})$ を展開します。
$$ L(\bm{\beta}) = (\bm{y} - X\bm{\beta})^T (\bm{y} - X\bm{\beta}) = \bm{y}^T \bm{y} - 2\bm{\beta}^T X^T \bm{y} + \bm{\beta}^T X^T X \bm{\beta} $$

$\bm{\beta}$ に関する勾配を計算して $\bm{0}$ と置きます。
$$ \nabla_{\bm{\beta}} L(\bm{\beta}) = -2 X^T \bm{y} + 2 X^T X \bm{\beta} = \bm{0} $$

これにより、以下の正規方程式（Normal Equation）が得られます。
$$ X^T X \bm{\beta} = X^T \bm{y} $$

ここで、訓練データ数 $n$ と特徴量数 $p$ の関係、および $X$ のランクに応じて以下の2つのケースに分かれます。

1. **$n \ge p$ の場合 (Overdetermined System):**
   $X$ がフルカラムランク（rank $p$）であると仮定すると（成分が独立な正規分布に従うため、確率1で成り立ちます）、$X^T X$ は正則（可逆）です。
   $$ \hat{\bm{\beta}} = (X^T X)^{-1} X^T \bm{y} $$

2. **$n < p$ の場合 (Underdetermined System):**
   方程式の数よりも未知数の数が多いため、正規方程式には無数の解が存在します。この場合、パラメータのL2ノルム $\|\bm{\beta}\|$ を最小化する一意な最小ノルム解（Minimum-Norm Solution）を採用するのが標準的です。$X$ がフルローランク（rank $n$）であると仮定すると、$X X^T$ は正則になり、最小ノルム解は以下のように与えられます。
   $$ \hat{\bm{\beta}} = X^T (X X^T)^{-1} \bm{y} $$

Moore-Penroseの擬似逆行列（Pseudo-inverse）$X^+$ を用いると、これら2つのケースを統一的に以下のように表すことができます。
$$ \hat{\bm{\beta}} = X^+ \bm{y} $$
ここで、
$$ X^+ = \begin{cases} (X^T X)^{-1} X^T & (n \ge p) \\ X^T (X X^T)^{-1} & (n < p) \end{cases} $$
です。

---

## 4.2 推定量 $\hat{\bm{\beta}}$ の期待値と共分散行列

真のデータ生成プロセスは以下の通りです。
$$ \bm{y} = X\bm{\beta} + \bm{\epsilon}, \quad \bm{\epsilon} \sim N(\bm{0}, \sigma^2 I_n) $$
以下では、訓練データ $X$ を固定した（条件付き）期待値と共分散行列を求めます。

### 期待値 $E[\hat{\bm{\beta}}]$
$$ E[\hat{\bm{\beta}}] = E[X^+ \bm{y}] = E[X^+ (X\bm{\beta} + \bm{\epsilon})] = X^+ X \bm{\beta} + X^+ E[\bm{\epsilon}] $$
$E[\bm{\epsilon}] = \bm{0}$ であるため、
$$ E[\hat{\bm{\beta}}] = X^+ X \bm{\beta} $$

* **$n \ge p$ の場合:**
  $$ X^+ X = (X^T X)^{-1} X^T X = I_p \implies E[\hat{\bm{\beta}}] = \bm{\beta} $$
  （最小二乗推定量は不偏推定量になります。）

* **$n < p$ の場合:**
  $$ X^+ X = X^T (X X^T)^{-1} X := P_X \implies E[\hat{\bm{\beta}}] = P_X \bm{\beta} $$
  ここで $P_X$ は $X$ の行空間（次元 $n$）への直交射影行列（$P_X^2 = P_X, P_X^T = P_X$）です。そのため、特徴量次元がサンプル数より大きい場合、推定量の期待値は真のパラメータ $\bm{\beta}$ を $X$ の行空間に投影したものになり、バイアスが生じます。

### 共分散行列 $\text{Cov}[\hat{\bm{\beta}}]$
$$ \text{Cov}[\hat{\bm{\beta}}] = E[(\hat{\bm{\beta}} - E[\hat{\bm{\beta}}])(\hat{\bm{\beta}} - E[\hat{\bm{\beta}}])^T] $$
$\hat{\bm{\beta}} - E[\hat{\bm{\beta}}] = X^+ \bm{\epsilon}$ であるため、
$$ \text{Cov}[\hat{\bm{\beta}}] = E[(X^+ \bm{\epsilon})(X^+ \bm{\epsilon})^T] = X^+ E[\bm{\epsilon}\bm{\epsilon}^T] (X^+)^T = \sigma^2 X^+ (X^+)^T $$

* **$n \ge p$ の場合:**
  $$ X^+ (X^+)^T = (X^T X)^{-1} X^T X (X^T X)^{-1} = (X^T X)^{-1} \implies \text{Cov}[\hat{\bm{\beta}}] = \sigma^2 (X^T X)^{-1} $$

* **$n < p$ の場合:**
  $$ X^+ (X^+)^T = X^T (X X^T)^{-1} (X X^T)^{-1} X = X^T (X X^T)^{-2} X \implies \text{Cov}[\hat{\bm{\beta}}] = \sigma^2 X^T (X X^T)^{-2} X $$

---

## 4.3 $\text{Test MSE}$ の期待値の導出

テスト入力データ $\bm{x}_{\text{new}} \in \mathbb{R}^{1 \times p} \sim N(\bm{0}, I_p)$ と、対応する独立なテストノイズ $\epsilon_{\text{new}} \sim N(0, \sigma^2)$ に対し、真の出力 $y_{\text{new}}$ と予測値 $\hat{y}_{\text{new}}$ は以下の通りです。
$$ y_{\text{new}} = \bm{x}_{\text{new}} \bm{\beta} + \epsilon_{\text{new}}, \quad \hat{y}_{\text{new}} = \bm{x}_{\text{new}} \hat{\bm{\beta}} $$

予測誤差は以下のようになります。
$$ y_{\text{new}} - \hat{y}_{\text{new}} = \bm{x}_{\text{new}} (\bm{\beta} - \hat{\bm{\beta}}) + \epsilon_{\text{new}} $$

訓練データ $X$ を固定した下での $\text{Test MSE}$ の期待値は、テストデータの生成（$\bm{x}_{\text{new}}, \epsilon_{\text{new}}$）および訓練データのノイズ（$\bm{\epsilon}$）に関する期待値をとることで得られます。
$$ E[\text{Test MSE} \mid X] = E_{\bm{\epsilon}, \bm{x}_{\text{new}}, \epsilon_{\text{new}}} [ (y_{\text{new}} - \hat{y}_{\text{new}})^2 \mid X ] $$

テストノイズ $\epsilon_{\text{new}}$ は平均 0 で他のすべてと独立であるため、
$$ E_{\epsilon_{\text{new}}} [ (y_{\text{new}} - \hat{y}_{\text{new}})^2 ] = E_{\bm{x}_{\text{new}}, \bm{\epsilon}} [ (\bm{x}_{\text{new}} (\bm{\beta} - \hat{\bm{\beta}}))^2 \mid X ] + \sigma^2 $$

ここで、任意の定数ベクトル $\bm{v} \in \mathbb{R}^p$ に対して、$\bm{x}_{\text{new}} \sim N(\bm{0}, I_p)$ の性質から以下が成り立ちます。
$$ E_{\bm{x}_{\text{new}}} [ (\bm{x}_{\text{new}} \bm{v})^2 ] = E_{\bm{x}_{\text{new}}} [ \bm{v}^T \bm{x}_{\text{new}}^T \bm{x}_{\text{new}} \bm{v} ] = \bm{v}^T E[\bm{x}_{\text{new}}^T \bm{x}_{\text{new}}] \bm{v} = \bm{v}^T I_p \bm{v} = \|\bm{v}\|^2 $$

これに $\bm{v} = \bm{\beta} - \hat{\bm{\beta}}$ （訓練データのノイズ $\bm{\epsilon}$ に対して確率的に変動）を適用します。
$$ E_{\bm{x}_{\text{new}}} [ (\bm{x}_{\text{new}} (\bm{\beta} - \hat{\bm{\beta}}))^2 \mid X, \bm{\epsilon} ] = \|\bm{\beta} - \hat{\bm{\beta}}\|^2 $$

したがって、Test MSE は真のパラメータと推定されたパラメータのL2距離（自乗ノルム）とノイズの和になります。
$$ E[\text{Test MSE} \mid X] = E_{\bm{\epsilon}} [ \|\bm{\beta} - \hat{\bm{\beta}}\|^2 \mid X ] + \sigma^2 $$

期待値の性質を用いて、二乗誤差をバイアスとバリアンスに分解します。
$$ \bm{\beta} - \hat{\bm{\beta}} = (\bm{\beta} - E[\hat{\bm{\beta}}]) - (\hat{\bm{\beta}} - E[\hat{\bm{\beta}}]) $$
$$ E_{\bm{\epsilon}} [ \|\bm{\beta} - \hat{\bm{\beta}}\|^2 \mid X ] = \|\bm{\beta} - E[\hat{\bm{\beta}}]\|^2 + E_{\bm{\epsilon}} [ \|\hat{\bm{\beta}} - E[\hat{\bm{\beta}}]\|^2 \mid X ] $$
ここで、第1項はバイアスの二乗、第2項は推定量のバリアンス（共分散行列のトレース）です。
$$ E_{\bm{\epsilon}} [ \|\hat{\bm{\beta}} - E[\hat{\bm{\beta}}]\|^2 \mid X ] = E_{\bm{\epsilon}} [ \text{Tr}((\hat{\bm{\beta}} - E[\hat{\bm{\beta}}])(\hat{\bm{\beta}} - E[\hat{\bm{\beta}}])^T) \mid X ] = \text{Tr}(\text{Cov}[\hat{\bm{\beta}} \mid X]) $$

よって、Test MSE の期待値は一般に以下のように表されます。
$$ E[\text{Test MSE} \mid X] = \sigma^2 + \|\bm{\beta} - E[\hat{\bm{\beta}}]\|^2 + \text{Tr}(\text{Cov}[\hat{\bm{\beta}} \mid X]) $$

#### 1. $n \ge p$ の場合
$E[\hat{\bm{\beta}}] = \bm{\beta}$、$\text{Cov}[\hat{\bm{\beta}}] = \sigma^2 (X^T X)^{-1}$ より：
$$ E[\text{Test MSE} \mid X] = \sigma^2 + \sigma^2 \text{Tr}((X^T X)^{-1}) $$

#### 2. $n < p$ の場合
$E[\hat{\bm{\beta}}] = P_X \bm{\beta}$、$\text{Cov}[\hat{\bm{\beta}}] = \sigma^2 X^T (X X^T)^{-2} X$ より：
* **バイアス項:**
  $$ \|\bm{\beta} - E[\hat{\bm{\beta}}]\|^2 = \|\bm{\beta} - P_X \bm{\beta}\|^2 = \|(I_p - P_X) \bm{\beta}\|^2 = \bm{\beta}^T (I_p - P_X) \bm{\beta} $$
* **バリアンス項:**
  トレースの巡回対称性 $\text{Tr}(AB) = \text{Tr}(BA)$ を用いると：
  $$ \text{Tr}(\text{Cov}[\hat{\bm{\beta}} \mid X]) = \sigma^2 \text{Tr}(X^T (X X^T)^{-2} X) = \sigma^2 \text{Tr}((X X^T)^{-2} X X^T) = \sigma^2 \text{Tr}((X X^T)^{-1}) $$
したがって：
$$ E[\text{Test MSE} \mid X] = \sigma^2 + \bm{\beta}^T (I_p - X^T (X X^T)^{-1} X) \bm{\beta} + \sigma^2 \text{Tr}((X X^T)^{-1}) $$

---

## 4.5 理論曲線の導出 (ランダム行列理論)

無限次元極限 $n, p \to \infty$（$\gamma = p/n$ 固定）において、訓練データ $X$ 自体についての期待値をとることで、理論的な極限曲線を導きます。

### 1. $\gamma < 1$ ($n \ge p$) の場合
式は以下の通りです。
$$ E[\text{Test MSE}] = \sigma^2 + \sigma^2 E_X [ \text{Tr}((X^T X)^{-1}) ] $$
ランダム行列理論（問題文のヒント）より、$\text{Tr}[(X^T X)^{-1}] \sim \frac{\gamma}{1-\gamma}$ です。したがって：
$$ E[\text{Test MSE}] \sim \sigma^2 + \sigma^2 \frac{\gamma}{1-\gamma} = \frac{\sigma^2}{1-\gamma} $$
$\gamma \to 1^-$ において、分母が 0 に近づくため、Test MSE は無限大に発散します。

### 2. $\gamma > 1$ ($n < p$) の場合
式は以下の通りです。
$$ E[\text{Test MSE}] = \sigma^2 + E_X [ \bm{\beta}^T (I_p - P_X) \bm{\beta} ] + \sigma^2 E_X [ \text{Tr}((X X^T)^{-1}) ] $$

各項について極限を評価します。

* **バイアス項 $E_X [ \bm{\beta}^T (I_p - P_X) \bm{\beta} ]$:**
  $P_X$ は独立同分布な正規乱数からなる行列 $X$ の行ベクトルが張る $n$ 次元部分空間への射影行列です。$X$ の回転不変性から、この部分空間は $\mathbb{R}^p$ 内で等方的に（ランダムに）分布します。
  したがって、真のパラメータベクトル $\bm{\beta}$（固定または $X$ と独立）が、このランダムな部分空間の直交補空間（次元 $p-n$）へ投影されたときの自乗ノルムの期待値は、全次元に対する直交補空間の次元の比に比例します。
  $$ E_X [ \|(I_p - P_X) \bm{\beta}\|^2 ] = \|\bm{\beta}\|^2 \frac{p-n}{p} = \|\bm{\beta}\|^2 \left( 1 - \frac{1}{\gamma} \right) $$

* **バリアンス項 $\sigma^2 E_X [ \text{Tr}((X X^T)^{-1}) ]$:**
  ランダム行列理論のヒントより、$\text{Tr}[(X X^T)^{-1}] \sim \frac{1}{\gamma-1}$ です。したがって：
  $$ \sigma^2 E_X [ \text{Tr}((X X^T)^{-1}) ] \sim \frac{\sigma^2}{\gamma - 1} $$

これらを足し合わせると、$\gamma > 1$ における期待 Test MSE の理論曲線が得られます。
$$ E[\text{Test MSE}] \sim \sigma^2 + \|\bm{\beta}\|^2 \left( 1 - \frac{1}{\gamma} \right) + \frac{\sigma^2}{\gamma - 1} $$

### まとめ
理論曲線は、ノイズ分散 $\sigma^2 = 1.0$、およびパラメータノルム $\|\bm{\beta}\|^2 = 2.0$ のとき、次のようになります。

$$
E[\text{Test MSE}] \sim \begin{cases}
\frac{1}{1-\gamma} & (\gamma < 1) \\
1 + 2\left(1 - \frac{1}{\gamma}\right) + \frac{1}{\gamma - 1} & (\gamma > 1)
\end{cases}
$$

これは $\gamma = 1$ を境界としてピーク（発散）を持つ、典型的な **二重降下現象（Double Descent）** を表す理論曲線です。
* $\gamma < 1$ ではモデルのパラメータ数 $p$ が増えるにつれて過学習により誤差が上昇します。
* $\gamma > 1$ になると、最小ノルム解によって過パラメータ領域でパラメトリックな表現力が向上し、バリアンス（第3項）が減少し、同時にバイアス（第2項）が下がるため、ふたたびテスト誤差が減少します。
