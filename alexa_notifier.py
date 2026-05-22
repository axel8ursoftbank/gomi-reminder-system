#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alexa通知モジュール
Amazon Notifications APIを使用してAlexa画面に通知を送信
"""

import requests
import json
import sys
import os
from typing import Optional
from datetime import datetime

# UTF-8 encoding対応
if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)


class AlexaNotifier:
    """Alexa通知送信クラス"""

    # Amazon Notifications API エンドポイント
    API_ENDPOINT = "https://api.amazonalexa.com/v1/notifications/reminder-notifications"

    def __init__(self, config_file: str = None):
        """
        初期化

        Args:
            config_file: 設定ファイルのパス（含む: device_id, refresh_token）
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
                "config.jsonの作成方法については、setup_alexa.mdを参照してください"
            )

        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_access_token(self) -> str:
        """
        Refresh TokenからAccess Tokenを取得

        Returns:
            Access Token
        """
        refresh_token = self.config.get('refresh_token')
        if not refresh_token:
            raise ValueError("Refresh TokenがConfig.jsonに設定されていません")

        token_url = "https://api.amazon.com/auth/o2/token"

        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.config.get('client_id'),
            'client_secret': self.config.get('client_secret'),
        }

        try:
            response = requests.post(token_url, data=payload)
            response.raise_for_status()
            return response.json()['access_token']

        except requests.exceptions.RequestException as e:
            raise Exception(f"Access Token取得エラー: {e}")

    def send_notification(self, message: str, test_mode: bool = False) -> bool:
        """
        Alexa画面に通知を送信

        Args:
            message: 送信するメッセージ
            test_mode: テストモード（実際のAPI送信はしない）

        Returns:
            成功したかどうか
        """
        device_id = self.config.get('device_id')
        if not device_id:
            raise ValueError("Device IDがConfig.jsonに設定されていません")

        if test_mode:
            print(f"[テストモード] Alexa通知送信")
            print(f"  Device ID: {device_id}")
            print(f"  Message: {message}")
            return True

        try:
            # Access Token取得
            access_token = self._get_access_token()

            # 通知リクエスト作成
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            }

            payload = {
                'notification': {
                    'targetDeviceId': device_id,
                    'alexaText': message,
                    'initiationTimestamp': datetime.now().isoformat() + 'Z',
                }
            }

            # API送信
            response = requests.post(
                self.API_ENDPOINT,
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                print(f"✓ Alexa通知送信完了: {message}")
                return True
            else:
                print(f"✗ Alexa通知送信失敗 (Status: {response.status_code})")
                print(f"  Response: {response.text}")
                return False

        except Exception as e:
            print(f"✗ エラー: {e}")
            return False

    def send_garbage_reminder(self, garbage_types: list, test_mode: bool = False) -> bool:
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

        return self.send_notification(message, test_mode=test_mode)


def main():
    """メイン処理"""

    try:
        notifier = AlexaNotifier()

        print("="*50)
        print("Alexa通知テスト")
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
        print("  1. setup_alexa.md を参照")
        print("  2. Amazon Developer Consoleで認証情報を取得")
        print("  3. config.json を以下の形式で作成:")
        print("""
{
    "device_id": "YOUR_DEVICE_ID",
    "refresh_token": "YOUR_REFRESH_TOKEN",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
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
