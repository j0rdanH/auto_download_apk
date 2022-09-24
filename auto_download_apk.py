from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import time
import pyautogui
import os


already_try = []
'''current_file_path 用于记录点击下载后文件夹内的文件是否+1， 没有则下载失败，需要记录在log中'''
def auto_down(page_URL, ajax_URL, browser, current_file_path, package):

    apk_num = len(os.listdir(current_file_path))
    print(apk_num)

    url_list = [page_URL, ajax_URL]
    if (package) not in already_try:
        for i in range(2):
            down_url = url_list[i]
            windows_open = "window.open( ' " + down_url + "' )"
            browser.execute_script(windows_open)
            time.sleep(6)
        all_handles = browser.window_handles
        #print(len(all_handles))
        current_handle = all_handles[1]
        browser.switch_to.window(current_handle)
        browser.execute_script('window.scrollTo(40, 500);')
        pyautogui.click(520, 580, clicks=1, interval=0.0, button='left')        # click to start downloading
        time.sleep(9)                     # considering the network fluctuation, use the upper limit

        '''判断apk文件数量是否增加'''
        print(str(apk_num)+'   '+str(len(os.listdir(current_file_path))))
        print(current_file_path+'failure.txt')
        if(len(os.listdir(current_file_path))==apk_num):
            with open(current_file_path+'failure.txt', 'a') as f:
                f.write(package+'\n')
                already_try.append(package)
        else:
            already_try.append(package)
            pass
            #f_s.write(package+'\n')

        ''' close redundant tag, only one tag left '''
        browser.close()
        browser.switch_to.window(all_handles[2])
        browser.close()
        browser.switch_to.window(all_handles[0])
    else:
        pass

def main(browser, page_base_url, ajax_base_url, download_list, current_file_path):
    #failure_count = 0




    for current_pack in download_list:
        package_name = current_pack.split('\n')[0]
        print(package_name)
        page_URL = page_base_url+package_name
        ajax_URL = ajax_base_url+package_name+'&ajax=1'
        try:
            auto_down(page_URL, ajax_URL, browser, current_file_path, package_name)
            #print('当前正下载'+package_name)
            time.sleep(3)             # in case that the server find suspicious activity
        except:
            pass
            #print(package_name+'  下载失败')
            #failure_count += 1


    #print(str(failure_count))



if __name__ == '__main__':
    category = ['sports']
    options = webdriver.ChromeOptions()
    #prefs = {'download.default_directory': 'D:\\privacy_project\\UDE-SA\\dowloading_apks\\'}
    #download_list = download_list[-100:-1]
    page_base_url = 'https://apkcombo.com/apk-downloader/?utm_source=chrome-extension#package='
    ajax_base_url = 'https://apkcombo.com/apk-downloader/?package='
    for item in category:
        current_file_path = 'D:\\privacy_project\\UDE-SA\\dowloading_apks\\'+item+'\\'
        prefs = {'download.default_directory': current_file_path}
        options.add_experimental_option('prefs', prefs)
        browser = webdriver.Chrome('C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe', options=options)
        f = open('D:\\privacy_project\\UDE-SA\\downloading_list\\'+item+'.txt')
        download_list = f.readlines()  # 获取下载列表
        main(browser, page_base_url, ajax_base_url, download_list, current_file_path)
        already_try = []    # 最后将其清空，防止影响下一轮循环