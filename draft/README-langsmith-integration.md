# Strands Agents と LangSmith の連携

このドキュメントでは、Strands Agents と LangSmith を連携させる方法について説明します。

## 概要

**はい、Strands Agents と LangSmith を連携させることができます！**

主な連携方法は以下の通りです：

1. **LiteLLM経由での連携** - Strands AgentsのLiteLLMモデルプロバイダーを使用
2. **カスタムコールバックハンドラー** - 詳細なログとトレーシング
3. **環境変数による設定** - LangSmithの自動トレーシング

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements-langsmith.txt
```

### 2. 環境変数の設定

```bash
# LangSmith設定
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
export LANGCHAIN_API_KEY=your-langsmith-api-key
export LANGCHAIN_PROJECT=strands-agents-project

# OpenAI API Key (LiteLLM使用時)
export OPENAI_API_KEY=your-openai-api-key
```

または、`.env`ファイルを作成：

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your-langsmith-api-key
LANGCHAIN_PROJECT=strands-agents-project
OPENAI_API_KEY=your-openai-api-key
```

## 実装例

### 基本的な連携 (`strands-langsmith-integration.py`)

```python
import os
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel

# LangSmith環境変数設定
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-api-key"

# LiteLLMモデルでエージェント作成
litellm_model = LiteLLMModel(
    client_args={"api_key": "your-openai-api-key"},
    model_id="gpt-4o"
)

agent = Agent(model=litellm_model, tools=[...])
```

### 高度な連携 (`strands-langsmith-advanced.py`)

カスタムコールバックハンドラーを使用した詳細なトレーシング：

```python
class LangSmithCallbackHandler:
    def __init__(self):
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.tool_uses = []
        self.conversation_log = []
    
    def __call__(self, **kwargs):
        # ストリーミングデータ、ツール使用、エラーをログ
        if "data" in kwargs:
            # テキストチャンクをログ
        elif "current_tool_use" in kwargs:
            # ツール使用をログ
        elif "error" in kwargs:
            # エラーをログ

agent = Agent(callback_handler=LangSmithCallbackHandler())
```

## 連携の利点

### 1. **自動トレーシング**
- エージェントの会話履歴が自動的にLangSmithに記録
- ツール使用の詳細な追跡
- エラーとパフォーマンスの監視

### 2. **詳細な分析**
- 会話フローの可視化
- ツール使用パターンの分析
- レスポンス時間とコストの追跡

### 3. **デバッグとモニタリング**
- リアルタイムでのエージェント動作監視
- 問題の特定と解決の迅速化
- A/Bテストとパフォーマンス比較

## 対応モデルプロバイダー

### LiteLLM経由で利用可能
- OpenAI (GPT-4, GPT-3.5など)
- Anthropic Claude
- Google PaLM
- Cohere
- その他多数のプロバイダー

### 直接連携
- Amazon Bedrock (デフォルト)
- Anthropic直接
- Ollama (ローカルモデル)

## 実行方法

### 基本版の実行
```bash
python strands-langsmith-integration.py
```

### 高度版の実行
```bash
python strands-langsmith-advanced.py
```

## トラブルシューティング

### よくある問題

1. **API キーエラー**
   - LangSmith API キーが正しく設定されているか確認
   - OpenAI API キー（LiteLLM使用時）が有効か確認

2. **依存関係エラー**
   - `pip install strands-agents[litellm]` を実行
   - `pip install langsmith langchain` を実行

3. **トレーシングが表示されない**
   - `LANGCHAIN_TRACING_V2=true` が設定されているか確認
   - LangSmithプロジェクト名が正しいか確認

## 次のステップ

1. **カスタムメトリクス** - 独自の評価指標を追加
2. **バッチ処理** - 複数の会話を一括でトレース
3. **アラート設定** - 異常検知とアラート機能
4. **ダッシュボード作成** - カスタムダッシュボードでの監視

## 参考リンク

- [Strands Agents Documentation](https://strandsagents.com)
- [LangSmith Documentation](https://docs.smith.langchain.com)
- [LiteLLM Documentation](https://docs.litellm.ai)
