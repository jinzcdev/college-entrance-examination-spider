import pandas as pd
from exam_api import ExamAPI
from utils import ExamProgress, build_logger
import logging


def main():

    exam_api = ExamAPI()
    exam_progress = ExamProgress(
        progress_file="./progress.txt", output_file="./output/zj.csv"
    )
    logger = build_logger("Exam", "./logs/exam_api.log")

    province_id = 33

    # 获取当前进度和已抓取的数据
    # sch_idx = exam_progress.get_progress()
    sch_idx = 1

    # 获取学校列表
    lst_sch = exam_api.get_school_list(province_id=province_id)

    logger.info(
        f"\n获取到 {len(lst_sch)} 所学校\n"
        + "\n".join([f"{i+1}. {sch[2]}" for i, sch in enumerate(lst_sch)])
        + "\n"
    )

    columns = [
        "年份",
        "省份",
        "院校代码",
        "学校",
        "专业名称",
        "最低分",
        "最低位次",
        "选科要求",
        "城市",
        "录取批次",
        "网址",
    ]

    df = pd.DataFrame(columns=columns)
    try:
        # 遍历学校列表
        for sid, scode, sname, province, city in lst_sch:
            school_details = []
            # 获取2023年至2019年的详细信息
            for year in range(2023, 2019, -1):
                logger.info(f"正在获取 {sname} {year} 年的详细信息")
                details = exam_api.get_score_line_detail(
                    year=year, school_id=sid, province_id=province_id
                )
                for item in details:
                    school_details.append(
                        [
                            year,
                            province,
                            scode[:-2],
                            sname,
                            item["spname"],
                            item["min"],
                            item["min_section"],
                            item["sp_info"],
                            city,
                            item["local_batch_name"],
                            f"https://www.gaokao.cn/school/{sid}/provinceline",
                        ]
                    )
            # 将详细信息添加到DataFrame
            df = pd.concat([df, pd.DataFrame(school_details, columns=df.columns)])
            # 增加进度
            sch_idx += 1
    finally:
        # 保存进度和抓取的数据
        exam_progress.save_progress(sch_idx, df)


if __name__ == "__main__":
    main()
