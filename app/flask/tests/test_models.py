import unittest
import hashlib
import models


class TestModels(unittest.TestCase):
    email = "test@mail.com"
    password = "123456789"

    def register_user_if_not_exist(self, email=email):
        user = models.users.find_by_email(email)
        if not user:
            hashed_password = hashlib.sha256(self.password.encode())
            models.users.signup(
                {"email": email, "password": hashed_password.hexdigest()}
            )
        return models.users.find_by_email(email)[0]

    def add_task(self, name="task name", comment="task comment"):
        user = self.register_user_if_not_exist()
        models.tasks.add_task({"name": name, "comment": comment}, user["id"])
        return user

    # USER
    def test_create_user(self):
        user = self.register_user_if_not_exist()
        self.assertIsNotNone(user)
        self.assertEqual(
            user["password"], hashlib.sha256(self.password.encode()).hexdigest()
        )

    def test_delete_user(self):
        email = "delete@mail.com"

        user = self.register_user_if_not_exist(email)
        self.assertIsNotNone(user)
        models.users.delete_user(user["id"])
        user = models.users.find_by_email(email)
        self.assertEqual([], user)

    # TASKS
    def test_add_task(self):
        task_name = "task name"
        task_comment = "task comment"

        task_owner = self.add_task(task_name, task_comment)
        task_list = models.tasks.get_tasks(task_owner["id"])
        self.assertIsNotNone(task_list)
        created_task = list(filter(lambda x: x["name"] == task_name, task_list))
        self.assertEqual(created_task[0]["name"], task_name)
        self.assertEqual(created_task[0]["comment"], task_comment)

    def test_complete_task(self):
        task_name = "complete task name"
        task_comment = "complete task comment"

        task_owner = self.add_task(task_name, task_comment)
        task_list = models.tasks.get_tasks(task_owner["id"])
        task_list = [
            x for x in task_list if x["name"] == task_name and x["complete"] == False
        ]
        completed_task_id = task_list[0]["id"]
        models.tasks.complete_task(completed_task_id)
        task_list = models.tasks.get_tasks(task_owner["id"])
        completed_task = [x for x in task_list if x["id"] == completed_task_id]
        self.assertNotEqual(completed_task, [])
        self.assertEqual(completed_task[0]["complete"], True)

        models.tasks.not_complete_task(completed_task_id)
        task_list = models.tasks.get_tasks(task_owner["id"])
        completed_task = [x for x in task_list if x["id"] == completed_task_id]
        self.assertNotEqual(completed_task, [])
        self.assertEqual(completed_task[0]["complete"], False)

    def test_delete_task(self):
        task_name = "delete task name"
        task_comment = "delete task name"

        task_owner = self.add_task(task_name, task_comment)
        task_list = models.tasks.get_tasks(task_owner["id"])
        task_list = [
            x for x in task_list if x["name"] == task_name and x["deleted"] == False
        ]
        deleted_task_id = task_list[0]["id"]

        models.tasks.delete_task(deleted_task_id)
        task_list = models.tasks.get_deleted_tasks(task_owner["id"])
        deleted_task = [x for x in task_list if x["id"] == deleted_task_id]
        self.assertNotEqual(deleted_task, [])
        self.assertEqual(deleted_task[0]["deleted"], True)

        models.tasks.delete_task_permanently(deleted_task_id)
        task_list = models.tasks.get_tasks(task_owner["id"])
        deleted_task = [x for x in task_list if x["id"] == deleted_task_id]
        self.assertEqual(deleted_task, [])

    def test_recover_deleted_task(self):
        task_owner = self.add_task("recover", "recover this task")
        task_list = models.tasks.get_tasks(task_owner["id"])
        deleted_task_id = task_list[0]["id"]
        models.tasks.delete_task(deleted_task_id)
        task_list = models.tasks.get_deleted_tasks(task_owner["id"])
        deleted_task = [x for x in task_list if x["id"] == deleted_task_id]
        self.assertNotEqual(deleted_task, [])
        self.assertEqual(deleted_task[0]["deleted"], True)

        models.tasks.recover_task(deleted_task_id)
        task_list = models.tasks.get_tasks(task_owner["id"])
        recovered_task = [x for x in task_list if x["id"] == deleted_task_id][0]
        self.assertEqual(recovered_task["deleted"], False)


if __name__ == "__main__":
    unittest.main()
