#include <stdio.h>      // 표준 입출력 함수 사용
#include <stdlib.h>     // 표준 라이브러리 (파일 입출력 등)
#include <string.h>     // 문자열 처리 함수 사용

#define MAX_LEN 100             // 아이디, 비밀번호, 입력 문자열 최대 길이
#define FILE_NAME "userFile.txt" // 사용자 정보 저장 파일 이름

// 함수 선언
void signUp();  // 회원가입 기능
void login();   // 로그인 기능

int main() {
    char input[MAX_LEN];  // 사용자 입력을 받을 문자열 버퍼
    int choice;           // 메뉴 선택 번호

    while (1) {  // 무한 반복 루프
        // 메뉴 출력
        printf("\n1. 회원가입\n2. 로그인\n3. 종료\n메뉴 선택: ");

        // 입력을 문자열로 받아 안전하게 처리
        if (fgets(input, sizeof(input), stdin) == NULL) {
            printf("입력 오류\n");
            continue;
        }

        // 문자열에서 정수 추출 (메뉴 번호 확인)
        if (sscanf(input, "%d", &choice) != 1) {
            printf("숫자를 입력해주세요.\n");
            continue;
        }

        // 메뉴 번호에 따라 기능 실행
        switch (choice) {
            case 1:
                signUp();  // 회원가입 실행
                break;
            case 2:
                login();   // 로그인 실행
                break;
            case 3:
                printf("프로그램 종료\n");
                return 0;  // 프로그램 정상 종료
            default:
                printf("1/ 2/ 3 중에 선택하세요.\n");  // 잘못된 번호 처리
        }
    }

    return 0;
}

// 회원가입 함수 정의
void signUp() {
    char id[MAX_LEN], pw[MAX_LEN];                // 입력 받을 아이디, 비밀번호
    char file_id[MAX_LEN], file_pw[MAX_LEN];      // 파일에서 읽은 아이디, 비밀번호
    char buffer[MAX_LEN];                         // 임시 입력 버퍼
    int duplicate = 0;                            // 중복 아이디 플래그

    // 아이디 입력
    printf("회원가입 - 아이디 입력: ");
    fgets(buffer, sizeof(buffer), stdin);
    sscanf(buffer, "%s", id);  // 공백 제외하고 문자열 추출

    // 비밀번호 입력
    printf("회원가입 - 비밀번호 입력: ");
    fgets(buffer, sizeof(buffer), stdin);
    sscanf(buffer, "%s", pw);

    // 기존 아이디 중복 확인
    FILE *fp = fopen(FILE_NAME, "r");  // 파일 읽기 모드로 열기
    if (fp != NULL) {
        while (fscanf(fp, "%s %s", file_id, file_pw) != EOF) {
            if (strcmp(id, file_id) == 0) {  // 동일한 아이디가 존재할 경우
                duplicate = 1;
                break;
            }
        }
        fclose(fp);
    }

    if (duplicate) {
        printf("회원가입 실패: 이미 존재하는 아이디입니다.\n");
        return;
    }

    // 중복이 없으면 파일에 저장 (추가 모드)
    fp = fopen(FILE_NAME, "a");
    if (fp == NULL) {
        perror("파일 열기 실패");
        return;
    }

    fprintf(fp, "%s %s\n", id, pw);  // 아이디와 비밀번호 파일에 기록
    fclose(fp);

    printf("회원가입이 완료되었습니다.\n");
}

// 로그인 함수 정의
void login() {
    char id[MAX_LEN], pw[MAX_LEN];                // 입력 받을 아이디, 비밀번호
    char file_id[MAX_LEN], file_pw[MAX_LEN];      // 파일에서 읽은 아이디, 비밀번호
    char buffer[MAX_LEN];                         // 임시 입력 버퍼
    int found = 0;                                // 로그인 성공 여부

    FILE *fp = fopen(FILE_NAME, "r");  // 파일 읽기 모드로 열기
    if (fp == NULL) {
        perror("파일 열기 실패");
        return;
    }

    // 아이디 입력
    printf("로그인 - 아이디 입력: ");
    fgets(buffer, sizeof(buffer), stdin);
    sscanf(buffer, "%s", id);

    // 비밀번호 입력
    printf("로그인 - 비밀번호 입력: ");
    fgets(buffer, sizeof(buffer), stdin);
    sscanf(buffer, "%s", pw);

    // 파일에서 아이디/비밀번호 탐색
    while (fscanf(fp, "%s %s", file_id, file_pw) != EOF) {
        if (strcmp(id, file_id) == 0 && strcmp(pw, file_pw) == 0) {
            found = 1;  // 일치하는 사용자 발견
            break;
        }
    }

    fclose(fp);

    // 로그인 결과 출력
    if (found)
        printf("로그인 성공!\n");
    else
        printf("로그인 실패: 아이디 또는 비밀번호가 틀렸습니다.\n");
}
