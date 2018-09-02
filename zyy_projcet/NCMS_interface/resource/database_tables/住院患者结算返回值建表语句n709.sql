-- Create table
create table NCMS_inppay_709
(
  N709_01                     VARCHAR2(100) not null,
  N709_05                     VARCHAR2(24) not null,
  N709_06                     VARCHAR2(192) not null,
  N709_07                     NUMBER(20,4) not null,
  N709_08                     NUMBER(20,4) not null,
  N709_09                     NUMBER(20,4) not null,
  N709_10                     VARCHAR2(300) not null
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
comment on column NCMS_inppay_709.N709_01 is '住院处方流水号';
comment on column NCMS_inppay_709.N709_05 is 'HIS系统项目代码';
comment on column NCMS_inppay_709.N709_06 is 'HIS系统项目名称';
comment on column NCMS_inppay_709.N709_07 is '费用金额';
comment on column NCMS_inppay_709.N709_08 is '报销金额';
comment on column NCMS_inppay_709.N709_09 is '扣减金额';
comment on column NCMS_inppay_709.N709_10 is '扣减原因';
-- Create/Recreate indexes 
create index IND_1_NCMS_inppay_709 on NCMS_inppay_709 (N709_01)
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