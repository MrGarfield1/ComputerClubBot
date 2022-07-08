--Удаление игры
USE КомпьютерныйКлуб
GO
CREATE PROC Удаление_игр
@name nvarchar(50)
AS BEGIN
DECLARE @id integer
SELECT @id=ИДИгры
FROM Игра
WHERE @name=НазваниеИгры
DELETE FROM ИграКатегория
WHERE ИДИгры=@id
DELETE FROM Игра
WHERE ИДИгры=@id
END
