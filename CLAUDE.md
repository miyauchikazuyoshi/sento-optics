# sento-optics

## 概要
電子の非局在化(δ)を統一記述子として、界面特性（光沢、表面張力）を説明する研究プログラム。

## 構成
```
theory/          → 理論メモ（optics, surface_tension, phase）
simulation/      → 数値検証
drafts/          → 論文ドラフト
data/            → 実験・シミュレーションデータ
references/      → 参考文献
```

## 環境
```bash
pip install -r requirements.txt
```

## 注意事項
- 理論メモ → 数値テスト → 論文 の流れを守る
- 数式は LaTeX 記法で統一する
- データファイルが大きい場合は Git LFS を使う
