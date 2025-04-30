import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from konlpy.tag import Okt
from wordcloud import WordCloud
import networkx as nx

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

titles = [
    '악성코드 탐지 결과 문의', '위협 분석 리포트 요청', '데이터 수집 방법 문의',
    '탐지 오류 관련 질문', '결제 시스템 오류 문의', '악성코드 삭제 방법 질문',
    '데이터 분석 결과 요청', '네트워크 보안 점검 문의', '서버 공격 탐지 질문', '로그 관리 방법 문의'
]

categories = {
    '악성코드': '보안',
    '탐지': '보안',
    '위협': '보안',
    '네트워크': '보안',
    '서버': '보안',
    '데이터': '분석',
    '분석': '분석',
    '로그': '분석',
    '결제': '결제',
    '오류': '결제'
}


data = {
    '번호': list(range(1, 366)),
    '제목': [random.choice(titles) for _ in range(365)],
    '등록일': pd.date_range(start='2024-01-01', periods=365, freq='D'),
    '응답시간(분)': [random.randint(5, 120) for _ in range(365)]
}
df = pd.DataFrame(data)

def categorize(title):
    for keyword, category in categories.items():
        if keyword in title:
            return category
    return '기타'

df['카테고리'] = df['제목'].apply(categorize)

okt = Okt()
all_text = ' '.join(df['제목'])
nouns = okt.nouns(all_text)
word_count = pd.Series(nouns).value_counts()
top_words = word_count.head(5)

monthly_random = {month: random.randint(30, 50) for month in range(1, 13)}

def plot_pie():
    plt.clf()
    plt.pie(top_words.values, labels=top_words.index, autopct='%1.1f%%', startangle=90)
    plt.title('주요 단어 비율')
    plt.axis('equal')

def plot_wordcloud():
    plt.clf()
    wordcloud = WordCloud(font_path='C:/Windows/Fonts/malgun.ttf', background_color='white', width=800, height=600)
    wordcloud.generate_from_frequencies(word_count.to_dict())
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('WordCloud')

def plot_monthly():
    plt.clf()
    months = list(monthly_random.keys())
    counts = list(monthly_random.values())
    sns.lineplot(x=months, y=counts, marker='o')
    plt.title('월별 문의량 추이')
    plt.xlabel('월')
    plt.ylabel('문의 건수')
    plt.xticks(range(1, 13))
    plt.ylim(0, 60)
    plt.grid(True)

def plot_category():
    plt.clf()
    category_counts = df['카테고리'].value_counts()
    sns.barplot(x=category_counts.values, y=category_counts.index, palette='muted')
    plt.title('카테고리별 문의 수')
    plt.xlabel('문의 건수')
    plt.ylabel('카테고리')
    plt.grid(True)

def plot_network():
    plt.clf()
    G = nx.Graph()

    pairs = [
        ('악성코드', '탐지'), ('악성코드', '삭제'), 
        ('위협', '탐지'), ('서버', '네트워크'), ('네트워크', '오류'),
        ('데이터', '분석'), ('로그', '관리'), ('결제', '오류'),
        ('서버', '로그'), ('위협', '데이터')
    ]

    for a, b in pairs:
        G.add_edge(a, b)

    pos = nx.spring_layout(G, k=1.2, iterations=100, seed=42)

    important_nodes = ['악성코드', '위협', '서버', '네트워크', '데이터', '결제']
    colors = []
    for node in G.nodes():
        if node in important_nodes:
            colors.append('gold') 
        else:
            colors.append('lightgrey')  

    nx.draw_networkx(
        G, pos,
        font_family='Malgun Gothic',
        node_color=colors,
        node_size=2500,
        font_size=12,
        edge_color='gray',
        width=2
    )
    plt.title('연관 단어 네트워크 ')
    plt.axis('off')

plots = [plot_pie, plot_wordcloud, plot_monthly, plot_category, plot_network]
current_plot = [0]

def on_key(event):
    if event.key == 'right':
        current_plot[0] = (current_plot[0] + 1) % len(plots)
    elif event.key == 'left':
        current_plot[0] = (current_plot[0] - 1) % len(plots)
    
    plt.clf()
    plots[current_plot[0]]()
    plt.draw()

fig, ax = plt.subplots()
plots[current_plot[0]]()
fig.canvas.mpl_connect('key_press_event', on_key)
plt.show()