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
        self.config_file = config_file or r"C:\Users\user\gomi_reminder_system\config.json"
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """
        設定ファイルから認証情報を読み込む

        Returns:
            設定情報の辞書
        """
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(
                f"設定ファイルが見つかりません: {self.config_file}\n"
                "config.json を作成してください"
            )

        with open(self.config_file, 'r', encoding='utf-8') as f:
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
        user_ids = self.config.get('line_user_ids') or [self.config.get('line_user_id')]

        if not channel_access_token:
            raise ValueError("line_channel_access_token が config.json に設定されていません")

        if not user_ids or all(uid is None for uid in user_ids):
            raise ValueError("line_user_ids または line_user_id が config.json に設定されていません")

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
