from app.plumbit import Plumbit


class Main:
    @classmethod
    def run(cls):
        Plumbit().display_menu()


if __name__ == "__main__":
    Main.run()
