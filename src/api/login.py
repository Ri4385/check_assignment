import requests
from bs4 import BeautifulSoup
from config import setting

def login_with_password(username: str, password: str) -> requests.Session:
    # セッションを開始
    session = requests.Session()

    # ヘッダーにUser-Agentを追加
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # ログイン情報を設定
    initial_login_url = setting.login_url

    try:
        # 最初にログインページを取得
        initial_response = session.get(initial_login_url, headers=headers)
        print(f"Initial response URL: {initial_response.url}")

        # リダイレクト先のURLを確認
        if initial_response.url != initial_login_url:
            print(f"Redirected to: {initial_response.url}")
            login_url = initial_response.url
        else:
            login_url = initial_login_url

        # ログインページを再取得して隠しフィールドを取得
        login_page = session.get(login_url, headers=headers)
        soup = BeautifulSoup(login_page.text, 'html.parser')

        # 隠しフィールドの値を取得
        lt = soup.find('input', {'name': 'lt'})['value']
        execution = soup.find('input', {'name': 'execution'})['value']
        event_id = soup.find('input', {'name': '_eventId'})['value']

        # ログイン情報をPOSTリクエストで送信
        login_data = {
            'username': username,
            'password': password,
            'lt': lt,
            'execution': execution,
            '_eventId': event_id
        }

        # ログインリクエストを送信
        login_response = session.post(login_url, data=login_data, headers=headers)

        # レスポンスを出力して内容を確認
        # if setting.debug:
        #     data_url = "https://panda.ecs.kyoto-u.ac.jp/direct/site.json"
        #     data = session.get(data_url).json()
        #     print(str(data)[:200])

    except Exception as e:
        print(f"An error occurred: {e}")
        raise NotImplementedError

    return session

if __name__ == "__main__":
    pass