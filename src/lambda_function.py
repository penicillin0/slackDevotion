import requests
import datetime
import random
import os

message_list = ['すごい！', '偉い!!', '素敵!!', 'ステーキ！！！']


def lambda_handler(event, context):

    usernames = os.environ['MEMBERS'].split(',')

    post_message_to_channel("みんな！結果発表の時間だよ！！\n----------")
    for username in usernames:

        url = "https://kenkoooo.com/atcoder/atcoder-api/results?user="\
        + username
        respose = requests.get(url)
        respose_list = respose.json()

        # 上のjsonとは別物なのでここでimport
        import json

        dt_tody = datetime.date.today()

        solved_num = 0
        for problem_dict in respose_list:
            judge = problem_dict['result']
            dt = datetime.datetime.fromtimestamp(problem_dict['epoch_second'])
            if (dt.month == dt_tody.month and dt.year == dt_tody.year and
                    dt.day == dt_tody.day and judge == 'AC'):
                solved_num += 1
        if solved_num > 0:
            post_message_to_channel(
                username + "は今日" + str(solved_num) + "問ACしました！"\
                + random.choice(message_list))
        else:
            post_message_to_channel(username + "は今日問題を解いていません、、、草")
    post_message_to_channel("\n----------\n明日も頑張ってね〜！")
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def post_message_to_channel(message):
    import json
    url = os.environ['SLACK_INCOMMING_WEBHOOK']
    requests.post(url, data=json.dumps({
        "text": message,
    }))
