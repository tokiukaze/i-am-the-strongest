# AWS Lambdaプロジェクト開発環境構築　サンプルプロジェクト

```text
.
├── .devcontainer        # Dev Containerの設定ファイルなど
├── .vscode              # vscodeの設定ファイル
├── README.md
├── app.py
├── cdk.json
├── doc
├── i_am_the_strongest   # CDKを使用してサービスを定義するスクリプト
├── poetry.lock
├── pyproject.toml
├── strongest_function   # Lambdaに配置するスクリプト
└── tests                # Lambdaスクリプトのユニットテスト
```

## 開発環境のセットアップ

- [Developing inside a Container using Visual Studio Code Remote Development](https://code.visualstudio.com/docs/remote/containers)
- [Get started with development Containers in Visual Studio Code](https://code.visualstudio.com/docs/remote/containers-tutorial#_install-the-extension)

[Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)を使用して、開発環境を構築します。

1. このプロジェクトを vscode を使用して開きます。
2. vscode 拡張機能の[Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)と[Docker](https://www.docker.com/)をインストールします。
3. vscode にて`ctrl + shift + p`(windows)または`cmd + shift + p`(mac)を押しコマンド`Remote-Containers : Reopen in Container`を選択します。

コンテナ初回起動時には下記の設定を行う必要があります。

### [aws のセットアップ](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/getting-started-quickstart.html)

aws アカウントを設定しておく。

```bash
aws configure

> AWS Access Key ID [None]: <入力>
> AWS Secret Access Key [None]: <入力>
> Default region name [None]: ap-northeast-1
> Default output format [None]: json
```

## 使用する aws ツール

このプロジェクトでは、下記ツールの操作が必要になることがあります。これらのツールは Docker 開発環境に含まれます。

- [aws-cli](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-chap-welcome.html)
- [sam-cli](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-getting-started.html)
- [cdk-cli](https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/cli.html)

### cdk デプロイ方法

cdkを使用し、プロジェクトをawsにデプロイする方法です。

### pythonパッケージの追加

もしpythonパッケージを追加する場合は、デプロイの前に python パッケージを`/strongest_function/requirements.txt`に書き出しておく必要があります。

1. パッケージのインストール

`requests`を追加する場合

```bash
poetry add requests
```

2. パッケージの書き出し

```bash
poetry export --output ./strongest_function/requirements.txt
```

### cdkの操作

[cdk コマンド一覧](https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/cli.html)

1. スタックのビルド

```bash
cdk synthesize
```

2. スタックのデプロイ**

```bash
cdk deploy
```

## [sam を使用したローカルでのテスト](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-cdk-testing.html)

ローカル環境にてAPIをテストすることができます。

1. サービスの起動

```bash
cdk synth
sam local start-api -t ./cdk.out/IAmTheStrongestStack.template.json
```

2. ローカルテスト

WEB APIにアクセスしてみます。
ターミナルをもう一つ開き、下記のコマンドを実行します。

```bash
curl http://127.0.0.1:3000/status | jq
```

しばらくすると環境が作成され、下記の返答が表示されます。

```JSON
{
  "status": "ok"
}
```

`ctrl + c`でサービスは停止します。

## ユニットテスト

ターミナルでは、下記で実行できる。
`/workspaces/aws-strongest-development-environment/tests/unit/test_i_am_the_strongest_stack.py`のテストが実行される。

```
pytest
```