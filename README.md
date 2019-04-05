# 日報
## 初期化
```
$ git clone https://github.com/tatHi/daily_report.git
$ cd daily_report
$ python3 update.py
```

## 使い方
`new_report.md`に今日の日報を書く。  
`python3 update.py`で更新する。  
`new_report.md`の内容が`reports/`以下に日付タイトルで保存され、`new_report.md`が`template.md`で更新される。  
`# TODO`の内容は翌日に持ち越される。 
勝手に削除とかはされないので、翌日不要ならリストからTODOを削除しておく。 
