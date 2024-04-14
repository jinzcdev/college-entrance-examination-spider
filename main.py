import pandas as pd
from exam_api import ExamAPI
from utils import ExamProgress, get_logger

def fetch_score_line(
    province_id=33, date_range=(2020, 2023), output_file=None, progress_file=None
):
    """获取全国各学校对特定省份的特定年份的录取分数线

    Args:
        province_id (int, optional): 省份 ID，默认为 33
        date_range (tuple, optional): 年份范围，默认为 (2020, 2023)
        output_file (str, optional): 输出文件路径，默认为 None
        progress_file (str, optional): 进度文件路径，默认为 None
    """

    if output_file is None:
        output_file = f"./data/score_line_{province_id}.csv"
    if progress_file is None:
        progress_file = f"./progress/score_line_{province_id}.txt"

    exam_api = ExamAPI(delay=1.2)
    exam_progress = ExamProgress(progress_file=progress_file, output_file=output_file)

    logger = get_logger(
        logger_name="ExamScore", log_file=f"./logs/score_line_{province_id}.log"
    )

    # 获取当前进度和已抓取的数据
    start_idx = exam_progress.get_progress()

    # 获取全国学校列表，省份 ID 为 0
    lst_sch = exam_api.get_school_list()[start_idx:]

    if start_idx != 0:
        logger.warn(f"断点续传，从第 {start_idx} 所学校开始（从 0 开始计数）")
    else:
        logger.info(
            f"\n获取到 {len(lst_sch)} 所学校\n"
            + "\n".join([f"{i+1}. {sch[0]} {sch[2]}" for i, sch in enumerate(lst_sch)])
            + "\n"
        )

    idx = start_idx

    columns = [
        "年份",
        "省份",
        "院校代码",
        "学校",
        "专业名称",
        "最低分",
        "最低位次",
        "选科要求",
        "录取批次",
        "隶属",
        "办学层次",
        "办学类型",
        "学校性质",
        "是否双一流",
        "是否 985",
        "是否 211",
        "城市",
        "网址",
    ]

    start_year, end_year = date_range

    df = pd.DataFrame(columns=columns)

    try:
        # 遍历学校列表
        for i, (
            sid,
            scode,
            sname,
            province,
            city,
            belong,
            level,
            sch_type,
            nature,
            is_dual_class,
            is_985,
            is_211,
        ) in enumerate(lst_sch):
            school_details = []
            for year in range(end_year, start_year - 1, -1):
                details = exam_api.get_score_line_detail(
                    year=year, school_id=sid, province_id=province_id
                )
                logger.info(
                    f"{start_idx + i}. 正在获取 {sname} {year} 年的详细信息，共 {len(details)} 个专业"
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
                            item["local_batch_name"],
                            belong,
                            level,
                            sch_type,
                            nature,
                            is_dual_class,
                            is_985,
                            is_211,
                            city,
                            f"https://www.gaokao.cn/school/{sid}/provinceline",
                        ]
                    )
            # 将详细信息添加到 DataFrame
            df = pd.concat([df, pd.DataFrame(school_details, columns=df.columns)])
            # 增加进度
            idx += 1
    finally:
        # 保存进度和抓取的数据
        exam_progress.save_progress(idx, df)


def fetch_enrollment(
    province_id=33, date_range=(2020, 2023), output_file=None, progress_file=None
):
    """获取全国各学校对特定省份的特定年份的招生计划

    Args:
        province_id (int, optional): 省份 ID，默认为 33
        date_range (tuple, optional): 年份范围，默认为 (2020, 2023)
        output_file (str, optional): 输出文件路径，默认为 None
        progress_file (str, optional): 进度文件路径，默认为 None
    """

    if output_file is None:
        output_file = f"./data/enrollment_{province_id}.csv"
    if progress_file is None:
        progress_file = f"./progress/enrollment_{province_id}.txt"

    exam_api = ExamAPI(delay=1.3)
    exam_progress = ExamProgress(progress_file=progress_file, output_file=output_file)

    logger = get_logger(
        logger_name="ExamEnrollment",
        log_file=f"./logs/enrollment_{province_id}.log",
    )

    # 获取当前进度和已抓取的数据
    start_idx = exam_progress.get_progress()

    # 获取全国学校列表，省份 ID 为 0
    lst_sch = exam_api.get_school_list()[start_idx:]

    if start_idx != 0:
        logger.warn(f"断点续传，从第 {start_idx} 所学校开始（从 0 开始计数）")
    else:
        logger.info(
            f"\n获取到 {len(lst_sch)} 所学校\n"
            + "\n".join([f"{i+1}. {sch[0]} {sch[2]}" for i, sch in enumerate(lst_sch)])
            + "\n"
        )

    idx = start_idx

    columns = [
        "年份",
        "省份",
        "院校代码",
        "学校",
        "学科门类",
        "专业名称",
        "计划招生",
        "学制",
        "学费(年)",
        "选科要求",
        "录取批次",
        "隶属",
        "办学层次",
        "办学类型",
        "学校性质",
        "是否双一流",
        "是否 985",
        "是否 211",
        "城市",
        "网址",
    ]

    start_year, end_year = date_range

    df = pd.DataFrame(columns=columns)
    try:
        # 遍历学校列表
        for i, (
            sid,
            scode,
            sname,
            province,
            city,
            belong,
            level,
            sch_type,
            nature,
            is_dual_class,
            is_985,
            is_211,
        ) in enumerate(lst_sch):
            school_details = []
            for year in range(end_year, start_year - 1, -1):
                details = exam_api.get_enrollment_plan(
                    year=year, school_id=sid, province_id=province_id
                )
                logger.info(
                    f"{start_idx + i}. 正在获取 {sname} {year} 年的详细信息，共 {len(details)} 个专业"
                )
                for item in details:
                    school_details.append(
                        [
                            year,
                            province,
                            scode[:5],
                            sname,
                            item["level2_name"],
                            item["spname"],
                            item["num"],
                            item["length"],
                            item["tuition"],
                            item["sp_info"],
                            item["local_batch_name"],
                            belong,
                            level,
                            sch_type,
                            nature,
                            is_dual_class,
                            is_985,
                            is_211,
                            city,
                            f"https://www.gaokao.cn/school/{sid}/provinceline",
                        ]
                    )
            # 将详细信息添加到 DataFrame
            df = pd.concat([df, pd.DataFrame(school_details, columns=df.columns)])
            # 增加进度
            idx += 1
    finally:
        # 保存进度和抓取的数据
        exam_progress.save_progress(idx, df)


if __name__ == "__main__":
    fetch_score_line(province_id=33, date_range=(2017, 2019))
    # fetch_enrollment(province_id=33, date_range=(2020, 2023))
