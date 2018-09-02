-- Create table
create table NCMS_inpdetails
(
  N707_01                     VARCHAR2(100) not null,
  N707_02                     VARCHAR2(36) not null,
  N707_03                     VARCHAR2(6) not null,
  N707_04                     VARCHAR2(192) not null,
  N707_05                     VARCHAR2(24) not null,
  N707_06                     VARCHAR2(192)not null,
  N707_07                     VARCHAR2(150),
  N707_08                     VARCHAR2(300),
  N707_09                     VARCHAR2(20),
  N707_10                     NUMBER(20,4)not null,
  N707_11                     NUMBER(20,4)not null,
  N707_12                     VARCHAR2(50),
  N707_13                     DATE not null,
  N707_14                     NUMBER(20,4),
  N707_15                     NUMBER(20,4),
  N707_16                     VARCHAR2(24),
  N707_17                     VARCHAR2(192),
  N707_18                     NUMBER(20,4) not null,
  N707_19                     DATE not null,
  N707_20                     DATE not null,
  N707_21                     VARCHAR2(100) not null,
  N707_22                     VARCHAR2(50) not null,
  N707_23                     VARCHAR2(192) not null,
  N707_24                     VARCHAR2(1),
  N707_25                     VARCHAR2(192),
  N707_28                     VARCHAR2(1),
  N707_29                     VARCHAR2(50),
  N707_30                     VARCHAR2(50) 
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
comment on column NCMS_inpdetails.N707_01 is '住院处方流水号';
comment on column NCMS_inpdetails.N707_02 is '项目序号（费用明细HIS系统唯一标识）';
comment on column NCMS_inpdetails.N707_03 is '费用类别代码';
comment on column NCMS_inpdetails.N707_04 is '费用类别名称';
comment on column NCMS_inpdetails.N707_05 is 'HIS 系统项目代码';
comment on column NCMS_inpdetails.N707_06 is 'HIS 系统项目名称';
comment on column NCMS_inpdetails.N707_07 is '剂型';
comment on column NCMS_inpdetails.N707_08 is '规格';
comment on column NCMS_inpdetails.N707_09 is '单位';
comment on column NCMS_inpdetails.N707_10 is '单价（元）';
comment on column NCMS_inpdetails.N707_11 is '费用金额（元）';
comment on column NCMS_inpdetails.N707_12 is '医生姓名';
comment on column NCMS_inpdetails.N707_13 is '开单日期';
comment on column NCMS_inpdetails.N707_14 is '付数';
comment on column NCMS_inpdetails.N707_15 is '数量';
comment on column NCMS_inpdetails.N707_16 is '农合项目代码';
comment on column NCMS_inpdetails.N707_17 is '农合项目名称';
comment on column NCMS_inpdetails.N707_18 is '可报销金额（元）';
comment on column NCMS_inpdetails.N707_19 is '创建时间';
comment on column NCMS_inpdetails.N707_20 is '更新时间';
comment on column NCMS_inpdetails.N707_21 is '住院登记流水号';
comment on column NCMS_inpdetails.N707_22 is '就医机构代码';
comment on column NCMS_inpdetails.N707_23 is '就医机构名称';
comment on column NCMS_inpdetails.N707_24 is '国产/进口标识代码';
comment on column NCMS_inpdetails.N707_25 is '国产/进口标识名称';
comment on column NCMS_inpdetails.N707_28 is '目录属性代码';
comment on column NCMS_inpdetails.N707_29 is '目录属性名称';
comment on column NCMS_inpdetails.N707_30 is '集中招标采购项目编码';


-- Create/Recreate indexes 
create index IND_1_NCMS_inpdetails on NCMS_inpdetails (N707_01)
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
create index IND_2_NCMS_inpdetails on NCMS_inpdetails (N707_02)
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
  
create index IND_3_NCMS_inpdetails on NCMS_inpdetails (N707_21)
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
