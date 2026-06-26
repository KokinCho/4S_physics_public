import os
import numpy as np
import matplotlib.pyplot as plt

# プロット設定
plt.rcParams["font.size"] = 12
plt.rcParams["figure.figsize"] = (10, 6)

# ディレクトリ作成
script_dir = "/Users/chokokin/4S_physics/機械学習概論/problem4"
plots_dir = os.path.join(script_dir, "plots")
os.makedirs(plots_dir, exist_ok=True)

# パラメータ設定
n = 100
p_list = np.arange(10, 405, 5)  # 10 から 400 まで 5 刻み
N_TRIALS = 500
sigma = 1.0  # ノイズの標準偏差 (sigma^2 = 1.0)
beta_norm_sq = 2.0  # ||beta||^2 = 2.0 (||beta|| = sqrt(2))

mean_test_mses = []

print("--- 線形回帰のシミュレーションを開始 ---")

for p in p_list:
    # beta の生成と規格化 (同じ p では共通)
    # 乱数シードを固定して再現性を確保
    np.random.seed(p)
    beta = np.random.normal(0, 1, (p, 1))
    beta = beta / np.linalg.norm(beta) * np.sqrt(beta_norm_sq)
    
    trial_mses = []
    
    for trial in range(N_TRIALS):
        # 試行ごとのシード
        np.random.seed(p * 1000 + trial)
        
        # 入力データ X_train (n x p)
        X_train = np.random.normal(0, 1, (n, p))
        
        # ノイズ epsilon (n x 1)
        epsilon = np.random.normal(0, sigma, (n, 1))
        
        # 出力 y_train (n x 1)
        y_train = X_train @ beta + epsilon
        
        # 最小二乗推定量 beta_hat の計算 (擬似逆行列を用いる)
        # pinv は Moore-Penrose 擬似逆行列を計算する
        beta_hat = np.linalg.pinv(X_train) @ y_train
        
        # テストデータ x_new (100 x p) とテストノイズ epsilon_new (100 x 1)
        X_test = np.random.normal(0, 1, (100, p))
        epsilon_test = np.random.normal(0, sigma, (100, 1))
        
        # テストデータの真値 y_test (100 x 1)
        y_test = X_test @ beta + epsilon_test
        
        # 予測値 y_pred (100 x 1)
        y_pred = X_test @ beta_hat
        
        # Test MSE
        mse = np.mean((y_test - y_pred) ** 2)
        trial_mses.append(mse)
        
    mean_test_mses.append(np.mean(trial_mses))
    if p % 50 == 0:
        print(f"p = {p:3d} (gamma = {p/n:.2f}) | 平均 Test MSE: {np.mean(trial_mses):.4f}")

gamma_list = p_list / n

# 4.5 理論曲線の計算
theory_mses = []
for gamma in gamma_list:
    if gamma < 1.0:
        # gamma < 1 の理論値: sigma^2 / (1 - gamma)
        val = (sigma ** 2) / (1 - gamma)
    elif gamma > 1.0:
        # gamma > 1 の理論値: sigma^2 + ||beta||^2 * (1 - 1/gamma) + sigma^2 / (gamma - 1)
        val = (sigma ** 2) + beta_norm_sq * (1.0 - 1.0 / gamma) + (sigma ** 2) / (gamma - 1.0)
    else:
        val = np.nan  # gamma = 1 では発散するため除外
    theory_mses.append(val)

# グラフ描画
plt.figure()
plt.scatter(gamma_list, mean_test_mses, color="red", alpha=0.6, label="Simulation (n=100)")
plt.plot(gamma_list, theory_mses, color="blue", linewidth=2, label="Theory ($n, p \\to \\infty$)")
plt.axvline(x=1.0, color="gray", linestyle="--", alpha=0.7, label="$\gamma = 1.0$ (Interpolation Threshold)")

# 縦軸のスケールを制限（発散付近で見やすくするため）
plt.ylim(0, 30)
plt.xlabel("$\gamma = p / n$")
plt.ylabel("Test MSE")
plt.title("Double Descent in Linear Regression (Simulation vs Theory)")
plt.legend()
plt.grid(True, which="both", ls="--", color="0.9")
plt.tight_layout()

plot_path = os.path.join(plots_dir, "double_descent.png")
plt.savefig(plot_path, dpi=300)
plt.close()

print(f"グラフを保存しました: {plot_path}")
