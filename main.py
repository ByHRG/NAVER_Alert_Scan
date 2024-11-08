import sys
import cookiemaker
import scan

class Naver_Tools:

    def cookie(self):
        cookies = cookiemaker.Cookiemake().naver_cookie()
        cookie_list = []
        for i in cookies:
            cookie_list.append(f"{i['name']}={i['value']}")
        return "; ".join(cookie_list)

    def log_check(self):
        data = scan.Scan().load()
        for i in data:
            print(i)

    def run(self):
        while True:
            run_type = input("기능 선택\n1 - 스캐너 작동\n2 - 스캐너 로그 불러오기\n기능:")
            if run_type == "1":
                scan.Scan().run(self.cookie())
            elif run_type == "2":
                try:
                    self.log_check()
                except:
                    sys.stdout.write(f"\r저장된 로그 데이터가 없습니다.\n")
                    sys.stdout.flush()
            else:
                sys.stdout.write(f"\r기능 선택 입력을 제대로 해주세요.\n")
                sys.stdout.flush()


Naver_Tools().run()
