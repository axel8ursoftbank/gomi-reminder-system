#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE Messaging API を使用したゴミ出し通知モジュール
"""

import requests
import json
import sys
import os
from typing import List
import logging

# UTF-8 encoding対応
if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

# ロギング設定
logger = logging.getLogger(__name__)


class LineNotifier:
    """LINE Messaging API 通知クラス"""

    LINE_API_ENDPOINT = "https://api.line.me/v2/bot/message/push"

    def __init__(self, config_file: str = None):
        """
        初期化

        Args:
            config_file: 設定ファイルのパス
        """
        _base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = config_file or os.path.join(_base_dir, 'config.json')
        self.config = self._load_config()

    @staticmethod
    def _normalize_user_ids(raw) -> list:
        """
        さまざまな形式のユーザーID入力を、クリーンなリストに正規化する

        対応形式:
          - JSON配列:        ["U123", "U456"]
          - JSON文字列:      "U123"
          - 素の文字列:      U123
          - カンマ区切り:    U123,U456
          - すでにリスト:    ["U123"]

        Returns:
            ユーザーIDのリスト（前後の空白・引用符を除去済み）
        """
        # すでにリストならそのまま使う
        if isinstance(raw, list):
            candidates = raw
        elif isinstance(raw, str):
            text = raw.strip()
            parsed = None
            try:
                parsed = json.loads(text)
            except (json.JSONDecodeError, ValueError):
                parsed = None

            if isinstance(parsed, list):
                candidates = parsed
            elif isinstance(parsed, str):
                # JSON文字列リテラル "U123" -> 単一要素
                candidates = [parsed]
            else:
                # 素の文字列。カンマ区切りの可能性も考慮
                candidates = text.split(',')
        else:
            candidates = [raw]

        # 各要素を文字列化し、前後の空白・引用符・括弧を除去
        cleaned = []
        for item in candidates:
            s = str(item).strip().strip('"').strip("'").strip()
            if s:
                cleaned.append(s)

        # LINEのユーザーIDは 'U' で始まる。妥当そうなものだけ残す
        valid = [s for s in cleaned if s.startswith('U') and len(s) > 10]

        if not valid and cleaned:
            # 検証で全部はじかれた場合は警告を出しつつ元の値を返す
            logger.warning(
                f"ユーザーIDの形式が不正な可能性があります: {cleaned}. "
                "LINEのユーザーIDは 'U' から始まる33文字程度の文字列です"
            )
            return cleaned

        return valid

    def _load_config(self) -> dict:
        """
        設定ファイルまたは環境変数から認証情報を読み込む
        GitHub Actions では環境変数から読み込む

        Returns:
            設定情報の辞書
        """
        # 環境変数から読み込む（GitHub Actions用）
        env_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
        env_user_ids = os.environ.get('LINE_USER_IDS')

        if env_token:
            logger.info("環境変数から設定を読み込みました（GitHub Actions モード）")
            config = {'line_channel_access_token': env_token.strip()}

            if env_user_ids:
                user_ids = self._normalize_user_ids(env_user_ids)
                config['line_user_ids'] = user_ids
                logger.info(f"LINE_USER_IDS: {len(user_ids)}人 -> {user_ids}")

            return config

        # 環境変数がなければ config.json から読み込む（ローカル実行用）
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(
                f"設定ファイルが見つかりません: {self.config_file}\n"
                "config.json を作成してください"
            )

        with open(self.config_file, 'r', encoding='utf-8') as f:
            logger.info(f"config.json から設定を読み込みました")
            return json.load(f)

    def send_message(self, message: str, test_mode: bool = False) -> bool:
        """
        LINE にメッセージを送信（複数ユーザー対応）

        Args:
            message: 送信するメッセージ
            test_mode: テストモード（実際の送信はしない）

        Returns:
            成功したかどうか
        """
        channel_access_token = self.config.get('line_channel_access_token')

        # 複数ユーザー（line_user_ids）と単数ユーザー（line_user_id）の両方に対応
        raw_user_ids = self.config.get('line_user_ids') or self.config.get('line_user_id')

        # 文字列が1文字ずつバラバラに送られるバグを防ぐため、必ず正規化する
        user_ids = self._normalize_user_ids(raw_user_ids) if raw_user_ids else []

        if not channel_access_token:
            raise ValueError("line_channel_access_token が設定されていません")

        if not user_ids:
            raise ValueError(
                "有効な line_user_ids が設定されていません。"
                "'U' から始まるLINEユーザーIDを設定してください"
            )

        if test_mode:
            print(f"[テストモード] LINE通知送信")
            print(f"  送信先ユーザー数: {len(user_ids)}")
            print(f"  メッセージ: {message}")
            return True

        try:
            headers = {
                "Authorization": f"Bearer {channel_access_token}",
                "Content-Type": "application/json"
            }

            # 各ユーザーに送信
            all_success = True
            for user_id in user_ids:
                payload = {
                    "to": user_id,
                    "messages": [
                        {
                            "type": "text",
                            "text": message
                        }
                    ]
                }

                response = requests.post(
                    self.LINE_API_ENDPOINT,
                    headers=headers,
                    json=payload
                )

                if response.status_code == 200:
                    print(f"✓ LINE通知送信完了 ({user_id}): {message}")
                    logger.info(f"LINE通知送信完了 ({user_id}): {message}")
                else:
                    print(f"✗ LINE通知送信失敗 ({user_id}, Status: {response.status_code})")
                    print(f"  Response: {response.text}")
                    logger.error(f"LINE通知送信失敗 ({user_id}): {response.text}")
                    all_success = False

            return all_success

        except Exception as e:
            print(f"✗ エラー: {e}")
            logger.error(f"LINE通知エラー: {e}")
            return False

    def send_garbage_reminder(self, garbage_types: List[str], test_mode: bool = False) -> bool:
        """
        ゴミ出し通知を送信

        Args:
            garbage_types: ゴミの種類リスト
            test_mode: テストモード

        Returns:
            成功したかどうか
        """
        if not garbage_types:
            logger.info("通知対象のゴミがありません")
            print("通知対象のゴミがありません")
            return False

        # メッセージを組み立て
        if len(garbage_types) == 1:
            message = f"明日は{garbage_types[0]}の日です"
        else:
            types_str = "、".join(garbage_types)
            message = f"明日は{types_str}の日です"

        return self.send_message(message, test_mode=test_mode)


def main():
    """メイン処理（テスト用）"""

    try:
        notifier = LineNotifier()

        print("="*50)
        print("LINE通知テスト")
        print("="*50)

        # テスト通知送信
        garbage_types = ['燃やすごみ', '缶']
        success = notifier.send_garbage_reminder(garbage_types, test_mode=True)

        if success:
            print("\n✓ 通知送信テスト成功")
            return True
        else:
            print("\n✗ 通知送信テスト失敗")
            return False

    except FileNotFoundError as e:
        print(f"\n設定エラー: {e}")
        print("\n設定ファイルを作成するには:")
        print("  1. LINE_MESSAGING_API_SETUP.md を参照")
        print("  2. Channel Access Token と User ID を取得")
        print("  3. config.json を以下の形式で作成:")
        print("""
{
    "notification_type": "line",
    "line_channel_access_token": "YOUR_CHANNEL_ACCESS_TOKEN",
    "line_user_id": "YOUR_USER_ID"
}
""")
        return False

    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
