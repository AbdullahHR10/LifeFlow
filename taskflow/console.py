"""Module that contains Taskflow's shell."""
import cmd
from backend.models.base_model import BaseModel
from backend.models.user import User
from backend.models.task import Task
from backend.app import app

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "Task": Task
    }

class TaskflowShell(cmd.Cmd):
    """Taskflow's shell."""
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
            args = arg.split()
            if args[0] not in classes:
                print("(ERROR) ** Class doesn't exist **")
                return

            class_name = args[0]
            try:
                params = {}
                for param in args[1:]:
                    if "=" in param:
                        key, value = param.split("=", 1)
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

        args = arg.split()
        if args[0] not in classes:
            print("(ERROR) ** Class doesn't exist **")
            return
        if len(args) < 2:
            print("(ERROR) ** Instance ID missing for class: {class_name} **")
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

        args = arg.split()
        if args[0] not in classes:
            print("(ERROR) ** Class doesn't exist **")
            return

        if len(args) < 2:
            print("(ERROR) ** Instance ID missing for class: {class_name} **")
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

    def do_all(self, arg):
        """Prints all string representation of all instances
        based on the class name."""
        if not arg:
            print("(ERROR) ** Class name missing **")

        args = arg.split()
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

        args = arg.split()
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
        args = arg.split()
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
    