# 监管数据集市 - STG层详细设计

## 一、STG层概述

### 1.1 设计原则
- 数据清洗与标准化
- 统一数据编码
- 数据脱敏处理
- 增量与全量结合

### 1.2 表清单

| 表名 | 中文名 | 数据来源 | 更新方式 |
|------|--------|----------|----------|
| stg_customer | 客户信息清洗表 | ods_customer | 全量 |
| stg_account | 账户信息清洗表 | ods_account | 增量 |
| stg_transaction | 交易流水清洗表 | ods_transaction | 增量 |
| stg_contract | 合同信息清洗表 | ods_contract | 增量 |
| stg_organization | 机构信息清洗表 | ods_organization | 全量 |
| stg_risk_indicator | 风险指标清洗表 | ods_risk_indicator | 增量 |

---

## 二、详细表结构

### 2.1 客户信息清洗表 (stg_customer)

```sql
CREATE TABLE stg_customer (
    customer_id        STRING COMMENT '客户号',
    customer_name      STRING COMMENT '客户姓名',
    id_type            STRING COMMENT '证件类型',
    id_number          STRING COMMENT '证件号码',
    id_number_hash     STRING COMMENT '证件号码哈希',
    gender             STRING COMMENT '性别(M/F/U)',
    birthday           DATE COMMENT '出生日期',
    nationality        STRING COMMENT '国籍(ISO代码)',
    occupation         STRING COMMENT '职业(标准编码)',
    address            STRING COMMENT '通讯地址',
    phone              STRING COMMENT '联系电话',
    customer_type      STRING COMMENT '客户类型(1个人/2企业)',
    customer_level     STRING COMMENT '客户等级',
    risk_level         STRING COMMENT '风险等级',
    annual_income      DECIMAL(18,2) COMMENT '年收入',
    source_channel     STRING COMMENT '获客渠道',
    branch_id          STRING COMMENT '所属机构',
    create_date        DATE COMMENT '开户日期',
    update_date        DATE COMMENT '更新日期',
    is_active          STRING COMMENT '是否有效(Y/N)',
    etl_time           TIMESTAMP COMMENT 'ETL时间',
    etl_batch_no       STRING COMMENT 'ETL批次号'
) COMMENT '客户信息清洗表'
PARTITIONED BY (dt STRING)
STORED AS PARQUET;
```

### 2.2 账户信息清洗表 (stg_account)

```sql
CREATE TABLE stg_account (
    account_id         STRING COMMENT '账户号',
    customer_id        STRING COMMENT '客户号',
    account_type       STRING COMMENT '账户类型(1活期/2定期/3理财)',
    account_sub_type   STRING COMMENT '账户子类型',
    account_status     STRING COMMENT '账户状态(0正常/1冻结/2销户)',
    open_date          DATE COMMENT '开户日期',
    close_date         DATE COMMENT '销户日期',
    balance            DECIMAL(18,2) COMMENT '账户余额',
    currency           STRING COMMENT '币种(ISO代码)',
    interest_rate      DECIMAL(10,4) COMMENT '利率',
    branch_id          STRING COMMENT '开户机构',
    manager_id         STRING COMMENT '客户经理',
    is_virtual         STRING COMMENT '是否虚拟账户(Y/N)',
   关联账户           STRING COMMENT '关联主账户',
    update_date        DATE COMMENT '更新日期',
    etl_time           TIMESTAMP COMMENT 'ETL时间',
    etl_batch_no       STRING COMMENT 'ETL批次号'
) COMMENT '账户信息清洗表'
PARTITIONED BY (dt STRING)
STORED AS PARQUET;
```

### 2.3 交易流水清洗表 (stg_transaction)

```sql
CREATE TABLE stg_transaction (
    trans_id           STRING COMMENT '交易流水号',
    account_id         STRING COMMENT '账户号',
    customer_id        STRING COMMENT '客户号',
    trans_type         STRING COMMENT '交易类型(标准编码)',
    trans_sub_type     STRING COMMENT '交易子类型',
    trans_amount       DECIMAL(18,2) COMMENT '交易金额',
    trans_currency     STRING COMMENT '交易币种',
    trans_amount_cny   DECIMAL(18,2) COMMENT '交易金额(人民币)',
    trans_date         DATETIME COMMENT '交易时间',
    trans_timestamp    BIGINT COMMENT '交易时间戳',
    trans_channel      STRING COMMENT '交易渠道(1柜面/2自助/3网银/4手机)',
    trans_channel_name STRING COMMENT '交易渠道名称',
    opposite_account  STRING COMMENT '对方账户',
    opposite_name     STRING COMMENT '对方姓名',
    opposite_bank     STRING COMMENT '对方行号',
    trans_desc         STRING COMMENT '交易描述',
    branch_id          STRING COMMENT '交易机构',
    terminal_id       STRING COMMENT '终端编号',
    operator_id       STRING COMMENT '操作员',
    trans_status       STRING COMMENT '交易状态(0成功/1失败/2冲正)',
    is_reversed        STRING COMMENT '是否被冲正(Y/N)',
    risk_flag          STRING COMMENT '风险标识',
    update_date        DATE COMMENT '更新日期',
    etl_time           TIMESTAMP COMMENT 'ETL时间',
    etl_batch_no       STRING COMMENT 'ETL批次号'
) COMMENT '交易流水清洗表'
PARTITIONED BY (dt STRING)
STORED AS PARQUET;
```

### 2.4 合同信息清洗表 (stg_contract)

```sql
CREATE TABLE stg_contract (
    contract_id        STRING COMMENT '合同编号',
    customer_id        STRING COMMENT '客户号',
    loan_account       STRING COMMENT '贷款账号',
    contract_type      STRING COMMENT '合同类型(1贷款/2担保/3其他)',
    contract_amount    DECIMAL(18,2) COMMENT '合同金额',
    balance            DECIMAL(18,2) COMMENT '余额',
    interest_rate      DECIMAL(10,4) COMMENT '执行利率',
    rate_type          STRING COMMENT '利率类型(1固定/2浮动)',
    loan_term          INT COMMENT '贷款期限(月)',
    start_date         DATE COMMENT '开始日期',
    end_date           DATE COMMENT '到期日期',
    repay_type         STRING COMMENT '还款方式(1等额本息/2等额本金/3一次性)',
    repay_freq         STRING COMMENT '还款频率(月/季/年)',
    contract_status    STRING COMMENT '合同状态(1正常/2逾期/3结清/4核销)',
    asset_class        STRING COMMENT '资产分类(1正常/2关注/3次级/4可疑/5损失)',
    five_class_status  STRING COMMENT '五级分类状态',
    overdue_days       INT COMMENT '逾期天数',
    overdue_amount    DECIMAL(18,2) COMMENT '逾期金额',
    guarantee_type     STRING COMMENT '担保方式(1信用/2抵押/3质押/4保证)',
    guarantee_amount   DECIMAL(18,2) COMMENT '担保金额',
    branch_id          STRING COMMENT '所属机构',
    manager_id         STRING COMMENT '客户经理',
    update_date        DATE COMMENT '更新日期',
    etl_time           TIMESTAMP COMMENT 'ETL时间',
    etl_batch_no       STRING COMMENT 'ETL批次号'
) COMMENT '合同信息清洗表'
PARTITIONED BY (dt STRING)
STORED AS PARQUET;
```

### 2.5 机构信息清洗表 (stg_organization)

```sql
CREATE TABLE stg_organization (
    org_id             STRING COMMENT '机构编码',
    org_name           STRING COMMENT '机构名称',
    org_short_name     STRING COMMENT '机构简称',
    parent_org_id     STRING COMMENT '上级机构编码',
    org_level          INT COMMENT '机构层级(1总行/2分行/3支行)',
    org_type           STRING COMMENT '机构类型',
    region_code        STRING COMMENT '地区代码(省市区)',
    region_name        STRING COMMENT '地区名称',
    address            STRING COMMENT '机构地址',
    phone              STRING COMMENT '联系电话',
    manager_name       STRING COMMENT '负责人',
    establish_date     DATE COMMENT '成立日期',
    license_no         STRING COMMENT '金融许可证号',
    is_active          STRING COMMENT '是否有效(Y/N)',
    update_date        DATE COMMENT '更新日期',
    etl_time           TIMESTAMP COMMENT 'ETL时间',
    etl_batch_no       STRING COMMENT 'ETL批次号'
) COMMENT '机构信息清洗表'
PARTITIONED BY (dt STRING)
STORED AS PARQUET;
```

### 2.6 风险指标清洗表 (stg_risk_indicator)

```sql
CREATE TABLE stg_risk_indicator (
    indicator_id       STRING COMMENT '指标ID',
    indicator_code     STRING COMMENT '指标代码',
    indicator_name     STRING COMMENT '指标名称',
    indicator_type     STRING COMMENT '指标类型',
    indicator_category STRING COMMENT '指标分类',
    unit               STRING COMMENT '计量单位',
    threshold_value    DECIMAL(18,4) COMMENT '阈值',
    warning_value      DECIMAL(18,4) COMMENT '预警值',
    standard_value     DECIMAL(18,4) COMMENT '标准值',
    calc_formula       STRING COMMENT '计算公式',
    data_source        STRING COMMENT '数据来源',
    calc_frequency     STRING COMMENT '计算频率',
    is_active          STRING COMMENT '是否有效(Y/N)',
    update_date        DATE COMMENT '更新日期',
    etl_time           TIMESTAMP COMMENT 'ETL时间',
    etl_batch_no       STRING COMMENT 'ETL批次号'
) COMMENT '风险指标清洗表'
PARTITIONED BY (dt STRING)
STORED AS PARQUET;
```

---

## 三、数据清洗规则

### 3.1 客户信息清洗规则

| 字段 | 清洗规则 | 示例 |
|------|----------|------|
| customer_name | 去除首尾空格、统一全角半角 | " 张三 " -> "张三" |
| id_type | 标准化编码 | "身份证" -> "01" |
| id_number | 统一格式、大写、哈希脱敏 | "110101199001011234" |
| id_number_hash | SHA256哈希(仅存储哈希值) | |
| gender | 标准化为M/F/U | "男" -> "M", "1" -> "M" |
| nationality | 转换为ISO国家代码 | "中国" -> "CN" |
| occupation | 转换为标准职业编码 | |
| phone | 只保留数字 | "138-0000-0000" -> "13800000000" |
| customer_type | 标准化编码 | "个人" -> "1", "企业" -> "2" |
| risk_level | 标准化为H/M/L | "高" -> "H" |

### 3.2 账户信息清洗规则

| 字段 | 清洗规则 | 示例 |
|------|----------|------|
| account_type | 标准化编码 | "活期" -> "1", "定期" -> "2" |
| account_status | 标准化状态码 | "正常" -> "0", "冻结" -> "1" |
| currency | 转换为ISO币种代码 | "人民币" -> "CNY", "美元" -> "USD" |
| balance | 空值填充为0 | NULL -> 0.00 |
| interest_rate | 百分比转小数 | 3.5% -> 0.035 |

### 3.3 交易流水清洗规则

| 字段 | 清洗规则 | 示例 |
|------|----------|------|
| trans_type | 标准化交易类型编码 | |
| trans_amount | 空值填充为0 | NULL -> 0.00 |
| trans_amount_cny | 汇率转换为人民币 | |
| trans_date | 转换为标准日期时间格式 | |
| trans_timestamp | 转换为毫秒时间戳 | |
| trans_channel | 标准化渠道编码 | "手机银行" -> "4" |
| opposite_account | 脱敏处理 | 6222****890 |
| opposite_name | 脱敏处理 | 张* |
| trans_desc | 去除特殊字符 | |
| risk_flag | 标记高风险交易标识 | |

### 3.4 合同信息清洗规则

| 字段 | 清洗规则 | 示例 |
|------|----------|------|
| contract_type | 标准化编码 | |
| asset_class | 标准化五级分类 | "正常" -> "1", "关注" -> "2" |
| five_class_status | 标准化分类状态 | |
| guarantee_type | 标准化担保方式 | "抵押" -> "2", "信用" -> "1" |
| overdue_days | 空值填充为0 | NULL -> 0 |

---

## 四、ETL逻辑设计

### 4.1 客户信息清洗ETL

```sql
INSERT OVERWRITE TABLE stg_customer PARTITION(dt='${bizdate}')
SELECT 
    customer_id,
    TRIM(customer_name) AS customer_name,
    CASE id_type
        WHEN '身份证' THEN '01'
        WHEN '护照' THEN '02'
        WHEN '军官证' THEN '03'
        ELSE '99'
    END AS id_type,
    UPPER(TRIM(id_number)) AS id_number,
    SHA2(id_number, 256) AS id_number_hash,
    CASE 
        WHEN gender IN ('1', '男', 'M') THEN 'M'
        WHEN gender IN ('2', '女', 'F') THEN 'F'
        ELSE 'U'
    END AS gender,
    TO_DATE(birthday) AS birthday,
    CASE nationality
        WHEN '中国' THEN 'CN'
        WHEN '美国' THEN 'US'
        ELSE 'OT'
    END AS nationality,
    occupation,
    TRIM(address) AS address,
    REGEXP_REPLACE(phone, '[^0-9]', '') AS phone,
    CASE customer_type
        WHEN '个人' THEN '1'
        WHEN '企业' THEN '2'
        ELSE customer_type
    END AS customer_type,
    customer_level,
    CASE risk_level
        WHEN '高' THEN 'H'
        WHEN '中' THEN 'M'
        WHEN '低' THEN 'L'
        ELSE risk_level
    END AS risk_level,
    COALESCE(annual_income, 0) AS annual_income,
    source_channel,
    branch_id,
    TO_DATE(create_date) AS create_date,
    TO_DATE(update_date) AS update_date,
    is_active,
    CURRENT_TIMESTAMP() AS etl_time,
    '${batch_no}' AS etl_batch_no
FROM ods_customer
WHERE is_valid = '1';
```

### 4.2 交易流水清洗ETL

```sql
INSERT OVERWRITE TABLE stg_transaction PARTITION(dt='${bizdate}')
SELECT 
    trans_id,
    account_id,
    customer_id,
    trans_type,
    trans_sub_type,
    COALESCE(trans_amount, 0) AS trans_amount,
    trans_currency,
    CASE trans_currency
        WHEN 'CNY' THEN trans_amount
        ELSE COALESCE(trans_amount * NVL(exchange_rate, 1), trans_amount)
    END AS trans_amount_cny,
    trans_date,
    UNIX_TIMESTAMP(trans_date) * 1000 AS trans_timestamp,
    CASE trans_channel
        WHEN '柜面' THEN '1'
        WHEN '自助' THEN '2'
        WHEN '网银' THEN '3'
        WHEN '手机' THEN '4'
        ELSE trans_channel
    END AS trans_channel,
    trans_channel_name,
    opposite_account,
    CONCAT(LEFT(opposite_name, 1), '*') AS opposite_name,
    opposite_bank,
    REGEXP_REPLACE(trans_desc, '[^\w\u4e00-\u9fa5]', '') AS trans_desc,
    branch_id,
    terminal_id,
    operator_id,
    trans_status,
    is_reversed,
    CASE 
        WHEN trans_amount >= 500000 THEN 'Y'
        ELSE 'N'
    END AS risk_flag,
    CURRENT_DATE() AS update_date,
    CURRENT_TIMESTAMP() AS etl_time,
    '${batch_no}' AS etl_batch_no
FROM ods_transaction t
LEFT JOIN ods_exchange_rate e ON t.trans_currency = e.currency_code AND e.bizdate = '${bizdate}'
WHERE t.bizdate = '${bizdate}';
```

### 4.3 大额交易识别ETL

```sql
INSERT INTO stg_large_trans_temp
SELECT 
    trans_id,
    account_id,
    customer_id,
    trans_amount,
    trans_date,
    trans_type,
    trans_channel,
    CASE 
        WHEN trans_amount >= 500000 THEN 'LARGE'
        ELSE 'NORMAL'
    END AS trans_flag
FROM stg_transaction
WHERE dt = '${bizdate}'
    AND trans_amount >= 500000;
```

---

## 五、数据质量检查

### 5.1 检查规则

| 检查类型 | 检查规则 | 阈值 | 处理方式 |
|----------|----------|------|----------|
| 完整性 | customer_id为空 | >0条 | 阻断 |
| 完整性 | 必填字段为空 | >0条 | 阻断 |
| 准确性 | id_number格式错误 | >0条 | 标记异常 |
| 准确性 | 日期格式错误 | >0条 | 标记异常 |
| 准确性 | 金额为负数 | >0条 | 标记异常 |
| 一致性 | customer_id在ods存在但在stg不存在 | >0条 | 警告 |
| 重复性 | customer_id重复 | >0条 | 标记异常 |

### 5.2 数据质量报告

```sql
-- 生成数据质量报告
INSERT INTO dq_check_report
SELECT 
    '${bizdate}' AS check_date,
    'stg_customer' AS table_name,
    'customer_id' AS check_field,
    ' Completeness' AS check_type,
    COUNT(*) AS error_count,
    CASE WHEN COUNT(*) > 0 THEN 'FAIL' ELSE 'PASS' END AS check_result,
    CURRENT_TIMESTAMP() AS etl_time
FROM stg_customer
WHERE dt = '${bizdate}' AND customer_id IS NULL;
```

---

## 六、调度配置

### 6.1 调度时间

| 任务 | 调度频率 | 执行时间 |
|------|----------|----------|
| stg_customer | 每日全量 | 01:00 |
| stg_account | 每日增量 | 01:30 |
| stg_transaction | 每日增量 | 02:00 |
| stg_contract | 每日增量 | 02:30 |
| stg_organization | 每月全量 | 03:00 |
| stg_risk_indicator | 每日增量 | 03:30 |

### 6.2 调度依赖

```
ods_customer_load -> stg_customer_clean -> dq_check_customer
ods_account_load -> stg_account_clean -> dq_check_account
ods_transaction_load -> stg_transaction_clean -> dq_check_transaction
```

---

## 七、数据脱敏规则

### 7.1 敏感字段脱敏

| 字段 | 脱敏方式 | 示例 |
|------|----------|------|
| id_number | 哈希+掩码 | 110101****1234 |
| phone | 掩码 | 138****0000 |
| opposite_account | 掩码 | 6222****890 |
| opposite_name | 掩码 | 张* |
| address | 掩码 | 北京市海淀区*** |
| account_id | 掩码 | 6222****7890 |

### 7.2 脱敏函数

```sql
-- 证件号脱敏
CREATE FUNCTION mask_id_number AS 'com.dw.MaskUDF.maskIdNumber';

-- 手机号脱敏
CREATE FUNCTION mask_phone AS 'com.dw.MaskUDF.maskPhone';

-- 账户号脱敏
CREATE FUNCTION mask_account AS 'com.dw.MaskUDF.maskAccount';

-- 姓名脱敏
CREATE FUNCTION mask_name AS 'com.dw.MaskUDF.maskName';
```
