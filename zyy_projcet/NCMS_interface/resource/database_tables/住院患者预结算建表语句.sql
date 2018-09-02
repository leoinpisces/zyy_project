-- Create table
create table NCMS_preinppay
(
 N706_01                     VARCHAR2(100) not null,
 N706_02                     VARCHAR2(100) not null,
 N706_03                     VARCHAR2(50) not null,
 N706_04                     VARCHAR2(192) not null,
 N706_05                     VARCHAR2(2) not null,
 N706_06                     VARCHAR2(192) not null,
 N706_07                     VARCHAR2(50) not null,
 N706_08                     VARCHAR2(50) not null,
 N706_09                     VARCHAR2(50) not null,
 N706_10                     VARCHAR2(1) not null,
 N706_11                     VARCHAR2(192) not null,
 N706_12                     VARCHAR2(18) not null,
 N706_13                     NUMBER(3) not null,
 N706_14                     VARCHAR2(192) ,
 N706_15                     VARCHAR2(6) not null,
 N706_16                     VARCHAR2(192) not null,
 N706_17                     VARCHAR2(6) not null,
 N706_18                     VARCHAR2(192) not null,
 N706_19                     VARCHAR2(6) not null,
 N706_20                     VARCHAR2(192) not null,
 N706_21                     VARCHAR2(50) ,
 N706_22                     VARCHAR2(30) ,
 N706_23                     VARCHAR2(2) not null,
 N706_24                     VARCHAR2(192) not null,
 N706_25                     VARCHAR2(50) not null,
 N706_26                     DATE not null,
 N706_27                     DATE not null,
 N706_28                     DATE not null,
 N706_29                     VARCHAR2(20) not null,
 N706_30                     VARCHAR2(50) not null,
 N706_31                     VARCHAR2(50) not null,
 N706_32                     VARCHAR2(150) not null,
 N706_33                     VARCHAR2(50) ,
 N706_34                     VARCHAR2(150) ,
 N706_35                     VARCHAR2(20) ,
 N706_36                     VARCHAR2(300) ,
 N706_37                     VARCHAR2(8) ,
 N706_38                     VARCHAR2(192) ,
 N706_39                     VARCHAR2(8) ,
 N706_40                     VARCHAR2(192) ,
 N706_41                     VARCHAR2(1) ,
 N706_42                     VARCHAR2(192) ,
 N706_43                     VARCHAR2(1) not null,
 N706_44                     VARCHAR2(192) not null,
 N706_45                     VARCHAR2(300) ,
 N706_46                     VARCHAR2(10) ,
 N706_47                     VARCHAR2(75) ,
 N706_48                     VARCHAR2(50) ,
 N706_49                     NUMBER(20,4) not null,
 N706_50                     NUMBER(20,4) not null,
 N706_51                     VARCHAR2(4) not null,
 N706_60                     DATE ,
 N706_52                     DATE not null,
 N706_53                     DATE not null,
 N706_54                     NUMBER(20,4) ,
 N706_55                     NUMBER(20,4) ,
 N706_56                     NUMBER(20,4) ,
 N706_57                     NUMBER(20,4) 
)
tablespace TSP_JHEMR
  pctfree 10
  pctused 40
  initrans 1
  maxtrans 255
  storage
  (
    initial 25M
    next 8K
    minextents 1
    maxextents unlimited
  );
-- Add comments to the columns 
comment on column NCMS_preinppay.N706_01 is 'HIS系统单据编码';
comment on column NCMS_preinppay.N706_02 is '住院登记流水号';
comment on column NCMS_preinppay.N706_03 is '就医机构代码';
comment on column NCMS_preinppay.N706_04 is '就医机构名称';
comment on column NCMS_preinppay.N706_05 is '就医机构级别代码';
comment on column NCMS_preinppay.N706_06 is '就医机构级别名称';
comment on column NCMS_preinppay.N706_07 is '医院信息系统操作者代码';
comment on column NCMS_preinppay.N706_08 is '医院信息系统操作者姓名';
comment on column NCMS_preinppay.N706_09 is '患者姓名';
comment on column NCMS_preinppay.N706_10 is '患者性别代码';
comment on column NCMS_preinppay.N706_11 is '患者性别名称';
comment on column NCMS_preinppay.N706_12 is '患者身份证号';
comment on column NCMS_preinppay.N706_13 is '年龄';
comment on column NCMS_preinppay.N706_14 is '患者通讯地址';
comment on column NCMS_preinppay.N706_15 is '参合省代码';
comment on column NCMS_preinppay.N706_16 is '参合省名称';
comment on column NCMS_preinppay.N706_17 is '参合市代码';
comment on column NCMS_preinppay.N706_18 is '参合市名称';
comment on column NCMS_preinppay.N706_19 is '参合区代码';
comment on column NCMS_preinppay.N706_20 is '参合区名称';
comment on column NCMS_preinppay.N706_21 is '联系人姓名';
comment on column NCMS_preinppay.N706_22 is '电话号码';
comment on column NCMS_preinppay.N706_23 is '就诊类型代码';
comment on column NCMS_preinppay.N706_24 is '就诊类型名称';
comment on column NCMS_preinppay.N706_25 is '医生姓名';
comment on column NCMS_preinppay.N706_26 is '入院日期';
comment on column NCMS_preinppay.N706_27 is '出院日期';
comment on column NCMS_preinppay.N706_28 is '结算日期';
comment on column NCMS_preinppay.N706_29 is '住院号';
comment on column NCMS_preinppay.N706_30 is '医疗证/卡号';
comment on column NCMS_preinppay.N706_31 is '主要诊断代码';
comment on column NCMS_preinppay.N706_32 is '主要诊断名称';
comment on column NCMS_preinppay.N706_33 is '其他诊断代码';
comment on column NCMS_preinppay.N706_34 is '其他诊断名称';
comment on column NCMS_preinppay.N706_35 is '手术名称代码';
comment on column NCMS_preinppay.N706_36 is '手术名称';
comment on column NCMS_preinppay.N706_37 is '入院科室代码';
comment on column NCMS_preinppay.N706_38 is '入院科室名称';
comment on column NCMS_preinppay.N706_39 is '出院科室代码';
comment on column NCMS_preinppay.N706_40 is '出院科室名称';
comment on column NCMS_preinppay.N706_41 is '入院状态代码';
comment on column NCMS_preinppay.N706_42 is '入院状态名称';
comment on column NCMS_preinppay.N706_43 is '出院状态代码';
comment on column NCMS_preinppay.N706_44 is '出院状态名称';
comment on column NCMS_preinppay.N706_45 is '出院情况';
comment on column NCMS_preinppay.N706_46 is '并发症代码';
comment on column NCMS_preinppay.N706_47 is '并发症名称';
comment on column NCMS_preinppay.N706_48 is '居民健康卡号';
comment on column NCMS_preinppay.N706_49 is '费用总额（元）';
comment on column NCMS_preinppay.N706_50 is '可报销总额（元）';
comment on column NCMS_preinppay.N706_51 is '报销（政策）年度';
comment on column NCMS_preinppay.N706_60 is '出生日期';
comment on column NCMS_preinppay.N706_52 is '创建时间';
comment on column NCMS_preinppay.N706_53 is '更新时间';
comment on column NCMS_preinppay.N706_54 is '单病种费用定额';
comment on column NCMS_preinppay.N706_55 is '民政救助补偿额';
comment on column NCMS_preinppay.N706_56 is '大病保险可补偿额';
comment on column NCMS_preinppay.N706_57 is '大病保险实际补偿额';


-- Create/Recreate indexes 
create index IND_1_NCMS_preinppay on NCMS_preinppay (N706_01)
  tablespace TSP_JHEMR
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 2M
    next 1M
    minextents 1
    maxextents unlimited
  );
create index IND_2_NCMS_preinppay on NCMS_preinppay (N706_02)
  tablespace TSP_JHEMR
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 2M
    next 1M
    minextents 1
    maxextents unlimited
  );
  
create index IND_3_NCMS_preinppay on NCMS_preinppay (N706_12)
  tablespace TSP_JHEMR
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 2M
    next 1M
    minextents 1
    maxextents unlimited
  );