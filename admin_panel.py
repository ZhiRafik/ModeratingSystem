from services.rule_engine import RuleEngine
from repositories.in_memory_repo import InMemoryRepository
from services.moderation_service import ModerationService
from rules import ForbiddenWordsRule, LinksRule, RepetitionsRule, LengthRule


class AdminPanel:
    def __init__(self):
        self.engine = RuleEngine()
        self.engine.add_rule(ForbiddenWordsRule())
        self.engine.add_rule(LinksRule())
        self.engine.add_rule(RepetitionsRule())
        self.engine.add_rule(LengthRule())

        self.repo = InMemoryRepository()
        self.service = ModerationService(self.engine, self.repo)

    def run(self):
        while True:
            self._show_menu()
            choice = input("\nВыберите действие: ")

            if choice == "1":
                self._show_rules()
            elif choice == "2":
                self._toggle_rule()
            elif choice == "3":
                self._change_priority()
            elif choice == "4":
                self._add_forbidden_word()
            elif choice == "5":
                self._show_stats()
            elif choice == "6":
                self._show_history()
            elif choice == "7":
                self._test_moderation()
            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("❌ Неверный выбор")

    def _show_menu(self):
        print("\n" + "=" * 50)
        print("АДМИН ПАНЕЛЬ - СИСТЕМА МОДЕРАЦИИ")
        print("=" * 50)
        print("1. Показать все правила")
        print("2. Включить/выключить правило")
        print("3. Изменить приоритет правила")
        print("4. Добавить запрещённое слово")
        print("5. Показать статистику")
        print("6. Показать историю проверок")
        print("7. Протестировать текст")
        print("0. Выход")

    def _show_rules(self):
        print("\n--- ПРАВИЛА ---")
        for rule in self.engine.rules:
            status = "✅" if rule.enabled else "❌"
            print(f"{status} {rule.name} (приоритет: {rule.priority})")

    def _toggle_rule(self):
        name = input("Имя правила: ")
        rule = self.engine.get_rule(name)
        if rule:
            rule.enabled = not rule.enabled
            print(f"✅ {name} {'включено' if rule.enabled else 'выключено'}")
        else:
            print(f"❌ Правило {name} не найдено")

    def _change_priority(self):
        name = input("Имя правила: ")
        rule = self.engine.get_rule(name)
        if rule:
            try:
                new_priority = int(input("Новый приоритет (1-10): "))
                rule.priority = new_priority
                self.engine._sort_by_priority()
                print(f"✅ Приоритет изменён на {new_priority}")
            except ValueError:
                print("❌ Неверное значение")

    def _add_forbidden_word(self):
        rule = self.engine.get_rule("forbidden_words")
        if rule:
            word = input("Слово для добавления: ").strip()
            if word:
                rule.add_word(word)
                print(f"✅ Слово '{word}' добавлено")

    def _show_stats(self):
        stats = self.service.get_stats()
        print("\n--- СТАТИСТИКА ---")
        print(f"Всего проверок: {stats['total']}")
        print(f"✅ Одобрено: {stats['approved']}")
        print(f"❌ Отклонено: {stats['rejected']}")
        print(f"⚠️ Ручная проверка: {stats['manual_review']}")
        print(f"📊 Процент одобрения: {stats['approval_rate']}%")

    def _show_history(self):
        history = self.service.get_history(limit=10)
        if not history:
            print("История пуста")
            return

        print("\n--- ПОСЛЕДНИЕ ПРОВЕРКИ ---")
        for record in history:
            icon = "✅" if record.status.value == "approved" else "❌" if record.status.value == "rejected" else "⚠️"
            print(f"{icon} [{record.id}] {record.created_at.strftime('%H:%M:%S')} - {record.status.value}")
            print(f"   Текст: {record.text[:50]}...")
            print(f"   {record.final_message}")

    def _test_moderation(self):
        text = input("Введите текст для проверки: ")
        result = self.service.moderate(text)
        print(f"\nРЕЗУЛЬТАТ: {result.final_message}")
        print(f"Статус: {result.status.value}")
        print("\nДетали по правилам:")
        for rr in result.rule_results:
            mark = "✅" if rr.passed else "❌"
            print(f"  {mark} {rr.rule_name}: {rr.message}")


if __name__ == "__main__":
    panel = AdminPanel()
    panel.run()