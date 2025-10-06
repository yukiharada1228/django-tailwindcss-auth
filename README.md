# Django TailwindCSS Auth プロジェクト

Django 5.2.7とTailwindCSSを使用した認証機能付きWebアプリケーションです。

## 機能

- ユーザー認証（登録・ログイン）
- カスタムユーザーモデル（メールアドレス必須）
- TailwindCSSによるモダンなUI
- 日本語対応

## 必要な環境

- Docker
- Docker Compose v2 以降

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/yukiharada1228/django-tailwindcss-auth.git
cd django-tailwindcss-auth
```

### 2. 環境変数の設定

`.env`ファイルを作成し、以下の設定を行います：

```bash
# 基本設定
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# データベース設定
DATABASE_URL=sqlite:///db.sqlite3

# フロントエンドURL
FRONTEND_URL=http://localhost:8000
```

### 3. コンテナのビルドと起動

```bash
docker compose up --build -d
```

### 4. データベースの初期化

```bash
# マイグレーションを実行
docker compose exec web uv run python manage.py migrate

# スーパーユーザーを作成（オプション）
docker compose exec web uv run python manage.py createsuperuser
```

これで `http://127.0.0.1/`（または `http://localhost/`）でアプリケーションにアクセスできます。

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

## カスタマイズ

### TailwindCSSの設定
`tailwind.config.js`を編集してTailwindCSSの設定をカスタマイズできます。

### スタイルの追加
`static/css/input.css`にTailwindCSSのクラスやカスタムCSSを追加できます。

### テンプレートのカスタマイズ
`templates/`ディレクトリ内のHTMLファイルを編集してUIをカスタマイズできます。

## トラブルシューティング

### よくある問題

1. **CSSが適用されない**
   - 変更を反映するには再ビルドが必要です: `docker compose build --no-cache && docker compose up -d`
   - `docker compose logs web` で `collectstatic` の実行を確認してください

2. **データベースエラー**
   - `docker compose exec web uv run python manage.py migrate` を実行してください

## 貢献

プルリクエストやイシューの報告を歓迎します。
