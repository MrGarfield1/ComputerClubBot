from aiogram import executor
from create_bot import dp

from handlers import client, admin, other

other.register_handlers_other(dp)
client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=True)