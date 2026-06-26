# 課題4（線形回帰の理論誤差）の数学的解説

このファイルでは、課題4の各小問に対する数学的な導出プロセスを記述しています。
数式が正しく表示されるよう、Markdown Preview (`Cmd + Shift + V` on macOS) を起動してご覧ください。

---

## 4.1 最小二乗推定量 $\hat{\bm{\beta}}$ の導出

求めるパラメータ推定量 $\hat{\bm{\beta}}$ は、次の二乗誤差（残差平方和）を最小化する問題の解です。
$$\hat{\bm{\beta}} = \arg\min_{\bm{\beta}} \|\bm{y} - X\bm{\beta}\|^2$$

残差平方和を $S(\bm{\beta})$ と置きます。
$$S(\bm{\beta}) = (\bm{y} - X\bm{\beta})^T (\bm{y} - X\bm{\beta}) = \bm{y}^T \bm{y} - 2 \bm{\beta}^T X^T \bm{y} + \bm{\beta}^T X^T X \bm{\beta}$$

これを $\bm{\beta}$ について微分して $0$ と置きます（正規方程式の導出）。
$$\frac{\partial S}{\partial \bm{\beta}} = -2 X^T \bm{y} + 2 X^T X \bm{\beta} = \bm{0}$$
$$X^T X \bm{\beta} = X^T \bm{y}$$

この方程式の一般解は、ムーア・ペンローズの擬似逆行列 $X^+$ を用いて次のように表されます。
$$\hat{\bm{\beta}} = X^+ \bm{y}$$

### ケースごとの表現：
1. **$n \ge p$ （かつ $\text{rank}(X) = p$：過決定系）のとき**
   $X^T X$ は正則（逆行列が存在する）であるため：
   $$X^+ = (X^T X)^{-1} X^T$$
   $$\hat{\bm{\beta}} = (X^T X)^{-1} X^T \bm{y}$$

2. **$n < p$ （かつ $\text{rank}(X) = n$：劣決定系）のとき**
   解が一意に定まらず無数に存在しますが、擬似逆行列は二乗誤差を最小にする解の中で、パラメータのL2ノルム $\|\hat{\bm{\beta}}\|^2$ を最小にする解（最小ノルム解）を与えます。
   $$X^+ = X^T (X X^T)^{-1}$$
   $$\hat{\bm{\beta}} = X^T (X X^T)^{-1} \bm{y}$$

---

## 4.2 推定量 $\hat{\bm{\beta}}$ の期待値と共分散行列

データの真の関係式 $\bm{y} = X\bm{\beta} + \bm{\epsilon}$ （ここで $E[\bm{\epsilon}] = \bm{0}$、$\text{Cov}[\bm{\epsilon}] = \sigma^2 I_n$）を、推定量 $\hat{\bm{\beta}} = X^+ \bm{y}$ に代入します。
$$\hat{\bm{\beta}} = X^+ (X\bm{\beta} + \bm{\epsilon}) = X^+ X \bm{\beta} + X^+ \bm{\epsilon}$$

### 1. 期待値 $E[\hat{\bm{\beta}}]$
ノイズ $\bm{\epsilon}$ に関する期待値をとります。
$$E[\hat{\bm{\beta}}] = E[X^+ X \bm{\beta} + X^+ \bm{\epsilon}] = X^+ X \bm{\beta} + X^+ E[\bm{\epsilon}] = X^+ X \bm{\beta}$$

- **$n \ge p$ のとき**
  $X^+ X = (X^T X)^{-1} X^T X = I_p$ となるため：
  $$E[\hat{\bm{\beta}}] = \bm{\beta} \quad (\text{不偏推定量})$$
- **$n < p$ のとき**
  $X^+ X = X^T (X X^T)^{-1} X$ となり、$I_p$ とは一致しません。これは $X$ の行空間（次元 $n$）への直交射影行列です。
  $$E[\hat{\bm{\beta}}] = X^T (X X^T)^{-1} X \bm{\beta} \quad (\text{バイアスが生じる})$$

### 2. 共分散行列 $\text{Cov}[\hat{\bm{\beta}}]$
定義より：
$$\text{Cov}[\hat{\bm{\beta}}] = E\left[ (\hat{\bm{\beta}} - E[\hat{\bm{\beta}}]) (\hat{\bm{\beta}} - E[\hat{\bm{\beta}}])^T \right]$$
ここで $\hat{\bm{\beta}} - E[\hat{\bm{\beta}}] = X^+ \bm{\epsilon}$ であるため、
$$\text{Cov}[\hat{\bm{\beta}}] = E\left[ (X^+ \bm{\epsilon}) (X^+ \bm{\epsilon})^T \right] = X^+ E[\bm{\epsilon} \bm{\epsilon}^T] (X^+)^T = \sigma^2 X^+ (X^+)^T$$

- **$n \ge p$ のとき**
  $$X^+ (X^+)^T = (X^T X)^{-1} X^T X (X^T X)^{-1} = (X^T X)^{-1}$$
  よって、
  $$\text{Cov}[\hat{\bm{\beta}}] = \sigma^2 (X^T X)^{-1}$$
- **$n < p$ のとき**
  $$X^+ (X^+)^T = X^T (X X^T)^{-1} (X X^T)^{-1} X = X^T (X X^T)^{-2} X$$
  よって、
  $$\text{Cov}[\hat{\bm{\beta}}] = \sigma^2 X^T (X X^T)^{-2} X$$

---

## 4.3 テストデータの予測誤差（Test MSE）の期待値

テストデータ $\bm{x}_{\text{new}} \sim N(\bm{0}, I_p)$ に対する真の出力を $y_{\text{new}} = \bm{x}_{\text{new}} \bm{\beta} + \epsilon_{\text{new}}$ （ここで $\epsilon_{\text{new}} \sim N(0, \sigma^2)$ は訓練データと独立なテストノイズ）とします。
予測値は $\hat{y}_{\text{new}} = \bm{x}_{\text{new}} \hat{\bm{\beta}}$ です。

テストデータ $\bm{x}_{\text{new}}$ とテストノイズ $\epsilon_{\text{new}}$ に対する二乗誤差の期待値を計算します。
$$\text{Test MSE} = E_{\bm{x}_{\text{new}}, \epsilon_{\text{new}}} \left[ (y_{\text{new}} - \hat{y}_{\text{new}})^2 \right]$$
$$= E_{\bm{x}_{\text{new}}, \epsilon_{\text{new}}} \left[ (\bm{x}_{\text{new}} (\bm{\beta} - \hat{\bm{\beta}}) + \epsilon_{\text{new}})^2 \right]$$

$\bm{x}_{\text{new}}$ と $\epsilon_{\text{new}}$ は独立であり、それぞれ期待値は $0$ なので、クロスタームの期待値は消えます。
$$\text{Test MSE} = E_{\bm{x}_{\text{new}}} \left[ (\bm{x}_{\text{new}} (\bm{\beta} - \hat{\bm{\beta}}))^2 \right] + E_{\epsilon_{\text{new}}}[\epsilon_{\text{new}}^2]$$
$$= (\bm{\beta} - \hat{\bm{\beta}})^T E_{\bm{x}_{\text{new}}}[\bm{x}_{\text{new}}^T \bm{x}_{\text{new}}] (\bm{\beta} - \hat{\bm{\beta}}) + \sigma^2$$

ここで、テストデータが標準正規分布に従うため、その自己相関行列は単位行列 $E_{\bm{x}_{\text{new}}}[\bm{x}_{\text{new}}^T \bm{x}_{\text{new}}] = I_p$ です。したがって：
$$\text{Test MSE} = \|\bm{\beta} - \hat{\bm{\beta}}\|^2 + \sigma^2$$

さらに、この $\text{Test MSE}$ のノイズ $\bm{\epsilon}$ に関する期待値をとります。
$$E_{\bm{\epsilon}}[\text{Test MSE}] = E_{\bm{\epsilon}} \left[ \|\bm{\beta} - \hat{\bm{\beta}}\|^2 \right] + \sigma^2$$

ここで、$\bm{\beta} - \hat{\bm{\beta}} = (I_p - X^+ X)\bm{\beta} - X^+ \bm{\epsilon}$ を代入して展開し、期待値をとると（クロスタームは $E[\bm{\epsilon}] = \bm{0}$ により消失）：
$$E_{\bm{\epsilon}} \left[ \|\bm{\beta} - \hat{\bm{\beta}}\|^2 \right] = \|(I_p - X^+ X)\bm{\beta}\|^2 + E_{\bm{\epsilon}} \left[ \bm{\epsilon}^T (X^+)^T X^+ \bm{\epsilon} \right]$$
$$= \bm{\beta}^T (I_p - X^+ X)^T (I_p - X^+ X) \bm{\beta} + \sigma^2 \text{Tr}\left( X^+ (X^+)^T \right)$$

### ケースごとの期待値：
1. **$n \ge p$ のとき（射影行列 $X^+ X = I_p$）**
   バイアス項は $0$ になり、$\text{Tr}(X^+ (X^+)^T) = \text{Tr}((X^T X)^{-1})$ なので：
   $$E_{\bm{\epsilon}}[\text{Test MSE}] = \sigma^2 + \sigma^2 \text{Tr}\left[ (X^T X)^{-1} \right]$$

2. **$n < p$ のとき（射影行列 $X^+ X = P$ は直交射影行列）**
   $I_p - P$ は直交補空間への直交射影行列なので $(I_p - P)^T (I_p - P) = I_p - P$ です。
   また、トレース項は $\text{Tr}(X^+ (X^+)^T) = \text{Tr}(X^T(XX^T)^{-2}X) = \text{Tr}(XX^T(XX^T)^{-2}) = \text{Tr}((XX^T)^{-1})$ なので：
   $$E_{\bm{\epsilon}}[\text{Test MSE}] = \sigma^2 + \bm{\beta}^T \left( I_p - X^T (X X^T)^{-1} X \right) \bm{\beta} + \sigma^2 \text{Tr}\left[ (X X^T)^{-1} \right]$$
