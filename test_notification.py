#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE通知の実送信テスト
2026-05-24を「今日」として、明日(2026-05-25=燃やすごみ)の通知をLINEに実際に送る
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_schedule import ScheduleChecker
from line_notifier import LineNotifier

# テスト日付: 2026-05-24を「今日」とする
test_today = datetime.strptime('2026-05-24', '%Y-%m-%d')
tomorrow = test_today + timedelta(days=1)

print("=" * 60)
print("LINE通知 実送信テスト")
print("=" * 60)

# ステップ1: スケジュール確認
print("\n【ステップ1】明日のゴミをチェック...")
_base_dir = os.path.dirname(os.path.abspath(__file__))
_cache_path = os.path.join(_base_dir, 'schedule_cache.json')

checker = ScheduleChecker(_cache_path)
has_garbage, garbage_types = checker.check_date(tomorrow)

print(f"今日: {test_today.strftime('%Y年%m月%d日')}")
print(f"明日: {tomorrow.strftime('%Y年%m月%d日')}")
print(f"ゴミあり: {has_garbage}")
print(f"ゴミ種類: {garbage_types}")

if has_garbage:
    # ステップ2: LINE通知を実際に送信
    print("\n【ステップ2】LINEに実際に送信します...")
    notifier = LineNotifier()
    # test_mode=False で実際に送信
    success = notifier.send_garbage_reminder(garbage_types, test_mode=False)

    if success:
        print("\n✓ 送信成功！スマートフォンのLINEを確認してください")
    else:
        print("\n✗ 送信失敗。上のエラーメッセージを確認してください")
else:
    print("\n✗ 明日はゴミ出し日ではありません（テストデータのエラー）")
