import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="大樂透號碼分析", page_icon="🎲", layout="wide")

st.title('大樂透號碼分析')

url = 'https://www.taiwanlottery.com.tw/lotto/lotto649/history.aspx'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

result = []

for td in soup.find_all('td'):
    if '開出順序' in td.text:
        for num in td.find_next_siblings('td'):
            span = num.find('span')
            if span is not None:
                result.append(int(span.text))

result = [result[i:i+7] for i in range(0, len(result), 7)]

st.write("最近10組大樂透號碼:")
result_df = pd.DataFrame(result, columns=["號碼1", "號碼2", "號碼3", "號碼4", "號碼5", "號碼6", "特別號"])
st.write(result_df)

data = result[:3]

def calculate_mean(numbers):
    return sum(numbers) / len(numbers)

def round_mean(mean):
    return round(mean)

unique_numbers = sorted(list(set(sum(data, []))))
ranges = [(1, 7), (8, 16), (17, 21), (22, 28), (29, 35), (36, 42), (43, 49)]
combined_data = []

for r in ranges:
    combined_data.append([x for x in unique_numbers if r[0] <= x <= r[1]])

rounded_means_1 = []
for group in combined_data:
    if group:
        mean = calculate_mean(group)
        rounded_mean = round_mean(mean)
        rounded_means_1.append(rounded_mean)
    else:
        rounded_means_1.append(None)

sorted_data = [sorted(d) for d in data]
mean_values = []

for i in range(len(data[0])):
    mean = calculate_mean([d[i] for d in sorted_data])
    rounded_mean = round_mean(mean)
    mean_values.append(rounded_mean)

rounded_means_2 = sorted(mean_values)

ranges_2 = [(1, 10), (11, 20), (21, 30), (31, 40), (41, 49)]
combined_data_2 = []

for r in ranges_2:
    combined_data_2.append(
        [x for x in rounded_means_1 if x is not None and r[0] <= x <= r[1]] +
        [x for x in rounded_means_2 if x is not None and r[0] <= x <= r[1]]
    )

rounded_means_3 = []
for group in combined_data_2:
    if group:
        mean = calculate_mean(group)
        rounded_mean = round_mean(mean)
        rounded_means_3.append(rounded_mean)
    else:
        rounded_means_3.append(None)

st.subheader("重心號碼一:")
rounded_means_1_df = pd.DataFrame(rounded_means_1, index=["1-7", "8-16", "17-21", "22-28", "29-35", "36-42", "43-49"]).T
st.write(rounded_means_1_df)

st.subheader("重心號碼二:")
rounded_means_2_df = pd.DataFrame(rounded_means_2, columns=["重心號碼二"])
st.write(rounded_means_2_df)

st.subheader("均質預測號碼:")
rounded_means_3_df = pd.DataFrame(rounded_means_3, index=["1-10", "11-20", "21-30", "31-40", "41-49"]).T
st.write(rounded_means_3_df)

