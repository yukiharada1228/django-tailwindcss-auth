# Django TailwindCSS Multimedia Auth プロジェクト

Django 5.2.7とTailwindCSSを使用した認証機能付きマルチメディア管理Webアプリケーションです。PostgreSQLデータベースとNginxリバースプロキシを使用した本格的な構成になっています。

## 機能

- ユーザー認証（登録・ログイン・アカウントアクティベーション）
- カスタムユーザーモデル（メールアドレス必須）
- メディアファイル管理（音声・動画ファイルのアップロード・管理）
- ファイルの安全な保存と管理
- TailwindCSSによるモダンなUI
- 日本語対応
- PostgreSQLデータベース
- Nginxリバースプロキシ
- Dockerコンテナ化

## 技術スタック

- **バックエンド**: Django 5.2.7
- **フロントエンド**: TailwindCSS 3.4.17
- **データベース**: PostgreSQL 17
- **Webサーバー**: Nginx
- **Python管理**: uv
- **コンテナ**: Docker & Docker Compose
- **メール送信**: Mailgun（本番環境）

## 必要な環境

- Docker
- Docker Compose v2 以降

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/yukiharada1228/django-tailwindcss-multimedia-auth.git
cd django-tailwindcss-multimedia-auth
```

### 2. 環境変数の設定

`.env`ファイルを作成し、以下の設定を行います：

```bash
# 基本設定
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL設定
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-postgres-password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# フロントエンドURL
FRONTEND_URL=http://localhost

# メール設定（本番環境用）
USE_MAILGUN=False
MAILGUN_API_KEY=your-mailgun-api-key
MAILGUN_SENDER_DOMAIN=your-domain.com
DEFAULT_FROM_EMAIL=Django TailwindCSS Multimedia <noreply@your-domain.com>
```

### 3. コンテナのビルドと起動

```bash
docker compose up --build -d
```

初回起動時にマイグレーションと静的ファイル収集（collectstatic）が自動実行されます。

### 4. 管理ユーザーの作成（任意）

```bash
# スーパーユーザーを作成
docker compose exec web uv run python manage.py createsuperuser
```

これで `http://localhost/`（または `http://127.0.0.1/`）でアプリケーションにアクセスできます。

## プロジェクト構造

```
django-tailwindcss-multimedia-auth/
├── app/                    # メインアプリケーション
│   ├── models.py          # カスタムユーザーモデル・メディアファイルモデル
│   ├── views.py           # ビュー
│   ├── forms.py           # フォーム（認証・メディアファイルアップロード）
│   ├── urls.py            # URL設定
│   ├── admin.py           # 管理画面設定
│   └── migrations/        # データベースマイグレーション
├── config/                # Django設定
│   ├── settings.py        # 設定ファイル
│   ├── urls.py            # メインURL設定
│   ├── asgi.py            # ASGI設定
│   └── wsgi.py            # WSGI設定
├── templates/             # HTMLテンプレート
│   ├── auth/              # 認証関連テンプレート
│   │   ├── login.html     # ログインページ
│   │   ├── signup.html    # 登録ページ
│   │   ├── signup_done.html # 登録完了ページ
│   │   └── activate.html  # アクティベーションページ
│   ├── multimedia/        # メディアファイル関連テンプレート
│   │   ├── upload.html    # ファイルアップロードページ
│   │   ├── list.html      # ファイル一覧ページ
│   │   ├── detail.html    # ファイル詳細ページ
│   │   └── delete.html    # ファイル削除ページ
│   ├── base.html          # ベーステンプレート
│   └── index.html         # トップページ
├── static/                # 静的ファイル
│   └── css/
│       ├── input.css      # TailwindCSS入力ファイル
│       └── output.css     # ビルドされたCSS
├── media/                 # メディアファイル
├── docker-compose.yml     # Docker Compose設定
├── Dockerfile             # Dockerイメージ設定
├── nginx.conf             # Nginx設定
├── pyproject.toml         # Python依存関係（uv使用）
├── uv.lock                # 依存関係ロックファイル
├── package.json           # Node.js依存関係
├── package-lock.json      # npm依存関係ロックファイル
├── tailwind.config.js     # TailwindCSS設定
└── main.py                # アプリケーションエントリーポイント
```

## 利用可能なページ

### 認証関連
- `/` - トップページ
- `/accounts/signup/` - ユーザー登録
- `/accounts/login/` - ログイン
- `/accounts/activate/<uidb64>/<token>/` - アカウントアクティベーション

### メディアファイル管理
- `/multimedia/upload/` - ファイルアップロード
- `/multimedia/list/` - ファイル一覧
- `/multimedia/detail/<id>/` - ファイル詳細
- `/multimedia/delete/<id>/` - ファイル削除

### 管理画面
- `/admin/` - 管理画面

## 開発

### ローカル開発環境での実行

Dockerを使用せずにローカルで開発する場合：

```bash
# Python依存関係のインストール
uv sync

# データベースのマイグレーション
uv run python manage.py migrate

# 静的ファイルの収集
uv run python manage.py collectstatic

# 開発サーバーの起動
uv run python manage.py runserver
```

### TailwindCSSのビルド

フロントエンドの変更を反映するには：

```bash
# 一回だけビルド
npm run build

# ファイル監視モード（開発時）
npm run build:watch
```

## カスタマイズ

### TailwindCSSの設定
`tailwind.config.js`を編集してTailwindCSSの設定をカスタマイズできます。

### スタイルの追加
`static/css/input.css`にTailwindCSSのクラスやカスタムCSSを追加できます。

### テンプレートのカスタマイズ
`templates/`ディレクトリ内のHTMLファイルを編集してUIをカスタマイズできます。

### データベースの変更
モデルを変更した後は、マイグレーションを作成・適用してください：

```bash
# マイグレーションファイルの作成
docker compose exec web uv run python manage.py makemigrations

# マイグレーションの適用
docker compose exec web uv run python manage.py migrate
```

### メディアファイルの管理
アップロードされたメディアファイルは以下の機能を提供します：

- **安全なファイル保存**: タイムスタンプベースのファイル名で重複を回避
- **ファイルサイズ制限**: 100MB以下のファイルのみアップロード可能
- **ファイル形式検証**: 音声・動画ファイルの形式を自動検証
- **完全削除**: ファイルとデータベースレコードの両方を安全に削除

#### サポートされるファイル形式
- **音声ファイル**: MP3, WAV, AAC, OGG等
- **動画ファイル**: MP4, AVI, MOV, WMV等

## トラブルシューティング

### よくある問題

1. **CSSが適用されない**
   - 変更を反映するには再ビルドが必要です: `docker compose build --no-cache && docker compose up -d`
   - `docker compose logs web` で `collectstatic` の実行を確認してください

2. **データベースエラー**
   - 起動時にマイグレーションが自動実行されます。失敗した場合は `docker compose logs web` を確認し、必要に応じて `docker compose exec web uv run python manage.py migrate` を実行してください

3. **PostgreSQL接続エラー**
   - `.env`ファイルのPostgreSQL設定を確認してください
   - `docker compose logs postgres` でデータベースのログを確認してください

4. **Nginxエラー**
   - `docker compose logs nginx` でNginxのログを確認してください
   - 静的ファイルのマウントが正しく行われているか確認してください

5. **ポートが既に使用されている**
   - ポート80が既に使用されている場合は、`docker-compose.yml`でポート番号を変更してください

6. **メディアファイルのアップロードエラー**
   - ファイルサイズが100MBを超えている場合は、より小さなファイルを選択してください
   - サポートされていないファイル形式の場合は、音声・動画ファイルを選択してください
   - `docker compose logs web` でアップロードエラーの詳細を確認してください

### ログの確認

```bash
# 全サービスのログ
docker compose logs

# 特定のサービスのログ
docker compose logs web
docker compose logs postgres
docker compose logs nginx

# リアルタイムでログを監視
docker compose logs -f web
```

### コンテナの再起動

```bash
# 全サービスを再起動
docker compose restart

# 特定のサービスを再起動
docker compose restart web

# 全サービスを停止・削除
docker compose down

# ボリュームも含めて完全に削除
docker compose down -v
```

## 本番環境へのデプロイ

本番環境では以下の設定を変更してください：

1. `.env`ファイルで`DEBUG=False`に設定
2. `SECRET_KEY`を強力な値に変更
3. `ALLOWED_HOSTS`に本番ドメインを設定
4. `USE_MAILGUN=True`に設定し、Mailgunの認証情報を設定
5. PostgreSQLのパスワードを強力な値に変更

## 貢献

プルリクエストやイシューの報告を歓迎します。
