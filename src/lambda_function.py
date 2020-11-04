import requests
import datetime
import random
import os
import time

message_list = ['やるねぇ〜〜', 'よっ！', 'すごい！', '偉い!!', '素敵!!', 'ステーキ！！！']
bad_message_list = ['怠慢: ']


def lambda_handler(event, context):

    usernames = os.environ['MEMBERS'].split(',')

    information_list_for_daily_report = []

    for username in usernames:

        url = "https://kenkoooo.com/atcoder/atcoder-api/results?user=" + username
        respose = requests.get(url)
        # 提出時間順にsort
        respose_list = sorted(respose.json(), key=lambda x: x['epoch_second'])

        # 上のjsonとは別物なのでここでimport
        import json

        # 日本に合わせるために+9時間
        dt_now_jp = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=9)))

        today_solved_num = 0
        today_point = 0

        # 1つの問題につき1報告/日までにしたい
        today_solved_problem = set()

        for problem_dict in respose_list:
            # 提出情報
            judge = problem_dict['result']

            dt = datetime.datetime.fromtimestamp(problem_dict['epoch_second'])
            # 日本に合わせるために+9時間
            dt_jp = dt + datetime.timedelta(hours=9)

            contest_id = problem_dict['contest_id']
            submission_id = problem_dict['id']
            point = int(problem_dict['point'])
            problem_name = problem_dict['problem_id']

            submission_url = 'https://atcoder.jp/contests/' + \
                contest_id + '/submissions/' + str(submission_id)

            # 毎時間の報告
            if match_for_year_to_hour(dt_jp, dt_now_jp) and judge == 'AC' and (problem_name not in today_solved_problem):
                post_message_to_channel(username + 'さん!\n' + '「' + problem_name + '」' + ' ACおめでとう! ' + str(
                    point) + 'ポイントゲット!!! ' + random.choice(message_list) + '\n' + submission_url)

            if match_for_year_to_day(dt_jp, dt_now_jp) and judge == 'AC' and (problem_name not in today_solved_problem):
                today_solved_problem.add(problem_name)
                today_solved_num += 1
                today_point += point

        information_for_daily_report = {
            'name': username,
            'today_solved_num': today_solved_num,
            'today_point': today_point
        }
        information_list_for_daily_report.append(information_for_daily_report)

    if dt_now_jp.hour == 23:
        daily_response = str(dt_now_jp.month) + '/' + \
            str(dt_now_jp.day) + '日報！\n'
        information_list_for_daily_report.sort(key=lambda x: x['today_point'])

        rank = 1
        for daily_info in information_list_for_daily_report:
            username = daily_info['name']
            today_solved_num = daily_info['today_solved_num']
            today_point = daily_info['today_point']

            if today_solved_num > 0:
                rank_info = '第' + str(rank) + '位: ' + \
                    str(today_point) + 'pt.  '
                msg = username + ': ' + str(today_solved_num) + '問AC！\n'
                rank += 1
            else:
                rank_info = random.choice(bad_message_list)
                msg = username + "!\n"
            daily_response += rank_info
            daily_response += msg
        daily_response += '\n明日も頑張れ〜〜〜！'
        post_message_to_channel(daily_response)

        # APIを叩く間隔の確保
        time.sleep(1)

    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }


def match_for_year_to_hour(dt_a, dt_b):
    return (dt_a.year == dt_b.year) and (dt_a.month == dt_b.month) and (dt_a.day) == (dt_b.day) and (dt_a.hour) == (dt_b.hour)


def match_for_year_to_day(dt_a, dt_b):
    return (dt_a.year == dt_b.year) and (dt_a.month == dt_b.month) and (dt_a.day) == (dt_b.day)


def post_message_to_channel(message):
    import json
    url = os.environ['SLACK_INCOMMING_WEBHOOK']
    requests.post(url, data=json.dumps({
        "text": message,
    }))
