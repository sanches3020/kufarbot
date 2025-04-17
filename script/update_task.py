from loader import cursor, bot, scheduler, con
from script.parser import parser_update


def recreate_tasks():
    
    try:
        cursor.execute("SELECT id, id_task, url FROM MyTable")
        users = cursor.fetchall() 

        for user in users:
            id, id_task, url = user

            try:
              
                job = scheduler.add_job(
                    parser_update,
                    trigger='interval',
                    seconds=60,
                    kwargs={'id': id, 'bot': bot}  
                )

                cursor.execute(
                    "UPDATE MyTable SET id_task = ? WHERE id = ?",
                    (job.id, id)
                )
                con.commit()

            except Exception as job_error:
                print(f"Ошибка при добавлении задачи для пользователя {id}: {job_error}")

        print("Все задачи успешно пересозданы!")

    except Exception as e:
        print(f"Ошибка при пересоздании задач: {e}")
