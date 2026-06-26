import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import mean_squared_error

# ==========================================
# 0. プロットのフォントやサイズ設定
# ==========================================
plt.rcParams["font.size"] = 12
plt.rcParams["figure.figsize"] = (10, 6)

# ==========================================
# 1. データの読み込みと理解
# ==========================================
# スクリプトの場所を基準にして相対パスを解決します。
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(script_dir, "../DATASET.csv")
df = pd.read_csv(dataset_path, sep=";")

print("--- [1] データの基本情報 ---")
print(f"データ件数: {df.shape[0]}, 特徴量数: {df.shape[1] - 1} (G3は目的変数)")

# 目的変数 G3 (期末試験の成績) と説明変数 X に分けます。
X = df.drop(columns=["G3"])
y = df["G3"]

# ==========================================
# 2. 前処理 (カテゴリ変数のOne-Hotエンコーディング)
# ==========================================
# 線形回帰モデルは数値データしか入力として受け取れません。
# そのため、文字列で表現されているカテゴリ変数（例: school, sex, Mjob など）を、
# 0か1のみを取るダミー変数（One-Hotベクトル）に変換する必要があります。
#
# ここでは pandas の get_dummies 関数を使用します。
# drop_first=True にすることで、各カテゴリの最初の要素を削除します（ダミー変数の罠を防止）。
# 例: 性別 sex が 「F」か「M」のとき、sex_M という1つのカラムだけに変換され、
#     F のときは 0、M のときは 1 となります。これにより多重共線性を防ぐことができます。
X_encoded = pd.get_dummies(X, drop_first=True)

print("\n--- [2] 前処理後の特徴量 ---")
print(f"One-Hotエンコーディング後の特徴量数: {X_encoded.shape[1]}")
print(f"変換後の特徴量一覧: {list(X_encoded.columns)[:10]} ... など")

# ==========================================
# 3. データの分割 (Train:Test = 8:2)
# ==========================================
# モデルの汎化性能（未知のデータに対する予測性能）を測るため、
# 手元のデータを訓練データ(80%)とテストデータ(20%)に分割します。
# random_state=42 は、実行するたびに分割結果が変わらないようにするための乱数シードです。
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)

# ==========================================
# 4. 標準化 (Standardization)
# ==========================================
# 正則化（L1, L2）付きの線形回帰では、各特徴量のスケール（値の大きさの範囲）が異なると、
# 係数に対するペナルティが不公平にかかってしまいます。
# （例えば、値の範囲が 0〜1 の特徴量と 0〜1000 の特徴量では、学習される重みのサイズが変わり、
#   正則化ペナルティの影響度が異なってしまいます。）
# したがって、すべての特徴量を平均 0、分散 1 に変換する「標準化」を行います。
#
# 【学習上の重要な注意点（Data Leakage の防止）】
# テストデータの情報が訓練時の標準化処理に漏洩（リーク）するのを防ぐため、
# `fit`（平均と標準偏差の計算）は訓練データ（X_train）に対してのみ行い、
# その計算された値を用いて訓練データとテストデータの双方を `transform` します。
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==========================================
# 5. 線形回帰（正則化なし、OLS）の学習
# ==========================================
# まずは基準となる正則化なしの通常線形回帰を実行します。
ols = LinearRegression()
ols.fit(X_train_scaled, y_train)

# 訓練データとテストデータに対する平均二乗誤差 (MSE) を計算します。
y_train_pred_ols = ols.predict(X_train_scaled)
y_test_pred_ols = ols.predict(X_test_scaled)
mse_train_ols = mean_squared_error(y_train, y_train_pred_ols)
mse_test_ols = mean_squared_error(y_test, y_test_pred_ols)

# 重み（係数）の絶対値が 10^-6 より大きいものの数をカウントします。
# 通常の線形回帰では、すべての特徴量に対して0以外の重みが学習されます。
num_active_weights_ols = np.sum(np.abs(ols.coef_) > 1e-6)

print("\n--- [3] 通常の線形回帰（正則化なし）の結果 ---")
print(f"Train MSE: {mse_train_ols:.4f}")
print(f"Test  MSE: {mse_test_ols:.4f}")
print(f"重み (|w| > 10^-6) の数: {num_active_weights_ols} / {X_encoded.shape[1]}")

# ==========================================
# 6. L1正則化 (Lasso) と L2正則化 (Ridge) の学習
# ==========================================
# 正則化の強度を示すハイパーパラメータ alpha を 10^-4 から 10^6 まで動かします。
# 対数スケール（log scale）で滑らかにプロットするために、100点を生成します。
alphas = np.logspace(-4, 6, 200)

# 結果を格納するためのリストを用意します。
lasso_train_mses = []
lasso_test_mses = []
lasso_active_weights = []

ridge_train_mses = []
ridge_test_mses = []
ridge_active_weights = []

for alpha in alphas:
    # --- L1正則化 (Lasso) ---
    # Lassoは L1ノルム（重みの絶対値の和）をペナルティ項として追加します。
    # 特徴: 不要な特徴量の重みが完全に 0 になる（スパース性）。
    # max_iterを十分に大きく設定し、収束を保証します。
    lasso = Lasso(alpha=alpha, max_iter=100000, random_state=42)
    lasso.fit(X_train_scaled, y_train)
    
    y_train_pred_l1 = lasso.predict(X_train_scaled)
    y_test_pred_l1 = lasso.predict(X_test_scaled)
    lasso_train_mses.append(mean_squared_error(y_train, y_train_pred_l1))
    lasso_test_mses.append(mean_squared_error(y_test, y_test_pred_l1))
    lasso_active_weights.append(np.sum(np.abs(lasso.coef_) > 1e-6))
    
    # --- L2正則化 (Ridge) ---
    # Ridgeは L2ノルム（重みの二乗和）をペナルティ項として追加します。
    # 特徴: 重みが全体的に小さく抑えられますが、完全に 0 にはなりにくいです。
    ridge = Ridge(alpha=alpha, random_state=42)
    ridge.fit(X_train_scaled, y_train)
    
    y_train_pred_l2 = ridge.predict(X_train_scaled)
    y_test_pred_l2 = ridge.predict(X_test_scaled)
    ridge_train_mses.append(mean_squared_error(y_train, y_train_pred_l2))
    ridge_test_mses.append(mean_squared_error(y_test, y_test_pred_l2))
    ridge_active_weights.append(np.sum(np.abs(ridge.coef_) > 1e-6))

# ==========================================
# 7. プロットの作成と保存
# ==========================================
# フォルダが存在しない場合は作成します。
plots_dir = os.path.join(script_dir, "plots")
os.makedirs(plots_dir, exist_ok=True)

# グラフ 1: Train/Test MSE の比較 (1.1 用)
plt.figure()
# L1 (Lasso) のプロット
plt.plot(alphas, lasso_train_mses, label="L1 (Lasso) Train MSE", color="red", linestyle="--")
plt.plot(alphas, lasso_test_mses, label="L1 (Lasso) Test MSE", color="red", linestyle="-")

# L2 (Ridge) のプロット
plt.plot(alphas, ridge_train_mses, label="L2 (Ridge) Train MSE", color="blue", linestyle="--")
plt.plot(alphas, ridge_test_mses, label="L2 (Ridge) Test MSE", color="blue", linestyle="-")

# 正則化なし (OLS) のプロット (定数として水平線を表示)
plt.axhline(y=mse_train_ols, label="No Reg (OLS) Train MSE", color="gray", linestyle=":")
plt.axhline(y=mse_test_ols, label="No Reg (OLS) Test MSE", color="black", linestyle=":")

plt.xscale("log")
plt.xlabel("Regularization strength (alpha)")
plt.ylabel("Mean Squared Error (MSE)")
plt.title("Train and Test MSE vs Regularization Strength (alpha)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, which="both", ls="-", color="0.9")
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "mse_comparison.png"), dpi=300)
plt.close()

# グラフ 2: 重みが 10^-6 より大きい変数の数 (1.2 用)
plt.figure()
plt.plot(alphas, lasso_active_weights, label="L1 (Lasso)", color="red")
plt.plot(alphas, ridge_active_weights, label="L2 (Ridge)", color="blue")
plt.axhline(y=num_active_weights_ols, label="No Reg (OLS)", color="black", linestyle=":")

plt.xscale("log")
plt.xlabel("Regularization strength (alpha)")
plt.ylabel("Number of weights (|w| > 10^-6)")
plt.title("Number of Active Weights vs Regularization Strength (alpha)")
plt.legend()
plt.grid(True, which="both", ls="-", color="0.9")
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "weight_comparison.png"), dpi=300)
plt.close()

print("\nグラフの保存に成功しました！")
print(f"1. {os.path.join(plots_dir, 'mse_comparison.png')}")
print(f"2. {os.path.join(plots_dir, 'weight_comparison.png')}")

# ==========================================
# 8. 追加情報（最良のalphaとMSE）
# ==========================================
best_l1_idx = np.argmin(lasso_test_mses)
best_l2_idx = np.argmin(ridge_test_mses)

print("\n--- [4] 詳細な分析結果 ---")
print(f"L1 (Lasso) 最低 Test MSE: {lasso_test_mses[best_l1_idx]:.4f} (at alpha = {alphas[best_l1_idx]:.4e})")
print(f"L2 (Ridge) 最低 Test MSE: {ridge_test_mses[best_l2_idx]:.4f} (at alpha = {alphas[best_l2_idx]:.4e})")

# 最良の Lasso における各変数の係数を調べて、スパース性を確認します。
lasso_best = Lasso(alpha=alphas[best_l1_idx], max_iter=100000, random_state=42)
lasso_best.fit(X_train_scaled, y_train)
active_features = [col for col, coef in zip(X_encoded.columns, lasso_best.coef_) if abs(coef) > 1e-6]
eliminated_features = [col for col, coef in zip(X_encoded.columns, lasso_best.coef_) if abs(coef) <= 1e-6]

print(f"\n最良の L1 (Lasso) モデルにおいて有効な特徴量数: {len(active_features)} / {X_encoded.shape[1]}")
print(f"完全に 0 (消去) になった特徴量数: {len(eliminated_features)}")
print(f"消去された特徴量の一例: {eliminated_features[:10]}")
