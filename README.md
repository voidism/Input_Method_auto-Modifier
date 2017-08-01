Modify Input Type Automatically 自動切換輸入法程式
===

> Mon, Jul 31, 2017 5:48 PM

## 程式效果
- 使用英文輸入法鍵入兩個中文字之按鍵組合時，會自動切換成中文輸入法，並幫你刪錯字再重新輸入原本想打的字
- 英文效果亦同，但為避免誤換輸入法，只有在輸入字庫中的單字時，才會轉換成英文輸入法，字庫會自動新增單字 (詳見 [關於字庫](https://hackmd.io/JwMwpgzAhgRgxgRgLTCgDjEgLGgrBJKKONJEABgXJgHYaAmANmGHKA==?both#關於字庫) )
- 應該有比[微軟內建自動切換](https://answers.microsoft.com/zh-hant/windows/forum/windows_10-ime/windows-10/cda818ad-1081-4165-89cd-6d43349c4b9a)好用87倍
<!--
(內建是只要輸入沒有對應合法中文就直接跳成英文QQ)
-->

![GIF](http://i.imgur.com/s8SDrcZ.gif)
## 環境需求(Windows)
- 有[Python2.7](https://www.python.org/downloads/)
- [PyHook](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook)
(下載 pyHook‑1.5.1‑cp27‑cp27m‑win32.whl 
*#如果你python裝的是64bit，可以載amd64的*
然後在檔案目錄`pip install pyHook‑1.5.1‑cp27‑cp27m‑win32.whl`)
- [pythoncom (附在pypiwin32裡面)](https://pypi.python.org/pypi/pypiwin32/219)
(下載 pypiwin32-219-cp27-none-win32.whl
*#如果你python裝的是64bit，可以載amd64的*
然後在檔案目錄`pip install pypiwin32-219-cp27-none-win32.whl`)
- [PyUserInput](https://pypi.python.org/pypi/PyUserInput/)
(下載 PyUserInput-0.1.11-py2-none-any.whl ，然後`pip install PyUserInput-0.1.11-py2-none-any.whl`)
- PyAutoGUI
(有內建，直接`pip install pyautogui`就好)
- requests
(有內建，直接`pip install requests`就好)

※ 以上建議在[虛擬環境](https://hackmd.io/s/HycT9L68W)中裝設，會比較乾淨

## 前置作業
由於微軟新注音輸入法不是什麼開源的軟體，一般情況下程式沒有方法可以取得當前的輸入法，所以要用PyAutoGUI來偷吃步：

1. 找到工具列右下角顯示中英文輸入法的地方
2. 找到一個像素位置，當中文輸入時是白色，英文輸入時是黑色(黑色的RGB值須分別皆大於200)
p.s. 我是選英字撇捺中間的地方

<center class="half">
<img src="https://i.imgur.com/S4X7hl3.png">
<img src="https://i.imgur.com/Sj8buTE.png">
</center>

3. 用[Hook.py]()來查看該像素格的座標位置
    (Hook.py需在環境建置好之後才能用)
    
Hook.py會不斷更新顯示滑鼠游標的座標位置及RGB值：
```
---
Position: (1361, 1002) #-->座標位置
RGB: (270, 270, 270)   #-->RGB值
---
```
4. 將[ModifyInputType.py]()程式碼128行的`pixel=(1683, 1063)`改成你自己取得的pixel位置
5. If it's stupid but it works, it isn't stupid.

## 啟動
就直接執行 `ModifyInputType.py`

如果有使用virtualenv，可以寫一個bat檔，像這樣：
```dockerfile=
@echo off
cmd /k "cd /d C:\path\to\your\virtualenv_location\Scripts & activate & cd /d  C:\path\to\to\your\file & python ModifyInputType.py"
```
之後就不用先開虛擬環境再執行囉，可以直接執行或是設定排程。

## 結束

直接關閉視窗
或是輸入`enter, z, x, c, v` 跳出程序回到cmd

## 關於字庫
- 取用自Mac及Linux的內建字庫，原有45000餘字，刪去"so", "up", "go"...等會與中文輸入混淆的字( so: "ㄋㄟ", up: "ㄧㄣ", go: "ㄕㄟ"...)
- 當使用者使用中文輸入法打進一串英文字，但因英文字並不在字庫裡，所以沒有自動切換輸入法時，使用者通常會手動按shift切輸入法，這時剛剛所打的那串英文字會自動新增到字庫裡。因此使用者可藉此新增單字
- 另外可藉由[Dictionary_Add&Del.py]()的GUI介面來找查或新增刪除字庫內的字

![](http://i.imgur.com/mxGEGIZ.gif)

