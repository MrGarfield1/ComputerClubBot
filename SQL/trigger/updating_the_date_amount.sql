--Запись суммы на основе начала и конца сеанса и добавление транзакции в кошелек. 
--Проверка, свободно ли время выбранного сеанса. 
--Применение скидки, если это первый сеанс клиента. 
--Вывод информации о покупке (чек).
CREATE TRIGGER  ОбновлениеСуммыДаты  ON Сеанс
   AFTER INSERT
AS 
DECLARE @id integer
DECLARE @sum decimal(9, 2)
DECLARE @date datetime
DECLARE @session nvarchar(10)

DECLARE @i integer
SELECT @i=COUNT(с.ИнвентарныйНомер)
FROM inserted AS в INNER JOIN Сеанс AS с ON в.ИнвентарныйНомер=с.ИнвентарныйНомер 
WHERE в.ИнвентарныйНомер=с.ИнвентарныйНомер AND ((в.ВремяНачала BETWEEN с.ВремяНачала AND с.ВремяОкончания) OR (в.ВремяОкончания BETWEEN с.ВремяНачала AND с.ВремяОкончания))
GROUP BY с.ИнвентарныйНомер

IF @i=1
BEGIN
  DECLARE @j integer
  SELECT @j=COUNT(с.ИДКлиента) 
  FROM inserted AS в INNER JOIN Сеанс AS с ON в.ИДКлиента=с.ИДКлиента 
  WHERE в.ИДКлиента=с.ИДКлиента
  GROUP BY с.ИДКлиента

  IF @j=1
  BEGIN
    UPDATE Сеанс SET Сумма=(DATEDIFF(minute,в.ВремяНачала,в.ВремяОкончания)/60.0)*кк.ЦенаЗаЧасИгры-(DATEDIFF(minute,в.ВремяНачала,в.ВремяОкончания)/60.0)*кк.ЦенаЗаЧасИгры*15/100,
    @id=в.ИДКлиента, @sum=(DATEDIFF(minute,в.ВремяНачала,в.ВремяОкончания)/60.0)*кк.ЦенаЗаЧасИгры-(DATEDIFF(minute,в.ВремяНачала,в.ВремяОкончания)/60.0)*кк.ЦенаЗаЧасИгры*15/100, @session=в.ИДСеанса
    FROM inserted AS в INNER JOIN Компьютер AS к ON в.ИнвентарныйНомер=к.ИнвентарныйНомер INNER JOIN КатегорияКомпьютера AS кк ON к.ИДКатегории=кк.ИДКатегории
    WHERE в.ИДСеанса=Сеанс.ИДСеанса AND в.ИнвентарныйНомер=к.ИнвентарныйНомер
	PRINT('Применяется скидка')
  END
  ELSE
  BEGIN
    UPDATE Сеанс SET Сумма=(DATEDIFF(minute,в.ВремяНачала,в.ВремяОкончания)/60.0)*кк.ЦенаЗаЧасИгры, @id=в.ИДКлиента, @sum=(DATEDIFF(minute,в.ВремяНачала,в.ВремяОкончания)/60.0)*кк.ЦенаЗаЧасИгры, @session=в.ИДСеанса
    FROM inserted AS в INNER JOIN Компьютер AS к ON в.ИнвентарныйНомер=к.ИнвентарныйНомер INNER JOIN КатегорияКомпьютера AS кк ON к.ИДКатегории=кк.ИДКатегории
    WHERE в.ИДСеанса=Сеанс.ИДСеанса AND в.ИнвентарныйНомер=к.ИнвентарныйНомер
  END

  SET @date=GETDATE()
  INSERT INTO [Кошелек] VALUES
  (@id,@date,@sum,'Снятие')

  DECLARE @number integer
  DECLARE @name nvarchar(50)
  DECLARE @balance decimal(9, 2)
  DECLARE @daten datetime
  DECLARE @datek datetime
  DECLARE @category nvarchar(15)
  DECLARE @supernumber integer
  UPDATE Сеанс SET ДатаВремя=@date, @number=с.ИнвентарныйНомер, @name=кл.Никнейм, @balance=кл.БалансКошелька, @daten=с.ВремяНачала, @datek=с.ВремяОкончания, @category=кк.Категория
  FROM Сеанс AS с INNER JOIN Кошелек AS к ON с.ИДКлиента=к.ИДКлиента INNER JOIN Клиент AS кл ON с.ИДКлиента=кл.ИДКлиента INNER JOIN Компьютер AS ко ON с.ИнвентарныйНомер=ко.ИнвентарныйНомер 
  INNER JOIN КатегорияКомпьютера AS кк ON ко.ИДКатегории=кк.ИДКатегории
  WHERE с.ИДСеанса=@session

  SELECT @supernumber = FLOOR(RAND()*(999999-100000)+100000)

  PRINT('Спасибо за покупку, ' + @name)
  PRINT('Дата покупки: ' + CONVERT(nvarchar(19), @date))
  PRINT('Стоимость вашей покупки: ' + CONVERT(nvarchar(11), @sum) + ' руб.')
  PRINT('Выбранная категория компьютера: ' + @category)
  PRINT('Ваше время сеанса от ' + CONVERT(nvarchar(19), @daten) + ' до ' + CONVERT(nvarchar(19), @datek))
  PRINT('Перейдите к компьютеру с номером: ' + CONVERT(nvarchar(6), @number))
  PRINT('Осталось на счету: ' + CONVERT(nvarchar(11), @balance) + ' руб.')
  PRINT('Номер для входа в систему: ' + CONVERT(nvarchar(6), @supernumber))
END
ELSE 
BEGIN
  RAISERROR ('Время занято!', 11, 1)
  ROLLBACK TRANSACTION
END
GO
