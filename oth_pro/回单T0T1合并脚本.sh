## 1、 GENERAL_BILL
1. 逻辑:  对私T1的数据会先通过T0数据的ivc_typ进行筛选,然后参与merge
   ```sql
   T0数据 - BILL_FLOW_XBANK_G

   T1数据:  bill_flow_general_univ_tmp -> BILL_FLOW_GENERAL_MATCH
       -- 将bill_flow_general_univ_tmp表中 与T0中ivc_typ相同的数据筛选出来 进行merge打标      // 所以T0和T1的ivc_typ 要保持一致
       set sql_0 =  'SELECT * FROM bill.bill_flow_general_univ_tmp WHERE IVC_TYP IN (select SUBSTR(ivc_typ, 2) from bill.BILL_FLOW_XBANK_G where IVC_TYP like ''H%'' group by ivc_typ)';
       set sql_1 =  'load from ('|| sql_0 || ') of cursor insert into BILL.BILL_FLOW_GENERAL_MATCH' || ' nonrecoverable allow read access lock with force';
   ```

#2. 出问题: T0与T1的ivc_typ不一致,
#
#    BILL_FLOW_XBANK_G(T0数据) 中有ivc_typ为 'H2011253','H2013597' 的数据
#
#    而 T1中相同配置的 ivc_typ为 '2011897','201538' .
#
#    所以 筛选后的 BILL_FLOW_GENERAL_MATCH(T1参与merge的表) 中没有和T0'H2011253','H2013597' 相匹配的数据

3. 合并逻辑:
  ```sql
  MERGE INTO bill.BILL_GENERAL_XBANK_JOIN T0
      USING   BILL.BILL_FLOW_GENERAL_MATCH  T1
ON (
          T0.PAY_ID = T1.PAY_ID      -- 以 PAY_ID 为条件
          and T1.ACCT_TYP <> '2'
          and T0.RED_FLAG <> 'Y')
  WHEN  MATCHED THEN
  UPDATE SET T0.RED_FLAG = 'Y',T0.INNER_NO = T1.INNER_NO;
  ```

  1.  BILL_GENERAL_XBANK_JOIN (T0数据) 与 BILL_FLOW_GENERAL_MATCH (T1数据) 进行merge
  2. 如果匹配成功,则对T0中的数据 打上标志 'Y'.
#    - 这里 T0中 'H2011253','H2013597'  的数据**没有打上标志**
  3. 然后直接将BILL_GENERAL_XBANK_JOIN中没有标志Y的数据 写入bill_flow_general_univ_tmp中
#    - 所以T0中 'H2011253','H2013597'  的数据直接导入到了对私临时表, 与表中ivc_typ为 '2011897','201538' 的数据发生重复