# _*_ coding=utf-8 _*_
import os
import time
import subprocess


class ScreenRecord(object):

    def __init__(self, device_name):
        self.adb = "adb -s {0} ".format(device_name)
        self.adb_pid = None
        self.file_name = None

    def start(self, video_name, time_limit=180):
        self.file_name = video_name
        start_command = self.adb+"shell screenrecord --time-limit {0} /sdcard/{1}.mp4".format(time_limit, video_name)
        print start_command
        p = subprocess.Popen(start_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.adb_pid = p.pid

    def stop(self, path):
        kill_pid = "taskkill /pid {0} -t -f".format(self.adb_pid)
        os.popen(kill_pid)
        pull_command = self.adb + "pull /sdcard/{0}.mp4 {1}".format(self.file_name, path)
        stdout = os.popen(pull_command).readlines()
        self.delete_file(self.file_name, "video")
        print stdout

    # @staticmethod
    # def get_pid():
    #     stdout = os.popen("tasklist | findstr adb.exe").readlines()
    #     print stdout
    #     adb_pids = []
    #     for i in stdout:
    #         adb_pids.append(i.split()[1])
    #     return set(adb_pids)

    def get_screen_capture(self, path):
        image_name = self.get_time()
        cap_command = self.adb + "shell screencap -p /sdcard/{0}.png".format(image_name)
        os.popen(cap_command)
        pull_command = self.adb + "pull /sdcard/{0}.png {1}".format(image_name, path)
        stdout = os.popen(pull_command).readlines()
        self.delete_file(image_name, "image")
        print stdout

    @staticmethod
    def get_devices():
        stdout = os.popen("adb devices").readlines()
        result = []
        for i in stdout:
            temp = i.replace("\n", "").split()
            if len(temp) == 2:
                result.append(temp[0])
        return result

    @staticmethod
    def get_time():
        return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

    def delete_file(self, file_name, _type):
        delete_video_command = self.adb + "shell rm /sdcard/{0}.mp4".format(file_name)
        delete_picture_command = self.adb + "shell rm /sdcard/{0}.png".format(file_name)
        if _type == "video":
            os.popen(delete_video_command)
        else:
            os.popen(delete_picture_command)

# C:\Users\saas\Desktop\test53
s = ScreenRecord("1bd5686a")
print s.get_devices()
name = s.get_time()
print name
# print s.get_pid()
s.start(name)
time.sleep(5)
s.stop(r"C:\Users\saas\Desktop\test53")
# ScreenRecord("1bd5686a").start("test")
# ScreenRecord("1bd5686a").get_screen_capture(r"C:\Users\saas\Desktop\test53")
# os.popen("adb -s 1bd5686a shell screenrecord /sdcard/filename.mp4")



# import subprocess
# a = subprocess.Popen("adb devices", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# # print "####%s####" % a.wait()
# print a.pid
# print a.stdout.read()
# stdout, stderr = a.communicate()  #记录错误日志文件
# print stdout
# print stderr
# print a.returncode






