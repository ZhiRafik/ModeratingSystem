import sys
import uvicorn


def main():
    print("=" * 50)
    print("СИСТЕМА МОДЕРАЦИИ КОНТЕНТА")
    print("=" * 50)
    print("1. Запустить API сервер")
    print("2. Запустить админ-панель")
    print("0. Выход")

    choice = input("\nВыберите режим: ")

    if choice == "1":
        print("\n🚀 Запуск API сервера...")
        print("📝 Документация: http://localhost:8000/docs")
        uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
    elif choice == "2":
        print("\n🛠️ Запуск админ-панели...")
        from admin_panel import AdminPanel
        AdminPanel().run()
    elif choice == "0":
        print("До свидания!")
    else:
        print("❌ Неверный выбор")


if __name__ == "__main__":
    main()