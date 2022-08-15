
import requests
import csv

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json;charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'
}


def get_detail(year, sid):
    lst = []
    try:
        for i in range(1, 11):
            url = f"https://static-data.gaokao.cn/www/2.0/schoolspecialindex/{year}/{sid}/33/3/16/{i}.json"
            data = requests.request(
                "GET", url, headers=headers, timeout=0.1).json()['data']
            num = int(data['numFound'])
            lst += data['item']
            if num <= i * 10:
                break
    except Exception:
        print('Error:', url)
    return lst


def get_school_list(province_id="", is_985="", is_211="", is_dual_class=""):
    '''
        is_985 in (0, 1)
        is_211 in (0, 1)
        is_dual_class in (0, 1)
    '''
    page_size = 30
    lst_sch = []
    for i in range(1, 200):
        url = f"https://api.eol.cn/web/api/?admissions=&central=&department=&dual_class=&f211={is_211}&f985={is_985}&is_doublehigh=&keyword=&page={i}&ranktype=&request_type=1&school_type=6000&type=&uri=apidata/api/gk/school/lists&is_dual_class=&nature=36000&size={page_size}&province_id={province_id}"
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        num = int(data['data']['numFound'])
        for item in data['data']['item']:
            lst_sch.append([item['school_id'], str(item['code_enroll']), item['name'],
                           item['province_name'], item['city_name'], item['address']])

        if i * 30 >= num:
            break
    return lst_sch


def main():
    save_file = open('./output/result.csv', 'w')
    output = csv.writer(save_file)
    output.writerow(['年份', '省份', '院校代码', '学校', '学科门类', '专业类',
                    '专业名称', '最低分', '最低位次', '选科要求', '城市', '地址' '录取批次', '网址'])
    lst_sch = get_school_list(province_id="33")
    for sid, scode, sname, province, city, address in lst_sch:
        print(sid, scode[:-2], sname, province, city, address)
        for year in range(2021, 2016, -1):
            data = get_detail(year=year, sid=sid)
            for item in data:
                if item['level2'] in ('4', '5'):    # 经济学, 法学
                    tmp = [year, province, scode[:-2], sname, item['level2_name'], item['level3_name'], item['spname'], item['min'], item['min_section'],
                           item['sp_info'], city, address, item['local_batch_name'], f'https://www.gaokao.cn/school/{sid}/provinceline']
                    output.writerow(tmp)

    save_file.close()


if __name__ == '__main__':
    main()

'''
    0: {name: "哲学", code: "01", spe_id: "3"}
    1: {name: "经济学", code: "02", spe_id: "4"}
    2: {name: "法学", code: "03", spe_id: "5"}
    3: {name: "教育学", code: "04", spe_id: "6"}
    4: {name: "文学", code: "05", spe_id: "7"}
    5: {name: "历史学", code: "06", spe_id: "8"}
    6: {name: "理学", code: "07", spe_id: "9"}
    7: {name: "工学", code: "08", spe_id: "10"}
    8: {name: "农学", code: "09", spe_id: "11"}
    9: {name: "医学", code: "10", spe_id: "12"}
    10: {name: "管理学", code: "12", spe_id: "13"}
    11: {name: "艺术学", code: "13", spe_id: "14"}
'''
