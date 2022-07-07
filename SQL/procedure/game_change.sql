--Изменение игры
USE КомпьютерныйКлуб
GO
CREATE PROC Изменение_игры
@name nvarchar(50), @cell nvarchar(50), @cellchange nvarchar(50)
AS BEGIN
DECLARE @id integer
IF @cell='Жанр'
BEGIN
	UPDATE и SET ЖанрИгры = @cellchange
			FROM Игра и
			WHERE и.НазваниеИгры=@name 
END
IF @cell='Разработчик'
BEGIN
	UPDATE и SET Разработчик = @cellchange
			FROM Игра и
			WHERE и.НазваниеИгры=@name 
END
IF @cell='Дата выхода'
BEGIN
	UPDATE и SET  ДатаВыхода = @cellchange
			FROM Игра и
			WHERE и.НазваниеИгры=@name 
END
END
