import os
import numpy as np
import matplotlib.pyplot as plt

# =====================================================================
# パラメータ設定 (ガイドライン 3.3 に基づき、先頭で定数として管理)
# =====================================================================
# 乱数シードの固定（本問では格子点の決定的な計算を行うが、レポートの一般ルールに従い定義）
RANDOM_STATE = 0
np.random.seed(RANDOM_STATE)

# 2次元混合ガウス分布 p(x) のパラメータ
MU1 = np.array([-2.0, 2.0])  # 第1成分の平均ベクトル
MU2 = np.array([2.0, 2.0])   # 第2成分の平均ベクトル
PI1 = 1.0 / 3.0              # 第1成分の混合比
PI2 = 2.0 / 3.0              # 第2成分の混合比
SIGMA_SQ = 1.0               # 元のガウス分布の分散 (\sigma = 1)

# 可視化の格子点グリッドパラメータ
X1_MIN, X1_MAX = -6.0, 6.0
X2_MIN, X2_MAX = -2.0, 6.0
GRID_RESOLUTION = 100        # 等高線・ヒートマップ用のグリッド解像度
QUIVER_STEP = 5              # ベクトル場 (quiver) プロット用の間引き幅（矢印が密集するのを防ぐため）

# ノイズ強度 \tau のリスト (問題 4.3 で指定された 3 通り)
TAU_LIST = [0.5, 1.5, 3.0]

# プロット出力ディレクトリ
PLOT_DIR = "/Users/chokokin/4S_physics/機械学習概論/後半レポート/problem4/plots"
os.makedirs(PLOT_DIR, exist_ok=True)

# =====================================================================
# 数値計算用ヘルパー関数
# =====================================================================
def gaussian_pdf_2d(x, mu, var):
    """
    2次元等方性ガウス分布の確率密度関数 N(x; mu, var * I) を計算する。
    
    Parameters:
    -----------
    x : numpy.ndarray, shape (..., 2)
        確率密度を評価する座標点
    mu : numpy.ndarray, shape (2,)
        平均ベクトル
    var : float
        共分散行列の対角成分 (分散)
        
    Returns:
    --------
    pdf : numpy.ndarray, shape (...)
        各座標における確率密度値
    """
    # 式: N(x; mu, var * I) = 1 / (2 * pi * var) * exp( - ||x - mu||^2 / (2 * var) )
    diff = x - mu
    dist_sq = np.sum(diff**2, axis=-1)
    pdf = (1.0 / (2.0 * np.pi * var)) * np.exp(-dist_sq / (2.0 * var))
    return pdf

def calc_density_and_score(x, mu1, mu2, pi1, pi2, var):
    """
    混合ガウス分布の確率密度とスコアベクトル場を計算する。
    
    Parameters:
    -----------
    x : numpy.ndarray, shape (H, W, 2)
        格子点座標
    mu1, mu2 : numpy.ndarray, shape (2,)
        各成分の平均
    pi1, pi2 : float
        各成分の混合比
    var : float
        各成分の分散 (\sigma^2 + \tau^2)
        
    Returns:
    --------
    density : numpy.ndarray, shape (H, W)
        各格子点における混合ガウス分布の確率密度
    score : numpy.ndarray, shape (H, W, 2)
        各格子点におけるスコアベクトル \nabla_x \log p(x)
    """
    # 各成分の確率密度の計算
    n1 = gaussian_pdf_2d(x, mu1, var)
    n2 = gaussian_pdf_2d(x, mu2, var)
    
    # 全体の確率密度 p(x) の計算
    density = pi1 * n1 + pi2 * n2
    
    # 事後確率 P(i|x) の計算 (ベイズの定理)
    # P(1|x) = pi1 * N1 / p(x), P(2|x) = pi2 * N2 / p(x)
    # 分母が極めて小さい点でのゼロ除算を防ぐために微小値を加算
    eps_val = 1e-15
    p1 = (pi1 * n1) / (density + eps_val)
    p2 = (pi2 * n2) / (density + eps_val)
    
    # スコアの計算: \nabla_x \log p(x) = - P(1|x) * (x - mu1)/var - P(2|x) * (x - mu2)/var
    # x.shape = (H, W, 2) に対し、p1, p2 の形状を (H, W, 1) に拡張してブロードキャスト演算
    p1_expanded = np.expand_dims(p1, axis=-1)
    p2_expanded = np.expand_dims(p2, axis=-1)
    
    # レポート証明式に基づき、スコアベクトルを計算
    score = - p1_expanded * (x - mu1) / var - p2_expanded * (x - mu2) / var
    
    return density, score

# =====================================================================
# メイン処理
# =====================================================================
def main():
    print("[INFO] シミュレーションを開始します。")
    
    # 格子点グリッドの作成
    x1 = np.linspace(X1_MIN, X1_MAX, GRID_RESOLUTION)
    x2 = np.linspace(X2_MIN, X2_MAX, GRID_RESOLUTION)
    X1, X2 = np.meshgrid(x1, x2)
    # 形状 (GRID_RESOLUTION, GRID_RESOLUTION, 2) の座標配列を作成
    grid_coords = np.stack([X1, X2], axis=-1)
    
    # ガイドライン 3.4 に基づくデータの流れのログ出力
    print(f"[DEBUG] Grid coords shape: {grid_coords.shape}")
    print(f"[DEBUG] X1 grid range: [{X1.min():.1f}, {X1.max():.1f}]")
    print(f"[DEBUG] X2 grid range: [{X2.min():.1f}, {X2.max():.1f}]")
    
    # -----------------------------------------------------------------
    # 問題 4.2: ノイズなし p(x) の等高線とスコアベクトル場のプロット
    # -----------------------------------------------------------------
    print("[INFO] 問題 4.2: 元の分布 p(x) のプロットを作成中...")
    density_orig, score_orig = calc_density_and_score(
        grid_coords, MU1, MU2, PI1, PI2, SIGMA_SQ
    )
    
    plt.figure(figsize=(8, 6))
    # 確率密度の等高線プロット
    contour = plt.contour(X1, X2, density_orig, levels=15, cmap="viridis")
    plt.clabel(contour, inline=True, fontsize=8)
    
    # スコアベクトル場のプロット (間引きを行って矢印が重ならないようにする)
    X1_q = X1[::QUIVER_STEP, ::QUIVER_STEP]
    X2_q = X2[::QUIVER_STEP, ::QUIVER_STEP]
    U_q = score_orig[::QUIVER_STEP, ::QUIVER_STEP, 0]
    V_q = score_orig[::QUIVER_STEP, ::QUIVER_STEP, 1]
    
    # quiver のパラメータ設定 (ガイドライン 3.5 に基づく「呪文」の言語化):
    # - angles='xy', scale_units='xy': ベクトル方向と長さをグラフの座標スケールに一致させる
    # - scale=4.0: 矢印が長くなりすぎて重なるのを防ぐための表示スケーリング因子
    # - color='red', alpha=0.6: 等高線（緑〜青系）と重なっても視認しやすいように赤色半透明に設定
    plt.quiver(X1_q, X2_q, U_q, V_q, angles='xy', scale_units='xy', scale=4.0, color='red', alpha=0.6)
    
    plt.scatter([MU1[0], MU2[0]], [MU1[1], MU2[1]], color='black', marker='x', s=100, label="Component Means")
    plt.title("Probability Density Contour and Score Vector Field of $p(x)$")
    plt.xlabel("$x_1$")
    plt.ylabel("$x_2$")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    
    plot_path_42 = os.path.join(PLOT_DIR, "density_score_field.png")
    plt.savefig(plot_path_42, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[INFO] 図 4.2 を保存しました: {plot_path_42}")

    # -----------------------------------------------------------------
    # 問題 4.3: 各ノイズ強度 \tau における p(y) のプロットと比較
    # -----------------------------------------------------------------
    print("[INFO] 問題 4.3: ノイズ強度ごとのプロットを作成中...")
    
    fig, axes = plt.subplots(len(TAU_LIST), 2, figsize=(14, 15))
    
    for idx, tau in enumerate(TAU_LIST):
        # ガウス分布の再生性に基づく有効分散の更新: var = \sigma^2 + \tau^2 = 1.0 + \tau^2
        effective_var = SIGMA_SQ + tau**2
        
        # 確率密度とスコアの計算
        density_noise, score_noise = calc_density_and_score(
            grid_coords, MU1, MU2, PI1, PI2, effective_var
        )
        # スコアの大きさ (L2 ノルム) の計算
        score_norm = np.linalg.norm(score_noise, axis=-1)
        
        # ------------------ 左側: 確率密度等高線 + スコアベクトル場 ------------------
        ax_left = axes[idx, 0]
        # 等高線
        contour_noise = ax_left.contour(X1, X2, density_noise, levels=15, cmap="viridis")
        ax_left.clabel(contour_noise, inline=True, fontsize=8)
        
        # スコアベクトル場 (間引き)
        U_q_noise = score_noise[::QUIVER_STEP, ::QUIVER_STEP, 0]
        V_q_noise = score_noise[::QUIVER_STEP, ::QUIVER_STEP, 1]
        ax_left.quiver(X1_q, X2_q, U_q_noise, V_q_noise, angles='xy', scale_units='xy', scale=2.5, color='red', alpha=0.6)
        
        ax_left.scatter([MU1[0], MU2[0]], [MU1[1], MU2[1]], color='black', marker='x', s=80)
        ax_left.set_title(rf"$\tau = {tau}$: PDF Contour & Score Field")
        ax_left.set_xlabel("$y_1$")
        ax_left.set_ylabel("$y_2$")
        ax_left.grid(True, linestyle="--", alpha=0.5)
        
        # ------------------ 右側: スコアの大きさ ||\nabla_y \log p(y)|| のヒートマップ ------------------
        ax_right = axes[idx, 1]
        # pcolormesh によるヒートマップ描画 (shading='auto' でセル境界のズレを自動調整)
        im = ax_right.pcolormesh(X1, X2, score_norm, cmap="plasma", shading="auto", vmin=0, vmax=3.0)
        fig.colorbar(im, ax=ax_right, label=r"Score Magnitude $\Vert \nabla_y \log p(y) \Vert$")
        
        # 補助的にスコアの大きさの等高線も重ねる
        contour_norm = ax_right.contour(X1, X2, score_norm, levels=8, colors='white', alpha=0.3)
        ax_right.clabel(contour_norm, inline=True, fontsize=8)
        
        ax_right.scatter([MU1[0], MU2[0]], [MU1[1], MU2[1]], color='white', marker='x', s=80)
        ax_right.set_title(rf"$\tau = {tau}$: Score Magnitude $\Vert \nabla_y \log p(y) \Vert$")
        ax_right.set_xlabel("$y_1$")
        ax_right.set_ylabel("$y_2$")
        ax_right.grid(True, linestyle="--", alpha=0.3)
        
    plt.tight_layout()
    plot_path_43 = os.path.join(PLOT_DIR, "noise_comparison.png")
    plt.savefig(plot_path_43, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[INFO] 図 4.3 を保存しました: {plot_path_43}")
    print("[INFO] シミュレーションとグラフ生成が正常に完了しました。")

if __name__ == "__main__":
    main()
