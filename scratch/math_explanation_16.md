# バイアス・バリアンス分解の証明

レポートの式 (4.505) におけるバイアス・バリアンス分解：

$$
E_{\bm{\epsilon}} \left[ \|\bm{\beta} - \hat{\bm{\beta}}\|^2 \;\middle|\; X \right] = \|\bm{\beta} - E[\hat{\bm{\beta}}]\|^2 + E_{\bm{\epsilon}} \left[ \|\hat{\bm{\beta}} - E[\hat{\bm{\beta}}]\|^2 \;\middle|\; X \right]
$$

がなぜ成立するのかを詳しく証明します（簡潔にするため、以下の数式では条件付けの $\mid X$ や期待値の添え字 $\bm{\epsilon}$ を一部省略して記述します）。

---

### 1. ベクトルの展開（「足して引く」テクニック）
二乗ノルムの中身に、推定量 $\hat{\bm{\beta}}$ の期待値 $E[\hat{\bm{\beta}}]$ を引いて足します：

$$
\bm{\beta} - \hat{\bm{\beta}} = \left( \bm{\beta} - E[\hat{\bm{\beta}}] \right) - \left( \hat{\bm{\beta}} - E[\hat{\bm{\beta}}] \right)
$$

ここで、記述をわかりやすくするために、以下の2つのベクトルを定義します：

* **バイアスベクトル $\bm{c}$**（定数ベクトル）:
  $$ \bm{c} = \bm{\beta} - E[\hat{\bm{\beta}}] $$
  （真のパラメータ $\bm{\beta}$ も、期待値 $E[\hat{\bm{\beta}}]$ もノイズ $\bm{\epsilon}$ に依存しない確定値なので、$\bm{c}$ は定数です）

* **偏差ベクトル $\bm{d}$**（確率変数ベクトル）:
  $$ \bm{d} = \hat{\bm{\beta}} - E[\hat{\bm{\beta}}] $$
  （$\hat{\bm{\beta}}$ がノイズによって変動するため、$\bm{d}$ は確率変数です。定義から、その期待値は $\bm{0}$ になります：$E[\bm{d}] = E[\hat{\bm{\beta}}] - E[\hat{\bm{\beta}}] = \bm{0}$）

これらを用いると、ノルムの二乗は以下のように展開できます：

$$
\begin{aligned}
\|\bm{\beta} - \hat{\bm{\beta}}\|^2 &= \|\bm{c} - \bm{d}\|^2 \\
&= (\bm{c} - \bm{d})^T (\bm{c} - \bm{d}) \\
&= \bm{c}^T \bm{c} - 2\bm{c}^T \bm{d} + \bm{d}^T \bm{d} \\
&= \|\bm{c}\|^2 - 2\bm{c}^T \bm{d} + \|\bm{d}\|^2
\end{aligned}
$$

---

### 2. 期待値の計算
両辺の期待値を取ります。期待値の線形性 $E[A + B] = E[A] + E[B]$ を利用して各項を計算します。

$$
E\left[ \|\bm{\beta} - \hat{\bm{\beta}}\|^2 \right] = E\left[ \|\bm{c}\|^2 \right] - 2 E\left[ \bm{c}^T \bm{d} \right] + E\left[ \|\bm{d}\|^2 \right]
$$

それぞれの項を評価していきます。

#### 第1項：$E\left[ \|\bm{c}\|^2 \right]$
$\bm{c}$ は定数ベクトルであるため、期待値を取っても変化しません。
$$ E\left[ \|\bm{c}\|^2 \right] = \|\bm{c}\|^2 = \|\bm{\beta} - E[\hat{\bm{\beta}}]\|^2 $$

#### 第2項（交差項）：$E\left[ \bm{c}^T \bm{d} \right]$
$\bm{c}$ は定数ベクトルなので期待値の外に出すことができます。また、先述の通り $E[\bm{d}] = \bm{0}$ です。
$$ E\left[ \bm{c}^T \bm{d} \right] = \bm{c}^T E[\bm{d}] = \bm{c}^T \bm{0} = 0 $$
したがって、交差項（クロス項）は期待値を取ることで完全に消去されます。

#### 第3項：$E\left[ \|\bm{d}\|^2 \right]$
定義通り記述すると以下のようになります。
$$ E\left[ \|\bm{d}\|^2 \right] = E\left[ \|\hat{\bm{\beta}} - E[\hat{\bm{\beta}}]\|^2 \right] $$

---

### 3. 結論
これらを合わせると、以下の式が得られます。

$$
E\left[ \|\bm{\beta} - \hat{\bm{\beta}}\|^2 \right] = \|\bm{\beta} - E[\hat{\bm{\beta}}]\|^2 + E\left[ \|\hat{\bm{\beta}} - E[\hat{\bm{\beta}}]\|^2 \right]
$$

* **第1項**：予測値の期待値が真の値からどれだけズレているかを表す **バイアス（の二乗）** です。
* **第2項**：予測値がその平均値の周りでどれだけ散らばるかを表す **バリアンス** です。

これにより、二乗誤差の期待値が「バイアスの二乗」と「バリアンス」の和にきれいに分解できることが示されました。
