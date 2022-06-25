--Запрет удаления и изменения записей в кошельке
CREATE  TRIGGER  ЗапретУдаленияИзмененияЗаписейВКошельке  ON Кошелек
   AFTER   DELETE, UPDATE
AS 
RAISERROR ('Вы не можете удалять или изменять данные!', 11, 1);
ROLLBACK TRANSACTION ;
GO
