--Обновление баланса в зависимости от операции 
CREATE  TRIGGER  ОбновлениеБаланса  ON Кошелек
   AFTER  INSERT
AS 
DECLARE @i nvarchar(15)
SELECT @i=LAST_VALUE(КатегорияОперации) OVER (PARTITION BY КатегорияОперации ORDER BY КатегорияОперации)
FROM inserted
print(@i)
IF @i='Пополнение'
BEGIN
UPDATE Клиент SET БалансКошелька = БалансКошелька + ко.Сумма
FROM inserted AS ко INNER JOIN Клиент AS к ON ко.ИДКлиента=к.ИДКлиента
WHERE к.ИДКлиента=ко.ИДКлиента
END
IF @i='Снятие'
BEGIN
UPDATE Клиент SET БалансКошелька = БалансКошелька - ко.Сумма
FROM inserted AS ко INNER JOIN Клиент AS к ON ко.ИДКлиента=к.ИДКлиента
WHERE к.ИДКлиента=ко.ИДКлиента
END
GO
