#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
機械学習概論 後半レポート - 問題1: Gaussian Process と Multi-Layer Perceptron の比較

このスクリプトは、1次元データに対するガウス過程回帰 (GPR) とニューラルネットワーク (MLP) の挙動を比較します。
ライブラリのインポート意図、クラスの役割、および各モデルの引数の意味を詳細な日本語コメントで解説しています。
"""

import os
# numpy: 数値計算（ベクトル・行列演算、乱数生成）を効率的に行うための標準的ライブラリ
import numpy as np
# matplotlib.pyplot: データの可視化（グラフの描画、画像保存）を行うためのライブラリ
import matplotlib.pyplot as plt

# ==========================================
# 科学技術計算ライブラリ scikit-learn からモデルをインポート
# ==========================================
# GaussianProcessRegressor: ガウス過程回帰 (GPR) を実行するクラス。
# 入力データ間の相関関係（カーネル関数）に基づいて、予測平均値と同時に予測不確実性（分散・標準偏差）を代数的に計算します。
from sklearn.gaussian_process import GaussianProcessRegressor

# RBF: 放射基底関数 (Radial Basis Function) カーネル。ガウスカーネルとも呼ばれます。
# 近い距離の入力点同士は高い相関を持ち、遠い点同士は相関が指数関数的に減衰するという特性を持ち、滑らかな関数を表現するのに最適です。
# WhiteKernel: 観測データの「ノイズ（測定誤差など）」をモデル化するためのカーネル。
# カーネルの対角成分（各データ点自身）に一定の分散を追加し、GPRがデータ点を完全に通るのではなく、ノイズを許容して滑らかに回帰できるようにします。
from sklearn.gaussian_process.kernels import RBF, WhiteKernel

# MLPRegressor: 多層パーセプトロン (Multi-Layer Perceptron) による回帰を行うクラス。
# いわゆるディープニューラルネットワーク（全結合層の積み重ね）であり、多数の重みパラメータを最適化して非線形関数を学習します。
from sklearn.neural_network import MLPRegressor


# ==========================================
# 定数の定義 (ハイパーパラメータの設定)
# ==========================================
# RANDOM_STATE: 乱数のシード値。
# データの生成、GPのオプティマイザの初期値、MLPの初期重みの決定などに使用され、実行結果の再現性を担保します。
RANDOM_STATE = 0  

# N_SAMPLES_LIST: 比較を行う学習データ数のバリエーション。
# データ数によってモデルがどのように過学習・安定化するかを観察します。
N_SAMPLES_LIST = [10, 30, 100]

# NOISE_STD: 真のデータ生成プロセスにおける観測ノイズ (epsilon) の標準偏差。
# ここでは標準偏差 0.2 (分散 0.2^2 = 0.04) の白色雑音を加えます。
NOISE_STD = 0.2  

# X_MIN, X_MAX: 入力変数 x の定義域（範囲）。
X_MIN, X_MAX = 0.0, 1.0

# N_PLOT_POINTS: 予測曲線を滑らかに描画するためのテスト点の数。
# 0 から 1 までを 500 等分したグリッド上で各モデルの予測値を計算します。
N_PLOT_POINTS = 500


# ==========================================
# データ生成関数の定義
# ==========================================
def true_function(x):
    """
    真の関数 y = sin(2 * pi * x) の計算。
    モデルの予測曲線が、この真の曲線にどれだけ近づけるかを評価します。
    """
    return np.sin(2 * np.pi * x)

def generate_dataset(n_samples, random_state=0):
    """
    学習データを生成する関数。
    - x: 区間 [0, 1] からの一様分布 (Uniform Distribution) に従うランダムな入力。
    - y: 真の関数値に、平均 0、標準偏差 0.2 の正規分布 (Normal Distribution) に従うノイズ epsilon を加えた観測値。
    """
    # 推奨される新しい乱数生成器のインスタンス化 (Generator)
    rng = np.random.default_rng(random_state)
    
    # uniform(low, high, size): lowからhighの範囲から一様ランダムにサンプリング
    x = rng.uniform(X_MIN, X_MAX, size=(n_samples, 1))
    
    # normal(loc, scale, size): 平均 loc, 標準偏差 scale の正規分布からサンプリング
    noise = rng.normal(0.0, NOISE_STD, size=(n_samples, 1))
    
    # y = sin(2*pi*x) + epsilon
    y = true_function(x) + noise
    
    # y.ravel() は 2次元配列 (n, 1) を 1次元配列 (n,) に平坦化します。
    # scikit-learn のモデルが目的変数として 1次元配列を要求するためです。
    return x, y.ravel()


# ==========================================
# メインシミュレーション処理
# ==========================================
def main():
    print("=== Problem 1: GPR vs MLP Simulation Started ===")
    
    # 保存先ディレクトリの作成 (path_join を用いてプラットフォームに依存しないパスを作成)
    plot_dir = os.path.join(os.path.dirname(__file__), "plots")
    os.makedirs(plot_dir, exist_ok=True)
    print(f"[INFO] Plots will be saved to: {plot_dir}")

    # プロット用の評価点グリッドを作成
    # np.linspace(start, stop, num): startからstopまでをnum個に等分割したベクトルを生成
    # [:, np.newaxis] により、形状を (500,) から 2次元の縦ベクトル (500, 1) に変換します。
    # scikit-learn の入力 X は常に (サンプル数, 特徴量数) の2次元行列形式である必要があるためです。
    X_plot = np.linspace(X_MIN, X_MAX, N_PLOT_POINTS)[:, np.newaxis]
    y_true = true_function(X_plot).ravel()

    # 1行3列のマルチパネルプロット (サブプロット) を作成
    # figsize=(横幅, 高さ) で図のサイズを指定。sharey=True で3つのグラフのY軸の範囲を統一します。
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), sharey=True)
    
    for idx, n_samples in enumerate(N_SAMPLES_LIST):
        ax = axes[idx]
        print(f"\n--- Running simulation for n_samples = {n_samples} ---")
        
        # 1. 指定データ数での学習データの生成
        X_train, y_train = generate_dataset(n_samples, random_state=RANDOM_STATE)
        
        # データの統計量をログ出力して確認 (デバッグ用)
        print(f"[DEBUG] X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
        print(f"[DEBUG] y_train mean: {np.mean(y_train):.4f}, variance: {np.var(y_train):.4f}")
        
        # ==========================================
        # 2. ガウス過程回帰 (GPR) の実装
        # ==========================================
        # カーネル関数の構成:
        # RBF() : length_scale=0.5 (初期長さスケール。xがどのくらい離れると相関が弱まるかの初期仮定)
        #         length_scale_bounds=(1e-2, 1e2) (最適化の際の探索範囲下限・上限)
        # WhiteKernel() : noise_level=NOISE_STD**2 (初期観測ノイズ分散。真の 0.2^2 = 0.04 を初期値とする)
        #                 noise_level_bounds=(1e-5, 1e1) (ノイズ分散最適化の範囲)
        kernel = RBF(length_scale=0.5, length_scale_bounds=(1e-2, 1e2)) + \
                 WhiteKernel(noise_level=NOISE_STD**2, noise_level_bounds=(1e-5, 1e1))
        
        # GaussianProcessRegressor の引数説明:
        # - kernel: 事前共分散を記述する上記のカーネルオブジェクト
        # - normalize_y: True にすることで、yを平均0、分散1に正規化してから学習を行います。
        #   GPRは「事前平均が0」の確率過程であるため、データの平均が0から大きくズレている場合、
        #   このオプションをTrueにしないと予測値が事前平均の0に引っ張られて歪んでしまいます。
        # - n_restarts_optimizer: 対数周辺尤度 (LML) を最大化する最適化を、初期値を変えて指定回数 (5回) 繰り返します。
        #   LMLの最適化は非凸 (Non-convex) であり局所解に陥りやすいため、初期値を変えて再実行し、最も良い極大値（グローバル最適解）を採用します。
        # - random_state: 最適化再実行時の初期ランダムパラメータ決定用のシード値
        gp = GaussianProcessRegressor(
            kernel=kernel,
            normalize_y=True,
            n_restarts_optimizer=5,
            random_state=RANDOM_STATE
        )
        
        # モデルのフィッティング（GPRでは、グラム行列の逆行列計算とカーネルのハイパーパラメータの最適化が行われます）
        gp.fit(X_train, y_train)
        print(f"[INFO] Optimized GP kernel: {gp.kernel_}")
        
        # predict() の引数説明:
        # - X_plot: 予測を行いたいテスト点入力 (500, 1)
        # - return_std=True: 各テスト点における予測平均だけでなく、予測の「標準偏差 (std)」も同時に計算して返します。
        #   静的型チェッカーの型推論エラーを防ぐため、末尾に # type: ignore を付与しています。
        y_gp_mean, y_gp_std = gp.predict(X_plot, return_std=True)  # type: ignore
        
        # ==========================================
        # 3. 多層パーセプトロン (MLP) の実装
        # ==========================================
        # MLPRegressor の引数説明:
        # - hidden_layer_sizes=(50, 50): 隠れ層のニューロン構造。ここでは「50個のニューロンを持つ層」を「2層」重ねることを表します。
        # - activation="tanh": 活性化関数として双曲線正接関数 tanh(x) を使用します。
        #   tanhは出力が [-1, 1] で滑らかな曲線（微分可能）であるため、滑らかな回帰曲線を学習するのに適しています。
        # - solver="lbfgs": 最適化アルゴリズム（ソルバー）として準ニュートン法の一つである L-BFGS を指定します。
        #   一般的なニューラルネットで使われる Adam や SGD などの勾配降下法はデータ数が数万件のときに有効ですが、
        #   今回のように $n \le 100$ 程度の極めて少数のデータに対しては、2次情報（ヘシアンの近似）を利用する L-BFGS の方が
        #   圧倒的に収束が早く、極めて高精度なパラメータ探索が可能です。
        # - alpha=1e-4: L2正則化（Weight Decay）の強度。損失関数に重みの二乗和を加えることで、重みパラメータが不必要に大きくなるのを防ぎ、過学習を抑制します。
        # - max_iter=5000: ソルバーが最適化ループを回す最大反復回数。収束する前にループが打ち切られるのを防ぐため、十分に大きな値 (5000) を設定しています。
        # - random_state: 重みの初期値設定およびL-BFGS内のランダム性の再現性を担保するためのシード値。
        mlp = MLPRegressor(
            hidden_layer_sizes=(50, 50),
            activation="tanh",
            solver="lbfgs",
            alpha=1e-4,
            max_iter=5000,
            random_state=RANDOM_STATE
        )
        
        # MLPの学習（誤差逆伝播法とL-BFGS法により、2701個の重み・バイアスパラメータを更新します）
        mlp.fit(X_train, y_train)
        y_mlp_pred = mlp.predict(X_plot)
        
        # ==========================================
        # 4. 各結果のプロット
        # ==========================================
        # 真の正弦波を黒の破線で描画
        ax.plot(X_plot, y_true, color="black", linestyle="--", linewidth=1.5, label="True Function: $\sin(2\pi x)$")
        
        # 実際に生成した学習データ（ノイズ付き）を黒丸で散布図として描画
        ax.scatter(X_train, y_train, color="black", marker="o", s=30, label=f"Training Data ($n={n_samples}$)")
        
        # GPRの予測平均値を青の実線で描画
        ax.plot(X_plot, y_gp_mean, color="royalblue", linewidth=2.0, label="GP Mean Prediction")
        
        # GPRの 95% 信頼区間を青い網掛け（半透明）で描画
        # 1次元正規分布において、95%信頼区間は 平均 +/- 1.96 * 標準偏差 (std) で表されます。
        # fill_between(x, y1, y2): 曲線 y1 と y2 の間を塗りつぶします。alpha=0.2 で透明度を指定。
        ax.fill_between(
            X_plot.ravel(),
            y_gp_mean - 1.96 * y_gp_std,
            y_gp_mean + 1.96 * y_gp_std,
            color="royalblue",
            alpha=0.2,
            label="GP 95% Conf. Interval"
        )
        
        # MLPの予測曲線を赤の実線で描画
        ax.plot(X_plot, y_mlp_pred, color="crimson", linewidth=2.0, label="MLP Prediction")
        
        # サブプロットごとのレイアウト・ラベル調整
        ax.set_title(f"Sample Size $n = {n_samples}$", fontsize=13, fontweight="bold")
        ax.set_xlabel("$x$", fontsize=12)
        if idx == 0:
            ax.set_ylabel("$y$", fontsize=12)
        ax.set_xlim(X_MIN, X_MAX)
        ax.set_ylim(-2.0, 2.0)
        ax.grid(True, linestyle=":", alpha=0.6)
        
        # 凡例の配置 (1枚目のパネルのみに配置して、他のパネルの視認性を高めます)
        if idx == 0:
            # frameon=True で凡例の枠線を描画, framealpha=0.9 で半透明の白背景にして背後のグラフが隠れるのを防ぎます。
            ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="none", framealpha=0.9, fontsize=9)

    # サブプロット間の隙間が適切になるように自動調整
    plt.tight_layout()
    
    # グラフ画像ファイルとして高画質 (dpi=300) で保存
    plot_path = os.path.join(plot_dir, "gp_mlp_comparison.png")
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close()
    
    print(f"\n[SUCCESS] Comparison plot saved to: {plot_path}")
    print("=== Problem 1 Simulation Completed Successfully ===")

if __name__ == "__main__":
    main()
