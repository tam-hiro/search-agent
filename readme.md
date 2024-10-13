# 前提条件
1. VSCodeを利用しています。
2. AnthropicとTabilyのAPIが必要です。  

# 環境構築手順
1. 以下のコマンドを実行し仮想環境を用意する（ワークスペースを構築した環境に設定）  
・実行後のフォルダ構成　/search-agent/venv
```shell
python3 -m venv venv 
```
2. 仮想環境をアクティブ化する（Macの場合）
```shell
source venv/bin/activate　# Windows use venv\Scripts\activate
```
3. 必要なパッケージをインストールする
```shell
pip install -r requirements.txt
```
4. 環境変数を設定する（template.env）  
・ファイル名を”.env”に変更する  
・必要なAPIを設定する
```shell
ANTHROPIC_API_KEY = your_api_key
TAVILY_API_KEY = your_api_key
```
5. アプリケーションの実行
```shell
flask run
```
