-- Create table
create table NCMS_zzrecord
(
  N507_05                     VARCHAR2(100) not null,
  D507_01                     VARCHAR2(50) not null,
  D507_02                     VARCHAR2(50) not null,
  D507_03                     VARCHAR2(10),
  D507_04                     DATE not null,
  D507_05                     VARCHAR2(270),
  D507_06                     VARCHAR2(50),
  D507_07                     VARCHAR2(50),
  D507_08                     VARCHAR2(50) not null,
  D507_09                     VARCHAR2(2) not null,
  D507_10                     DATE not null,
  N507_01                     VARCHAR2(6) not null,
  N507_02                     VARCHAR2(192),
  N507_06                     VARCHAR2(192) not null,
  N507_07                     VARCHAR2(192),
  N507_08                     VARCHAR2(192) not null,
  N507_09                     VARCHAR2(50),
  N507_10                     VARCHAR2(200),
  N507_11                     VARCHAR2(192) not null,
  N507_12                     VARCHAR2(192) not null,
  N507_13                     VARCHAR2(18) not null,
  N507_14                     VARCHAR2(50),
  N507_15                     VARCHAR2(50) not null,
  N507_16                     VARCHAR2(50),
  N507_17                     DATE,
  N507_18                     VARCHAR2(1) not null,
  N507_19                     VARCHAR2(192) not null,
  N507_20                     VARCHAR2(50) not null,
  N507_21                     VARCHAR2(50) not null,
  N507_22                     VARCHAR2(50) not null,
  N507_23                     DATE not null,
  N507_03                     DATE not null,
  N507_04                     DATE not null,
  N507_24                     VARCHAR2(20),
  N507_25                     VARCHAR2(100),
  N507_26                     VARCHAR2(50) not null,
  N507_27                     VARCHAR2(50) not null,
  N507_28                     VARCHAR2(1),
  N507_29                     VARCHAR2(1),
  N507_30                     VARCHAR2(50) not null,
  N507_31                     VARCHAR2(50),
  N507_32                     VARCHAR2(192),
  N507_33                     VARCHAR2(50),
  N507_34                     VARCHAR2(192),
  N507_35                     NUMBER(20,4),
  N507_36                     VARCHAR2(192),
  N507_37                     VARCHAR2(50),
  N507_38                     VARCHAR2(192),
  N507_39                     VARCHAR2(2) not null,
  N507_40                     VARCHAR2(192) not null,
  N507_41                     VARCHAR2(6) not null,
  N507_42                     VARCHAR2(192) not null,
  N507_43                     VARCHAR2(6) not null,
  N507_44                     VARCHAR2(192) not null
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
comment on column NCMS_zzrecord.N507_05
  is '转诊单号';
comment on column NCMS_zzrecord.D507_01
  is '个人代码';
comment on column NCMS_zzrecord.D507_02
  is '患者姓名';
comment on column NCMS_zzrecord.D507_03
  is '疾病代码';
comment on column NCMS_zzrecord.D507_04
  is '申请时间';
comment on column NCMS_zzrecord.D507_05
  is '申请说明';
comment on column NCMS_zzrecord.D507_06
  is '经办机构代码';
comment on column NCMS_zzrecord.D507_07
  is '转出医院代码';
comment on column NCMS_zzrecord.D507_08
  is '转入医院1代码';
comment on column NCMS_zzrecord.D507_09
  is '转诊状态代码';
comment on column NCMS_zzrecord.D507_10
  is '审核日期';
comment on column NCMS_zzrecord.N507_01
  is '参合区（县）地区代码';
comment on column NCMS_zzrecord.N507_02
  is '疾病名称';
comment on column NCMS_zzrecord.N507_06
  is '经办机构名称';
comment on column NCMS_zzrecord.N507_07
  is '转出医院名称';
comment on column NCMS_zzrecord.N507_08
  is '转入医院1名称';
comment on column NCMS_zzrecord.N507_09
  is '审核人姓名';
comment on column NCMS_zzrecord.N507_10
  is '审核说明';
comment on column NCMS_zzrecord.N507_11
  is '参合区（县）地区名称';
comment on column NCMS_zzrecord.N507_12
  is '审核状态名称';
comment on column NCMS_zzrecord.N507_13
  is '身份证号';
comment on column NCMS_zzrecord.N507_14
  is '身份证号存储地址';
comment on column NCMS_zzrecord.N507_15
  is '医疗卡/证号';
comment on column NCMS_zzrecord.N507_16
  is '医疗卡/证号存储地址';
comment on column NCMS_zzrecord.N507_17
  is '就诊日期';
comment on column NCMS_zzrecord.N507_18
  is '性别代码';
comment on column NCMS_zzrecord.N507_19
  is '性别名称';
comment on column NCMS_zzrecord.N507_20
  is '机构联系人';
comment on column NCMS_zzrecord.N507_21
  is '机构联系方式';
comment on column NCMS_zzrecord.N507_22
  is '机构联系邮箱';
comment on column NCMS_zzrecord.N507_23
  is '出生日期';
comment on column NCMS_zzrecord.N507_03
  is '创建时间';
comment on column NCMS_zzrecord.N507_04
  is '更新时间';
comment on column NCMS_zzrecord.N507_24
  is '单病种代码';
comment on column NCMS_zzrecord.N507_25
  is '单病种名称';
comment on column NCMS_zzrecord.N507_26
  is '患者联系人';
comment on column NCMS_zzrecord.N507_27
  is '患者联系电话';
comment on column NCMS_zzrecord.N507_28
  is '民政救助标识';
comment on column NCMS_zzrecord.N507_29
  is '大病救助标志';
comment on column NCMS_zzrecord.N507_30
  is '家庭代码';
comment on column NCMS_zzrecord.N507_31
  is '转入医院2代码';
comment on column NCMS_zzrecord.N507_32
  is '转入医院2名称';
comment on column NCMS_zzrecord.N507_33
  is '转入医院3代码';
comment on column NCMS_zzrecord.N507_34
  is '转入医院3名称';
comment on column NCMS_zzrecord.N507_35
  is '累计金额（元）';
comment on column NCMS_zzrecord.N507_36
  is '账户名称';
comment on column NCMS_zzrecord.N507_37
  is '开户银行账号';
comment on column NCMS_zzrecord.N507_38
  is '开户银行名称';
comment on column NCMS_zzrecord.N507_39
  is '医疗付费方式代码';
comment on column NCMS_zzrecord.N507_40
  is '医疗付费方式名称';
comment on column NCMS_zzrecord.N507_41
  is '参合省代码';
comment on column NCMS_zzrecord.N507_42
  is '参合省名称';
comment on column NCMS_zzrecord.N507_43
  is '参合市代码';
comment on column NCMS_zzrecord.N507_44
  is '参合市名称';
-- Create/Recreate indexes 
create index IND_1_NCMS_zzrecord on NCMS_zzrecord (N507_05)
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
create index IND_2_NCMS_zzrecord on NCMS_zzrecord (D507_01)
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
-- Create/Recreate primary, unique and foreign key constraints 
alter table NCMS_zzrecord
  add constraint PK_NCMS_zzrecord primary key (N507_05, D507_01)
  using index 
  tablespace TSP_JHEMR
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 4M
    next 1M
    minextents 1
    maxextents unlimited
  );
