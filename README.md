# ChatGPT風 AIチャットアプリ

## 概要
このアプリはStreamlitとOpenAIのGPT-3.5 Turboを使用しています。ユーザーと対話するチャットボットをWeb上で展開します。

## 使い方

### セットアップ
1. まず、`config.ini` ファイルを作成し、OpenAI APIのキーを以下のように保存します。
    ```ini
    [OpenAI]
    API_KEY=your_openai_api_key_here
    ```
    *ただし、Streamlit Cloudを使用する場合は、この手順は不要です。Streamlit Cloud上でAPIキーを設定してください。*

2. 必要なPythonライブラリをインストールします。
    ```bash
    pip install streamlit openai tiktoken
    ```

### アプリの実行
1. ローカルで実行する場合、ターミナルで以下のコマンドを実行します。
    ```bash
    streamlit run deploy_app.py
    ```
2. Streamlit Cloudで実行する場合、リポジトリをStreamlit Cloudにデプロイします。

### 使用方法
1. アプリが起動すると、チャットボックスが表示されます。
2. チャットボックスに質問またはコメントを入力します。
3. "Enter"を押して送信します。AIが回答を生成して表示します。

## コード説明
- `openai.api_key`はStreamlitのsecretsから取得します。
- `st.session_state`を使用して、ユーザーとAIのメッセージを保管します。
- TikTokenを用いて、APIコールのトークン数を制限しています。
- Streamlitの`st.chat_message`と`st.chat_input`を使用して、チャットインターフェースを生成します。

## デバッグ情報
コンソールには問い合わせ履歴とそのトークン数が出力されます。
