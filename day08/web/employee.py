# employer.py 

# Flask 웹 프레임워크에서 필요한 모듈들 import
from flask import Flask, render_template, request

# Flask 애플리케이션 생성
app = Flask(__name__)

# 연락처 정보를 저장할 리스트 (초기화)
contacts = []

# 루트 경로 ('/')로 접속 시 실행될 함수 등록
@app.route('/')
def index():
    # 'add.html' 템플릿 렌더링 (사용자에게 입력 폼 보여줌)
    return render_template('add.html')

# POST 요청을 처리할 '/submit' 경로 설정
@app.route('/submit', methods=['POST'])
def submit():
    # 폼 데이터에서 name, phone, email 값을 가져옴
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')

    # 연락처 정보를 리스트에 저장
    contacts.append({'name': name, 'phone': phone, 'email': email})

    # 결과 메시지를 사용자에게 HTML 형식으로 반환
    return f"<h3>입력 완료 : {name} - {phone} - {email}</h3><br><a href='/'>돌아가기</a>"

@app.route('/list')
def contact_list():
    html = """
    <h2>📋 연락처 목록</h2>
    <table border="1" cellpadding="8">
        <tr>
            <th>이름</th>
            <th>전화번호</th>
            <th>이메일</th>
        </tr>
    """
    for contact in contacts:
        html += f"""
        <tr>
            <td>{contact['name']}</td>
            <td>{contact['phone']}</td>
            <td>{contact['email']}</td>
        </tr>
        """
    html += "</table><br><a href='/'>🏠 홈으로</a>"
    return html


# Python 파일이 직접 실행될 때 실행되는 메인 블록
if __name__ == '__main__':
    # 웹 서버 실행 (모든 IP에서 접속 허용, 포트 5000, 디버그 모드 ON)
    app.run(host='0.0.0.0', port=5000, debug=True)
