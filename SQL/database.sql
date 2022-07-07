CREATE DATABASE КомпьютерныйКлуб
GO
USE КомпьютерныйКлуб

CREATE TABLE [КатегорияКомпьютера]
( 
	[ИДКатегории]     integer  NOT NULL IDENTITY(1,1) PRIMARY KEY,
	[Категория]       nvarchar(15)  NOT NULL UNIQUE,
	[ЦенаЗаЧасИгры]   decimal(9, 2)  NOT NULL , CHECK([ЦенаЗаЧасИгры]>0))

CREATE TABLE [Игра]
(
        [ИДИгры]            integer  NOT NULL IDENTITY(1,1) PRIMARY KEY, 
	[НазваниеИгры]      nvarchar(50)  NOT NULL UNIQUE,
	[ЖанрИгры]          nvarchar(50)  NULL ,
	[Разработчик]       nvarchar(50)  NULL ,
	[ДатаВыхода]        date  NULL )

CREATE TABLE [ИграКатегория]
( 
	[ИДКатегории]       integer  NOT NULL ,
	[ИДИгры]            integer  NOT NULL ,
	CONSTRAINT [XPKИграКатегория] PRIMARY KEY  CLUSTERED ([ИДКатегории],[ИДИгры]),
	CONSTRAINT [КатегорияКомпьютера_ИграКатегория] FOREIGN KEY ([ИДКатегории]) REFERENCES [КатегорияКомпьютера]([ИДКатегории]) ON DELETE NO ACTION ON UPDATE NO ACTION,
	CONSTRAINT [Игра_ИграКатегория] FOREIGN KEY ([ИДИгры]) REFERENCES [Игра]([ИДИгры]) ON DELETE NO ACTION ON UPDATE NO ACTION)

CREATE TABLE [Клиент]
( 
        [ИДКлиента]          integer  NOT NULL IDENTITY(1,1) PRIMARY KEY,
	[Никнейм]            nvarchar(50)  NOT NULL UNIQUE,
	[Почта]              nvarchar(50)  NOT NULL UNIQUE,
	[Пароль]             nvarchar(15)  NOT NULL , CHECK(LEN([Пароль])>=5),
	[БалансКошелька]     decimal(9, 2)  NOT NULL DEFAULT 0, CHECK([БалансКошелька]>=0))

CREATE TABLE [Компьютер]
( 
	[ИнвентарныйНомер]  integer  NOT NULL IDENTITY(1,1) PRIMARY KEY,
	[ИДКатегории]       integer  NOT NULL ,
	[Модель]            nvarchar(15)  NULL ,
	[Производитель]     nvarchar(25)  NULL , 
        CONSTRAINT [КатегорияКомпьютера_Компьютер] FOREIGN KEY ([ИДКатегории]) REFERENCES [КатегорияКомпьютера]([ИДКатегории]) ON DELETE NO ACTION ON UPDATE NO ACTION)

CREATE TABLE [Кошелек]
( 
        [ИДКлиента]         integer  NOT NULL,
	[ДатаВремя]         datetime  NOT NULL DEFAULT GETDATE(),
	[Сумма]             decimal(9, 2) NOT NULL, CHECK([Сумма]>0),
	[КатегорияОперации] nvarchar(15)  NOT NULL , CHECK([КатегорияОперации]='Снятие' OR [КатегорияОперации]='Пополнение'), 
        CONSTRAINT [XPKКошелек] PRIMARY KEY  CLUSTERED ([ИДКлиента],[ДатаВремя]),
        CONSTRAINT [Клиент_Кошелек] FOREIGN KEY ([ИДКлиента]) REFERENCES [Клиент]([ИДКлиента]) ON DELETE NO ACTION ON UPDATE NO ACTION)   

CREATE TABLE [Сеанс]
( 
	[ИДСеанса]          integer  NOT NULL IDENTITY(1,1) PRIMARY KEY,
        [ИДКлиента]         integer  NOT NULL ,
	[ИнвентарныйНомер]  integer  NOT NULL , CHECK([ИнвентарныйНомер]>=0), 
	[ВремяНачала]       datetime  NOT NULL , CHECK([ВремяНачала]>=GETDATE()),
	[ВремяОкончания]    datetime  NOT NULL , CHECK([ВремяОкончания]>GETDATE()),
	[Сумма]             decimal(9, 2)  NULL ,
	[ДатаВремя]         datetime  NULL ,
        CONSTRAINT [Клиент_Сеанс] FOREIGN KEY ([ИДКлиента]) REFERENCES [Клиент]([ИДКлиента]) ON DELETE NO ACTION ON UPDATE NO ACTION,
        CONSTRAINT [Компьютер_Сеанс] FOREIGN KEY ([ИнвентарныйНомер]) REFERENCES [Компьютер]([ИнвентарныйНомер]) ON DELETE NO ACTION ON UPDATE NO ACTION,
        CONSTRAINT [Кошелек_Сеанс] FOREIGN KEY ([ИДКлиента],[ДатаВремя]) REFERENCES [Кошелек]([ИДКлиента],[ДатаВремя]) ON DELETE NO ACTION ON UPDATE NO ACTION)
