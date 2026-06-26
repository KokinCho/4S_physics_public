import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import BaggingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error

# ==========================================
# 0. プロットの設定
# ==========================================
plt.rcParams["font.size"] = 12
plt.rcParams["figure.figsize"] = (10, 6)

script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(script_dir, "../DATASET.csv")
plots_dir = os.path.join(script_dir, "plots")
os.makedirs(plots_dir, exist_ok=True)

# データの読み込み
df = pd.read_csv(dataset_path, sep=";")
X = df.drop(columns=["G3"])
y = df["G3"]

# 前処理：問題1と同じくOne-Hotエンコーディングと標準化を行います。
# 決定木はスケール不変（標準化しても結果は同じ）ですが、
# 比較のために同一の前処理フローを適用します。
X_encoded = pd.get_dummies(X, drop_first=True)

# ==========================================
# 1. 課題 2.1: 分割を変えて 100 回試行し、箱ひげ図を作成
# ==========================================
print("--- [1] 課題 2.1: 100回ランダム分割の評価を開始 ---")

dt_mses = []
bagging_mses = []
rf_mses = []

for i in range(100):
    # 毎回異なる乱数シードを用いてデータを 8:2 に分割（分割の仕方を変える）
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=i
    )
    
    # 標準化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 1. 単一の決定木 (制限なし)
    # 決定木の学習アルゴリズム自体にある程度の乱数性（同点の分岐の選択など）があるため、
    # 制御用に一貫した内部シードを設定します。
    dt = DecisionTreeRegressor(random_state=42)
    dt.fit(X_train_scaled, y_train)
    dt_mses.append(mean_squared_error(y_test, dt.predict(X_test_scaled)))
    
    # 2. Bagging (決定木の本数=50)
    # 単一決定木の分散を下げるため、ブートストラップサンプルで複数の木を並列学習します。
    bagging = BaggingRegressor(
        estimator=DecisionTreeRegressor(), n_estimators=50, random_state=42, n_jobs=-1
    )
    bagging.fit(X_train_scaled, y_train)
    bagging_mses.append(mean_squared_error(y_test, bagging.predict(X_test_scaled)))
    
    # 3. Random Forest (決定木の本数=50, max_features=0.6)
    # バギングに加え、分岐時の候補特徴量をランダムに制限（60%）し、木同士の相関を下げることで
    # アンサンブル全体の分散をさらに下げます。
    rf = RandomForestRegressor(
        n_estimators=50, max_features=0.6, random_state=42, n_jobs=-1
    )
    rf.fit(X_train_scaled, y_train)
    rf_mses.append(mean_squared_error(y_test, rf.predict(X_test_scaled)))

# 箱ひげ図の描画と保存
plt.figure()
plt.boxplot([dt_mses, bagging_mses, rf_mses], tick_labels=["Decision Tree", "Bagging", "Random Forest"])
plt.ylabel("Test MSE")
plt.title("Comparison of Test MSE (100 Random Splits)")
plt.grid(True, axis="y", ls="--", color="0.9")
plt.tight_layout()
boxplot_path = os.path.join(plots_dir, "boxplot_comparison.png")
plt.savefig(boxplot_path, dpi=300)
plt.close()

print(f"箱ひげ図を保存しました: {boxplot_path}")
print(f"Decision Tree 平均 Test MSE: {np.mean(dt_mses):.4f}")
print(f"Bagging       平均 Test MSE: {np.mean(bagging_mses):.4f}")
print(f"Random Forest 平均 Test MSE: {np.mean(rf_mses):.4f}")

# ==========================================
# 2. 課題 2.2: 本数 B に対する特定テスト点の予測分散の評価（周辺分散の評価）
# ==========================================
print("\n--- [2] 課題 2.2: 本数 B に対する予測分散の測定を開始 ---")

# 【方針】周辺分散 V[f_hat(x_i)] を評価する。
# テスト点 x_i は固定した上で、各試行ごとに訓練データ D_train をプールから
# ランダムにサンプリング（train_size=0.8）する。
#
# 木の深さは問題の指定通り制限なし（depth=None）、max_features=0.6 とする。

# テスト用の固定点 x_i (データセット全体の最初の行) を分離
x_i_raw = X_encoded.iloc[0:1]

# 残りのデータを訓練用プールにする
X_pool = X_encoded.iloc[1:]
y_pool = y.iloc[1:]

# アンサンブルの本数 B のリスト (2^0 から 2^8)
B_list = [2**k for k in range(9)]  # [1, 2, 4, 8, 16, 32, 64, 128, 256]

N_TRIALS = 50  # 試行回数
train_size = 0.8

bagging_variances = []
rf_variances = []

for B in B_list:
    bagging_preds = []
    rf_preds = []

    # 各 B に対し、データの分割シードを変えながら N_TRIALS 回試行を行う
    for seed in range(N_TRIALS):
        # 訓練用プールから 80% を訓練データとしてサンプリング（周辺分散）
        X_train, _, y_train, _ = train_test_split(
            X_pool, y_pool, train_size=train_size, random_state=seed
        )
        
        # 訓練データ基準で標準化
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        x_i_scaled = scaler.transform(x_i_raw)
        
        # Bagging (深さ制限なし)
        bagging = BaggingRegressor(
            estimator=DecisionTreeRegressor(max_depth=None),
            n_estimators=B,
            random_state=seed,
            n_jobs=-1,
        )
        bagging.fit(X_train_scaled, y_train)
        bagging_preds.append(bagging.predict(x_i_scaled)[0])

        # Random Forest (深さ制限なし, max_features=0.6)
        rf = RandomForestRegressor(
            max_depth=None,
            n_estimators=B,
            max_features=0.6,
            random_state=seed,
            n_jobs=-1,
        )
        rf.fit(X_train_scaled, y_train)
        rf_preds.append(rf.predict(x_i_scaled)[0])

    # N_TRIALS 個の予測値の不偏分散を算出
    bagging_variances.append(np.var(bagging_preds, ddof=1))
    rf_variances.append(np.var(rf_preds, ddof=1))

# 両対数（log-log）グラフの描画と保存
plt.figure()
plt.plot(B_list, bagging_variances, "o-", label="Bagging", color="red")
plt.plot(B_list, rf_variances, "s-", label="Random Forest", color="blue")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Number of trees (B)")
plt.ylabel("Variance of prediction V[f_hat(x_i)]")
plt.title("Log-Log Plot of Prediction Variance vs Ensemble Size (B)")
plt.legend()
plt.grid(True, which="both", ls="--", color="0.9")
plt.tight_layout()
loglog_path = os.path.join(plots_dir, "variance_loglog.png")
plt.savefig(loglog_path, dpi=300)
plt.close()

print(f"両対数グラフを保存しました: {loglog_path}")

# 各 B における分散データを出力
for B, v_bag, v_rf in zip(B_list, bagging_variances, rf_variances):
    print(f"B={B:3d} | Bagging 分散: {v_bag:.5f} | Random Forest 分散: {v_rf:.5f}")
