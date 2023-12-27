import os
import pandas as pd
import requests

# HTTP请求头
HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json;charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'
}

# 每页请求的项目数量
PAGE_SIZE = 30


def get_detail(year, school_id):
    """
    获取给定年份和学校ID的详细信息。

    :param year: (int) 要获取数据的年份。
    :param school_id: (str) 要获取数据的学校ID。

    :return: (list) 包含详细信息的字典列表。
    """
    details = []
    for i in range(1, 11):
        url = f"https://api.zjzw.cn/web/api/?page=1&school_id={school_id}&size=20&uri=apidata/api/gk/score/special&year={year}"
        response = requests.get(url, headers=HEADERS)
        data = response.json()['data']
        details += data['item']

        majors_num = int(data['numFound'])
        if majors_num <= i * 20:
            break
    return details


def get_school_list(province_id="", is_985="", is_211="", is_dual_class=""):
    """
    获取给定省份的学校列表。

    :param province_id: (str) 要获取学校的省份ID。
    :param is_985: (0, 1) 是否为985学校。
    :param is_211: (0, 1) 是否为211学校。
    :param is_dual_class: (0, 1) 是否为双一流学校。

    :return: (list) 包含学校信息的列表。
    """
    schools = []
    for i in range(1, 200):
        url = (f"https://api.zjzw.cn/web/api/?keyword=&is_dual_class={is_dual_class}&f211={is_211}&f985={is_985}"
               f"&page={i}&province_id={province_id}&school_type=&size={PAGE_SIZE}&uri=apidata/api/gkv3/school/lists")
        response = requests.get(url, headers=HEADERS)
        data = response.json()['data']
        schools += [[item['school_id'], str(item['code_enroll']),
                     item['name'], item['province_name'], item['city_name']]
                    for item in data['item']]

        schools_num = int(data['data']['numFound'])
        if i * PAGE_SIZE >= schools_num:
            break
    return schools


def get_progress():
    """
    获取数据抓取的当前进度和已抓取的数据。

    :return: (tuple) 包含当前进度(int)和已抓取的数据(DataFrame)的元组。
    """
    if os.path.exists('./progress.txt'):
        with open('./progress.txt', 'r') as f:
            return int(f.read()), pd.read_csv('./output/result.csv')
    else:
        return 0, pd.DataFrame(
            columns=['年份', '省份', '院校代码', '学校', '专业名称', '最低分', '最低位次', '选科要求', '城市',
                     '录取批次', '网址'])


def save_progress(i, df):
    """
    保存数据抓取的当前进度和抓取的数据。

    :param i: (int) 当前进度。
    :param df: (DataFrame) 抓取的数据。
    """
    with open('./progress.txt', 'w') as f:
        f.write(f'{i}')
    df.to_csv('./output/result.csv', index=False)


# 获取当前进度和已抓取的数据
i, df = get_progress()

# 获取学校列表
lst_sch = get_school_list(province_id="33")[i:]

try:
    # 遍历学校列表
    for sid, scode, sname, province, city in lst_sch:
        school_details = []
        # 获取2023年至2019年的详细信息
        for year in range(2023, 2019, -1):
            details = get_detail(year=year, school_id=sid)
            for item in details:
                school_details.append(
                    [year, province, scode[:-2], sname, item['spname'],
                     item['min'], item['min_section'], item['sp_info'], city,
                     item['local_batch_name'], f'https://www.gaokao.cn/school/{sid}/provinceline'])
        # 将详细信息添加到DataFrame
        df = df.append(pd.DataFrame(school_details, columns=df.columns))
        # 增加进度
        i += 1
finally:
    # 保存进度和抓取的数据
    save_progress(i, df)
