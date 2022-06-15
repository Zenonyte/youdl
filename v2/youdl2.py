'''
Programmi jaoks on vaja moviepy, requests ja pytube mooduleid.
'''
from pytube import YouTube, Playlist
import os, requests, re
from moviepy.editor import * # Plaanisin algul kasutada ffmpegi, aga ei saanud seda kuidagi tööle, seega otsustasin kasutada moviepy moodulit.
dldir = f'{os.getcwd()}\\DL\\' # Programmi praeguse asukoha järgi tehakse allalaetavate videote kaust.
dlformat = 'dash'

def dlvid(format, url):
    log = f'\nURL: {url}\nValitud formaat: {format}'
    try: # Esiteks kontrollib, kas saab youtube üldse kätte.
        requests.get('https://www.youtube.com/', timeout = 3)
    except:
        log += '\nKontrolli oma internetiühendust. '
        return {'success': False, 'log': log}
    try: # Teiseks kontrollib URLi korrektsust.
        video = YouTube(url)
        normaltitle =  re.sub(r"\W+|_", " ", video.title) # Programm võtab allalaetud videote nimetamisel ära kõik erilised karakterid (tekitavad probleeme). Kasutasin regex filtrit.
        log += f'\nNimi: {video.title}'
    except:
        log += '\nVale URL. '
        return {'success': False, 'log': log}
    if format == 'progressive': # Progressive formaadiga allalaadimine (madalam kvaliteet).
        try:
            video.streams.filter(progressive = True).get_highest_resolution().download(dldir, f'{normaltitle}.mp4') # Laeb alla kõige kõrgema kvaliteediga progressive formaadis video.
            log += '\nAlla laetud'
        except:
            log += '\nViga video allalaadimisel. '
            return {'success': False, 'log': log}
    elif format == 'dash' or format == 'audio':
        try:
            video.streams.filter(progressive = False, type = 'audio').order_by('abr').desc().first().download(dldir, f'{normaltitle}.webm') # Laeb alla kõige kõrgema kvaliteediga audiofaili (webm)
            log += '\nAudio alla laetud. '
            if format == 'dash':
                video.streams.filter(progressive=False, type='video', file_extension='mp4').order_by('resolution').desc().first().download(dldir, f'{normaltitle}.mp4') # Laeb alla kõige kõrgema kvaliteediga videofaili (mp4 formaadis)
                log += '\nVideo alla laetud. '
                # Siit hakkab video ja audio kokku monteerimine, kasutades moviepy'd
                videopath = f'{dldir}{normaltitle}.mp4'; audiopath = f'{dldir}{normaltitle}.webm'
                vid = VideoFileClip(videopath); aud = AudioFileClip(audiopath)
                vid.audio = aud
                vid.write_videofile(f'{dldir}{normaltitle} MERGED.mp4')
                os.remove(videopath); os.remove(audiopath)
                log += '\nVideo ja audio kombineeritud. '
        except:
            log += '\nViga video/audio allalaadimisel. '
            return {'success': False, 'log': log}
    return {'success': True, 'log': log}

while True: 
    try:
        inp = int(input(f'''\n
YouTube videote allalaadimisprogramm
------------------------------------
Praegune allalaadimiskoht: {dldir}
Praegune formaat: {dlformat}
1) videote allalaadimine
2) vaheta allalaetavate videote kausta
3) vaheta formaati
4) lõpeta sessioon
        '''))
    except:
        print('Sisesta number. ')
    if inp == 1:
        while True:
            try:
                inp = int(input('''\n
Vali sisend:
------------------------------------
1) video URL
2) esitusloendi URL
3) tekstifail
4) tagasi algusesse
                '''))
            except:
                print('Sisesta number. ')
            if inp == 1:
                inp = str(input('Sisesta URL: '))
                print(dlvid(dlformat, inp)['log'])
            elif inp == 2:
                inp = str(input('Sisesta URL: '))
                plist = Playlist(inp)
                vnum = len(plist.video_urls)
                vvar = 0
                print(f'Esitusloendis on {vnum} videot. ')
                for url in plist.video_urls:
                    print(f'Video {vvar + 1} ({round(vvar/vnum*100, 1)}%): ')
                    print(dlvid(dlformat, url)['log'])
                    vvar += 1
            elif inp == 3:
                inp = str(input('Sisesta fail: ')) # Näiteks C:\Users\kasutaja\fail.txt
                with open(inp, 'r') as file:
                    fvar = 0
                    for url in file:
                        fvar += 1
                        print(f'Video {fvar}: ')
                        print(dlvid(dlformat, url)['log'])
            elif inp == 4:
                break
    elif inp == 2:
        while True:
            dldir = str(input('\nSisesesta uus allalaadimiskoht: '))
            if dldir.isnumeric() == True:
                print('Vale sisend. ')
            else:  
                break
    elif inp == 3:
        while True:
            try:
                inp = int(input('''\n
Vali formaat:
------------------------------------
1) dash (kõrgem kvaliteet)
2) progressive (maladam kvaliteet, palju kiirem allalaadimine)
3) audio
                '''))
            except:
                print('Sisesta number.')
            if inp == 1:
                dlformat = 'dash'
                break
            elif inp == 2:
                dlformat = 'progressive'
                break
            elif inp == 3:
                dlformat = 'audio'
                break
            else:
                print('Vale sisend. ')
    elif inp == 4:
        break
