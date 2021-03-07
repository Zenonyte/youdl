from pytube import YouTube, Playlist
import sys, os, ffmpeg
cwd = os.getcwd()
dldir = '{}/DL/'.format(cwd)

def dlvid(o, v, d):
    if o == 'P':
        print('Downloading "{}", please wait.. '.format(v.title))
        v.streams.filter(progressive=True).get_highest_resolution().download(d)
        return True
    elif o == 'A' or o == 'D':
        print('Downloading "{}", please wait.. '.format(v.title))
        sa = v.streams.filter(progressive=False, type='audio').order_by('abr').desc().first()
        sa.download(d)
        if o == 'D':
            print('Audio downloaded, downloading video.. ')
            sv = v.streams.filter(progressive=False, type='video', file_extension='mp4').order_by('resolution').desc().first()
            sv.download(d)
            print('Merging audio and video.. ')
            viddir = '{}{}.mp4'.format(dldir, v.title.replace('.', ''))
            video = ffmpeg.input('{}{}.mp4'.format(dldir, v.title.replace('.', '')))
            auddir = '{}{}.webm'.format(dldir, v.title.replace('.', ''))
            audio = ffmpeg.input(auddir)
            out = ffmpeg.concat(video, audio, v=1, a=1).output('{} {}.mp4'.format(dldir, v.title.replace('.', ''))).run()
            os.remove(viddir)
            os.remove(auddir)
        return True
    else:
        return False

while True:
    dl = False
    q1 = str(input('(V)ideo, (p)laylist or (c)hange download directory: ')).upper()
    if q1 == 'V':
        vidlink = str(input('Video URL: ')) #https://www.youtube.com/watch?v=EIyixC9NsLI for testing
        vid = YouTube(vidlink)
        while dl == False:
            q2 = str(input('(P)rogressive, (D)ASH or (a)udio?: ')).upper()
            if dlvid(q2, vid, dldir) == True:
                dl = True
                print('Done!')
            else:
                print('Wrong input.')
    elif q1 == 'P':
        listurl = str(input('List URL: ')) #https://www.youtube.com/playlist?list=PLUWtUdopP1-9Zq-cVfW8oeulhvc33vC9P for testing
        plist = Playlist(listurl)
        vnum = len(plist.video_urls)
        vvar = 0
        print('{} videos. '.format(vnum))
        q2 = str(input('(P)rogressive, (D)ASH or (a)udio?: ')).upper()
        for vid in plist.videos:
            if dlvid(q2, vid, dldir) == True:
                vvar += 1
                print('Done! {} videos left to download. '.format(vnum - vvar))
            else:
                print('Wrong input. ')
    elif q1 == 'C':
        cd = str(input('Enter the new download directory, cwd for current working directory or change it to the (d)efault: '))
        if cd.upper() == 'D':
            dldir = '{}/DL'.format(cwd)
        elif cd.upper() == 'CWD':
            dldir = cwd
        else:
            dldir = cd
        print('The new download directory is {}. '.format(dldir))
    else:
        print('Wrong input. ')
    q0 = str(input('Press any key to continue, q to quit: '))
if q0.upper() == 'Q':
    exit()
