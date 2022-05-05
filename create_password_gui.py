"""    作成日
        2022/5/1

    使用モジュール
        PySimpleGUI:PythonでGUIを構築するためのライブラリです．
                    数あるGUIライブラリの中でも最も使いやすいものの1つだと思います．
        string：空白文字や英小文字や数字などが定義されている
        secrets：パスワードやアカウント認証、セキュリティトークンなどの機密を扱うのに適した、暗号学的に強い乱数を生成することができます。
                 特に、 random モジュールのデフォルトの擬似乱数ジェネレータよりも secrets を使用するべきです。
                 random モジュールはモデル化やシミュレーション向けで、セキュリティや暗号学的に設計されてはいません。
        pyperclip：Pythonでクリップボードに文字列（テキスト）をコピーしたりクリップボードから文字列をペースト（取得）したりする

    文字列定数参考url：https://docs.python.org/ja/3/library/string.html#string.ascii_lowercase
        string.ascii_lowercase：小文字 'abcdefghijklmnopqrstuvwxyz'
        string.ascii_uppercase：大文字 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        string.digits：文字列 '0123456789'
        string.punctuation：区切り文字として扱われるASCII文字の文字列 !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
                        　　注意：区切り文字はアプリによっては使用不可の場合がある

    文字列乱数生成参考url：https://docs.python.org/ja/3/library/secrets.html
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(8))

"""

import PySimpleGUI as sg
import string
import secrets
import re
import pyperclip as pyperclip


def main():
    # ウィンドウの内容を定義する_
    sg.theme("default1")  # テーマ色指定。sg.theme_previewer()を実行するとテーマ一覧が起動して確認できる
    choices = ("１：小文字", "２：小文字＋大文字", "３：小文字＋大文字＋数字", "４：小文字＋大文字＋数字＋記号", "５：数字")  # リストの中身
    layout = [[sg.Text(" ")], [sg.Text("パスワード文字数（6～24）"), sg.Input(size=(10, 1), default_text="8", key='-文字数-')],
              [sg.Text("パスワード文字組合せ"), sg.Listbox(choices, size=(30, len(choices)), default_values=["１：小文字"],
                                                 key='-文字種-')],
              [sg.Text(" ")], [sg.Text(size=(65, 1), key='-出力-')],
              [sg.Text("　　　　　　　　"), sg.Button(' 生成 '), sg.Text("　　　"), sg.Button(' 終了 ')]]

    # ウィンドウを作成する
    window = sg.Window('パスワード生成', layout)

    # イベントループを使用してウィンドウを表示し、対話する
    while True:
        event, values = window.read()
        # ユーザーが終了したいのか、ウィンドウが閉じられたかどうかを確認してください
        if event == sg.WINDOW_CLOSED or event == ' 終了 ':
            break

        # ユーザーが入力した条件でパスワードを生成する
        count = str(values["-文字数-"])  # 数字以外の入力除外のため一旦文字列に変換
        if count.isdecimal():  # .isdecimal():文字列がすべて数字かどうかを判定する
            count = int(values["-文字数-"])
            number = str(values["-文字種-"][0])
            if 6 <= count <= 24:
                if number == "１：小文字":
                    character = string.ascii_lowercase
                    password = ''.join(secrets.choice(character) for _ in range(count))
                elif number == "２：小文字＋大文字":
                    character = string.ascii_lowercase + string.ascii_uppercase
                    password = ''.join(secrets.choice(character) for _ in range(count))
                    if check_password(password, number):  # パスワードが指定通りに生成されているかチェック
                        window['-出力-'].update("パスワード生成に失敗しました。もう一度 生成してください")
                        continue
                elif number == "３：小文字＋大文字＋数字":
                    character = string.ascii_lowercase + string.ascii_uppercase + string.digits
                    password = ''.join(secrets.choice(character) for _ in range(count))
                    if check_password(password, number):  # パスワードが指定通りに生成されているかチェック
                        window['-出力-'].update("パスワード生成に失敗しました。もう一度 生成してください")
                        continue
                elif number == "４：小文字＋大文字＋数字＋記号":
                    character = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
                    password = ''.join(secrets.choice(character) for _ in range(count))
                    if check_password(password, number):  # パスワードが指定通りに生成されているかチェック
                        window['-出力-'].update("パスワード生成に失敗しました。もう一度 生成してください")
                        continue
                elif number == "５：数字":
                    character = string.digits
                    password = ''.join(secrets.choice(character) for _ in range(count))

                window['-出力-'].update('パスワード： 「 ' + password + " 」クリップボードにコピーしました")
                pyperclip.copy(password)  # クリップボードにコピー

            else:
                window['-出力-'].update('６～２４桁で指定してください ')
        else:
            window['-出力-'].update('パスワード文字数は ６～２４ の整数で指定してください ')
    # 画面から削除して終了
    window.close()


def check_password(verify_password, verify_number):  # 生成されたパスワードが条件を満たしているかを確認する
    is_match = [0, 0, 0, 0]  # 小文字、大文字、数字、記号があれば各要素に1をセット
    for c in verify_password:
        if re.match(r'[a-z]', c):  # 小文字であれば
            is_match[0] = 1
        elif re.match(r'[A-Z]', c):  # 大文字であれば
            is_match[1] = 1
        elif re.match(r'[0-9]', c):  # 数字であれば
            is_match[2] = 1
        elif re.match(r'[!-/:-~]', c):  # 記号であれば
            is_match[3] = 1
    # 条件満たしていなければTrueを返す
    if verify_number == "２：小文字＋大文字":
        if is_match != [1, 1, 0, 0]:
            return True
    if verify_number == "３：小文字＋大文字＋数字":
        if is_match != [1, 1, 1, 0]:
            return True
    if verify_number == "４：小文字＋大文字＋数字＋記号":
        if is_match != [1, 1, 1, 1]:
            return True
    return False


if __name__ == "__main__":  # よくわからないがおまじない → create_password_gui.pyを直接実行した時と importされたことで動作したものと区別するための記述
    main()
