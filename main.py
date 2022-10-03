# https://www.odndo.com/posts/1627006679066/
# from logging import root
import threading
import tkinter 
from tkinter import ttk, messagebox
from tkinter.constants import FALSE


import time
import datetime

from sqlalchemy import null
# import schedule
import queue
import os

import recognition_for_gcp as stt
import label_object as lo

MIC_INDEX = 2#USER側の入力デバイスインデックス
MIXER_INDEX = 1#PC側の入力デバイスインデックス

SAVE_AUDIO = True #音源を保存するかしないか（ストレージ対策）
DIR_NAME = "speech_to_text_2121040"
AUDIO_PATH = DIR_NAME+"/AUDIO_FILE/"
day = datetime.datetime.now().strftime('%Y-%m-%d')+"/"
AUDIO_DIR_PATH = DIR_NAME+"/AUDIO_FILE/"+day#音源を保存する場所
LOG_DIR_PATH = DIR_NAME+"/LOG_FILE/"#ログを保存する場所

# ディレクトリが存在しない場合、ディレクトリを作成する
if not os.path.exists(DIR_NAME):
    os.makedirs(DIR_NAME)
if not os.path.exists(AUDIO_PATH): 
    os.makedirs(AUDIO_PATH)
if not os.path.exists(LOG_DIR_PATH):
    os.makedirs(LOG_DIR_PATH)
if not os.path.exists(AUDIO_DIR_PATH):
    os.makedirs(AUDIO_DIR_PATH)


ttsMIC = stt.Listen_print(MIC_INDEX,"USER", 1,AUDIO_DIR_PATH,LOG_DIR_PATH,SAVE_AUDIO)
ttsMIXER = stt.Listen_print(MIXER_INDEX,"PC",0,AUDIO_DIR_PATH,LOG_DIR_PATH,SAVE_AUDIO)

num = 0 
class Display_result():
    def __init__(self):
        self.fontsize = 10;self.fontcolour = "black"
        self.num_comment = 3;self.alpha = 1;bold = "bold"

        self.root = tkinter.Tk()
        ww = self.root.winfo_screenwidth()
        self.label_window_width = ww/7                              #ラベルの幅
        print(self.label_window_width)

        self.wh = self.root.winfo_screenheight()
        self.root.wm_attributes("-topmost", True)               # ウインドウを最前面へ
        self.root.wm_attributes("-transparentcolor", "white")   # ウインドウを設定
        self.root.attributes("-alpha",self.alpha)               # 全オブジェクトの透過度を設定:1-0
        self.root.title("TranScriptoWindow")   
        # self.root.protocol("WM_DELETE_WINDOW",  lambda: on_closing(self.root))# windowを閉じれないようにする
        self.root.geometry(str(int(self.label_window_width))+"x"+str(int(self.wh))+"+"+str(int((ww-self.label_window_width)))+"+0") 
        f = ttk.Frame(master=self.root, style="TP.TFrame", width=ww, height=self.wh)
         
                     
        self.mic_progres = tkinter.StringVar()
        self.mixer_progres = tkinter.StringVar()
        tmp = ttsMIC.get_progress_result()
        self.mic_progres.set(tmp)
        tmp = ttsMIXER.get_progress_result()
        self.mixer_progres.set(tmp)
        font_size = [0,20,15,9]
        text_size =[0,13,31,int(len(self.mic_progres.get()))]
        self.prog = [null, null, null]
        self.prog [0]= tkinter.StringVar();self.prog [1]= tkinter.StringVar();self.prog [2]= tkinter.StringVar()
        
        self.label_fontsize =  [20,15,9]
        self.label_textsize =  [13,31,int(len(self.mic_progres.get()))]
        self.mic_progress_text_Value = [tkinter.StringVar(),tkinter.StringVar(),tkinter.StringVar()]
        self.mix_progress_text_Value = [tkinter.StringVar(),tkinter.StringVar(),tkinter.StringVar()]
        self.mic_label = [null,null,null]
        self.mix_label = [null,null,null]
        place_y = [100,145,175]
        self.mic_label_place = [(30,place_y[0]),(30,place_y[1]),(30,place_y[2])]
        self.mix_label_place = [(0,place_y[0]+200),(0,place_y[1]+200),(0,place_y[2]+200)]

        self.label_pack = []

        self.micob = lo.label_ob(self.root,"start_for", 5, self.mic_label_place,self.label_window_width,"black",'#fafad2')
        self.mixob = lo.label_ob(self.root,"start_for_mix", 5,self.mix_label_place,self.label_window_width,'#FFFAFA',"darkcyan")
        self.comic=self.comix=0  
        # self.label_pack.append(self.micob )
        # self.label_pack.append(self.mixob )
        def add_label(text="", fontsize=1):
            mxla=self.mixob.get()
            mxhh = mxla[2].winfo_height()
            mxy = mxla[2].winfo_y( )
            global num
            for i, la in enumerate(self.label_pack):
                try:
                    for_label = self.label_pack[i+1]
                    hh = for_label[2].winfo_height()
                    y = for_label[2].winfo_y( )
                    la.move(y+hh)
                except BaseException as e:
                    l = la.get()
                    hh = l[2].winfo_height()
                    y = l[2].winfo_y( )
                    la.move_label(y+hh)
            dd =lo.label_ob(self.root,text,fontsize ,self.mix_label_place,self.label_window_width)
            dd.pp(0,mxy+mxhh)
            self.label_pack.append(dd)

        # self.schedule_s(add_label) 
 
        # backgroundカラーに設定されたオブジェクトを完全透過する
        ttk.Style().configure("TP.TFrame", background="white")
        f.pack() 
    #option_windowの設定        
        self.option_window = tkinter.Tk()
        self.option_window.wm_attributes("-topmost", True)
        self.option_window.geometry("300x300+"+str(int(ww/2-300/2))+"+"+str(int(self.wh/2-300/2)))
        self.option_window.title("Settings")
            
        lfontsize = ttk.Label(self.option_window, text="学籍番号", wraplength=ww)
        # lfontsize.pack()
        self.studentNum = tkinter.Entry(self.option_window, width=20)
        self.studentNum.insert(tkinter.END, "b2222000")
        # self.studentNum.pack()
        
        # ラベル
        lbl = tkinter.Label(self.option_window,text='マイクのデバイスインデックス')
        self.label_m=tkinter.Label(self.option_window,text="接続デバイス")
        
        self.index_mic_box = tkinter.Entry(self.option_window,width=20)
        self.index_mic_box.insert(0,"1")
        
        lbl.pack()
        self.index_mic_box.pack()
        self.label_m.pack()

        # ラベル
        lbl = tkinter.Label(self.option_window,text='サウンドミキサーのデバイスインデックス')
        self.txt = tkinter.Entry(self.option_window,width=20)
        self.txt.insert(0,"2")

        self.text_mx = tkinter.StringVar()
        self.text_mx.set("a")
        self.label_mx=tkinter.Label(self.option_window,text='接続デバイス')
        lbl.pack()
        self.txt.pack()
        self.label_mx.pack()
        
        btn = ttk.Button(self.option_window, text="Start Recognize", command=self.start_btn)
        applybtn = ttk.Button(self.option_window, text="Stop", command=self.stop_btn)  
        applybtn.pack(side=tkinter.BOTTOM,anchor=tkinter.W)
        btn.pack(side=tkinter.BOTTOM,anchor=tkinter.W)


        
        # スケールバー～ラベル位置（オプションをいくつか設定）
        self.scale_var = tkinter.IntVar()
        fontsiza_sv = tkinter.Scale(
                    self.option_window, 
                    variable = self.scale_var, 
                    command = self.slider_scroll,
                    # orient=tkinter.HORIZONTAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                    length = 100,           # 全体の長さ
                    width = 15,             # 全体の太さ
                    sliderlength = 20,      # スライダー（つまみ）の幅
                    from_ = -50, to = 700, # 最小値（開始の値 # 最大値（終了の値）
                    resolution=1,           # 変化の分解能(初期値:1)
                    tickinterval=0,        # 目盛りの分解能(初期値0で表示なし)
                    showvalue=False,        # スライダー上の値を非表示にする
                    label = "ラベル位置"
                    )
        # fontsiza_sv.pack(side=tkinter.LEFT)
         
        # # スケールバー～ラベル位置２（オプションをいくつか設定）（オプションをいくつか設定）
        self.scale_mic = tkinter.IntVar()
        fontsiza_sv= tkinter.Scale(
                    self.option_window, 
                    variable = self.scale_mic, 
                    command = self.slider_mic,
                    # orient=tkinter.HORIZONTAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                    length = 100,           # 全体の長さ
                    width = 15,             # 全体の太さ
                    sliderlength = 20,      # スライダー（つまみ）の幅
                    from_ = -50, to = 700, # 最小値（開始の値 # 最大値（終了の値）
                    resolution=1,           # 変化の分解能(初期値:1)
                    tickinterval=0,        # 目盛りの分解能(初期値0で表示なし)
                    showvalue=False,        # スライダー上の値を非表示にする
                    label = "二つ目",
                    )
        # fontsiza_sv.pack(side=tkinter.LEFT)
        
        # # スケールバー～透過度（オプションをいくつか設定）（オプションをいくつか設定）
        self.scale_alfa = tkinter.DoubleVar()
        self.scale_alfa.set(1.0)
        fontsiza_sv = tkinter.Scale(
                    self.option_window, 
                    variable = self.scale_alfa, 
                    command = self.slider_alfa,
                    # orient=tkinter.HORIZONTAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                    length = 100,           # 全体の長さ
                    width = 15,             # 全体の太さ
                    sliderlength = 20,      # スライダー（つまみ）の幅
                    from_ = 0, to = 1, # 最小値（開始の値 # 最大値（終了の値）
                    resolution=0.05,           # 変化の分解能(初期値:1)
                    tickinterval=0.5,        # 目盛りの分解能(初期値0で表示なし)
                    showvalue=False,        # スライダー上の値を非表示にする
                    label = "ラベル透過度"
                    )
        
        # fontsiza_sv.pack(side=tkinter.LEFT)
        self.root.mainloop()
    """
    def schedule_s(self, event):    
        global num
        num = num +1
        # 定期実行したい操作をまとめた関数
        schedule.every(60).seconds.do(event) # 10分毎  
    """
    
    def slider_scroll(self, event=0):
        '''スライダーを移動したとき'''
        self.scale_var.set(event)
        
        self.mixer_label.place(x=0, y=(100-self.num_comment*20-self.alpha)+int(self.scale_var.get()))  # -αは下のタスクバーの分
        # for i in range(3):
        #     self.mic_label[i].place(x=self.mic_label_place[i][0],y=self.mic_label_place[i][1]+num*3+int(self.scale_var.get()))
    
    def slider_mic(self, event=0):
        '''スライダーを移動したとき'''
        self.scale_mic.set(event)
        self.mic_label[0].place(x=0, y=(200-self.num_comment*20-self.alpha)+int(self.scale_mic.get()))  # -αは下のタスクバーの分

    def slider_alfa(self, event=0):
        self.scale_alfa.set(event)
        self.root.attributes("-alpha",self.scale_alfa.get())
     
    def update_stt_result(self):
        # tmp = str(ttsMIC.get_connected_device())
        # self.label_m.config(text = tmp)
        # tmp = ttsMIXER.get_connected_device()
        # self.label_mx.config(text =tmp)

        tmp = ttsMIC.get_progress_result()
        # self.mic_progres.set(tmp)
        self.micob.set_text_value(tmp)

        tmp = ttsMIXER.get_progress_result()
        # self.mixer_progres.set(tmp)
        self.mixob.set_text_value(tmp)

        #確定した認識結果を追加していくラベル
        def display_result_on_textbox(ttsObject, text_color,backcolor):
            mxla=self.mixob.get()
            mxhh = mxla[2].winfo_height()
            mxy = mxla[2].winfo_y( )
            for i, la in enumerate(self.label_pack):
                try:
                    for_label = self.label_pack[i+1]
                    hh = for_label[2].winfo_height()
                    y = for_label[2].winfo_y( )
                    la.move(y+hh)
                except BaseException as e:
                    l = la.get()
                    hh = l[2].winfo_height()
                    y = l[2].winfo_y( )
                    la.move_label(y+hh)
                    # print("Exception occurred - {}".format(str(e)))  
                    # print("on_error_sstupdate")
                    # print(e)
            dd =lo.label_ob(self.root,ttsObject.get_result(),2 ,self.mix_label_place, self.label_window_width,text_color, backcolor)
            dd.pp(0,mxy+mxhh)
            self.label_pack.append(dd)
            
        if(ttsMIXER.get_condition()):
            self.comix+=1
            # self.mixerttmp = self._data[ttsMIXER.get_deviceName_or_number(1)]
            self.mixerttmp = ttsMIXER.get_chrCount()
            print(self.mixerttmp)
            # display_result_on_textbox(ttsMIXER,'#FFFAFA',"darkcyan") 
            ttsMIXER.init_object()
            print(str(self.comic)+str(self.comix)+str(threading.active_count))

        if(ttsMIC.get_condition()):
            self.comic+=1
            # self.mictmp = self._data[ttsMIC.get_deviceName_or_number(1)]
            self.mixerttmp = ttsMIC.get_chrCount()
            # self.add_label()
            # display_result_on_textbox(ttsMIC,"black",'#fafad2')   
            ttsMIC.init_object()
            # schedule.run_pending()

        self.root.after(10, self.update_stt_result)

    def stop_btn(self):
        ttsMIXER.set_stt_status(False)
        ttsMIC.set_stt_status(False)
        self.option_window.destroy()
        self.root.destroy()

    def start_btn(self):
        # テキストボックス内の値を取得
        index=self.index_mic_box.get()
        ttsMIC.set_stt_device_index(index)
        index=self.txt.get()
        ttsMIXER.set_stt_device_index(index)
        
        # sttの初期化
        ttsMIC.init_object()
        ttsMIXER.init_object()

        t1 = threading.Thread(target=ttsMIC.start_recognize, daemon=True)
        t1.start()
        time.sleep(5)#これを入れないとpysimpleGUIのWindowがクラッシュする
        t2 = threading.Thread(target=ttsMIXER.start_recognize, daemon=True)
        t2.start()
        time.sleep(5)
        
        tmp = str(ttsMIC.get_connected_device())
        # print(tmp+"aaa")
        self.label_m.config(text = tmp)
        tmp2 = str(ttsMIXER.get_connected_device())
        self.label_mx.config(text = tmp2)

        thread_dict=dict()
        error_queue = queue.Queue()
        # thread_dict[name] = ExcThread(error_queue, name)
        ttsMIC.set_progress_result("【・・】")
        ttsMIXER.set_progress_result("【・・】")
        
        self.root.after(1, self.update_stt_result)# self.update_stt_resultに移動する

        # subf.destroy()
        device_INDEX_MIKISER = 0
        device_INDEX_MIC = 2

if __name__ == '__main__':
    # draw_window()
    aa = Display_result()