#!/bin/bash

# 检查参数数量
if [ "$#" -ne 1 ] && [ "$#" -ne 2 ]; then
    echo "用法: $0 <开始日期(yyyymmdd)> [结束日期(yyyymmdd)]"
    exit 1
fi

# 获取开始和结束日期
if [ "$#" -eq 1 ]; then
    start_date="$1"
    end_date="$1"  # 如果只输入一个日期，开始和结束日期相同
else
    start_date="$1"
    end_date="$2"
fi

# 将 yyyymmdd 格式的日期转换为 YYYY-MM-DD 格式
start_date_formatted=$(date -d "${start_date:0:4}-${start_date:4:2}-${start_date:6:2}" +%Y-%m-%d)
end_date_formatted=$(date -d "${end_date:0:4}-${end_date:4:2}-${end_date:6:2}" +%Y-%m-%d)

# 将日期转换为时间戳
start_ts=$(date -d "$start_date_formatted" +%s)
end_ts=$(date -d "$end_date_formatted" +%s)

# 日志文件名
log_file="etl_$(date +'%Y%m%d').log"

# 循环遍历日期
current_ts=$start_ts
while [ $current_ts -le $end_ts ]; do
    # 格式化当前日期为 YYYY-MM-DD
    current_date=$(date -d "@$current_ts" +%Y-%m-%d)

    # 记录开始执行的时间到日志文件
    echo "$(date +'%Y-%m-%d %H:%M:%S') - 开始执行: python dsp_tdh.py new $current_date" >> "$log_file"

    # 执行 Python 脚本，传递当前日期作为参数，并等待其完成
    python dsp_tdh.py new "$current_date"

    # 检查上一个命令的返回值
    if [ $? -ne 0 ]; then
        echo "$(date +'%Y-%m-%d %H:%M:%S') - 执行失败: python dsp_tdh.py new $current_date" >> "$log_file"
        exit 1  # 如果执行失败，退出脚本
    fi

    # 记录结束执行的时间到日志文件
    echo "$(date +'%Y-%m-%d %H:%M:%S') - 执行完成: python dsp_tdh.py new $current_date" >> "$log_file"

    # 增加一天（86400秒）
    current_ts=$((current_ts + 86400))
done

echo "所有日期的处理已完成。"