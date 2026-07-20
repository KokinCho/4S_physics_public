# Variational AutoEncoder (VAE) の数理と解釈

本稿では、Variational AutoEncoder (VAE) におけるエビデンス下界 (ELBO) の導出、多次元正規分布間における KL ダイバージェンスの解析的計算、およびそれぞれの最適化項が潜在空間と学習に与える影響について詳細に解説する。

---

## 3.1. エビデンス下界 (ELBO) の導出と下界性の証明

### 確率的対数尤度の分解

与えられた入力データ $X$ に対し、潜在変数 $Z \in \mathbb{R}^J$ と任意の確率分布 $q(Z|X)$ を導入する。データの対数尤度 $\log p(X|\theta)$ は以下のように展開できる。

まず、対数尤度を $q(Z|X)$ に関する期待値の形で記述する。$\log p(X|\theta)$ は $Z$ に依存しないため、確率分布 $q(Z|X)$ による積分（期待値）をとっても値は不変である。

$$
\log p(X|\theta) = \int \mathrm{d}Z \, q(Z|X) \log p(X|\theta)
$$

ここで、条件付き確率の定義 $p(X|\theta) = \frac{p(X, Z|\theta)}{p(Z|X, \theta)}$ を代入し、さらに分子分母に $q(Z|X)$ を乗じる。

$$
\begin{aligned}
\log p(X|\theta) &= \int \mathrm{d}Z \, q(Z|X) \log \frac{p(X, Z|\theta)}{p(Z|X, \theta)} \\
&= \int \mathrm{d}Z \, q(Z|X) \log \left( \frac{p(X, Z|\theta)}{q(Z|X)} \cdot \frac{q(Z|X)}{p(Z|X, \theta)} \right) \\
&= \int \mathrm{d}Z \, q(Z|X) \left( \log \frac{p(X, Z|\theta)}{q(Z|X)} + \log \frac{q(Z|X)}{p(Z|X, \theta)} \right) \\
&= \int \mathrm{d}Z \, q(Z|X) \log \frac{p(X, Z|\theta)}{q(Z|X)} + \int \mathrm{d}Z \, q(Z|X) \log \frac{q(Z|X)}{p(Z|X, \theta)}
\end{aligned}
$$

ここで、右辺の第1項と第2項をそれぞれ整理する。

第1項は以下のように展開される。

$$
\begin{aligned}
\int \mathrm{d}Z \, q(Z|X) \log \frac{p(X, Z|\theta)}{q(Z|X)} &= \int \mathrm{d}Z \, q(Z|X) \log p(X, Z|\theta) - \int \mathrm{d}Z \, q(Z|X) \log q(Z|X) \\
&= \mathcal{L}(q, \theta)
\end{aligned}
$$

第2項は、分布 $q(Z|X)$ と事後分布 $p(Z|X, \theta)$ の間のカルバック・ライブラー (KL) ダイバージェンスの定義そのものである。

$$
\int \mathrm{d}Z \, q(Z|X) \log \frac{q(Z|X)}{p(Z|X, \theta)} = D_{\mathrm{KL}}(q(Z|X) \parallel p(Z|X, \theta))
$$

したがって、以下が示された。

$$
\log p(X|\theta) = \mathcal{L}(q, \theta) + D_{\mathrm{KL}}(q(Z|X) \parallel p(Z|X, \theta))
$$

### 下界性 (Lower Bound) の説明

KL ダイバージェンスは、任意の2つの確率分布 $q(Z)$ と $p(Z)$ に対して常に非負となる性質を持つ（ギブスの不等式）。

$$
D_{\mathrm{KL}}(q(Z|X) \parallel p(Z|X, \theta)) \geq 0
$$

等号成立は $q(Z|X) = p(Z|X, \theta)$（ほぼいたるところで等しい）のときに限られる。
この非負性を上記の分解式に適用すると、直ちに以下の不等式が得られる。

$$
\log p(X|\theta) \geq \mathcal{L}(q, \theta)
$$

これにより、$\mathcal{L}(q, \theta)$ は対数尤度 $\log p(X|\theta)$ を下から抑える**下界 (Evidence Lower Bound; ELBO)** であることが説明される。

---

## 3.2. 多次元正規分布間の KL ダイバージェンスの解析的導出

### 一般的な多次元正規分布間の KL ダイバージェンス

一般に、$J$ 次元空間における2つの多次元正規分布 $q(Z) = \mathcal{N}(\mu, \Sigma_q)$ と $p(Z) = \mathcal{N}(\mu_p, \Sigma_p)$ について、KL ダイバージェンスは以下のように表される。

$$
D_{\mathrm{KL}}(q \parallel p) = \frac{1}{2} \left[ \log \frac{|\Sigma_p|}{|\Sigma_q|} - J + \operatorname{tr}(\Sigma_p^{-1} \Sigma_q) + (\mu - \mu_p)^T \Sigma_p^{-1} (\mu - \mu_p) \right]
$$

### 本問の設定における計算

VAE において、エンコーダの出力分布 $q_\phi(Z|X)$ と潜在変数の事前分布 $p(Z)$ を以下のように仮定する。

$$
q_\phi(Z|X) = \mathcal{N}(\mu, \operatorname{diag}(\sigma^2_1, \dots, \sigma^2_J)), \quad p(Z) = \mathcal{N}(0, I_J)
$$

すなわち、各パラメータは以下のようになる。
*   $\mu_p = 0$
*   $\Sigma_p = I_J$ （単位行列、したがって $\Sigma_p^{-1} = I_J$, $|\Sigma_p| = 1$）
*   $\Sigma_q = \operatorname{diag}(\sigma^2_1, \dots, \sigma^2_J)$ （対角行列、したがって $|\Sigma_q| = \prod_{j=1}^J \sigma^2_j$）

これらを一般式に代入して各項を計算する。

1.  **対数行列式項**:
    $$
    \log \frac{|\Sigma_p|}{|\Sigma_q|} = \log \frac{1}{\prod_{j=1}^J \sigma^2_j} = -\sum_{j=1}^J \log \sigma^2_j
    $$
2.  **トレース項**:
    $$
    \operatorname{tr}(\Sigma_p^{-1} \Sigma_q) = \operatorname{tr}(I_J \Sigma_q) = \operatorname{tr}(\Sigma_q) = \sum_{j=1}^J \sigma^2_j
    $$
3.  **マハラノビス距離項**:
    $$
    (\mu - 0)^T I_J (\mu - 0) = \mu^T \mu = \sum_{j=1}^J \mu^2_j
    $$

これらをまとめると、求める KL ダイバージェンスは次のように解析的に得られる。

$$
\begin{aligned}
D_{\mathrm{KL}}(q_\phi(Z|X) \parallel p(Z)) &= \frac{1}{2} \left[ -\sum_{j=1}^J \log \sigma^2_j - J + \sum_{j=1}^J \sigma^2_j + \sum_{j=1}^J \mu^2_j \right] \\
&= \frac{1}{2} \sum_{j=1}^J \left( \mu^2_j + \sigma^2_j - \log \sigma^2_j - 1 \right)
\end{aligned}
$$

---

## 3.3. KL 項が潜在変数のパラメータに与える制約

損失関数に含まれる KL 項を最小化することは、上式を構成する各変数 $\mu_j$ および $\sigma^2_j$ に対して以下の数学的制約を課す。

### 平均 $\mu_j$ に対する制約
*   KL 項内の $\mu^2_j$ は非負であり、これが最小化されるのは $\mu_j = 0$ のときである。
*   したがって、エンコーダが各データから抽出する潜在表現の平均ベクトルを、**空間の原点 $\bm{0}$ に近づける**ような引き戻し力が働く。

### 分散 $\sigma^2_j$ に対する制約
*   分散パラメータ $\sigma^2_j > 0$ に対する関数 $f(\sigma^2_j) = \sigma^2_j - \log \sigma^2_j - 1$ を考える。
*   この関数の $\sigma^2_j$ に関する微分は $\frac{\mathrm{d}f}{\mathrm{d}\sigma^2_j} = 1 - \frac{1}{\sigma^2_j}$ となり、極値は $\sigma^2_j = 1$ のときのみである。
*   $\sigma^2_j \to 0$ で $f \to \infty$、$\sigma^2_j \to \infty$ で $f \to \infty$ となるため、$\sigma^2_j = 1$ で最小値 $0$ をとる凸関数である。
*   したがって、損失関数の最小化に伴い、各次元の分散 $\sigma^2_j$ は **$1$ に近づく** ように強く制約される。

### 直感的解釈
KL 項は、エンコーダが出力する条件付き分布 $q_\phi(Z|X)$ を、いかなる入力 $X$ に対しても一律で**標準正規分布 $\mathcal{N}(0, I)$ に一致させる**ように正則化を課す。これにより、潜在表現が過剰に局所化したり、発散したりするのを防ぐ。

---

## 3.4. VAE 損失関数における「再構成項」と「KL 項」の役割

VAE の損失関数は、以下の二つの競合する性質を持つ項から構成される。

$$
\mathrm{Loss}(\phi, \theta) = \underbrace{-\mathbb{E}_{q_\phi(Z|X)} \left[ \log p(X|Z, \theta) \right]}_{\text{再構成項}} + \underbrace{D_{\mathrm{KL}}(q_\phi(Z|X) \parallel p(Z))}_{\text{KL 正則化項}}
$$

### 1. 再構成項 (Reconstruction Term)
*   **数学的役割**:
    エンコーダによって射影された潜在変数 $Z \sim q_\phi(Z|X)$ を受け取り、デコーダ $p(X|Z, \theta)$ が元の入力 $X$ を復元する際の対数尤度の期待値を最大化（損失としては最小化）する。
    *(※ $p(X|Z, \theta)$ にガウス分布を仮定した場合は二乗誤差、ベルヌーイ分布を仮定した場合はクロスエントロピー誤差と等価になる)*
*   **表現上の役割**:
    モデルに入力データの特徴（エッセンス）を潜在空間 $Z$ へと極力情報を漏らさずにエンコードさせ、デコーダ側で鮮明に復元できるように促す。
*   **単独で最適化した際の問題点**:
    再構成項のみを最適化すると、エンコーダは各データ点 $X$ に対して互いに遠く離れた平均 $\mu$ と極めて小さな分散 $\sigma^2 \to 0$ を出力するようになる（決定論的な AE に近づく）。その結果、潜在空間はデータの離散的な「記憶装置」となり、学習データが存在しない隙間の領域においてデコーダが意味のある生成を行えなくなる（過学習・汎化性能の喪失）。

### 2. KL 正則化項 (KL Regularization Term)
*   **数学的役割**:
    エンコーダの出力分布 $q_\phi(Z|X)$ を事前分布である標準正規分布 $p(Z) = \mathcal{N}(0, I)$ に近づける。
*   **表現上の役割**:
    潜在空間の分布に**「連続性（Continuity）」**と**「完備性（Completeness）」**をもたらす。
    *   **連続性**: 潜在空間上で近くにある2つの点は、デコーダによって復元されたときにも類似したコンテンツになる。
    *   **完備性**: 潜在空間上のどの領域から $Z$ をサンプリングしても、デコーダは意味の通る出力を生成できる。
*   **単独で最適化した際の問題点**:
    KL 項のみを最適化すると、エンコーダは入力 $X$ に関わらず一律で $q_\phi(Z|X) = \mathcal{N}(0, I)$ を出力するようになる。このとき、潜在表現 $Z$ は入力データ $X$ の情報を全く保持しなくなるため、デコーダは一様な平均的ノイズ画像しか生成できなくなる。

### 協調動作（トレードオフ）による恩恵
VAE は、これら2項の絶妙なバランスによって成り立っている。
再構成項が潜在空間に「クラスタ（情報の整理）」を作り出そうとする力と、KL 項がそれを「原点中心の標準正規分布へ押し潰し、滑らかに重ね合わせよう」とする力のせめぎ合いにより、**「連続的で隙間がなく、かつデータの特徴をよく反映した生成可能な潜在表現空間」**が自己組織化される。
