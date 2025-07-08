# 📡 iot-raspi-2025
라즈베리파이 이론 및 실습

## 📅 1일차 - Raspberry Pi 환경 설정 및 기본 명령어 학습

### Raspberry Pi OS 설치 및 무선 설정 가이드 (Windows 기준)

### 1. Raspberry Pi Imager 다운로드 및 실행

- Raspberry Pi 공식 사이트 접속  
    - [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)

- **"Download for Windows"** 버튼 클릭하여 `.exe` 파일 다운로드

    <img src="./image/raspi001.png" width="600">

- 다운로드 완료 후 `.exe` 파일 실행

### 2. 설치 및 설정
1. **장치 선택**  
    - 사용하는 Raspberry Pi 모델 선택
2. **OS 선택**  
    - 원하는 Raspberry Pi OS 선택
3. **저장 장치 선택**  
    - 마이크로 SD 카드 선택

        <img src="./image/raspi002.png" width="600">

4. **설정 편집**
    - 라즈베리파이 디바이스, 운영체제, 저장소 설정 후 다음 클릭

    - OS 커스터마이징 설정을 적용
        - 설정을 편집하기 클릭

            <img src="./image/raspi003.png" width="600">

        - **Hostname**: 라즈베리파이의 네트워크 이름 지정  
        - **사용자 이름 및 비밀번호**: SSH 접속용 계정 설정  

        - **무선 네트워크 설정**
            - SSID : Wi-Fi 이름 입력 (공유기의 네트워크 이름 확인 후 입력)  
            - Password: Wi-Fi 비밀번호 입력  
            - 무선 LAN 국가 : `KR` (대한민국)

        - **로케일 설정**
            - 키보드 레이아웃: `kr`  
            - 언어/지역 설정: 한국어로 지정

        - **서비스**
            - SSH 활성화 체크 (원격 접속용)

5. 설정 후 ->  **저장** 클릭  -> 설치 진행


### 3. 공유기에서 Wi-Fi 정보 확인

- 웹 브라우저에서 `와이파이 IP` 접속
- 로그인 후 **[관리도구] → [무선랜 관리] → [Wi-Fi 기본설정]** 메뉴 이동
- **네트워크 이름 (SSID)** 및 **비밀번호** 확인


### 4. 소프트웨어 추가 다운로드

#### VNC Viewer 다운로드 (원격 데스크탑 연결용)

- VNC Viewer 공식 다운로드 페이지
    - [https://www.realvnc.com/en/connect/download/viewer/](https://www.realvnc.com/en/connect/download/viewer/)

- 사용 중인 OS(예: Windows)에 맞는 설치 파일 다운로드

#### SD Card Formatter 다운로드 (SD 카드 초기화용)

- SD 카드 포맷 공식 유틸리티
    - [https://www.sdcard.org/downloads/formatter/](https://www.sdcard.org/downloads/formatter/)
- Windows 또는 macOS용 다운로드 및 설치
- 마이크로 SD 카드 삽입 후 포맷 진행 (옵션: Quick Format 추천)

### 5. Raspberry Pi VNC 원격 접속 설정

#### SSH 접속 (PuTTY 사용)

1. **PuTTY 실행**  
2. Host Name에 **라즈베리파이 IP 주소 입력**  
    - 예: `192.168.0.xxx`
3. Port는 기본값 `22`, 연결 타입 `SSH`로 설정 후 `Open` 클릭  
4. 로그인 화면에서 다음 입력:
   - ID: `pi`  
   - Password: (설치 시 설정한 비밀번호)

#### VNC 기능 활성화

- SSH 접속 완료 후 명령어 입력

```bash
sudo raspi-config
```

1. Interface Options 선택

    <img src="./image/raspi004.png" width="600">

2. VNC 선택

    <img src="./image/raspi005.png" width="600">

3. Would you like the VNC Server to be enabled?
    - Yes 클릭 후 Finish 후 종료
    
4. 라즈베리파이 재시작

```bash
sudo reboot 
```

####  VNC Viewer로 원격 접속
- VNC Viewer 실행 -> 주소창에 라즈베리파이 IP 주소 입력 -> 사용자 이름과 비밀번호 입력

#### 한글 폰트 설치 및 등록

```bash
sudo apt install fonts-nanum fonts-nanum-extra  // 나눔폰트 설치
sudo apt install fonts-unfonts-core             // 폰트등록
sudo reboot now
```

#### 한글 입력기 설치
- 메뉴 -> 기본설정 -> 입력기 -> default 변경 후 확인

    <img src="./image/raspi006.png" width="600">

- VNC Viewer -> 터미널 -> 해당 명령어 실행

```bash
sudo apt install fcitx-hangul
```

#### Nano 설정 (`/etc/nanorc`)

- VNC Viewer -> 터미널 -> 해당 명령어 실행

```bash
sudo nano /etc/nanorc
```

- 주석 제거 항목
    - `set autoindent` : 새 줄 입력 시 이전 줄의 들여쓰기를 자동 복사하여 유지.\
    - `set linenumbers` : 편집 화면 왼쪽에 줄 번호를 표시
    - `set tabsize 3` : 탭 입력 시 들여쓰기 칸 수를 지정. 기본값 8칸 -> 3칸으로 줄임

### 🈶 한글 폰트 설치

```bash
sudo apt install fonts-nanum fonts-nanum-extra      # 나눔폰트 설치
sudo apt install fonts-unfonts-core                 # 한글 폰트 등록
```

### 기본 명령어
#### 📁 디렉토리 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `pwd` | 현재 디렉토리 경로 출력 |
| `cd [디렉토리]` | 지정한 디렉토리로 이동 |
| `cd ..` | 상위 디렉토리로 이동 |
| `cd` 또는 `cd ~` | 홈 디렉토리(`/home/pi`)로 이동 |
| `.` | 현재 디렉토리를 의미 |
| `..` | 상위 디렉토리를 의미 |
| `ls` | 현재 디렉토리의 파일/폴더 목록 출력 |
| `ls -l` | 상세 정보와 함께 출력 |
| `ls -a` | 숨김 파일 포함 전체 목록 출력 |

---

#### 📂 파일 및 폴더 관리 명령어

| 명령어 | 설명 |
|--------|------|
| `mkdir [폴더명]` | 새 폴더 생성 |
| `rmdir [폴더명]` | 비어있는 폴더 삭제 |
| `rm [파일명]` | 파일 삭제 |
| `rm -r [폴더명]` | 폴더와 그 안의 내용 모두 삭제 |
| `cp [원본] [대상]` | 파일 복사 |
| `mv [원본] [대상]` | 파일 이동 또는 이름 변경 |

---

#### ⚙️ 시스템 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `sudo` | 관리자 권한으로 명령 실행 |
| `sudo reboot` | 시스템 재부팅 |
| `sudo shutdown now` | 즉시 시스템 종료 |
| `sudo shutdown -r now` | 즉시 재부팅 |
| `top` | 현재 실행 중인 프로세스 보기 |
| `htop` | 리소스 상태 확인 (시각적, 설치 필요) |

---

#### 📦 패키지 관리 명령어 (APT)

| 명령어 | 설명 |
|--------|------|
| `sudo apt update` | 패키지 목록 업데이트 |
| `sudo apt upgrade` | 설치된 패키지 업그레이드 |
| `sudo apt install [패키지명]` | 새 패키지 설치 |
| `sudo apt remove [패키지명]` | 패키지 제거 |
| `sudo apt autoremove` | 사용하지 않는 패키지 자동 제거 |

---

#### 🌐 네트워크 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `hostname -I` | IP 주소 확인 |
| `ping [주소]` | 네트워크 연결 확인 |
| `ifconfig` 또는 `ip a` | 네트워크 상태 확인 |

---

#### 🛠 기타 유용한 명령어

| 명령어 | 설명 |
|--------|------|
| `clear` | 터미널 화면 지우기 |
| `nano [파일명]` | 간단한 텍스트 편집기 |
| `cat [파일명]` | 텍스트 파일 내용 출력 |
| `chmod +x [파일명]` | 실행 권한 부여 |
| `./[파일명]` | 현재 디렉토리에서 파일 실행 |

---
