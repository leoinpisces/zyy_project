-- Create table
create table NCMS_inpregister
(
  N801_01                     VARCHAR2(100) not null,
  N801_02                     VARCHAR2(50) not null,
  N801_03                     VARCHAR2(192) not null,
  N801_04                     VARCHAR2(50) not null,
  N801_05                     VARCHAR2(1) not null,
  N801_06                     VARCHAR2(10) not null,
  N801_07                     VARCHAR2(18) not null,
  N801_08                     NUMBER(3) not null,
  N801_09                     VARCHAR2(192) ,
  N801_10                     VARCHAR2(6) not null,
  N801_11                     VARCHAR2(192) not null,
  N801_12                     VARCHAR2(6) not null,
  N801_13                     VARCHAR2(192) not null,
  N801_14                     VARCHAR2(6) not null,
  N801_15                     VARCHAR2(192) not null,
  N801_16                     VARCHAR2(50) not null,
  N801_17                     VARCHAR2(50) not null,
  N801_18                     VARCHAR2(3) ,
  N801_19                     VARCHAR2(3) ,
  N801_20                     VARCHAR2(50) ,
  N801_21                     VARCHAR2(150) ,
  N801_22                     VARCHAR2(50) ,
  N801_23                     VARCHAR2(150) ,
  N801_24                     VARCHAR2(20) ,
  N801_25                     VARCHAR2(300) ,
  N801_26                     VARCHAR2(20) ,
  N801_27                     VARCHAR2(150) ,
  N801_28                     VARCHAR2(8) not null,
  N801_29                     VARCHAR2(192) not null,
  N801_30                     VARCHAR2(2) not null,
  N801_31                     VARCHAR2(192) not null,
  N801_32                     VARCHAR2(10) ,
  N801_33                     VARCHAR2(75) ,
  N801_34                     VARCHAR2(1) not null,
  N801_35                     VARCHAR2(192) not null,
  N801_36                     VARCHAR2(50) ,
  N801_37                     VARCHAR2(30) ,
  N801_38                     VARCHAR2(50) ,
  N801_39                     DATE not null,
  N801_40                     VARCHAR2(20) not null,
  N801_41                     VARCHAR2(10) ,
  N801_42                     VARCHAR2(50) ,
  N801_43                     VARCHAR2(1) ,
  N801_44                     VARCHAR2(20) ,
  N801_45                     VARCHAR2(100) not null,
  N801_47                     DATE ,
  N801_48                     VARCHAR2(50) ,
  N801_49                     VARCHAR2(50) ,
  N801_50                     VARCHAR2(50) ,
  N801_51                     VARCHAR2(50) not null,
  N801_52                     DATE not null,
  N801_53                     DATE not null,
  N801_54                     DATE not null,
  N801_55                     VARCHAR2(50) not null,
  N801_56                     VARCHAR2(50) not null
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
comment on column NCMS_inpregister.N801_01 is '住院登记流水号';
comment on column NCMS_inpregister.N801_02 is '就医机构代码';
comment on column NCMS_inpregister.N801_03 is '就医机构名称';
comment on column NCMS_inpregister.N801_04 is '患者姓名';
comment on column NCMS_inpregister.N801_05 is '患者性别代码';
comment on column NCMS_inpregister.N801_06 is '患者性别名称';
comment on column NCMS_inpregister.N801_07 is '患者身份证号';
comment on column NCMS_inpregister.N801_08 is '年龄';
comment on column NCMS_inpregister.N801_09 is '患者通讯地址';
comment on column NCMS_inpregister.N801_10 is '参合省代码';
comment on column NCMS_inpregister.N801_11 is '参合省名称';
comment on column NCMS_inpregister.N801_12 is '参合市代码';
comment on column NCMS_inpregister.N801_13 is '参合市名称';
comment on column NCMS_inpregister.N801_14 is '参合区代码';
comment on column NCMS_inpregister.N801_15 is '参合区名称';
comment on column NCMS_inpregister.N801_16 is '家庭代码';
comment on column NCMS_inpregister.N801_17 is '个人代码';
comment on column NCMS_inpregister.N801_18 is '身高';
comment on column NCMS_inpregister.N801_19 is '体重';
comment on column NCMS_inpregister.N801_20 is '住院疾病诊断代码';
comment on column NCMS_inpregister.N801_21 is '住院疾病诊断名称';
comment on column NCMS_inpregister.N801_22 is '第二疾病诊断代码';
comment on column NCMS_inpregister.N801_23 is '第二疾病诊断名称';
comment on column NCMS_inpregister.N801_24 is '手术代码';
comment on column NCMS_inpregister.N801_25 is '手术名称';
comment on column NCMS_inpregister.N801_26 is '治疗编码';
comment on column NCMS_inpregister.N801_27 is '治疗名称';
comment on column NCMS_inpregister.N801_28 is '入院科室代码';
comment on column NCMS_inpregister.N801_29 is '入院科室名称';
comment on column NCMS_inpregister.N801_30 is '就诊类型代码';
comment on column NCMS_inpregister.N801_31 is '就诊类型名称';
comment on column NCMS_inpregister.N801_32 is '并发症代码';
comment on column NCMS_inpregister.N801_33 is '并发症名称';
comment on column NCMS_inpregister.N801_34 is '入院状态代码';
comment on column NCMS_inpregister.N801_35 is '入院状态名称';
comment on column NCMS_inpregister.N801_36 is '联系人姓名';
comment on column NCMS_inpregister.N801_37 is '电话号码';
comment on column NCMS_inpregister.N801_38 is '医生姓名';
comment on column NCMS_inpregister.N801_39 is '入院日期';
comment on column NCMS_inpregister.N801_40 is '住院号';
comment on column NCMS_inpregister.N801_41 is '床位号';
comment on column NCMS_inpregister.N801_42 is '入院病区';
comment on column NCMS_inpregister.N801_43 is '转诊类型代码';
comment on column NCMS_inpregister.N801_44 is '转诊类型名称';
comment on column NCMS_inpregister.N801_45 is '转诊单号';
comment on column NCMS_inpregister.N801_47 is '转院日期';
comment on column NCMS_inpregister.N801_48 is '医院住院收费收据号';
comment on column NCMS_inpregister.N801_49 is '民政通知书号';
comment on column NCMS_inpregister.N801_50 is '生育证号';
comment on column NCMS_inpregister.N801_51 is '医疗证/卡号';
comment on column NCMS_inpregister.N801_52 is '出生日期';
comment on column NCMS_inpregister.N801_53 is '创建时间';
comment on column NCMS_inpregister.N801_54 is '更新时间';
comment on column NCMS_inpregister.N801_55 is '医院信息系统操作者代码';
comment on column NCMS_inpregister.N801_56 is '医院信息系统操作者姓名';

-- Create/Recreate indexes 
create index IND_1_NCMS_inpregister on NCMS_inpregister (N801_01)
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
create index IND_2_NCMS_inpregister on NCMS_inpregister (N801_40)
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
  
create index IND_3_NCMS_inpregister on NCMS_inpregister (N801_07)
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
alter table NCMS_inpregister
  add constraint PK_NCMS_inpregister primary key (N801_01)
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
