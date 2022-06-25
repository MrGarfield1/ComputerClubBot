--Выборка номеров компьютеров введенной категории, которые свободны во введенное время 
--и покупка сеанса на том свободном компьютере категории, у которого минимальный номер.
USE КомпьютерныйКлуб
GO
CREATE PROC Заказ_сеанса
@nickname nvarchar(50),@category nvarchar(15), @daten datetime, @datek datetime
AS BEGIN
DECLARE @i integer
DECLARE @j integer

SELECT @i=MIN(к.ИнвентарныйНомер)
FROM 
(SELECT к.ИнвентарныйНомер
FROM Компьютер AS к INNER JOIN КатегорияКомпьютера AS кк ON к.ИДКатегории=кк.ИДКатегории
WHERE @category=кк.Категория
EXCEPT
SELECT с.ИнвентарныйНомер
FROM Сеанс с INNER JOIN Компьютер AS к ON с.ИнвентарныйНомер=к.ИнвентарныйНомер INNER JOIN КатегорияКомпьютера AS кк ON к.ИДКатегории=кк.ИДКатегории
WHERE @daten<с.ВремяОкончания AND @datek>=с.ВремяНачала AND @category=кк.Категория) AS к

SELECT @j=ИДКлиента
FROM Клиент
WHERE @nickname=Никнейм

INSERT INTO [Сеанс] VALUES
(@j,@i,@daten,@datek,NULL,NULL)
END
