import requests
import csv

from fake_useragent import UserAgent


headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'User-Agent': UserAgent().random
}

# school_type=6000: benke; nature=36000 gongban

with open('./output/school_all.csv', 'w') as f:
    output = csv.writer(f)

    for i in range(1, 200):
        url = f"https://api.eol.cn/web/api/?admissions=&central=&department=&dual_class=&f211=&f985=&is_doublehigh=&keyword=&page={i}&ranktype=&request_type=1&school_type=6000&type=&uri=apidata/api/gk/school/lists&is_dual_class=&nature=36000&size=30"
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        num = int(data['data']['numFound'])
        for item in data['data']['item']:
            output.writerow([item['school_id'], item['code_enroll'], item['name'],
                            item['province_name'], item['city_name'], item['address']])

        if i * 30 >= num:
            break
