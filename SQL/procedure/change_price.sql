--Изменение стоимости тарифа
USE КомпьютерныйКлуб
GO
CREATE PROC Изменение_стоимости_тарифа
@tariff nvarchar(15), @price decimal(9, 2)
AS BEGIN
UPDATE к SET  ЦенаЗаЧасИгры = @price
	     FROM КатегорияКомпьютера к
		 WHERE к.Категория=@tariff 
END
