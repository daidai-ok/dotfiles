# dotfiles

MacOS 開発環境の設定ファイル集。

## ディレクトリ構造

```
dotfiles/
├── README.md
├── ghostty/
│   └── config         # Ghosttyターミナル設定
├── starship/
│   └── starship.toml  # Starshipプロンプト設定
├── tmux/
│   └── tmux.conf      # tmux設定ファイル
├── vimrc/
│   ├── .vimrc         # Vimメイン設定
│   ├── appearance.vimrc  # Vim外観設定
│   └── basic.vimrc    # Vim基本設定
└── claude-skills/     # Claude Code用カスタムスキル
```

## セットアップ

### Ghostty

Ghosttyはシンボリックリンク経由だと設定ファイルを正しく読み込めないため、デフォルトの設定ファイルに直接コピーして上書きする：

```bash
mkdir -p ~/.config/ghostty && cp ~/dotfiles/ghostty/config ~/.config/ghostty/config
```

設定を変更した場合は再度コピーを実行して反映する。

### tmux

tmuxの設定ファイルをシンボリックリンクで配置：

```bash
ln -sf ~/dotfiles/tmux/tmux.conf ~/.tmux.conf
```

設定の反映方法：
- 新規セッション: tmuxを起動すると自動的に適用
- 既存セッション内: `Ctrl-a r` で設定をリロード（prefix keyがCtrl-aに設定済み）
- または `Ctrl-a :` → `source-file ~/.tmux.conf` を実行

### Starship

Starshipプロンプトの設定ファイルをシンボリックリンクで配置：

```bash
mkdir -p ~/.config && ln -sf ~/dotfiles/starship/starship.toml ~/.config/starship.toml
```

