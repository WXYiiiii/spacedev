from hdfs.ext.kerberos import KerberosClient
from krbcontext import krbcontext
import time

# krbcontext 不支持自定义 con f文件的路径， 默认为 /etc / krb5.conf
# /etc/ krb5. conf中 lifet ime不能太短， 至少 5m
# 认证不同的hdf s用户使用不同的cache文件，否则 krbcontext会认证失效
# a = krbcontext 仅返回 krbcontext对象， 需要手动调用 init _ with _keytab （) 进行认证
# with krbcontext （） ： 会自动调用 a._ enter __ （） 和 a. __ exit  （） 必须都放在with语句内

src_file = '/data/tmp/xtyyxx_68_500000_20211231.csv!
dst_file = '/dsptdh/tmp/wxy_232.csv'

user = 'hive'
user = 'dsptdh'
keytab_file = f"/home/dspetl/tdh/{user}.keytab"
print(keytab_file)
principal = f"{user}@DEVTDH"
print(principal)
Cache = f"/home/dspetl/krb/krb5cc_{user}"
with krbcontext(using_ keytab=True, keytab _file=keytab _file, principal=principal, ccache_file=cache ):
    client = KerberosClient(url="http: //11.12.4.147 :50070;http: //11.12.4.146: 50070")
    print(client.list(hdfs_path=r"/"))
    print(client.list(hdfs_path=r"/dsptdh"))
    start_time = time.time()
    client.upload(hdfs_path=dst_file, local_path=src_file, n_threads=1, temp_dir=None, chunk_size=65536, progress=None,
                  cleanup=True)
    end_time = time.time()
print(f'all time is {end_time - start_time} ')
print(client.status('/dsptdh'))
