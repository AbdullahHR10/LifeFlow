"""Module that contains Taskflow's shell."""
import cmd
import shlex
from backend.models.base_model import BaseModel
from backend.models.user import User
from backend.models.task import Task
from backend.models.note import Note
from backend.models.habit import Habit
from backend.app import app
from datetime import datetime
from backend.utils.coverters import string_to_bool

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "Task": Task,
    "Habit": Habit,
    "Note": Note
    }

class TaskflowShell(cmd.Cmd):
    """TaskFlow's shell."""
    intro = "Welcome to the Taskflow Shell. type help to list commands.\n"
    prompt = "(taskflow) "

    def do_quit(self, arg):
        """Quits the shell."""
        print("Exiting Taskflow shell...")
        return True

    def do_EOF(self, arg):
        """Quits the shell."""
        print("Exiting Taskflow shell...")
        return True

    def do_create(self, arg):
        """Creates a new instance and saves it and prints the id."""
        if not arg:
            print("(ERROR) ** Class name missing **")
        else:
            args = args = shlex.split(arg)
            if args[0] not in classes:
                print("(ERROR) ** Class doesn't exist **")
                return

            class_name = args[0]
            try:
                params = {}
                for param in args[1:]:
                    if "=" in param:
                        key, value = param.split("=", 1)
                        if key == "completed":
                            value = bool(string_to_bool(value))
                        elif key in ("completed_at", "deadline"):
                            value = datetime.strptime(value, "%Y-%m-%d")
                        elif key == "priority":
                            value = value.capitalize()
                        params[key] = value
                cls = classes[class_name]
                instance = cls(**params)
            except Exception as e:
                print(f"(ERROR) ** Failed to create instance: {e} **")
                return
            with app.app_context():
                try:
                    instance.save()
                    print(f"{class_name} object has been "
                        f"created with the ID: {instance.id}")
                except Exception as e:
                    print(f"(ERROR) ** Failed to save instance: {e} **")

    def do_show(self, arg):
        """Prints the string representation of an instance
        based on class name and id."""
        if not arg:
            print("(ERROR) ** Class name missing **")

        args = args = shlex.split(arg)
        if args[0] not in classes:
            print("(ERROR) ** Class doesn't exist **")
            return
        if len(args) < 2:
            print("(ERROR) ** Instance ID missing **")
            return

        class_name = args[0]
        if class_name == "BaseModel":
            print("(ERROR) ** Cannot print instances of an abstract class: "
                    f"{class_name} **")
            return
        cls = classes[class_name]
        instance_id = args[1]
        with app.app_context():
            try:
                instance = cls.query.filter_by(id=instance_id).first()
                if not instance:
                    print(f"(ERROR) ** No {class_name} instance found"
                        f" with ID: {instance_id} **")
                    return
                print(instance)
            except Exception as e:
                print(f"(ERROR) ** Failed to fetch instance of the class with the ID: {instance_id}: {e} **")

    def do_delete(self, arg):
        """Deletes an instance based on the class name and id."""
        if not arg:
            print("(ERROR) ** Class name missing **")
            return

        args = args = shlex.split(arg)
        if args[0] not in classes:
            print("(ERROR) ** Class doesn't exist **")
            return

        if len(args) < 2:
            print(f"(ERROR) ** Instance ID missing**")
            return

        class_name = args[0]
        if class_name == "BaseModel":
            print("(ERROR) ** Cannot delete instances of an abstract class: "
                    f"{class_name} **")
            return

        cls = classes[class_name]
        instance_id = args[1]
        with app.app_context():
            try:
                instance = cls.query.filter_by(id=instance_id).first()
                if not instance:
                    print(f"(ERROR) ** No {class_name} instance found"
                          f" with ID: {instance_id} **")
                    return
                instance.delete()
                print(f"(INFO) ** Instance {instance_id} from {class_name}"
                      " has been deleted **")
            except Exception as e:
                print(f"(ERROR) ** Failed to delete instance of the class: {e} **")


    def do_truncate(self, arg):
        """Deletes all instances of a class."""
        if not arg:
            print("(ERROR) ** Class name missing **")
            return

        args = args = shlex.split(arg)
        if args[0] not in classes:
            print("(ERROR) ** Class doesn't exist **")
            return

        class_name = args[0]
        cls = classes[class_name]
        if class_name == "BaseModel":
            print("(ERROR) ** Cannot delete instances of an abstract class: "
                    f"{class_name} **")
            return

        with app.app_context():
            try:
                instances = cls.query.all()
                [instance.delete() for instance in instances]
                print(f"(INFO) ** All instances of {class_name}"
                      " have been truncated **")
            except Exception as e:
                print(f"(ERROR) ** Failed to truncate the class: {e} **")

    def do_all(self, arg):
        """Prints all string representation of all instances
        based on the class name."""
        if not arg:
            print("(ERROR) ** Class name missing **")
            return

        args = args = shlex.split(arg)
        if args[0] not in classes:
            print("(ERROR) ** Class doesn't exist **")
            return

        class_name = args[0]
        if class_name == "BaseModel":
            print("(ERROR) ** Cannot print instances of an abstract class: "
                    f"{class_name} **")
            return
        cls = classes[class_name]
        with app.app_context():
            try:
                instances = cls.query.all()
                if instances:
                    for instance in instances:
                        print(instance)
                else:
                    print(f"(INFO) No instances found for {class_name}.")
            except Exception as e:
                print(f"(ERROR) ** Failed to fetch instances of the class {class_name}: {e} **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id
        by adding or updating attribute."""
        if not arg:
            print("(ERROR) ** Class name missing **")
            return

        args = args = shlex.split(arg)
        if args[0] not in classes:
            print("(ERROR) ** Class doesn't exist **")
            return

        if len(args) < 2:
            print("(ERROR) ** Instance ID missing for class: {class_name} **")
            return

        if len(args) < 3:
            print("(ERROR) ** No attributes provided to update **")

        class_name = args[0]
        if class_name == "BaseModel":
            print("(ERROR) ** Cannot update instances of an abstract class: "
                    f"{class_name} **")
            return

        cls = classes[class_name]
        instance_id = args[1]
        updates = args[2:]
        with app.app_context():
            try:
                instance = cls.query.filter_by(id=instance_id).first()
                if not instance:
                    print(f"(ERROR) ** No {class_name} instance found"
                          f" with ID: {instance_id} **")
                    return

                for update in updates:
                    if "=" in update:
                        attr, attr_value = update.split("=", 1)
                        if hasattr(instance, attr):
                            setattr(instance, attr, attr_value)
                        else:
                            print(f"(ERROR) ** {class_name} has no attribute: {attr} **")
                            return

                instance.save()
                print(f"{class_name} instance with ID: {instance.id} has been updated.")

            except Exception as e:
                print(f"(ERROR) ** Failed to update instance of {class_name}"
                      f" with ID: {instance_id}: {e} **")

    def do_count(self, arg):
        """Retrieves the number of instances of a class."""
        if not arg:
            print("(ERROR) ** Class name missing **")
            return
        args = args = shlex.split(arg)
        if args[0] not in classes:
            print("(ERROR) ** Class doesn't exist **")
            return

        class_name = args[0]
        if class_name == "BaseModel":
            print("(ERROR) ** Cannot count instances of an abstract class: "
                    f"{class_name} **")
            return
        cls = classes[class_name]
        with app.app_context():
            try:
                print(cls.query.count())
            except Exception as e:
                print(f"(ERROR) ** Failed to fetch instances of the class: {e} **")


if __name__ == "__main__":
    try:
        TaskflowShell().cmdloop()
    except KeyboardInterrupt:
        print("Exiting Taskflow shell...")
    