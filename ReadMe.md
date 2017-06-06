# このソフトウェアについて

GitHubにログインするためのOTPを生成するツール。

# 開発環境

* Linux Mint 17.3 MATE 32bit
* [Python 3.4.3](https://www.python.org/downloads/release/python-343/)
* [SQLite](https://www.sqlite.org/) 3.8.2

## WebService

* [GitHub](https://github.com/)
    * [アカウント](https://github.com/join?source=header-home)
    * [AccessToken](https://github.com/settings/tokens)
    * [Two-Factor認証](https://github.com/settings/two_factor_authentication/intro)
    * [API v3](https://developer.github.com/v3/)

# 準備

* `GitHub.Accounts.sqlite`DBを用意する
    * 
        * `GitHubUserRegister.py insert -u username -p password -t two_factor_secret`
            * `./database/res/db/GitHub.Accounts.sqlite`

* `config.ini`ファイルのユーザ名を任意に指定する
```ini
[Default]
User=username
```

# 実行

iniファイルで指定したデフォルトユーザのOTPを標準出力する。
```sh
$ OtpCreator.py
```

起動引数で指定したユーザのOTPを標準出力する。

```sh
$ OtpCreator.py user0
```
```sh
username = user0
otp = 607040
```

そしてOTPの値だけはクリップボードにコピーされる。上記の例では`607040`がコピーされる。

## エラー

### 起動引数にもiniファイルにもユーザ名がない場合

```sh
$ OtpCreator.py
```
```sh
ユーザ名が必要です。しかし起動引数にもconfig.iniにも存在しません。起動引数なら第一引数にユーザ名を渡してください。iniならGitHubセクションUserキーにユーザ名を指定してください。
```

### DBに登録されていないユーザの場合

```sh
$ OtpCreator.py non-exist-username
```
```sh
ユーザ non-exist-username はDBのAccountsテーブルに存在しません。登録してから再度実行してください。
```
```sh
ユーザ non-exist-username はDBのTwoFactorsテーブルに存在しません。登録してから再度実行してください。
```

# ライセンス

このソフトウェアはCC0ライセンスである。

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)

Library|License|Copyright
-------|-------|---------
[requests](http://requests-docs-ja.readthedocs.io/en/latest/)|[Apache-2.0](https://opensource.org/licenses/Apache-2.0)|[Copyright 2012 Kenneth Reitz](http://requests-docs-ja.readthedocs.io/en/latest/user/intro/#requests)
[dataset](https://dataset.readthedocs.io/en/latest/)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2013, Open Knowledge Foundation, Friedrich Lindenberg, Gregor Aisch](https://github.com/pudo/dataset/blob/master/LICENSE.txt)
[bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)|[MIT](https://opensource.org/licenses/MIT)|[Copyright © 1996-2011 Leonard Richardson](https://pypi.python.org/pypi/beautifulsoup4),[参考](http://tdoc.info/beautifulsoup/)
[pytz](https://github.com/newvem/pytz)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2003-2005 Stuart Bishop <stuart@stuartbishop.net>](https://github.com/newvem/pytz/blob/master/LICENSE.txt)
[furl](https://github.com/gruns/furl)|[Unlicense](http://unlicense.org/)|[gruns/furl](https://github.com/gruns/furl/blob/master/LICENSE.md)
[PyYAML](https://github.com/yaml/pyyaml)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2006 Kirill Simonov](https://github.com/yaml/pyyaml/blob/master/LICENSE)
[pyperclip](https://github.com/asweigart/pyperclip)|[BSD 3-clause](https://github.com/asweigart/pyperclip/blob/master/LICENSE.txt)|[Copyright (c) 2014, Al Sweigart](https://github.com/asweigart/pyperclip/blob/master/LICENSE.txt)
