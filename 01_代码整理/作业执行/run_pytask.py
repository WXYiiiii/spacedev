import sys
import subprocess
import datetime
import logging
import os
import shutil

# 配置日志
logging.basicConfig(filename='run_pytask.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def move_files(date):
    trs_dir_date = f"/data/input/trs/{date}"
    trs_dir_tmp = "/data/input/trs/tmp"
    regsub_dir_date = f"/data/input/udas/{date}"
    regsub_dir_tmp = "/data/input/udas/tmp"

    # 检查目录是否存在
    if not os.path.isdir(trs_dir_tmp):
        logger.error("trs的tmp路径不存在")
        print("trs的tmp路径不存在")
        return

    if not os.path.isdir(regsub_dir_tmp):
        logger.error("regsub的tmp路径不存在")
        print("regsub的tmp路径不存在")
        return

    # 移动文件
    try:
        # 移动trs目录下的所有文件到tmp目录
        for filename in os.listdir(trs_dir_date):
            shutil.move(os.path.join(trs_dir_date, filename), trs_dir_tmp)
        logger.info(f"成功挪动文件: {trs_dir_date}/* 到 {trs_dir_tmp}/")

        # 移动regsub目录下的所有.zip文件到tmp目录
        for filename in os.listdir(regsub_dir_date):
            if filename.endswith('.zip'):
                shutil.move(os.path.join(regsub_dir_date, filename), regsub_dir_tmp)
        logger.info(f"成功挪动文件: {regsub_dir_date}/*.zip 到 {regsub_dir_tmp}/")

    except Exception as e:
        logger.error(f"移动文件时发生错误: {e}")
        print(f"移动文件时发生错误: {e}")

def main(start_date, end_date):
    # 将字符串日期转换为datetime对象
    start_date = datetime.datetime.strptime(start_date, '%Y%m%d')
    end_date = datetime.datetime.strptime(end_date, '%Y%m%d')

    current_date = start_date

    logger.info("脚本开始执行")

    while current_date <= end_date:
        current_dt = current_date.strftime('%Y%m%d')
        current_date_formatted = current_date.strftime('%Y-%m-%d')

        logger.info(f"开始日期: {start_date.strftime('%Y-%m-%d')}")
        logger.info(f"当前日期: {current_date_formatted}")
        logger.info(f"结束日期: {end_date.strftime('%Y-%m-%d')}")

        # 挪文件
        move_files(current_dt)

        # 开始执行 Python 脚本
        logger.info(f"开始执行: python dsp_etl.py new {current_date_formatted}")

        try:
            subprocess.run(['python', 'dsp_etl.py', 'new', current_date_formatted], check=True)
            logger.info(f"执行完成: python dsp_etl.py new {current_date_formatted}")
        except subprocess.CalledProcessError:
            logger.error(f"执行失败: python dsp_etl.py new {current_date_formatted}")
            sys.exit(1)

        # 增加一天
        current_date += datetime.timedelta(days=1)

    logger.info("所有日期的处理已完成")

if __name__ == "__main__":
    # 更新条件检查，允许一个参数或两个参数
    if len(sys.argv) != 2 and len(sys.argv) != 1:
        print("用法： python script.py <开始日期（yyyymmdd)> [结束日期（yyyymmdd）]")
        sys.exit(1)

    start_date = sys.argv[1]

    # 根据参数数量设置结束日期
    end_date = start_date if len(sys.argv) == 2 else sys.argv[2]

    main(start_date, end_date)