from chroma import ChromaDB
from warehouse_assistant import WarehouseAssistant


def main():

    database = ChromaDB(persistent=True)

    assistant = WarehouseAssistant(
        agent_name="Luna",
        chroma_db_instance=database,
        debug=True,
        insult="kleiner Lappen",
        listen_for_tick_duration=14,
        )

    assistant.run()

if __name__ == "__main__":
    main()