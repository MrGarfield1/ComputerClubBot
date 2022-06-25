--Добавление игры по введенной категории
USE КомпьютерныйКлуб
GO
CREATE PROC Добавление_игры
@category nvarchar(15), @name nvarchar(50), @genre nvarchar(50), @developer nvarchar(50), @date date
AS BEGIN
DECLARE @id integer
SELECT @id=ИДКатегории
FROM КатегорияКомпьютера
WHERE Категория=@category
INSERT INTO [Игра] VALUES
(@id,@name,@genre,@developer,@date)
END
