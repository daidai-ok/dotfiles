# Claude Skills Directory

このディレクトリは、Claude Codeで使用するカスタムスキルを管理します。

## 利用可能なスキル

### 1. git-commit-message-generator

git diffを分析して適切なコミットメッセージを生成するスキルです。

**主な機能：**
- git diffの自動解析
- 変更内容に基づくコミットタイプの判定
- Conventional Commit形式のメッセージ生成
- ファイルベースでのスコープ自動検出
- 複数のフォーマット対応（conventional/simple/detailed）

**使用方法：**

```bash
# 基本的な使用（未ステージの変更を解析）
python3 claude-skills/git-commit-message-generator.py

# ステージング済みの変更を解析
python3 claude-skills/git-commit-message-generator.py --staged

# 特定ブランチとの差分を解析
python3 claude-skills/git-commit-message-generator.py --branch main

# シンプルな形式で出力
python3 claude-skills/git-commit-message-generator.py --format simple
```

**Claude内での呼び出し：**

```
# コミットメッセージ生成
/skill git-commit-message-generator

# ステージング済み変更のメッセージ生成
/skill git-commit-message-generator --staged
```

### 2. tmux-config-manager

tmuxの設定ファイルを管理・検証するスキルです。

**主な機能：**
- 構文エラーの検出
- 設定の矛盾や競合の検出
- 非推奨オプションの警告
- カラー値の検証
- パスの存在確認

**使用方法：**

```bash
# 基本的な検証
python3 claude-skills/tmux_config_validator.py

# 特定のファイルを検証
python3 claude-skills/tmux_config_validator.py ~/.tmux.conf

# JSON形式で出力
python3 claude-skills/tmux_config_validator.py --json
```

**Claude内での呼び出し：**

```
# tmux設定を検証
/skill tmux-config-manager validate

# 競合をチェック
/skill tmux-config-manager check-conflicts
```

## スキルの追加方法

新しいスキルを追加する場合：

1. `claude-skills/`ディレクトリに新しいスキル用のファイルを作成
2. スキルのドキュメント（.mdファイル）を作成
3. 実装スクリプト（.pyまたは.shファイル）を作成
4. このREADMEに新しいスキルの情報を追加

## ディレクトリ構造

```
claude-skills/
├── README.md                          # このファイル
├── git-commit-message-generator.py    # コミットメッセージ生成スクリプト
├── commit-msg-gen.md                  # コミットメッセージ生成のドキュメント
├── tmux-config-manager.md             # tmuxスキルのドキュメント
└── tmux_config_validator.py           # tmux検証の実装
```

## スキル開発のガイドライン

1. **単一責任の原則**: 各スキルは1つの明確な目的を持つ
2. **エラー処理**: 適切なエラーメッセージと提案を提供
3. **ドキュメント**: 使用方法と例を含む明確なドキュメント
4. **テスト可能**: スタンドアロンで実行できる
5. **非破壊的**: デフォルトでは読み取り専用、変更前にバックアップ

## 今後の拡張予定

- [ ] vim設定管理スキル
- [ ] zsh設定管理スキル
- [ ] git設定管理スキル
- [ ] dotfilesの一括検証スキル

## トラブルシューティング

### tmux_config_validator.pyが動作しない場合

1. Python 3が必要です：
   ```bash
   python3 --version
   ```

2. tmuxがインストールされていることを確認：
   ```bash
   tmux -V
   ```

3. ファイルの実行権限を確認：
   ```bash
   chmod +x claude-skills/tmux_config_validator.py
   ```

## ライセンスとクレジット

これらのスキルは個人使用向けに作成されています。
tmux設定管理スキルはClaude Opus 4.1によって開発されました。