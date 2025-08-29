from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.constants import *
from tkinter import filedialog
from translate import Translator
import os
import sys
import speech_recognition as sr


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)


def import_(event):
    path = filedialog.askopenfile(initialdir='/', title='Select file',
                                  filetypes=(('txt files', '*.txt'),))
    if path is not None:
        input_text.insert(END, path.read())
        update(0)


def export(event):
    path = filedialog.asksaveasfile(initialdir='/', title='Save file',
                                    filetypes=(('txt file', '*.txt'),
                                               ('all files', '*.*')))
    if path is not None:
        path.write(result_text.get('1.0', 'end'))
        update(0)


def close(event):
    window.destroy()


def undo(event):
    try:
        input_text.edit_undo()
        update(0)
    except TclError:
        messagebox.showerror('error', 'There is nothing to undo.')


def redo(event):
    try:
        input_text.edit_redo()
        update(0)
    except TclError:
        messagebox.showerror('error', 'There is nothing to redo.')


def cut(event):
    try:
        selected = input_text.selection_get()
    except:
        selected = ''
    if selected:
        window.clipboard_clear()
        window.clipboard_append(selected)
        input_text.delete('sel.first', 'sel.last')
        update(0)


def copy(event):
    try:
        selected = input_text.selection_get()
    except:
        selected = ''
    if selected:
        window.clipboard_clear()
        window.clipboard_append(selected)


def paste(event):
    try:
        cliptext = window.clipboard_get()
    except:
        cliptext = ''
    position = input_text.index(INSERT)
    input_text.insert(position, cliptext)
    update(0)


def select_all(event=None):
    input_text.focus()
    input_text.tag_add(SEL, '1.0', END)
    input_text.mark_set(INSERT, '1.0')
    input_text.see(INSERT)

def delete(event):
    input_text.delete('1.0', 'end')
    update(0)


def swap_langs():
    if input_lang.get() == 'تشخیص خودکار':
        messagebox.showerror('خطا', '.برای زبان خروجی نمیتوانید از تشخیص خودکار استفاده کنید')
        return
    if swap_img.cget('file')==resource_path('assets/swap_left.png'):
        swap_img.configure(file=resource_path('assets/swap_right.png'))
        input_lang_cb.place(width=75, height=30, x=5, y=245)
        result_lang_cb.place(width=75, height=30, x=105, y=245)
    else:
        swap_img.configure(file=resource_path('assets/swap_left.png'))
        input_lang_cb.place(width=75, height=30, x=105, y=245)
        result_lang_cb.place(width=75, height=30, x=5, y=245)
    temporary_input_lang = input_lang.get()
    input_lang.set(result_lang.get())
    result_lang.set(temporary_input_lang)


def minimize(event):
    window.iconify()


def style_azlight():
    try:
        window.tk.call('set_theme', 'light')
    except TclError:
        messagebox.showerror('خطا', '.مشکلی پیش آمده است، لطفا بعدا دوباره تلاش کنید')
        return


def style_azdark():
    try:
        window.tk.call('set_theme', 'dark')
    except TclError:
        messagebox.showerror('خطا', '.مشکلی پیش آمده است، لطفا بعدا دوباره تلاش کنید')
        return
    else:
        style.configure('S.TButton', padding=0)
        style.configure('TCheckbutton', font=('calibri', font_size-2, 'normal'))
        style.configure('TButton', font=('calibri', font_size, 'normal'))


def zoom(event, type_):
    global font_size
    label1_x = int(label1.place_info().get('x'))
    label2_x = int(label2.place_info().get('x'))
    
    if type_=='in':
        if font_size<=20:
            font_size += 1
            label1.place(height=30, x=label1_x-5, y=0)
            label2.place(height=30, x=label2_x-7, y=250)
    elif type_=='out':
        if font_size>=8:
            font_size-=1
            label1.place(height=30, x=label1_x+5, y=0)
            label2.place(height=30, x=label2_x+7, y=250)
    elif type_=='actual_size':
        font_size=12
        label1.place(height=30, x=440, y=0)
        label2.place(height=30, x=415, y=250)
    else:
        return

    label1.configure(font=('calibri', font_size, 'bold'))
    label2.configure(font=('calibri', font_size, 'bold'))
    input_text.configure(font=('calibri', font_size, 'normal'))
    result_text.configure(font=('calibri', font_size, 'normal'))
    style.configure('TButton', font=('calibri', font_size, 'normal'))
    input_lang_cb.configure(font=('calibri', font_size-4, 'normal'))
    result_lang_cb.configure(font=('calibri', font_size-4, 'normal'))
    charCount.configure(font=('B nazanin', font_size, 'normal'))
    style.configure('TCheckbutton', font=('calibri', font_size-2, 'normal'))
    try:
        label_guide.configure(font=('B nazanin', font_size+3, 'normal'))
    except:
        pass


def zoom_in(event):
    zoom(0, 'in')


def zoom_out(event):
    zoom(0, 'out')


def actual_size(event):
    zoom(0, 'actual_size')


def about_us():
    messagebox.showinfo('درباره ما', 'برنامه نویسی شده توسط ستایش قدیری،سارینا ستوده از مدرسه خرد')


def guide():
    global label_guide
    guide_window = Toplevel()
    guide_window.geometry('750x770')
    guide_window.title('راهنما')
    guide_window.resizable(False, False)

    label_guide = Text(guide_window, font=('B nazanin', font_size+3, 'normal'),
                       padx=20, pady=10, relief='ridge', borderwidth=3)
    label_guide.tag_configure('tag-right', justify='right')
    label_guide.insert(END, '''برای اینکه متن خود را ترجمه کنید، ابتدا زبان متن ورودی و زبانی که می‌خواهید به آن ترجمه کنید را انتخاب کنید 
    (برای زبان ورودی می‌توانید از گزینه تشخیص خودکار هم استفاده کنید) 
    سپس متن خود را درون بخش «متن ورودی» تایپ کنید و دکمه ترجمه را بزنید


    برای پاک کردن متن ورودی دکمه حذف را بزنید سپس دکمه ترجمه را بزنید

   اگر می‌خواهید همزمان که تایپ می‌کنید، متنتان ترجمه شود، گزینه ترجمه‌ی همزمان را روشن کنید
  در صورتی که سیستمتان قوی نباشد این گزینه امکان دارد باعث کندی برنامه شود و در این صورت)
  (بهتر است این گزینه را خاموش نگه دارید
  برای ترجمه گفتاری ابتدا زبان ورودی را انتخاب کنید و بعد دکمه میکروفن را بزنید
  سپس لهجه کشور مورد نظرتان را انتخاب کنید و بعد از اینکه میکروفن روشن شد، عبارت خود را بیان کنید
  انتخاب کنيد swap langueges<--Editبرای جابه‌جا کردن زبان‌ها، دکمه بین زبان‌ها را بزنید یا از منو 

    :گزینه‌های دیگر
   .را انتخاب کنید import-->  file از منو txt برای وارد کردن فایل
   .را انتخاب کنید export-->  file از منو txtبرای ذخیره کردن فایل به قالب
   را انتخاب کنید.  style -->  window برای تغییر استایل (تم تیره یا روشن) از منو

   -کلید های میانبر-
   (به خاطر داشته باشيد موقع استفاده از کلید های میانبر، زبان کیبورد خود را به زبان انگلیسی تغییر دهید)
   Ctrl+I --> وارد کردن فایل
   Ctrl+E--> txt ذخیره کردن فایل به قالب
   Ctrl+W--> بستن پنجره
   Ctrl+Z --> برگرداندن به حالت قبلی
   Ctrl+Y--> اخرین عملکرد را دوباره انجام میدهد
   Ctrl+X--> کات کردن
   Ctrl+C--> مورد یا متن را کپی میکند
   Ctrl+V--> مورد یا متن کپی شده یا کات شده را پیست میکند
   Ctrl+T-->  متن نوشته شده را ترجمه میکند
   Ctrl+backspace--> متن نوشته شده را حذف میکند
   Ctrl+M-->  صفحه باز شده را به تسک بار میبرد
   Ctrl++--> افزایش سایز گزینه‌ها
   Ctrl-+--> کاهش سایز گزینه‌ها
   Ctrl+0--> برگشت به سایز پیش‌فرض
   ''')
    label_guide.tag_add('tag-right', 1.0, 'end')
    label_guide.configure(state=DISABLED)
    guide_scrollbar = ttk.Scrollbar(guide_window, orient=VERTICAL,
                                    command=label_guide.yview)
    label_guide.config(yscrollcommand=guide_scrollbar.set)
    label_guide.pack(side=LEFT, fill=Y)
    guide_scrollbar.place(height=770, x=750-20, y=15)


def translate(event):
    limit = len(input_text.get('1.0', 'end'))
    if limit >= 500:
        messagebox.showerror('Error', 'character limit: 500, try again')
        return
    pos_from_lang = languages_v.index(input_lang.get())
    pos_to_lang = languages_v.index(result_lang.get())
    options = Translator(from_lang=languages_k[pos_from_lang],
                         to_lang=languages_k[pos_to_lang],
                         email='sarina.sotoodeh@yahoo.com')
    try:
        translate = options.translate(input_text.get('1.0', 'end'))
    except:
        messagebox.showerror('شما آفلاین هستید', '.اینترنت خود را چک کنید و دوباره تلاش کنید')
    else:
        result_text.configure(state=NORMAL)
        result_text.delete('1.0', 'end')
        result_text.insert(END, translate)
        result_text.configure(state=DISABLED)


def update(event):
    var.set(str(len(input_text.get('1.0', 'end'))))


def auto_translate():
    global funcid
    if auto_translate_var.get():
        funcid = input_text.bind('<KeyRelease>', translate)
    else:
        input_text.unbind('<KeyRelease>', funcid)        


def define_speech_language():
    global language_window_is_open

    def country_btn_pressed(country):
        language_window.destroy()
        for i in language_list:
            if i[0] == country:
                speech_lang = i[1]
                mic_btn.after(500, lambda: set_mic_img(speech_lang))
                break
        else:
            messagebox.showerror('خطا', '.لطفا بعدا دوباره تلاش کنید')

    def language_window_status():
        global language_window_is_open
        language_window_is_open = False
        language_window.destroy()

    if input_lang.get() not in voice_langs.keys():
            messagebox.showerror('خطا', 'متاسفانه گزینه ترجمه گفتاری برای زبان ورودی که انتخاب کرده‌اید فعال نیست')
            return

    if language_window_is_open:
        return

    language_list = voice_langs[input_lang.get()]
    language_window = Toplevel()
    language_window_is_open = True
    language_window.protocol('WM_DELETE_WINDOW', language_window_status)
    language_window.title('انتخاب لهجه')
    btn_column = 0
    btn_row = 1
    for i in language_list:
        country_btn = ttk.Button(language_window, text=i[0],
                                 command=lambda: country_btn_pressed(i[0]))
        country_btn.grid(column=btn_column, row=btn_row, padx=1, pady=1)
        btn_column += 1
        if btn_column > 4:
            btn_row += 1
            btn_column = 0
    lbl_columnspan = btn_column if btn_row == 1 else 5
    country_lbl = ttk.Label(language_window, justify='right',
                            text='به لهجه کدام کشور می‌خواهید حرف بزنید؟',
                            font=('calibri', font_size+2, 'normal'))
    country_lbl.grid(column=0, row=0, columnspan=lbl_columnspan, pady=4)


def set_mic_img(speech_lang):
    if mic_img.cget('file')==resource_path('assets/mic.png'):
        mic_img.configure(file=resource_path('assets/mic_fill.png'))
        mic_btn.after(1, lambda: mic(speech_lang))
    else:
        return


def mic(speech_lang):
    recognizer = sr.Recognizer()
    try:
        mic = sr.Microphone()
    except AttributeError:
        messagebox.showerror('خطا', '.را نصب کنید pyaudio اگر میخواهید از سورس کد استفاده کنید کتابخانه')
        return
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    mic_img.configure(file=resource_path('assets/mic.png'))
    mic_btn.after(10, lambda: speech_to_text(speech_lang, recognizer, audio))


def speech_to_text(speech_lang, recognizer, audio):
    global language_window_is_open
    try:
        text = recognizer.recognize_google(audio, language=speech_lang)
    except sr.RequestError:
        messagebox.showerror('شما آفلاین هستید', '.اینترنت خود را چک کنید و دوباره تلاش کنید')
    except sr.UnknownValueError:
        messagebox.showerror('خطا', '.دوباره تکرار کنید')
    else:
        position = input_text.index(INSERT)
        input_text.insert(position, text)
        update(0)
    finally:
        language_window_is_open = False


languages = {'autodetect': 'تشخیص خودکار', 'af': 'Afrikaans', 'sq': 'Albanian',
             'am': 'Amharic', 'ar': 'Arabic', 'hy': 'Armenian', 'az':
             'Azerbaijani', 'ba': 'Bashkir', 'bn': 'Bengali', 'bs': 'Bosnian',
             'bg': 'Bulgarian', 'ca': 'Catalan', 'zh': 'Chinese',
             'en': 'English', 'et': 'Estonian', 'fi': 'Finnish', 'fr': 'French',
             'gl': 'Galician', 'ka': 'Georgian', 'de': 'German', 'el': 'Greek',
             'he': 'Hebrew', 'hi': 'Hindi', 'hu': 'Hungarian', 'id':
             'Indonesian', 'ga': 'Irish', 'ig': 'Igbo', 'is': 'Icelandic',
             'it': 'Italian', 'iu': 'Inuktitut', 'ja': 'Japanese', 'ko':
             'Korean', 'la': 'Latin', 'lv': 'Latvian', 'mk': 'Macedonian',
             'mt': 'Maltese', 'mn': 'Mongolian', 'fa': 'Persian', 'pl':
             'Polish', 'ps': 'Pashto, Pushto', 'pt': 'Portuguese', 'ro':
             'Romanian', 'ru': 'Russian', 'sr': 'Serbian', 'gd':
             'Scottish Gaelic', 'sk': 'Slovak', 'so': 'Somali', 'es': 'Spanish',
             'sw': 'Swahili', 'sv': 'Swedish', 'tg': 'Tajik', 'th': 'Thai',
             'bo': 'Tibetan', 'tk': 'Turkmen', 'tr': 'Turkish', 'uk':
             'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek', 'vi': 'Vietnamese',
             'yo': 'Yoruba', 'zu': 'Zulu'}
languages_v = list(languages.values())
languages_k = list(languages.keys())
voice_langs = {
  'Afrikaans': [
    ['South Africa', 'af-ZA']
  ],
  'Arabic': [
    ['Algeria','ar-DZ'],
    ['Bahrain','ar-BH'],
    ['Egypt','ar-EG'],
    ['Israel','ar-IL'],
    ['Iraq','ar-IQ'],
    ['Jordan','ar-JO'],
    ['Kuwait','ar-KW'],
    ['Lebanon','ar-LB'],
    ['Morocco','ar-MA'],
    ['Oman','ar-OM'],
    ['Palestinian Territory','ar-PS'],
    ['Qatar','ar-QA'],
    ['Saudi Arabia','ar-SA'],
    ['Tunisia','ar-TN'],
    ['UAE','ar-AE']
  ],
  'Bulgarian': [
    ['Bulgaria', 'bg-BG']
  ],
  'Catalan': [
    ['Spain', 'ca-ES']
  ],
  'Chinese': [
    ['China (Simp.)', 'cmn-Hans-CN'],
    ['Hong Kong SAR (Trad.)', 'cmn-Hans-HK'],
    ['Taiwan (Trad.)', 'cmn-Hant-TW']
  ],
  'Danish': [
    ['Denmark', 'da-DK']
  ],
  'English': [
    ['Australia', 'en-AU'],
    ['Canada', 'en-CA'],
    ['India', 'en-IN'],
    ['Ireland', 'en-IE'],
    ['New Zealand', 'en-NZ'],
    ['Philippines', 'en-PH'],
    ['South Africa', 'en-ZA'],
    ['United Kingdom', 'en-GB'],
    ['United States', 'en-US']
  ],
  'Persian': [
    ['Iran', 'fa-IR']
  ],
  'French': [
    ['France', 'fr-FR']
  ],
  'Filipino': [
    ['Philippines', 'fil-PH']
  ],
  'Galician': [
    ['Spain', 'gl-ES']
  ],
  'German': [
    ['Germany', 'de-DE']
  ],
  'Greek': [
    ['Greece', 'el-GR']
  ],
  'Finnish': [
    ['Finland', 'fi-FI']
  ],
  'Hebrew' :[
    ['Israel', 'he-IL']
  ],
  'Hindi': [
    ['India', 'hi-IN']
  ],
  'Hungarian': [
    ['Hungary', 'hu-HU']
  ],
  'Indonesian': [
    ['Indonesia', 'id-ID']
  ],
  'Icelandic': [
    ['Iceland', 'is-IS']
  ],
  'Italian': [
    ['Italy', 'it-IT'],
    ['Switzerland', 'it-CH']
  ],
  'Japanese': [
    ['Japan', 'ja-JP']
  ],
  'Korean': [
    ['Korea', 'ko-KR']
  ],
  'Polish': [
    ['Poland', 'pl-PL']
  ],
  'Portuguese': [
    ['Brazil', 'pt-BR'],
    ['Portugal', 'pt-PT']
  ],
  'Romanian': [
    ['Romania', 'ro-RO']
  ],
  'Russian': [
    ['Russia', 'ru-RU']
  ],
  'Serbian': [
    ['Serbia', 'sr-RS']
  ],
  'Slovak': [
    ['Slovakia', 'sk-SK']
  ],
  'Spanish': [
    ['Argentina', 'es-AR'],
    ['Bolivia', 'es-BO'],
    ['Chile', 'es-CL'],
    ['Colombia', 'es-CO'],
    ['Costa Rica', 'es-CR'],
    ['Dominican Republic', 'es-DO'],
    ['Ecuador', 'es-EC'],
    ['El Salvador', 'es-SV'],
    ['Guatemala', 'es-GT'],
    ['Honduras', 'es-HN'],
    ['México', 'es-MX'],
    ['Nicaragua', 'es-NI'],
    ['Panamá', 'es-PA'],
    ['Paraguay', 'es-PY'],
    ['Perú', 'es-PE'],
    ['Puerto Rico', 'es-PR'],
    ['Spain', 'es-ES'],
    ['Uruguay', 'es-UY'],
    ['United States', 'es-US'],
    ['Venezuela', 'es-VE']
  ],
  'Swedish': [
    ['Sweden', 'sv-SE']
  ],
  'Thai': [
    ['Thailand', 'th-TH']
  ],
  'Turkish': [
    ['Turkey', 'tr-TR']
  ],
  'Ukrainian': [
    ['Ukraine', 'uk-UA']
  ],
  'Vietnamese': [
    ['Viet Nam', 'vi-VN']
  ],
  'Zulu': [
    ['South Africa', 'zu-ZA']
  ]
}

window = Tk()
window.geometry('510x490')
window.resizable(False, False)
window.title('مترجم')
window.tk.call('source', resource_path('assets/themes/Azure/azure.tcl'))
window.tk.call('set_theme', 'light')
font_size = 12
window.option_add('*font', ('calibri', font_size, 'normal'))

menubar = Menu(window)

file = Menu(menubar, tearoff=0)
file.add_command(label='Import...', accelerator='Ctrl+I', command=lambda:
                 import_(0))
window.bind('<Control-i>', import_)
file.add_command(label='Export...', accelerator='Ctrl+E', command=lambda:
                 export(0))
window.bind('<Control-e>', export)
file.add_separator()
file.add_command(label='Close', accelerator='Ctrl+W', command=lambda: close(0))
window.bind('<Control-w>', close)
menubar.add_cascade(label='File', menu=file)

edit = Menu(menubar, tearoff=0)
edit.add_command(label='Undo', accelerator='Ctrl+Z', command=lambda: undo(0))
window.bind('<Control-z>', undo)
edit.add_command(label='Redo', accelerator='Ctrl+Y', command=lambda: redo(0))
window.bind('<Control-y>', redo)
edit.add_separator()
edit.add_command(label='Cut', accelerator='Ctrl+X', command=lambda: cut(0))
window.bind('<Control-x>', cut)
edit.add_command(label='Copy', accelerator='Ctrl+C', command=lambda: copy(0))
window.bind('<Control-c>', copy)
edit.add_command(label='Paste', accelerator='Ctrl+V', command=lambda: paste(0))
edit.add_command(label='Select All', underline=7, accelerator='Ctrl+A',
                 command=select_all)
window.bind('<Control-a>', select_all)
edit.add_separator()
edit.add_command(label='Translate', accelerator='Ctrl+T',
                 command=lambda: translate(0))
window.bind('<Control-t>', translate)
edit.add_command(label='Clear Input Text', accelerator='Ctrl+BackSpace',
                 command=lambda: delete(0))
window.bind('<Control-BackSpace>', delete)
edit.add_command(label='Swap Languages', command=swap_langs)
menubar.add_cascade(label='Edit', menu=edit)

window_m = Menu(menubar, tearoff=0)
window_m.add_command(label='Minimize', accelerator='Ctrl+M',
                     command=lambda: minimize(0))
window.bind('<Control-m>', minimize)
style_menu = Menu(menubar, tearoff=0)
style_menu.add_command(label='light', command=style_azlight)
style_menu.add_command(label='dark', command=style_azdark)
window_m.add_cascade(label='Style', menu=style_menu)
window_m.add_separator()
window_m.add_command(label='Zoom in', accelerator='Ctrl++',
                     command=lambda: zoom_in(0))
window.bind('<Control-=>', zoom_in)
window_m.add_command(label='Zoom out', accelerator='Ctrl+-',
                     command=lambda: zoom_out(0))
window.bind('<Control-minus>', zoom_out)
window_m.add_command(label='Actual Size', accelerator='Ctrl+0',
                     command=lambda: actual_size(0))
window.bind('<Control-0>', actual_size)
menubar.add_cascade(label='Window', menu=window_m)

help_ = Menu(menubar, tearoff=0)
help_.add_command(label='About us', command=about_us)
help_.add_command(label='Guide', command=guide)
menubar.add_cascade(label='Help', menu=help_)
window.config(menu=menubar)

label1 = ttk.Label(window, text=':متن ورودی', font=('calibri', font_size, 'bold'),
                   justify='right')
label1.place(height=30, x=440, y=0)
label2 = ttk.Label(window, text=':متن ترجمه شده', font=('calibri', font_size, 'bold'),
                   justify='right')
label2.place(height=30, x=415, y=250)

input_text = Text(window, padx=20, pady=20, wrap='word', relief='ridge',
                  borderwidth=3, undo=True, font=('calibri', font_size, 'normal'))
input_text.place(width=500, height=200, x=5, y=35)
result_text = Text(window, padx=20, pady=20, relief='ridge', borderwidth=3,
                   undo=True, state=DISABLED, font=('calibri', font_size, 'normal'))
result_text.place(width=500, height=200, x=5, y=285)

input_scrollbar = ttk.Scrollbar(window)
input_scrollbar.place(height=180, x=480, y=45)
input_scrollbar.config(command=input_text.yview)
input_text.config(yscrollcommand=input_scrollbar.set)
result_scrollbar = ttk.Scrollbar(window)
result_scrollbar.place(height=180, x=480, y=295)
result_scrollbar.config(command=result_text.yview)
result_text.config(yscrollcommand=result_scrollbar.set)

style = ttk.Style()
style.configure('TButton', font=('calibri', font_size, 'normal'))

translate_btn = ttk.Button(window, text='ترجمه', command=lambda: translate(0))
translate_btn.place(width=60, height=30, x=265, y=245)
delete_btn = ttk.Button(window, text='حذف', command=lambda: delete(0))
delete_btn.place(width=60, height=30, x=200, y=245)

window.option_add('*TCombobox*Font', ('calibri', font_size-2, 'normal'))
input_lang = StringVar()
input_lang_cb = ttk.Combobox(window, textvariable=input_lang, state='readonly',
                             font=('calibri', font_size-4, 'normal'))
input_lang_cb['values'] = tuple(languages_v)
input_lang_cb.place(width=75, height=30, x=105, y=245)
input_lang_cb.current(0)

style.configure('S.TButton', padding=0)
swap_img = PhotoImage(file=resource_path('assets/swap_left.png'))
swap_btn = ttk.Button(window, image=swap_img, command=swap_langs,
                      style='S.TButton')
swap_btn.place(x=81, y=249)

result_lang = StringVar()
result_lang_cb = ttk.Combobox(window, textvariable=result_lang, state='readonly',
                              font=('calibri', font_size-4, 'normal'))
result_languages = languages_v.copy()
result_languages.remove('تشخیص خودکار')
result_lang_cb['values'] = tuple(result_languages)
result_lang_cb.place(width=75, height=30, x=5, y=245)
result_lang_cb.current(36)

var = StringVar()
charCount = Label(textvariable=var, font=('B nazanin', font_size, 'normal'))
charCount.grid(row=1, column=1, pady=5, padx=5)
input_text.bind('<Key>', update)
limit = input_text.bind('<Key>', update)

style.configure('TCheckbutton', font=('calibri', font_size-2, 'normal'))
auto_translate_var = IntVar()
checkButton = ttk.Checkbutton(window, variable=auto_translate_var, 
                              command=auto_translate, text='ترجمه همزمان')
checkButton.place(x=40, y=5)

language_window_is_open = False
mic_img = PhotoImage(file=resource_path('assets/mic.png'))
mic_btn = ttk.Button(window, image=mic_img, style='S.TButton',
                     command=define_speech_language)
mic_btn.place(x=250, y=3)

window.mainloop()
