#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
機械学習概論 後半レポート - 問題2: Support Vector Machine (SVM) の比較

このスクリプトは、make_moons データセットに対して線形SVMおよびRBFカーネルSVMをフィッティングし、
決定領域、サポートベクトル、テスト精度を視覚化および評価します。
ライブラリのインポート意図、クラスの役割、および各モデルの引数の意味を詳細な日本語コメントで解説しています。
"""

import os
# numpy: 数値計算（ベクトル・行列演算、グリッド生成、配列操作）を行うためのライブラリ。
# SVMの決定境界を描画するために、2次元座標平面を格子点（グリッド）として生成・変換する際に使用します。
import numpy as np

# matplotlib.pyplot: データの視覚化（グラフの描画、画像ファイルとしての保存）を行うためのライブラリ。
import matplotlib.pyplot as plt

# ListedColormap: 任意のカラーコードから独自のカラーマップ（グラデーションや領域色分け用の配色パレット）を作成するクラス。
# 決定境界の背景色（クラス0とクラス1の領域）を塗り分けるために用います。
from matplotlib.colors import ListedColormap

# ==========================================
# 科学技術計算ライブラリ scikit-learn からモデルとユーティリティをインポート
# ==========================================
# make_moons: 2次元の非線形分離可能な半月型データセットを生成する関数。
# 直線では完璧に分類できないデータを人工的に生成し、非線形モデル（RBFカーネル）の優位性を検証するのに適しています。
# - 引数 n_samples: 生成する全データ数（本問では 1200 点）。
# - 引数 noise: データに加えるガウシアンノイズの大きさ（標準偏差）。値が大きいほど半月が互いに重なり合います。
# - 引数 random_state: 再現性を保つためのシード値。
from sklearn.datasets import make_moons

# train_test_split: データセットをトレーニングデータ（訓練用）とテストデータ（評価用）に分割する関数。
# モデルが未知のデータに対してどれだけ正しく予測できるか（汎化性能）を測るために使用します。
# - 引数 train_size / test_size: 分割比率またはサンプル数（本問では訓練用 200 点、テスト用 1000 点）。
# - 引数 stratify: 各クラスの存在比率を維持したまま分割を行うためのオプション。偏った学習を防ぎます。
from sklearn.model_selection import train_test_split

# SVC: Support Vector Classification (サポートベクトル分類器) を構築するクラス。
# 決定境界と最も近いデータ点（サポートベクトル）の間の距離（マージン）を最大化するように境界を学習するアルゴリズム。
# - 引数 kernel: カーネル関数の指定（"linear", "rbf" など）。
# - 引数 C: ソフトマージンSVMの正則化パラメータ。誤分類の許容度を調整します。
# - 引数 gamma: RBFカーネルの局所的影響範囲を制御するパラメータ。
from sklearn.svm import SVC


# ==========================================
# 定数の定義 (ハイパーパラメータの設定)
# ==========================================
# RANDOM_STATE: データの分割や決定境界の再現性を保証する乱数シード。
RANDOM_STATE = 0

# N_SAMPLES: 全データ数（学習200点 + テスト1000点 = 1200点）
N_SAMPLES = 1200
# NOISE: データに付与するガウシアンノイズの標準偏差。値が大きいほどクラスが重なり合います。
NOISE = 0.2

# C: ソフトマージンSVMの正則化パラメータ。
# 誤分類に対するペナルティの強さを表し、Cが大きいほど誤分類を許容せずハードマージンに近づきます（過学習の懸念）。
# Cが小さいほどマージンを広く取り、一部の誤分類を許容して汎化性能を高めます。本問では 1.0 に固定します。
C_PARAM = 1.0

# ==========================================
# 決定境界描画用のカラーマップ定義 (プレミアム・パステルデザイン)
# ==========================================
# クラス0（赤系パステル）、クラス1（青系パステル）を背景用としてマッピング
CMAP_LIGHT = ListedColormap(["#ffe3e3", "#e0f0ff"])
# データプロット用の鮮やかな赤と青
COLORS_DARK = ["#ff4d4d", "#0080ff"]


def plot_decision_boundary(clf, X, y, ax, title_str):
    """
    分類器の決定領域、サポートベクトル、および学習データを美しくプロットするヘルパー関数。
    
    引数:
        clf: 学習済みの分類器オブジェクト (SVC)
        X: 学習データの入力特徴量配列、形状は (N, 2)
        y: 学習データの正解ラベル配列、形状は (N,)
        ax: 描画先の matplotlib.axes オブジェクト
        title_str: グラフの上部に表示するタイトル文字列
    """
    # 1. グリッド点の生成 (高密度 500x500 で境界を非常に滑らかに描写)
    # X[:, 0] は第1特徴量 (x1)、X[:, 1] は第2特徴量 (x2) の列を取り出します。
    # 描画に余白を持たせるため、最小値・最大値から 0.5 だけ外側まで描画範囲を広げています。
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    
    # np.linspace(start, stop, num): start から stop までを num 等分した1次元配列を作成。
    # np.meshgrid: 2つの1次元座標配列から、平面上の格子点を表す2次元座標行列 (xx, yy) を生成。
    # これにより、格子状に並んだすべての点のx座標行列とy座標行列が用意されます。
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 500),
        np.linspace(y_min, y_max, 500)
    )
    
    # 2. グリッドの各点に対する分類予測の実行
    # - ravel(): 2次元配列を平坦化して1次元配列に変換。
    # - np.c_[A, B]: 2つの1次元配列を列（横）方向に結合して、(500x500, 2) の座標ペアの行列を生成。
    #   scikit-learn の predict メソッドが受け取る形式に変換するための「呪文」です。
    grid_points = np.c_[xx.ravel(), yy.ravel()]
    
    # clf.predict(): 格子点データすべてに対して、予測クラスラベル (0 または 1) を計算。
    # reshape(xx.shape): 予測結果の1次元配列を、再び元の格子状の2次元配列 (500, 500) に戻します。
    Z = clf.predict(grid_points)
    Z = Z.reshape(xx.shape)
    
    # 3. 決定領域を等高線プロット (contourf) でパステルカラーに塗りつぶし
    # contourf は、同じ値（クラスラベル）の領域境界を検出し、その間を cmap (カラーマップ) で塗りつぶします。
    # これにより、モデルがどのように分類空間を切り分けているかが一目で視覚化されます。
    ax.contourf(xx, yy, Z, cmap=CMAP_LIGHT, alpha=1.0)
    
    # 4. 学習データ点 (Training Data) をプロット
    # クラスごとにループを回し、色とラベルを明示的に指定して散布図 (scatter) として描画します。
    # mask: ラベルが各クラスインデックスと一致するインデックスを True としたブールマスク配列。
    for class_idx, color in enumerate(COLORS_DARK):
        mask = (y == class_idx)
        ax.scatter(
            X[mask, 0], X[mask, 1],
            color=color, edgecolor="k", s=40,
            label=f"Train Class {class_idx}", linewidths=0.8
        )
        
    # 5. サポートベクトル (Support Vectors) のプロットと強調表示
    # - clf.support_vectors_: 分類境界（マージン境界）の構築に実際に関与した、
    #   境界に最も近い学習データの座標が格納されている (N_SV, 2) 形状の配列です。
    # - facecolors="none": サポートベクトルの散布図の内側を塗りつぶさず透明にします。
    # - edgecolors="black", linewidths=1.3: サポートベクトルの外枠を太めの黒線で描画し、強調します。
    sv = clf.support_vectors_
    ax.scatter(
        sv[:, 0], sv[:, 1],
        s=90, facecolors="none", edgecolors="black",
        linewidths=1.3, label="Support Vectors"
    )
    
    # 6. グラフの装飾
    ax.set_title(title_str, fontsize=12, fontweight="bold")
    ax.set_xlabel("$x_1$", fontsize=11)
    ax.set_ylabel("$x_2$", fontsize=11)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    # グリッド線を表示 (linestyle=":" で点線にし、alpha=0.5 で半透明にして主役のデータを邪魔しないようにします)
    ax.grid(True, linestyle=":", alpha=0.5)


def main():
    print("=== Problem 2: SVM Simulation Started ===")
    
    # 1. フォルダの準備
    # os.path.dirname(__file__) は実行しているスクリプトのディレクトリパスを取得します。
    plot_dir = os.path.join(os.path.dirname(__file__), "plots")
    os.makedirs(plot_dir, exist_ok=True)
    
    # 2. make_moons によるデータ生成
    # noise=0.2 で適度に重なり合う2つの半月形状データを生成
    X, y = make_moons(n_samples=N_SAMPLES, noise=NOISE, random_state=RANDOM_STATE)
    
    # 3. データの分割 (学習用 200 点、テスト用 1000 点)
    # - stratify=y (層化分割): 学習用データとテスト用データのクラス割合（0と1の比率）を、元のデータ全体と同じ比率（50%:50%）に強制的に揃えます。
    #   偏ったデータで学習・評価が行われるのを防止する必須の「呪文」です。
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        train_size=200,
        test_size=1000,
        random_state=RANDOM_STATE,
        stratify=y
    )
    
    # ガイドライン 3.4 に基づく、データの流れ（形状と統計量）のログ出力
    print(f"[DEBUG] X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
    print(f"[DEBUG] X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")
    print(f"[DEBUG] Train Class 0: {np.sum(y_train == 0)} points, Class 1: {np.sum(y_train == 1)} points")
    
    # ==========================================
    # 4. 実験 2.1: 線形 SVM vs RBF カーネル SVM (gamma=1.0)
    # ==========================================
    # subplots(1, 2) により、横に2つのグラフが並んだ 1行2列 の描画領域を生成します。
    fig21, axes21 = plt.subplots(1, 2, figsize=(13, 5.5))
    
    # (a) 線形 SVM (Linear SVM)
    # - kernel="linear": 線形カーネル K(x, x') = x^T x を使用します。元の空間で直線の決定境界を引きます。
    # - C=C_PARAM: マージン違反に対するペナルティ係数。
    clf_linear = SVC(kernel="linear", C=C_PARAM, random_state=RANDOM_STATE)
    # fit(): 凸二次計画問題を解く最適化を実行し、サポートベクトルおよび超平面の係数を決定します。
    clf_linear.fit(X_train, y_train)
    # score(): テストデータに対して予測を行い、正解率（テスト精度）を計算して返します。
    acc_linear = clf_linear.score(X_test, y_test)
    # clf_linear.support_: サポートベクトルとして選択されたデータの訓練データ上のインデックス配列。
    # len() でその個数を算出します。
    n_sv_linear = len(clf_linear.support_)
    print(f"[INFO] Linear SVM - Test Accuracy: {acc_linear:.4f}, Support Vectors: {n_sv_linear}")
    
    # ヘルパー関数を呼び出して決定領域を描画
    plot_decision_boundary(
        clf_linear, X_train, y_train, axes21[0],
        f"Linear SVM (C=1.0)\nTest Acc: {acc_linear:.3f} (SV: {n_sv_linear})"
    )
    # 凡例を左下に配置 (frameon=True で枠線をつけ、半透明にして視認性を高めます)
    axes21[0].legend(loc="lower left", frameon=True, framealpha=0.9, fontsize=9)
    
    # (b) RBF カーネル SVM (gamma=1.0)
    # - kernel="rbf": 動径基底関数（RBF/ガウス）カーネル K(x, x') = exp(-gamma * ||x - x'||^2) を使用します。
    #   データを無限次元の多項式特徴空間へ写像することと等価であり、曲線の決定境界を引くことができます。
    # - gamma: ガウス関数の広がりの狭さ（影響範囲の狭さ）を決定。gamma=1.0 は今回のデータ間隔に適した標準的な影響範囲です。
    clf_rbf_1 = SVC(kernel="rbf", C=C_PARAM, gamma=1.0, random_state=RANDOM_STATE)
    clf_rbf_1.fit(X_train, y_train)
    acc_rbf_1 = clf_rbf_1.score(X_test, y_test)
    n_sv_rbf_1 = len(clf_rbf_1.support_)
    print(f"[INFO] RBF SVM (gamma=1.0) - Test Accuracy: {acc_rbf_1:.4f}, Support Vectors: {n_sv_rbf_1}")
    
    plot_decision_boundary(
        clf_rbf_1, X_train, y_train, axes21[1],
        f"RBF SVM (C=1.0, $\\gamma=1.0$)\nTest Acc: {acc_rbf_1:.3f} (SV: {n_sv_rbf_1})"
    )
    axes21[1].legend(loc="lower left", frameon=True, framealpha=0.9, fontsize=9)
    
    # レイアウトの自動微調整を行い、グラフ同士やラベルの重なりを防ぎます。
    plt.tight_layout()
    # グラフ画像を 300 dpi の高画質で保存します。
    plot_path_21 = os.path.join(plot_dir, "svm_comparison_linear_rbf.png")
    plt.savefig(plot_path_21, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SUCCESS] Plot saved: {plot_path_21}")
    
    # ==========================================
    # 5. 実験 2.2: RBF カーネル SVM における gamma の影響の比較
    # ==========================================
    # gamma の値を 1000倍 変化させて、決定境界の「局所性（うねり）」がどう変わるかを観察します。
    gamma_list = [0.1, 1.0, 100.0]
    # subplots(1, 3) により、横に3つのグラフが並んだ 1行3列 の描画領域を生成します。
    fig22, axes22 = plt.subplots(1, 3, figsize=(18, 5.5))
    
    # 各 gamma でフィッティングと評価
    for idx, gamma in enumerate(gamma_list):
        ax = axes22[idx]
        
        # SVCクラスのパラメータ説明:
        # - gamma: RBFの広がりを制御。数学的には gamma = 1 / (2 * sigma^2) に対応。
        #   - gammaが小さい(0.1)と、影響範囲 sigma が広くなり、遠くの点同士の相関が高くなるため、
        #     境界はほぼ直線（線形SVM）に近くなり、シンプルな分類になります（過小適合・アンダーフィッティング傾向）。
        #   - gammaが大きい(100.0)と、個々のデータ点の局所影響範囲 sigma が極めて狭くなり、
        #     各データ点の周囲（至近距離）だけを別クラスとして囲むような、無数の「島」が点在する複雑な決定境界になります（過学習・オーバーフィッティング傾向）。
        clf_rbf = SVC(kernel="rbf", C=C_PARAM, gamma=gamma, random_state=RANDOM_STATE)
        clf_rbf.fit(X_train, y_train)
        acc_rbf = clf_rbf.score(X_test, y_test)
        n_sv_rbf = len(clf_rbf.support_)
        print(f"[INFO] RBF SVM (gamma={gamma}) - Test Accuracy: {acc_rbf:.4f}, Support Vectors: {n_sv_rbf}")
        
        # 決定境界と各クラスデータをプロット
        plot_decision_boundary(
            clf_rbf, X_train, y_train, ax,
            f"RBF SVM ($\\gamma={gamma}$)\nTest Acc: {acc_rbf:.3f} (SV: {n_sv_rbf})"
        )
        # 最初のグラフにのみ凡例を表示して、全体の視認性を保ちます
        if idx == 0:
            ax.legend(loc="lower left", frameon=True, framealpha=0.9, fontsize=9)
            
    plt.tight_layout()
    plot_path_22 = os.path.join(plot_dir, "svm_gamma_comparison.png")
    plt.savefig(plot_path_22, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SUCCESS] Plot saved: {plot_path_22}")
    print("=== Problem 2 Simulation Completed Successfully ===")


if __name__ == "__main__":
    main()
