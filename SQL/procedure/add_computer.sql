--Добавление компьютера по введенной категории
USE КомпьютерныйКлуб
GO
CREATE PROC Добавление_компьютера
@category nvarchar(15)
AS BEGIN
DECLARE @id integer
SELECT @id=ИДКатегории
FROM КатегорияКомпьютера
WHERE Категория=@category
INSERT INTO [Компьютер] VALUES
(@id,NULL,NULL)
END
