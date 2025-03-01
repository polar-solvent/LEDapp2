# import argparse
import sys
import os
import re
import cv2
from moviepy import VideoFileClip

# parser = argparse.ArgumentParser(description="画像群を読み込み、末尾の数字の順番通りに一定の速さで表示する。qを押すと終了する。")
# parser.add_argument("input_path", type=str, help="表示する画像群のパス。一つの画像のパスを入力すればよい。")
# parser.add_argument("-f","--fps", type=int, default=60, help="表示するときの、次の画像へ移る速さ。デフォルトは60fps。数字が大きいほど速い。")
# parser.add_argument("-s","--save", nargs="?", type=str, const="./assets/dest/video.mp4", default="", help="表示した画像群を動画にして保存する。保存場所と名前を拡張子'.mp4'をつけて入力する。")
# args = parser.parse_args()
    
def main(input_path, speed=60, dest=""):
    # input_path, speed, dest = args.input_path, args.fps, args.save
    
    if speed < 1:
        print("enter frame rate more than 0")
        sys.exit(1)

    elif speed > 0xFFFF:
        print("enter frame rate less than 0xFFFF")
        sys.exit(1)

    dir_path, frame_name_original= os.path.split(input_path)
    underscore_index = frame_name_original.rindex("_")
    frame_name = frame_name_original[:underscore_index]

    if not os.path.isdir(dir_path):
        print("no such directory")
        sys.exit(1)

    def is_frame(f:str):
        return re.match(rf"{frame_name}_\d+\.bmp", f)

    def sort_frame(f:str):
        m = re.match(rf"{frame_name}_(\d+)\.bmp", f)
        return int(m.group(1))

    def frame_check(dir_path):
        frames_name = [
            f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and is_frame(f)
        ]
        if frames_name == []:
            print("no such frames in this directory")
            sys.exit(1)
        
        frames_name_sorted = sorted(frames_name,key=sort_frame)
        return frames_name_sorted

    cv2.namedWindow("image")

    frames = [cv2.imread(rf"{dir_path}/{f}") for f in frame_check(dir_path)]

    wait_ms = int(1000//speed)
    for f in frames:
        cv2.imshow("image", f)

        key = cv2.waitKey(wait_ms)
        if key == ord("q"):
            break
        elif key == ord("p"):
            while cv2.waitKey(0) != ord("p"):
                pass

    cv2.destroyAllWindows()
    
    if dest != "":
        des_path, save_name= os.path.split(dest)

        try :
            os.makedirs(des_path, exist_ok=True)
        except Exception as e:
            print("enter correct dest")
            sys.exit(1)

        name, ext = os.path.splitext(dest)[0], os.path.splitext(dest)[1]

        if name == des_path:
            print("enter valid name")
            sys.exit(1)

        if ext != ".mp4" and ext != ".gif":
            print("extension of video must be '.mp4' or '.gif'")
            sys.exit(1)
        else:
            h,w,c = frames[0].shape
            fourcc = cv2.VideoWriter.fourcc('m', 'p', '4', 'v')
            video  = cv2.VideoWriter("temp.mp4", fourcc, speed, (w, h))

            for frame in frames:
                video.write(frame)
            
            video.release()

            if ext == ".mp4":
                os.rename("temp.mp4", f"{name}.mp4")

            if ext == ".gif":
                clip = VideoFileClip("temp.mp4")
                clip.write_gif(f"{name}.gif", fps=30)
                os.remove("temp.mp4")

if __name__ == "__main__":
    main()
