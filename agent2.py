import os
import sys
import argparse
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
from strands_tools import current_time, python_repl

load_dotenv()

@tool
def letter_counter(word: str, letter: str) -> int:
    return word.lower().count(letter.lower())

def get_query_input():
    parser = argparse.ArgumentParser(description='データモデル設計エージェント')
    parser.add_argument('--query', '-q', type=str, help='分析対象のユーザー入力テキスト')
    parser.add_argument('--file', '-f', type=str, help='ユーザー入力を含むファイルのパス')
    
    args = parser.parse_args()
    
    if args.query:
        return args.query
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"エラー: ファイル {args.file} が見つかりません")
            sys.exit(1)
        except Exception as e:
            print(f"エラー: ファイル読み込み中にエラーが発生しました: {e}")
            sys.exit(1)
    else:
        print("エラー: --query または --file のいずれかを指定してください")
        print("使用例:")
        print("  python agent2.py --query 'ECサイトの注文管理システム'")
        print("  python agent2.py --file input.txt")
        sys.exit(1)

litellm_model = LiteLLMModel(
    client_args={
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
    model_id="gpt-4o",
    params={
        "temperature": 0.7,
    }
)

agent = Agent(model=litellm_model, tools=[current_time, python_repl, letter_counter])

query = get_query_input()

message = f"""
ユーザーの入力を分析し、以下の手順でデータモデルを設計してください。

手順:
1. エンティティを抽出する。(提示されたユースケースの名詞、動詞に着目)
2. 洗い出したエンティティを[リソース]と[イベント]に分類する。イベントに分類する基準は属性に"日時・日付（イベントが実行された日時・日付）"を持つものである。
3. イベントエンティティには1つの日時属性しかもたないようにする。
4. リソースに隠されたイベントを抽出する。（リソースに更新日時をもちたい場合にはイベントが隠されている可能性がある）
  例）社員情報（リソース）の更新日時がある場合には、社員異動（イベントエンティティ）を抽出する。
5. エンティティ間の依存度が強すぎる場合には、交差エンティティ（関連エンティティ）を導入する。（カーディナリティが多対多の関係を持つような場合に導入する）
6. 最終的にデータモデルをMermaid記法で出力する。

ユーザーの入力: {query}
"""

agent(message)
