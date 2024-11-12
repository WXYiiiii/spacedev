#!/bin/bash

# 一、传入的参数
if [ "$#" -ne 1 ] && [ "$#" -ne 2 ]; then
    echo "用法： sh $0 <开始日期（yyyymmdd)> [结束日期（yyyymmdd）]"
    exit 1
fi

# 获取开始和结束日期
if [ "$#" -eq 1 ]; then
    start_date="$1"
    end_date="$1"
else
    start_date="$1"
    end_date="$2"
fi

# 将 yyyymmdd 转成 yyyy-mm-dd
start_date_formatted=$(date -d "${start_date:0:4}-${start_date:4:2}-${start_date:6:2}" +%Y-%m-%d)
end_date_formatted=$(date -d "${end_date:0:4}-${end_date:4:2}-${end_date:6:2}" +%Y-%m-%d)

# 将日期转为时间戳
start_ts=$(date -d "$start_date_formatted" +%s)
end_ts=$(date -d "$end_date_formatted" +%s)

# 日志文件名
log_file="run_pytask_$(date +'%Y%m%d').log"

# 日志记录函数
function logs {
    current=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$current INFO]: $*" >> "$log_file" 2>&1
}

logs "脚本开始执行"

# 循环遍历日期
current_ts=$start_ts
while [ $current_ts -le $end_ts ]; do
    # 格式化日期 YYYY-MM-DD
    current_date=$(date -d "@$current_ts" +%Y-%m-%d)
    current_dt=$(date -d "@$current_ts" +%Y%m%d)

    logs "开始日期: $start_date_formatted"
    logs "当前日期: $current_date"
    logs "结束日期: $end_date_formatted"

    # 挪文件
    logs "挪回文件: /data/script/python/restore.sh $current_dt"
    /data/script/python/restore.sh "$current_dt" >> "$log_file" 2>&1

    # 开始执行 Python 脚本
    logs "开始执行: python dsp_etl.py new ${current_date}"

    # 执行 Python 脚本并检查结果
    python dsp_etl.py new "$current_date" >> "$log_file" 2>&1
    if [ $? -ne 0 ]; then
        logs "执行失败: python dsp_etl.py new ${current_date}"
        exit 1
    fi

    # 执行结束日志记录
    logs "执行完成: python dsp_etl.py new ${current_date}"

    # 增加一天（86400秒）
    current_ts=$((current_ts + 86400))
done

echo "所有日期的处理已完成"