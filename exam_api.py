import requests
import time
from fake_useragent import UserAgent
import logging


class ExamAPI:

    header = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": UserAgent().random,
    }

    def __init__(
        self, base_url="https://api.zjzw.cn/web/api/", page_size=20, delay=0.8
    ):
        """高考数据 API


        Args:
            base_url (str): API 的基础 URL
            page_size (int): 每页请求的项目数量
            delay (float): 请求的延迟时间
        """
        self.base_url = base_url
        self.page_size = page_size
        self.delay = delay

    def get_school_list(self, province_id=0, is_985=0, is_211=0, is_dual_class=0):
        """获取给定省份的学校列表

        Args:
            province_id (int): 要获取学校的省份ID
            is_985 (int): 是否为 985 学校
            is_211 (int): 是否为 211 学校
            is_dual_class (int): 是否为双一流学校

        Returns:
            list: 包含学校信息的列表
        """
        schools = []
        page = 1
        while True:
            time.sleep(self.delay)
            url = (
                f"{self.base_url}?keyword=&is_dual_class={is_dual_class}&f211={is_211}&f985={is_985}"
                f"&page={page}&province_id={province_id}&school_type=&size={self.page_size}&uri=apidata/api/gkv3/school/lists"
            )
            try:
                response = requests.get(url, headers=self.header)
                data = response.json()["data"]
                schools += [
                    [
                        item["school_id"],
                        str(item["code_enroll"]),
                        item["name"],
                        item["province_name"],
                        item["city_name"],
                    ]
                    for item in data["item"]
                ]

                schools_num = int(data["numFound"])
                if page * self.page_size >= schools_num:
                    break
                page += 1
            except Exception as e:
                logging.error(f"读取学校列表失败：{e}")
                time.sleep(15)
        return schools

    def get_score_line_detail(self, year, province_id, school_id):
        """获取给定年份和学校 ID 的详细信息

        Args:
            year (int): 年份
            school_id (int): 学校 ID

        Returns:
            list: 包含详细信息的列表
        """
        details = []
        page = 1
        while True:
            time.sleep(self.delay)
            url = f"{self.base_url}?local_province_id={province_id}&page={page}&school_id={school_id}&size={self.page_size}&uri=apidata/api/gk/score/special&year={year}"
            try:
                response = requests.get(url, headers=self.header)
                data = response.json()["data"]
                details += data["item"]

                num_majors = int(data["numFound"])
                if page * self.page_size >= num_majors:
                    break
                page += 1
            except Exception as e:
                logging.error(f"读取 {year} 年 {school_id} 学校的数据失败：{e}")
                time.sleep(15)

        return details
