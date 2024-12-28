# import argparse
import cv2
import numpy as np
import sys
import os
import re

# parser = argparse.ArgumentParser(description="指定した画像ファイルを任意のpxずつずらし、bmp画像にして出力する。")
# parser.add_argument("input_path", nargs="+", type=str, help="指定する画像のパス。複数のパスを入力可")
# parser.add_argument("-u","--upright", action="store_true", help="指定した画像をずらす方向を定める。デフォルトは横向き、オプションを入れると縦向きになる。")
# parser.add_argument("-r","--reverse", action="store_true", help="オプションを入れると指定した画像をずらす向きを逆転させる。")
# parser.add_argument("-a","--arrange", type=int, choices=range(3), default=0, help="複数の画像を読み込むとき、上ぞろえ(0)・中央ぞろえ(1)・下ぞろえ(2)を選択できる。デフォルトは上ぞろえ(0)")
# parser.add_argument("-W","--width", type=int, default=None, help="出力する画像の幅。デフォルトは入力した画像の横幅の和")
# parser.add_argument("-H","--height", type=int, default=None, help="出力する画像の高さ。デフォルトは入力した画像の高さのうち最大のもの")
# parser.add_argument("-I","--interval", type=int, default=1, help="出力する画像1枚ごとにずらすpx数。デフォルトは1px")
# parser.add_argument("-d","--dest", type=str, default="./assets/dest", help="出力先のディレクトリ(指定したディレクトリが存在しない場合は作成される)。デフォルトはカレントディレクトリ内のassets/dest")
# parser.add_argument("-n","--name", type=str, default="frame", help="出力する画像の名前。デフォルトはframe_数字.bmpで、frameの部分を変えられる。")
# args = parser.parse_args()

# # parserのtype=boolはだめらしいのでなんとかした(-u, -r)

def shape(input_path):
    import_imgs = [cv2.imread(i) for i in input_path]
    if any(e is None for e in import_imgs):
        print('not correct path of image')
        return 1

    img_shape = np.array([i.shape for i in import_imgs]) #動いた。縦だけデータ取る
    return img_shape[:,0], img_shape[:,1], img_shape[:,2]

def main(input_path, upright=False, reverse=False, arrange=0, width=None, height=None, interval=1, dest="./assets/dest", name="frame"):

    # if width is not None and width < 1:
    #     print("enter width more than 0")
    #     sys.exit(1)

    # if height is not None and height < 1:
    #     print("enter height more than 0")
    #     sys.exit(1)

    # if interval < 1:
    #     print("enter interval more than 0")
    #     sys.exit(1)

    if not re.fullmatch(r"[-\w]+", name):
        print("enter valid file name")
        sys.exit(1)

    if shape(input_path) == 1:
        sys.exit(1)
    else:
        h,w,c = shape(input_path)

    import_imgs = [cv2.imread(i) for i in input_path]
    # if any(e is None for e in import_imgs):
    #     print('not correct path of image')
    #     sys.exit(1)

    # img_shape = np.array([i.shape for i in import_imgs]) #動いた。縦だけデータ取る
    # h,w,c = img_shape[:,0], img_shape[:,1], img_shape[:,2]

    try :
        os.makedirs(dest, exist_ok=True)
    except Exception as e:
        print(e)
        sys.exit(1)


    if upright:
        if width == 0:
            frame_height = max(w)
        else:
            frame_height = width
        if height == 0:
            frame_width = sum(h)
        else:
            frame_width = height
        if interval > frame_width:
            print("enter interval less than width")
            sys.exit(1)
        img = np.zeros((2*frame_width+sum(h),max(w),3),dtype=np.uint8)
        if arrange == 0:
            for i, image in enumerate(import_imgs):
                img[frame_width+sum(h[:i]):frame_width+sum(h[:i+1]), :w[i], :] = image
            if max(w) >= frame_height:
                img = img[:,:frame_height,:]
            else:
                img = np.hstack([img, np.zeros((2*frame_width+sum(h),frame_height-max(w),3),dtype=np.uint8)])
        elif arrange == 1:
            for i, image in enumerate(import_imgs):
                m = int((max(w)-w[i])//2)
                if max(w)%2 == 0 and w[i]%2 == 1:
                    m+=1
                img[frame_width+sum(h[:i]):frame_width+sum(h[:i+1]), m:m+w[i], :] = image
            if max(w) >= frame_height:
                margin = int((max(w)-frame_height)//2)
                if max(w)%2 == 0 and frame_height%2 == 1:
                    margin+=1
                img = img[:,margin:margin+frame_height,:]
            else:
                margin = int((frame_height-max(w))//2)
                if frame_height%2 == 0 and max(w)%2 == 1:
                    margin+=1
                img = np.hstack([np.zeros((2*frame_width+sum(h),margin,3),dtype=np.uint8),img,np.zeros((2*frame_width+sum(h),frame_height-margin-max(w),3),dtype=np.uint8)])
        elif arrange == 2:
            for i, image in enumerate(import_imgs):
                img[frame_width+sum(h[:i]):frame_width+sum(h[:i+1]), max(w)-w[i]:, :] = image
            if max(w) >= frame_height:
                img = img[:,max(w)-frame_height:,:]
            else:
                img = np.hstack([np.zeros((2*frame_width+sum(h),frame_height-max(w),3),dtype=np.uint8), img])
        start, i = 0, 0
        if reverse: start, interval = sum(h)+frame_width-1, -interval
        while start <= sum(h) + frame_width and start >= 0:
            currentframe=img[start:start+frame_width,:,:]
            cv2.imwrite(f"{dest}/{name}_{i}.bmp",currentframe)
            start += interval
            i += 1
    else:
        if height == 0:
            frame_height = max(h)
        else:
            frame_height = height
        if width == 0:
            frame_width = sum(w)
        else:
            frame_width = width
        if interval > frame_width:
            print("enter interval less than width")
            sys.exit(1)
        img = np.zeros((max(h),2*frame_width+sum(w),3),dtype=np.uint8)
        if arrange == 0:
            for i, image in enumerate(import_imgs):
                img[:h[i], frame_width+sum(w[:i]):frame_width+sum(w[:i+1]), :] = image
            if max(h) >= frame_height:
                img = img[:frame_height,:,:]
            else:
                img = np.vstack([img, np.zeros((frame_height-max(h),2*frame_width+sum(w),3),dtype=np.uint8)])
        elif arrange == 1:      #原因はおそらく//2を二回しているから--→102行目imgの縦を最初からframe_heightに設定するとできる？
            for i, image in enumerate(import_imgs): #↑貼り付ける側と貼り付けられる側の偶奇で場合分けして解決
                m = int((max(h)-h[i])//2)         #大=小または大：奇、小：偶のとき
                if max(h)%2 == 0 and h[i]%2 == 1: #大：偶、小：奇のとき
                    m+=1
                img[m:m+h[i], frame_width+sum(w[:i]):frame_width+sum(w[:i+1]), :] = image
            if max(h) >= frame_height:
                margin = int((max(h)-frame_height)//2)
                if max(h)%2 == 0 and frame_height&2 == 1:
                    margin+=1
                img = img[margin:margin+frame_height,:,:]
            else:
                margin = int((frame_height-max(h))//2)
                if frame_height%2 == 0 and max(h)%2 == 1:
                    margin+=1
                img = np.vstack([np.zeros((margin,2*frame_width+sum(w),3),dtype=np.uint8),img,np.zeros((frame_height-margin-max(h),2*frame_width+sum(w),3),dtype=np.uint8)])
        elif arrange == 2:
            for i, image in enumerate(import_imgs):
                img[max(h)-h[i]:, frame_width+sum(w[:i]):frame_width+sum(w[:i+1]), :] = image
            if max(h) >= frame_height:
                img = img[max(h)-frame_height:,:,:]
            else:
                img = np.vstack([np.zeros((frame_height-max(h),2*frame_width+sum(w),3),dtype=np.uint8), img])
        start, i = 0, 0
        if reverse: start, interval = sum(w)+frame_width-1, -interval
        while start <= sum(w) + frame_width and start >= 0:
            currentframe=img[:,start:start+frame_width,:]
            cv2.imwrite(f"{dest}/{name}_{i}.bmp",currentframe)
            start += interval
            i += 1

if __name__ == "__main__":
    main()
    