#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ゴミ出し日程チェックモジュール
JSONキャッシュから明日のゴミ出し情報を判定
"""

import json
import sys
from datetime import datetime, timedelta, timezone
from typing import List, Tuple
import os

# UTF-8 encoding対応
if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

# 日本標準時（JST = UTC+9）
# GitHub Actions のサーバーはUTCで動くため、明示的にJSTで日付を計算する
JST = timezone(timedelta(hours=9))


def now_jst() -> datetime:
    """現在の日本時間を返す（実行環境のタイムゾーンに依存しない）"""
    return datetime.now(JST)


class ScheduleChecker:
    """ゴミ出し日程チェッカークラス"""

    def __init__(self, schedule_json_path: str):
        """
        初期化

        Args:
            schedule_json_path: スケジュールJSONファイルのパス
        """
        self.schedule_json_path = schedule_json_path
        self.schedule = self._load_schedule()

    def _load_schedule(self) -> dict:
        """
        JSONキャッシュからスケジュール情報を読み込む

        Returns:
            スケジュール情報の辞書
        """
        if not os.path.exists(self.schedule_json_path):
            raise FileNotFoundError(f"スケジュールファイルが見つかりません: {self.schedule_json_path}")

        with open(self.schedule_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data.get('schedule', {})

    def check_tomorrow(self) -> Tuple[bool, List[str]]:
        """
        明日のゴミ出し情報を確認（日本時間基準）

        Returns:
            (ゴミ出しがあるか, ゴミの種類リスト)
        """
        tomorrow = now_jst() + timedelta(days=1)
        return self.check_date(tomorrow)

    def check_date(self, target_date: datetime) -> Tuple[bool, List[str]]:
        """
        指定日付のゴミ出し情報を確認

        Args:
            target_date: チェック対象日付

        Returns:
            (ゴミ出しがあるか, ゴミの種類リスト)
        """
        garbage_types = []
        target_month = target_date.month
        target_day = target_date.day
        target_weekday = target_date.weekday()  # 0=月, 1=火, ..., 6=日

        # 各ゴミ種別をチェック
        for garbage_name, schedule_data in self.schedule.items():

            # 燃やすごみは日付リスト
            if garbage_name == '燃やすごみ':
                target_date_str = target_date.strftime('%Y-%m-%d')
                if isinstance(schedule_data, list) and target_date_str in schedule_data:
                    garbage_types.append(garbage_name)

            # その他は月別スケジュール
            elif isinstance(schedule_data, dict):
                month_dates = schedule_data.get(str(target_month), [])
                if target_day in month_dates:
                    garbage_types.append(garbage_name)

        has_garbage = len(garbage_types) > 0
        return has_garbage, garbage_types

    def get_notification_messages(self, garbage_types: List[str]) -> List[str]:
        """
        ゴミ種別から通知メッセージを生成

        Args:
            garbage_types: ゴミの種類リスト

        Returns:
            通知メッセージのリスト
        """
        messages = []
        for garbage in garbage_types:
            # 「○○ゴミ」形式の名前を作成
            if garbage == '燃やすごみ':
                messages.append('明日は燃やすゴミの日です')
            elif garbage == '燃やさないごみ':
                messages.append('明日は燃やさないゴミの日です')
            elif garbage == 'かん':
                messages.append('明日は缶の日です')
            elif garbage == 'びん':
                messages.append('明日は瓶の日です')
            elif garbage == '剪定枝・草':
                messages.append('明日は剪定枝・草の日です')
            elif garbage == 'ペットボトル':
                messages.append('明日はペットボトルの日です')
            elif garbage == '紙類':
                messages.append('明日は紙類の日です')
            elif garbage == '蛍光灯・電池':
                messages.append('明日は蛍光灯・電池の日です')
            else:
                messages.append(f'明日は{garbage}の日です')

        return messages


def main(test_date_str: str = None):
    """メイン処理

    Args:
        test_date_str: テスト用の日付文字列 (例: '2026-05-24')
    """

    _base_dir = os.path.dirname(os.path.abspath(__file__))
    schedule_json = os.path.join(_base_dir, 'schedule_cache.json')

    try:
        checker = ScheduleChecker(schedule_json)

        print("="*50)
        print("ゴミ出し日程チェック")
        print("="*50)

        # テスト日付が指定されている場合はそれを使用
        if test_date_str:
            today = datetime.strptime(test_date_str, '%Y-%m-%d')
            tomorrow = today + timedelta(days=1)
            has_garbage, garbage_types = checker.check_date(tomorrow)
        else:
            # 明日のゴミをチェック（日本時間基準）
            today = now_jst()
            tomorrow = today + timedelta(days=1)
            has_garbage, garbage_types = checker.check_tomorrow()

        print(f"\n今日: {today.strftime('%Y年%m月%d日（%A）')}")
        print(f"明日: {tomorrow.strftime('%Y年%m月%d日（%A）')}")

        if has_garbage:
            print(f"\n✓ 明日はゴミ出しがあります")
            print(f"ゴミの種類: {', '.join(garbage_types)}\n")

            messages = checker.get_notification_messages(garbage_types)
            print("通知メッセージ:")
            for msg in messages:
                print(f"  - {msg}")

            return True, messages

        else:
            print("\n✗ 明日はゴミ出し日ではありません")
            return False, []

    except FileNotFoundError as e:
        print(f"エラー: {e}")
        return False, []
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()
        return False, []


if __name__ == '__main__':
    test_date = None
    if len(sys.argv) > 1:
        test_date = sys.argv[1]
        print(f"[テストモード] 日付を指定: {test_date}\n")

    has_garbage, messages = main(test_date)
    sys.exit(0)
