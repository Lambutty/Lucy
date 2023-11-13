from chroma import ChromaDB
from warehouse_assistant import WarehouseAssistant


def main():
    # im Memory
    database = ChromaDB()

    assistant = WarehouseAssistant(
        chroma_db_instance=database,
        debug=False,
        insult="kleiner Lappen",
        listen_for_tick_duration=14,
        )

    assistant.run()

if __name__ == "__main__":
    main()