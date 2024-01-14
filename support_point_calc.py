import pandas as pd
import requests
import datetime
import time

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"请求错误 {url}")

def process_data(data_a, data_b, s1_df, s2_df):
    # Extracting and combining 'list' from 'skus' in data_a and data_b
    skus_list_a = data_a['data'].get('skus', {}).get('list', [])
    skus_list_b = data_b['data'].get('skus', {}).get('list', [])
    combined_skus_list_df = pd.DataFrame(skus_list_a + skus_list_b)

    # Merging with s1 and s2 data and calculating total support values
    combined_df = pd.merge(combined_skus_list_df, s1_df, on='s1', how='left')
    combined_df['总应援值'] = combined_df['sold_num'] * combined_df['应援值']
    combined_df = pd.merge(combined_df, s2_df, on='s2', how='left')

    # Grouping by member and calculating total support values
    final_df = combined_df.groupby('成员')[['总应援值']].sum().reset_index()
    final_df.sort_values(by='总应援值', ascending=False, inplace=True)

    
    # Adding a rank column

    final_df['排名'] = range(1, len(final_df) + 1)

    # Reordering columns to put '排名' as the first column
    final_df = final_df[['排名', '成员', '总应援值']]
    
    # Return the final DataFrame
    return final_df

def create_html_table(df):
    # Convert DataFrame to HTML
    html_table = df.to_html(index=False)

    # Add timestamp
    timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    html_content = f'''
    <html>
    <head>
        <meta charset='UTF-8'>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>AKB48 TeamSH 5th总选举应援值统计</title>
        <style>
            th, td {{
                text-align: center;
                padding: 8px;
            }}
            body {{
                font-family: Calibri, sans-serif;
            }}
            @media screen and (max-width: 600px) {{
                table {{
                    width: 100%;
                    font-size: 14px;
                }}
                th, td {{
                    word-break: break-word;
                }}
        </style>
    </head>
    <body>
        <p><b>AKB48 TeamSH 5th总选举应援值统计</b></p>
        <p><i>注意：使用储值卡产生的48%应援值加成未被计算在内，该计算结果仅供参考，最终结果请以官方发布为准</i></p>
        <p>统计数据每 {sleeptime} 秒自动更新一次，请刷新网页以获得最新的数据，当前展示的统计数据获取于 {timestamp}</p>{html_table}    </body>
    </html>'''

    # Save to HTML file
    with open("index.html", "w", encoding='utf-8') as file:
        file.write(html_content)

# URLs for data A and B
url_a = "https://maijia.youzan.com/v3/goods/getGoodsByAlias.json?alias=3evj71r3nrb0zm7&continueFlag=3bdf2ae1bb32dd52208eae876a08fc34"
url_b = "https://maijia.youzan.com/v3/goods/getGoodsByAlias.json?alias=1y6kd1tdkj76rln&continueFlag=3bdf2ae1bb32dd52208eae876a08fc34"
# s1 and s2 dataframes
s1_data = [{"s1": 533050517, "名称": "整包48元", "应援值": 100}, {"s1": 533050634, "名称": "整盒（50包）", "应援值": 5000}, {"s1": 533050760, "名称": "整条（6盒）", "应援值": 30000}, {"s1": 533050862, "名称": "整箱（8条）", "应援值": 240000}, {"s1": 533061153, "名称": "珍藏版", "应援值": 400}, {"s1": 533061300, "名称": "普通版", "应援值": 100}, {"s1": 533061427, "名称": "应援版", "应援值": 2000}
]
s2_data = [{"s2": 533073818, "成员": "王予婷", "歌曲": "法定速度与优越感"}, {"s2": 533070026, "成员": "毛唯嘉", "歌曲": "欲望者"}, {"s2": 533070346, "成员": "宋欣然", "歌曲": "最美之人"}, {"s2": 533073619, "成员": "曾艺", "歌曲": "那时的locker"}, {"s2": 533070703, "成员": "吴安琪", "歌曲": "无法逃离的梦"}, {"s2": 533071516, "成员": "桂楚楚", "歌曲": "大人列车"}, {"s2": 533073977, "成员": "张雅茜", "歌曲": "去47个美丽城市"}, {"s2": 533070230, "成员": "施可妍", "歌曲": "only today"}, {"s2": 533073103, "成员": "谢雯婕", "歌曲": "盛夏 sounds good"}, {"s2": 533071284, "成员": "周念琪", "歌曲": "掌"}, {"s2": 533071105, "成员": "庄晓媞", "歌曲": "眼泪的表面张力"}, {"s2": 533073568, "成员": "吴凡", "歌曲": "Pionner"}, {"s2": 533073776, "成员": "杜昕懿", "歌曲": "变成樱花树"}, {"s2": 533070421, "成员": "魏新", "歌曲": "不需要翅膀"}, {"s2": 533073451, "成员": "陈嘉意", "歌曲": "因为有你在"}, {"s2": 533074463, "成员": "韦筱雅", "歌曲": "dreamin'girls"}, {"s2": 533071596, "成员": "渐蔷薇", "歌曲": "没有国境的时代"}, {"s2": 533071430, "成员": "龚露雯", "歌曲": "青春的闪电"}, {"s2": 533073171, "成员": "张嘉哲", "歌曲": "爱的洄游鱼"}, {"s2": 533073294, "成员": "周陈雨轩", "歌曲": "梦之河"}, {"s2": 533073371, "成员": "张艺琳", "歌曲": "直呼其名的幻想"}, {"s2": 533073493, "成员": "朱景晨", "歌曲": "无论如何都喜欢你"}, {"s2": 533069938, "成员": "刘念", "歌曲": "10年樱花"}, {"s2": 533072669, "成员": "马小雨", "歌曲": "我不在"}, {"s2": 533071733, "成员": "李于淼", "歌曲": "残念少女"}, {"s2": 533072303, "成员": "张倩霏", "歌曲": "so long!"}, {"s2": 533072864, "成员": "王安妮", "歌曲": "浪漫手枪"}, {"s2": 533073879, "成员": "张诗瑜", "歌曲": "布偶熊"}, {"s2": 533071385, "成员": "程安子", "歌曲": "眨眼3次（只有live版的）"}, {"s2": 533072397, "成员": "张乔瑜", "歌曲": "不要让梦想死去"}, {"s2": 533072594, "成员": "李佳慧", "歌曲": "beginner"}, {"s2": 533072797, "成员": "邱笛尔", "歌曲": "剧场女神"}, {"s2": 533074056, "成员": "郑雨姗", "歌曲": "支柱"}, {"s2": 533072750, "成员": "彭露萱", "歌曲": "再见自由式"}, {"s2": 533070952, "成员": "翟羽佳", "歌曲": "勇往直前"}, {"s2": 533070752, "成员": "徐依婷", "歌曲": "风正在吹"}, {"s2": 533070879, "成员": "袁瑞希", "歌曲": "悬铃木"}, {"s2": 533072539, "成员": "邹若男", "歌曲": "Every day、发箍"}, {"s2": 533072935, "成员": "王暄雅", "歌曲": "Halloween night"}, {"s2": 533074169, "成员": "黄桢璇", "歌曲": "希望的副歌"}, {"s2": 533070120, "成员": "沈莹", "歌曲": "梦之路"}, {"s2": 533074326, "成员": "鹿兮", "歌曲": "那天的风铃"}, {"s2": 533071015, "成员": "朱苓", "歌曲": "初恋蝴蝶"}, {"s2": 533071213, "成员": "叶知恩", "歌曲": "你、彩虹和太阳"}, {"s2": 533071653, "成员": "孔珂昕", "歌曲": "永远的压力"}, {"s2": 533071972, "成员": "施蔼倍", "歌曲": "无用的愿望"}, {"s2": 533072104, "成员": "谭珺兮", "歌曲": "眼泪深呼吸"}, {"s2": 533071894, "成员": "梁时安", "歌曲": "心爱的娜塔莎"}, {"s2": 533073671, "成员": "王晓阳", "歌曲": "你最爱的人是谁"}, {"s2": 533072465, "成员": "张樱璐", "歌曲": "在樱色的天空下"}, {"s2": 533072183, "成员": "曾鸶淳", "歌曲": "光与影交织的日子"}
]
s1_df = pd.DataFrame(s1_data)
s2_df = pd.DataFrame(s2_data)

# Main loop to run the script every minute
while True:
    data_a = fetch_data(url_a)
    data_b = fetch_data(url_b)
    final_df = process_data(data_a, data_b, s1_df, s2_df)
    sleeptime = 60
    create_html_table(final_df)
    refreshtime = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print ("Sucessfully refreshed at " + refreshtime)
    time.sleep(sleeptime)  # Wait for 60 seconds before the next run