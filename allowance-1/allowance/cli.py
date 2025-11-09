from allowance.ui.main_window import MainWindow
import argparse

def main():
    parser = argparse.ArgumentParser(description="Allowance CLI")
    parser.add_argument('--ui', action='store_true', help='Launch the UI')
    args = parser.parse_args()

    if args.ui:
        window = MainWindow()
        window.run()
    else:
        print("No UI option selected. Use --ui to launch the user interface.")

if __name__ == "__main__":
    main()