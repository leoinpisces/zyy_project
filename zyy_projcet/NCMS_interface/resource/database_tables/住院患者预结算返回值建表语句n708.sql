-- Create table
create table NCMS_preinppay_708
(
  N708_01                     VARCHAR2(100) not null,
  N708_02                     VARCHAR2(100) not null,
  N708_03                     VARCHAR2(50) not null,
  N708_04                     VARCHAR2(192) not null,
  N708_05                     VARCHAR2(1) not null,
  N708_06                     VARCHAR2(192) not null,
  N708_07                     VARCHAR2(6) not null,
  N708_08                     VARCHAR2(192) not null,
  N708_09                     VARCHAR2(100) not null,
  N708_10                     VARCHAR2(50) not null,
  N708_11                     VARCHAR2(18) not null,
  N708_12                     VARCHAR2(30) ,
  N708_13                     VARCHAR2(1) not null,
  N708_14                     VARCHAR2(192) not null,
  N708_15                     VARCHAR2(50) not null,
  N708_16                     VARCHAR2(2) not null,
  N708_17                     VARCHAR2(192) not null,
  N708_18                     VARCHAR2(50) ,
  N708_19                     VARCHAR2(192) ,
  N708_20                     VARCHAR2(20) not null,
  N708_21                     DATE not null,
  N708_22                     DATE not null,
  N708_23                     VARCHAR2(50) not null,
  N708_24                     VARCHAR2(150) not null,
  N708_25                     VARCHAR2(20) ,
  N708_26                     VARCHAR2(300) ,
  N708_27                     VARCHAR2(50) ,
  N708_28                     VARCHAR2(192) ,
  N708_29                     NUMBER(20,4) not null,
  N708_30                     NUMBER(20,4) not null,
  N708_31                     NUMBER(20,4) not null,
  N708_32                     VARCHAR2(4) not null,
  N708_33                     NUMBER(20,4) not null,
  N708_34                     NUMBER(20,4) ,
  N708_35                     NUMBER(20,4) ,
  N708_36                     NUMBER(20,4) ,
  N708_37                     NUMBER(20,4) ,
  N708_38                     NUMBER(20,4) ,
  N708_39                     NUMBER(20,4) not null,
  N708_40                     NUMBER(20) not null,
  N708_41                     NUMBER(20,4) not null,
  N708_42                     NUMBER(20,4) ,
  N708_43                     VARCHAR2(300) ,
  N708_44                     VARCHAR2(50) ,
  N708_45                     VARCHAR2(192) ,
  N708_46                     NUMBER(20,4) ,
  N708_47                     VARCHAR2(300) ,
  N708_48                     NUMBER(20,4) not null,
  N708_49                     VARCHAR2(36) not null
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
comment on column NCMS_preinppay_708.N708_01 is 'HIS系统单据编码';
comment on column NCMS_preinppay_708.N708_02 is '住院登记流水号';
comment on column NCMS_preinppay_708.N708_03 is '就医机构代码';
comment on column NCMS_preinppay_708.N708_04 is '就医机构名称';
comment on column NCMS_preinppay_708.N708_05 is '就医机构级别代码';
comment on column NCMS_preinppay_708.N708_06 is '就医机构级别名称';
comment on column NCMS_preinppay_708.N708_07 is '参合地区编码';
comment on column NCMS_preinppay_708.N708_08 is '参合地区名称';
comment on column NCMS_preinppay_708.N708_09 is '个人参合编码';
comment on column NCMS_preinppay_708.N708_10 is '患者姓名';
comment on column NCMS_preinppay_708.N708_11 is '患者身份证号';
comment on column NCMS_preinppay_708.N708_12 is '电话号码';
comment on column NCMS_preinppay_708.N708_13 is '患者性别代码';
comment on column NCMS_preinppay_708.N708_14 is '患者性别名称';
comment on column NCMS_preinppay_708.N708_15 is '医疗证号';
comment on column NCMS_preinppay_708.N708_16 is '就诊类型代码';
comment on column NCMS_preinppay_708.N708_17 is '就诊类型名称';
comment on column NCMS_preinppay_708.N708_18 is '户主姓名';
comment on column NCMS_preinppay_708.N708_19 is '家庭住址';
comment on column NCMS_preinppay_708.N708_20 is '住院号';
comment on column NCMS_preinppay_708.N708_21 is '入院日期';
comment on column NCMS_preinppay_708.N708_22 is '出院日期';
comment on column NCMS_preinppay_708.N708_23 is '主要诊断代码';
comment on column NCMS_preinppay_708.N708_24 is '主要诊断名称';
comment on column NCMS_preinppay_708.N708_25 is '手术名称代码';
comment on column NCMS_preinppay_708.N708_26 is '手术名称';
comment on column NCMS_preinppay_708.N708_27 is '新农合经办机构代码';
comment on column NCMS_preinppay_708.N708_28 is '新农合经办机构名称';
comment on column NCMS_preinppay_708.N708_29 is '费用总额';
comment on column NCMS_preinppay_708.N708_30 is '自付总额';
comment on column NCMS_preinppay_708.N708_31 is '实际报销总额';
comment on column NCMS_preinppay_708.N708_32 is '报销（政策）年度';
comment on column NCMS_preinppay_708.N708_33 is '可报销总额';
comment on column NCMS_preinppay_708.N708_34 is '单病种费用定额';
comment on column NCMS_preinppay_708.N708_35 is '大病保险可补偿额';
comment on column NCMS_preinppay_708.N708_36 is '大病保险实际补偿额';
comment on column NCMS_preinppay_708.N708_37 is '民政救助补偿额';
comment on column NCMS_preinppay_708.N708_38 is '整体报销比例';
comment on column NCMS_preinppay_708.N708_39 is '本年度累计报销金额';
comment on column NCMS_preinppay_708.N708_40 is '本年度累计报销次数';
comment on column NCMS_preinppay_708.N708_41 is '起付线';
comment on column NCMS_preinppay_708.N708_42 is '封顶线';
comment on column NCMS_preinppay_708.N708_43 is '备注信息';
comment on column NCMS_preinppay_708.N708_44 is '结算单元编码';
comment on column NCMS_preinppay_708.N708_45 is '结算单元名称';
comment on column NCMS_preinppay_708.N708_46 is '扣减总额';
comment on column NCMS_preinppay_708.N708_47 is '扣减原因';
comment on column NCMS_preinppay_708.N708_48 is '垫付总额（元）';
comment on column NCMS_preinppay_708.N708_49 is '预结算流水号';
-- Create/Recreate indexes 
create index IND_1_NCMS_preinppay_708 on NCMS_preinppay_708 (N708_01)
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
create index IND_2_NCMS_preinppay_708 on NCMS_preinppay_708 (N708_02)
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
  
create index IND_3_NCMS_preinppay_708 on NCMS_preinppay_708 (N708_11)
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