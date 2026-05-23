#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ゴミ出し日程LINE通知システム メインスケジューラー
APSchedulerを使用して毎日18:00に1回実行
LINE Messaging API で LINE に通知送信
"""

import sys
import os
from datetime import datetime, timedelta
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time

# UTF-8 encoding対応
if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

# モジュールのインポート
from check_schedule import ScheduleChecker
from line_notifier import LineNotifier

# ロギング設定（スクリプトがあるフォルダにログを保存）
_script_dir = os.path.dirname(os.path.abspath(__file__))
_log_file = os.path.join(_script_dir, 'gomi_reminder.log')

_handlers = [logging.StreamHandler()]
try:
    _handlers.append(logging.FileHandler(_log_file, encoding='utf-8'))
except Exception:
    pass  # GitHub Actions などでファイル書き込みできない場合はスキップ

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=_handlers
)
logger = logging.getLogger(__name__)


class GomiReminderScheduler:
    """ゴミ出し日程Alexa通知スケジューラー"""

    def __init__(self, config_mode='real'):
        """
        初期化

        Args:
            config_mode: 'real' (実通知) または 'test' (テストモード)
        """
        self.config_mode = config_mode
        self.scheduler = BackgroundScheduler()

        # チェッカー初期化
        _base_dir = os.path.dirname(os.path.abspath(__file__))
        _cache_path = os.path.join(_base_dir, 'schedule_cache.json')
        try:
            self.schedule_checker = ScheduleChecker(_cache_path)
        except Exception as e:
            logger.error(f"スケジュールチェッカー初期化エラー: {e}")
            self.schedule_checker = None

        # LINE通知送信者初期化
        try:
            self.line_notifier = LineNotifier()
        except Exception as e:
            logger.warning(f"LINE通知初期化: {e}")
            self.line_notifier = None

    def check_and_notify(self):
        """
        スケジュール確認と通知実行
        """
        try:
            if not self.schedule_checker:
                logger.warning("スケジュールチェッカーが初期化されていません")
                return

            # 明日のゴミをチェック
            has_garbage, garbage_types = self.schedule_checker.check_tomorrow()

            if has_garbage:
                logger.info(f"明日のゴミ: {', '.join(garbage_types)}")

                if self.line_notifier:
                    # テストモードかどうか判定
                    test_mode = (self.config_mode == 'test')

                    # LINE通知送信
                    self.line_notifier.send_garbage_reminder(
                        garbage_types,
                        test_mode=test_mode
                    )
                else:
                    logger.warning("LINE通知が利用できません")

            else:
                logger.debug("明日はゴミ出し日ではありません")

        except Exception as e:
            logger.error(f"スケジュール確認エラー: {e}")
            import traceback
            traceback.print_exc()

    def start(self):
        """
        スケジューラーを開始
        """
        logger.info(f"="*60)
        logger.info("ゴミ出し日程LINE通知システムを起動")
        logger.info(f"モード: {self.config_mode}")
        logger.info(f"="*60)

        # ジョブスケジュール設定
        # 毎日18:00に1回実行
        self.scheduler.add_job(
            self.check_and_notify,
            trigger=CronTrigger(hour=18, minute=0),
            id='gomi_check_18:00',
            name='ゴミ日程チェック (18:00)',
            replace_existing=True
        )
        logger.info("ジョブ登録: 毎日 18:00 にチェック実行")

        # スケジューラー開始
        try:
            self.scheduler.start()
            logger.info("スケジューラーが開始されました")

            # 無限ループで実行継続
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            logger.info("キーボード割り込みで停止します")
            self.scheduler.shutdown()
            sys.exit(0)

        except Exception as e:
            logger.error(f"スケジューラーエラー: {e}")
            import traceback
            traceback.print_exc()
            self.scheduler.shutdown()
            sys.exit(1)

    def run_once(self):
        """
        1回だけ実行（テスト用）
        """
        logger.info("1回のテスト実行を開始")
        self.check_and_notify()
        logger.info("テスト実行完了")


def main():
    """メイン処理"""

    import argparse

    parser = argparse.ArgumentParser(
        description='ゴミ出し日程Alexa通知システム'
    )
    parser.add_argument(
        '--mode',
        choices=['real', 'test'],
        default='test',
        help='実行モード（real=実通知、test=テスト）'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='1回だけ実行してから終了'
    )

    args = parser.parse_args()

    print(f"{"="*60}")
    print(f"ゴミ出し日程Alexa通知システム")
    print(f"{"="*60}")
    print(f"実行モード: {args.mode}")
    print(f"テスト実行: {args.once}")
    print(f"{"="*60}\n")

    # スケジューラー作成と実行
    scheduler = GomiReminderScheduler(config_mode=args.mode)

    if args.once:
        scheduler.run_once()
    else:
        scheduler.start()


if __name__ == '__main__':
    main()
