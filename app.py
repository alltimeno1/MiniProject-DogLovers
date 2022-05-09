# flask 패키지
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# mongoDB - pymongo, dnspython 패키지
from pymongo import MongoClient

# 스크래핑 - requests, bs4 패키지
import requests
from bs4 import BeautifulSoup

# 몽고DB 연결
client = MongoClient('mongodb+srv://test:sparta@cluster0.m7jzf.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


# 기본 메인 페이지 - index.html
@app.route('/')
def home():
    return render_template('index.html')


# 크롤링 데이터를 DB 로 보냅니다
@app.route('/find', methods=['POST'])
def save_diary():
    # 크롤링 준비
    url = 'https://www.animal.go.kr/front/awtis/loss/lossList.do?totalCount=192&pageSize=10&menuNo=1000000057&&page=1#moveUrl'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    # selector 로 데이터 크롤링해서 변수에 저장
    name_receive = soup.select_one('');
    image_receive = soup.select_one('');
    desc_receive = soup.select_one('"]');

    # db로 보낼 자료 정리
    doc = {
        'name': name_receive,
        'image': image_receive,
        'desc': desc_receive,
    }

    # db로 보내기
    # db.doglovers.insert_one(doc)

    # 로딩될때 - 지금은 테스트로 메시지를 보내지만, 배포할땐 메시지를 지웁니다.
    return jsonify({'msg':'scrapping success'})


# 크롤링 했던 데이터를 DB에서 꺼내옵니다.
@app.route("/find", methods=["GET"])
def movie_get():
    # 모든 정보를 꺼내서 datas 변수에 저장하고 그 변수를 return해서 클라이언트로 보냅니다.
    datas = list(db.doglovers.find({}, {'_id': False}))
    return jsonify({'datas':datas})







# 5000 포트 사용
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)