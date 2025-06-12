# CLAUDE.md

このファイルは、このリポジトリでコードを扱う際のClaude Code (claude.ai/code) への指示を提供します。

## プロジェクト概要

このプロジェクトは、LangSmith統合を伴うStrands Agentsフレームワークを探索するための研究プロジェクトです。ツールを使用し、LangSmithトレーシングを通じて監視できるAIエージェントの構築を実演します。

## 開発コマンド

### メインエージェントの実行
```bash
uv run python agent.py
```

### LangSmith統合例の実行
```bash
uv run python strands-langsmith-integration.py
uv run python strands-langsmith-advanced.py
```

### パッケージ管理
このプロジェクトでは、Pythonパッケージ管理に`uv`を使用します：
```bash
uv sync  # 依存関係をインストール
uv add <package>  # 新しい依存関係を追加
```

## アーキテクチャ

### コアコンポーネント

- **agent.py**: カスタムツールを使用した基本的なStrands Agent実装
- **strands-langsmith-integration.py**: LiteLLMModelを使用したLangSmithトレーシング統合のデモンストレーション
- **strands-langsmith-advanced.py**: 詳細なロギングと監視のためのカスタムコールバックハンドラーを使用した高度なLangSmith統合

### ツールシステム

このプロジェクトはStrands Agentsツールシステムを使用します：
- カスタムツールは`@tool`デコレータを使用して定義されます
- `strands_tools`からの組み込みツール（current_time、python_repl）
- カスタムツールの例：単語内の文字数をカウントする`letter_counter`

### LangSmith統合パターン(draftディレクトリに格納)

LangSmithトレーシングの場合：
1. 環境変数を設定：`LANGCHAIN_TRACING_V2`、`LANGCHAIN_ENDPOINT`、`LANGCHAIN_API_KEY`、`LANGCHAIN_PROJECT`
2. 適切なクライアント設定で`LiteLLMModel`を使用
3. 高度な監視の場合、ツール使用、会話フロー、エラーを捕捉するカスタムコールバックハンドラーを実装

### 状態管理

- エージェント状態はREPLセッション中に`repl_state/repl_state.pkl`に永続化されます
- 高度な例のコールバックハンドラーは、セッションデータとツール使用統計を追跡します

## 依存関係

コアフレームワーク：`strands-agents`、`strands-agents-builder`、`strands-agents-tools`
LangSmith統合用：`requirements-langsmith.txt`で定義された追加の依存関係
