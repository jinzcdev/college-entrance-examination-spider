from .progress import IProgress

import os.path as osp
import pandas as pd


class ExamProgress(IProgress):

    def __init__(
        self, progress_file="./progress.txt", output_file="./output/result.csv"
    ):
        self.progress_file = progress_file
        self.output_file = output_file

    def get_progress(self):
        """获取数据抓取的当前进度（最后被抓取的学校序号）"""
        if osp.exists(self.progress_file):
            with open(self.progress_file, "r") as f:
                return int(f.read())
        return 0

    def save_progress(self, i, df: pd.DataFrame):
        """
        保存数据抓取的当前进度和抓取的数据。

        :param i: (int) 当前进度。
        :param df: (DataFrame) 抓取的数据。
        """
        with open(self.progress_file, "w") as f:
            f.write(f"{i}")
        df.to_csv(self.output_file, index=False, mode="a")
