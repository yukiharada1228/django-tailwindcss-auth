# Django TailwindCSS Auth プロジェクト

Django 5.2.7とTailwindCSSを使用した認証機能付きWebアプリケーションです。

## 機能

- ユーザー認証（登録、ログイン、アクティベーション）
- カスタムユーザーモデル（メールアドレス必須）
- TailwindCSSによるモダンなUI
- メール送信機能（Mailgun対応）
- 日本語対応

## 必要な環境

- Python 3.12以上
- Node.js（TailwindCSS用）
- uv（Pythonパッケージ管理）

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd django-tailwindcss-auth
```

### 2. Python環境のセットアップ

```bash
# uvを使用して依存関係をインストール
uv sync
```

### 3. 環境変数の設定

`.env`ファイルを作成し、以下の設定を行います：

```bash
# 基本設定
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# データベース設定
DATABASE_URL=sqlite:///db.sqlite3

# メール設定（オプション）
USE_MAILGUN=False
MAILGUN_API_KEY=your_mailgun_api_key_here
MAILGUN_SENDER_DOMAIN=your_domain.mailgun.org

# フロントエンドURL
FRONTEND_URL=http://localhost:8000
```

### 4. データベースの初期化

```bash
# マイグレーションを実行
uv run python manage.py migrate

# スーパーユーザーを作成（オプション）
uv run python manage.py createsuperuser
```

### 5. TailwindCSSのセットアップ

```bash
# Node.jsの依存関係をインストール
npm install

# TailwindCSSをビルド（開発モード）
npm run build
```

## 開発サーバーの起動

### 1. Djangoサーバーの起動

```bash
uv run python manage.py runserver
```

### 2. TailwindCSSの監視（別ターミナル）

```bash
npm run build
```

これで `http://127.0.0.1:8000` でアプリケーションにアクセスできます。

## プロジェクト構造

```
django-tailwindcss-auth/
├── app/                    # メインアプリケーション
│   ├── models.py          # カスタムユーザーモデル
│   ├── views.py           # ビュー
│   ├── forms.py           # フォーム
│   └── urls.py            # URL設定
├── config/                # Django設定
│   ├── settings.py        # 設定ファイル
│   └── urls.py            # メインURL設定
├── templates/             # HTMLテンプレート
│   ├── auth/              # 認証関連テンプレート
│   ├── base.html          # ベーステンプレート
│   └── index.html         # トップページ
├── static/                # 静的ファイル
│   └── css/
│       ├── input.css      # TailwindCSS入力ファイル
│       └── output.css     # ビルドされたCSS
├── pyproject.toml         # Python依存関係
├── package.json           # Node.js依存関係
└── tailwind.config.js     # TailwindCSS設定
```

## 利用可能なページ

- `/` - トップページ
- `/auth/signup/` - ユーザー登録
- `/auth/login/` - ログイン
- `/auth/activate/<token>/` - アカウントアクティベーション
- `/admin/` - 管理画面

## メール設定

### 開発環境
デフォルトでは、メールはコンソールに出力されます。

### 本番環境（Mailgun使用）
`.env`ファイルで以下の設定を行います：

```bash
USE_MAILGUN=True
MAILGUN_API_KEY=your_actual_api_key
MAILGUN_SENDER_DOMAIN=your_domain.mailgun.org
```

## カスタマイズ

### TailwindCSSの設定
`tailwind.config.js`を編集してTailwindCSSの設定をカスタマイズできます。

### スタイルの追加
`static/css/input.css`にTailwindCSSのクラスやカスタムCSSを追加できます。

### テンプレートのカスタマイズ
`templates/`ディレクトリ内のHTMLファイルを編集してUIをカスタマイズできます。

## デプロイ

### 本番環境での設定

1. `DEBUG=False`に設定
2. `SECRET_KEY`を安全な値に変更
3. `ALLOWED_HOSTS`に適切なドメインを設定
4. データベースを本番用に設定
5. 静的ファイルの収集: `uv run python manage.py collectstatic`

## トラブルシューティング

### よくある問題

1. **TailwindCSSが適用されない**
   - `npm run build`を実行してCSSをビルドしてください
   - `static/css/output.css`が存在することを確認してください

2. **メールが送信されない**
   - `.env`ファイルの設定を確認してください
   - 開発環境ではコンソールに出力されます

3. **データベースエラー**
   - `uv run python manage.py migrate`を実行してください

## 貢献

プルリクエストやイシューの報告を歓迎します。
