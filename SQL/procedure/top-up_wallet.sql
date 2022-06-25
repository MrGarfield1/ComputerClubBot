--Новая запись пополнения в кошельке на основе введенных параметров (подставляется текущая дата операции)
USE КомпьютерныйКлуб
GO
CREATE PROC Пополнение_в_кошельке
@nickname nvarchar(50), @sum decimal(9, 2)  
AS BEGIN
DECLARE @id integer
SELECT @id=ИДКлиента
FROM Клиент
WHERE Никнейм=@nickname
INSERT INTO [Кошелек] VALUES
(@id,DEFAULT,@sum,'Пополнение')
END
