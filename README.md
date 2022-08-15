# 爬取浙江高考录取分数线

使用 Python 爬取全国对浙江省的录取分数线，数据来源于[掌上高考](https://www.gaokao.cn/)

## 相关链接

1. https://api.eol.cn/web/api/?admissions=&central=&department=&dual_class=&f211={is_211}&f985={is_985}&is_doublehigh=&keyword=&page={i}&ranktype=&request_type=1&school_type=6000&type=&uri=apidata/api/gk/school/lists&is_dual_class=&nature=36000&size={page_size}&province_id={province_id}
2. https://static-data.gaokao.cn/www/2.0/schoolspecialindex/{year}/{sid}/33/3/16/{i}.json
3. https://www.gaokao.cn/school/{sid}/provinceline