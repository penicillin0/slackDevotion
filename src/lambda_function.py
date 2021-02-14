import requests
import datetime
import random
import os
import time

message_list = ['やるねぇ〜〜', 'よっ！', 'すごい！', '偉い!!', '素敵!!', 'ステーキ！！！']
bad_message_list = ['👿 <(']
dt_now_jp = datetime.datetime.now(
    datetime.timezone(datetime.timedelta(hours=9)))


def lambda_handler(event, context):

    usernames: list[str] = os.environ['MEMBERS'].split(',')

    at_users = []

    all_hourly_massage = ""
    for username in usernames:

        at_user: AtCoder_user = AtCoder_user(username)
        all_hourly_massage += at_user.hourly_report()
        at_users.append(at_user)
        # APIを叩く間隔の確保
        time.sleep(1)
    post_message_to_channel(all_hourly_massage)

    if dt_now_jp.hour == 23:
        daily_response: str = str(dt_now_jp.month) + '/' + \
            str(dt_now_jp.day) + '日報！\n'
        at_users.sort(
            key=lambda at_user: at_user.get_daily_status()['today_point'],
            reverse=True)
        print(at_users)
        for rank, at_user in enumerate(at_users, start=1):

            daily_response += make_daily_message(rank, at_user)

        post_message_to_channel(daily_response + '\n明日も頑張れ〜〜〜！')

    import json
    return {'statusCode': 200, 'body': json.dumps('OK')}


class AtCoder_user():
    def __init__(self, at_username: str):
        self.at_username = at_username
        self.today_solved_problems = self._get_today_solved()

    def _get_today_solved(self):
        url = "https://kenkoooo.com/atcoder/atcoder-api/results?user=" + self.at_username
        respose = requests.get(url)
        # 提出時間順にsort
        submission_list = sorted(respose.json(),
                                 key=lambda x: x['epoch_second'])

        today_solved_problems: list[dict] = []
        for submission_dict in submission_list:

            # ACじゃなければskip
            if submission_dict['result'] != 'AC':
                continue

            # 今日すでに解いた問題であればskip
            if submission_dict['problem_id'] in [
                    d.get('problem_name') for d in today_solved_problems
            ]:
                continue

            # 日本時間に
            submit_time = datetime.datetime.fromtimestamp(
                submission_dict['epoch_second']) + datetime.timedelta(hours=9)

            # 今日解いた問題でなければskip
            if not match_for_year_to_day(submit_time, dt_now_jp):
                continue

            today_solved_problem = {
                'submit_time':
                submit_time,
                'problem_name':
                submission_dict['problem_id'],
                'point':
                int(submission_dict['point']),
                'submission_id':
                str(submission_dict['id']),
                'contest_id':
                submission_dict['contest_id'],
                'submission_url':
                'https://atcoder.jp/contests/' +
                submission_dict['contest_id'] + '/submissions/' +
                str(submission_dict['id'])
            }

            today_solved_problems.append(today_solved_problem)
        return today_solved_problems

    def hourly_report(self) -> str:
        hourly_message: str = ""
        for submission in self.today_solved_problems:
            if match_for_year_to_hour(submission['submit_time'], dt_now_jp):
                hourly_message += self.at_username + 'さん!\n' + '「' + \
                    submission['problem_name'] + '」' + \
                    ' ACおめでとう! ' + str(submission['point']) + 'ポイントゲット!!! ' + random.choice(
                        message_list) + '\n' + submission['submission_url'] + '\n'

        return hourly_message

    def get_daily_status(self):
        return {
            'name':
            self.at_username,
            'today_solved_num':
            len(self.today_solved_problems),
            'today_point':
            sum([d.get('point') for d in self.today_solved_problems])
        }


def make_daily_message(rank: int, at_user: AtCoder_user):
    user_status = at_user.get_daily_status()
    if user_status['today_solved_num'] == 0:
        daily_message = random.choice(
            bad_message_list) + user_status['name'] + " )\n"
    else:
        daily_message = '第' + str(rank) + '位: ' + \
            str(user_status['today_point']) + 'pt.  \n' + user_status['name'] + ': ' + \
            str(user_status['today_solved_num']) + '問AC！\n'

    return daily_message


def match_for_year_to_hour(dt_a: datetime, dt_b: datetime) -> bool:
    return (dt_a.year == dt_b.year) and (dt_a.month == dt_b.month) and (
        dt_a.day) == (dt_b.day) and (dt_a.hour) == (dt_b.hour)


def match_for_year_to_day(dt_a: datetime, dt_b: datetime) -> bool:
    return (dt_a.year
            == dt_b.year) and (dt_a.month
                               == dt_b.month) and (dt_a.day) == (dt_b.day)


def post_message_to_channel(message: str) -> None:
    import json
    url = os.environ['SLACK_INCOMMING_WEBHOOK']
    requests.post(url, data=json.dumps({
        "text": message,
    }))
