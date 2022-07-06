USE КомпьютерныйКлуб
GO
CREATE PROC Добавление_категории_игре
@category nvarchar(15), @name nvarchar(50)
AS BEGIN
DECLARE @idcategory integer
DECLARE @idgame integer
SELECT @idcategory=ИДКатегории
FROM КатегорияКомпьютера
WHERE Категория=@category
SELECT @idgame=ИДИгры
FROM Игра
WHERE НазваниеИгры=@name
INSERT INTO [ИграКатегория] VALUES
(@idcategory,@idgame)
END
