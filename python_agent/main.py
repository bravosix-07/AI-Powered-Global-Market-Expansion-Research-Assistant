from app.agent import CrossBorderAgent


def main() -> None:
    agent = CrossBorderAgent()
    print("Cross-Border E-Commerce Agent")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You> ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye.")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        response = agent.handle_message(user_input)
        print("\nAgent>")
        print(response)
        print()


if __name__ == "__main__":
    main()
