# HISTORY.md — Архив решений и история версий

Закрытые вопросы с обоснованием. Активные задачи → `BACKLOG.md`.

---

## Закрытые вопросы

### Q1 — Персонажи: сколько нужно для MVP?
✅ **Закрыт.** Один персонаж: Архитектор-предприниматель (Сергей). Охватывает ключевую механику. Остальные — иллюстрации в RESEARCH.md. Вернуться после первых 20 реальных пользователей.

### Q2 — Главная метрика
✅ **Закрыт.** Метрика MVP: **доля исполненных контрактов solo vs групповые** (цели с ≥2 активными участниками). Порог подтверждения гипотезы: разрыв ≥15%.
Реализация: `Commit.is_solo: bool = False` — один флаг при коммите.

### Q3 — Анонимность коммитов
✅ **Закрыт.** `is_public: bool = False` по умолчанию. Агрегаты всегда анонимны. Нет персональных рейтингов.

### Q4 — Роли пользователей
✅ **Закрыт.** Нет ролей в MVP. Все участники равны. Модератор — только AI + органическая фильтрация через happy moments.

### Q5 — Фреймворк Telegram-бота
✅ **Закрыт.** Выбор: **aiogram** (полностью асинхронный, встроенный FSM, активное русскоязычное сообщество, совместимость с FastAPI).

### Q6 — Масштаб MVP
✅ **Закрыт.** SQLite до ~10k коммитов, потом PostgreSQL. YAGNI.

### Q7 — Конкурентный анализ
✅ **Закрыт.** Прямых аналогов нет. StickK/Beeminder — ближайшие, но с денежными штрафами. Shared Goals заменяет негативную мотивацию на **social accountability без punishment**.

### Q8 — Персонаж «борьба с зависимостями»
✅ **Закрыт.** Подтверждён из Текста (p2-180 #social_capital_fighting_addictions). Зарок = Контракт, все 4 навыка задействованы. Переведён в раздел иллюстраций RESEARCH.md.

### Q9 — Obsidian интеграция
✅ **Закрыт.** Это text-forge плагин, не Shared Goals. Нет влияния на PRD платформы.

### Q10 — UX: показывать ли активность?
✅ **Закрыт.** Показывать свежесть: «Кто-то вложил X минут на этой неделе» (если коммиты за 7 дней). При нуле — только счётчик участников. При 0 участников — «Будь первым».

### Q11 — Cold start стратегия
✅ **Закрыт.** Seed goals вручную (3-5 штук) + invite 10-20 человек с активной жизненной позицией. Публичный онбординг — после ≥3 активных участников в seed goals.

### Q12 — shared-goals skill для ИИ-агентов
✅ **Закрыт.** Репозиторий github.com/shared-goals/skill создан. Операции: `find_goals`, `join_goal`, `commit`, `get_summary`. Протокол — MCP. Реализация — post-MVP.

### Q13 — Позиционирование относительно государства
✅ **Закрыт.** Независимый гражданский инструмент, дополняющий нацели снизу вверх. `instance_id` в Goal — архитектурная заготовка для будущей государственной инстанции. Партнёрства — после MVP.

### Q_new — instance_id в data model
✅ **Закрыт. Вариант Б принят.** `instance_id: str = "default"` в модель Goal. `instance_id + goal_id` = универсальный глобальный идентификатор цели. Стоимость отсутствия: дорогая миграция позже.

### Q — Seed Network
✅ **Закрыт (2026-04-02).**

Seed Network определяется Партнёром MVP. Из Текста (p2-180): «достаточно реализовать процесс для одной целевой группы и цели, которая будет предложена Партнёром MVP». Партнёр приходит со своей аудиторией — это и есть seed. Отдельной стратегии cold start не нужно.

### Q — Права создателя цели на модерацию коммитов
✅ **Закрыт (2026-04-02). Вариант А.**

Из Текста (p2-180, коммит c53f1d2): создатель не модерирует коммиты участников. Вместо этого — три механизма:
1. Создатель заранее определяет критерии цели (CI-подход — открыты, автоматически проверяются)
2. Автоматическая проверка формулировок при создании
3. Органическая модерация через happy moments — цели без радости не попадают в рекомендации

> «Таким образом создатель Цели может заранее продумать и расширить существующие критерии проверки по движению к цели, чтобы не отвлекаться на модерацию впоследствии.»

### Q_faith — Понятие «Вера» в PRD
✅ **Закрыт. Вариант Б принят.** Из Текста (p2-999-death.md): «Веру потребуется включить в систему, чтобы на всех жизненных этапах, включая крайние, можно было говорить о Радости». Вера = четвёртый навык (Дух по Андрееву), равноправный с Волей, Разумом, Чувствами. Без конфессиональной привязки. Реализация: `skill_tag` enum с вариантом `faith` в Commit.

### Q Goal Contagion UX
✅ **Закрыт.** UX-правило: свежесть отдельно от счётчика. Если коммиты за 7 дней → «Кто-то вложил X минут на этой неделе». Нет коммитов → только счётчик. Нет участников → «Будь первым».

### Q_partner_vodoplav — Первый кандидат Партнёра MVP
✅ **Частично закрыт (2026-04-21).** Из Текста (коммит `3a7fea1`): #vodoplav — Александр Бердников, создатель плавдома — приведён в Тексте как пример эксперта-партнёра для желающих проводить время на воде. Вопрос сузился до «есть ли у #vodoplav готовность стать Партнёром MVP?» — остаётся открытым в BACKLOG.

---

## История версий

| Версия | Дата | Изменения |
|---|---|---|
| 1.32 | 2026-07-19 | README/ACCEPTANCE/IMPLEMENTATION: MVP acceptance refocused on `Compass.md` as human-readable planning base; added human-readable Shared Goals tags (`#sg-music`, `#sg-oss-coding`), joined-contract registry replacement, recommended `next_step` flow, happy-moment-informed advice, and user-approved CUD rule |
| 1.31 | 2026-07-18 | README: уточнена hosting strategy для shared-goals/instance — dev на local development workstation, controlled MVP production на private Armbian homelab host, external Debian VPS как public-production path |
| 1.30 | 2026-07-18 | README: таблица репозиториев разделена на core platform, tooling/infrastructure, source texts/future partner providers; `robbo-provider` заменён на planned `shared-goals/robbo`; добавлены `text-forge`, `thunder-forge`, внешний `bongiozzo/whattodo`, planned `shared-goals/plavdom` и `shared-goals/pm-forge`; уточнено, что Plavdom — цель строительства домов на воде, а не generic water activity |
| 1.29 | 2026-07-18 | Добавлен IMPLEMENTATION.md как implementation-facing contract для shared-goals/instance: acceptance traceability, HTTP-level backend tests, minimal agent API; README связан с implementation contract и уточнены операции shared-goals skill |
| 1.28 | 2026-07-18 | README/ACCEPTANCE: добавлена shared development memory/RAG как coordination layer для решений, MVP status и blockers; PRD/git зафиксированы как source of truth; canonical tags упрощены до `project:sg` + `scope:dev`; добавлены KISS/DRY/YAGNI principles |
| 1.27 | 2026-07-18 | Добавлен ACCEPTANCE.md как TDD-first acceptance layer для MVP; README связан с acceptance spec; уточнены platform anti-goals и user-scoped agent keys |
| 1.26 | 2026-07-18 | README: Development Process приведён к шестифазному MVP-плану; acceptance lanes разделены на product и PRD-maintenance; простой поиск целей отделён от post-MVP Goal Discovery |
| 1.25 | 2026-07-18 | README: добавлена основная vision Shared Goals как agent-facing платформы; добавлен TDD-first development process; agent-platform пример заменён на Hermes-compatible формулировку в README; неактуальные AI-runtime детали удалены из диаграмм |
| 0.1 | 2026-02-16 | Первичный спек моделей данных |
| 0.2 | 2026-03-02 | PRD структура, visibility, анонимность, Q1–Q5 закрыты |
| 0.7 | 2026-03-03 | Q8 закрыт, персонаж зависимости, Matthews 2007, shared-goals skill |
| 0.8 | 2026-03-03 | Q5 закрыт — выбор aiogram |
| 0.9 | 2026-03-04 | Q9 закрыт, ИИ-компаньон как основной сценарий |
| 1.0–1.5 | 2026-03-04–11 | Критерии модерации, примеры, тест-вопросы, Q10–Q11 |
| 1.6 | 2026-03-12 | Q1, Q2 закрыты; `is_solo` в Commit |
| 1.7–1.10 | 2026-03-14–19 | Примеры долженствования, 4 критерия расшифрованы, Кьеркегор |
| 1.12–1.14 | 2026-03-21–23 | Силуан Афонский, архитектура инстанций, organic moderation |
| 1.16 | 2026-03-26 | Q_new закрыт, instance_id в Goal |
| 1.17–1.18 | 2026-03-28–29 | Q Goal Contagion UX закрыт, молитва как Контракт (Антоний Сурожский) |
| 1.20 | 2026-03-31 | Q_faith закрыт, `skill_tag` в Commit, раздел 10.22 |
| 1.24 | 2026-04-21 | Коммит 3a7fea1: open harness формулировка уточнена; #vodoplav кандидат Партнёра в Section 4.4 и RESEARCH; Goal Discovery + Education/Travel в README; Harness ecosystem в RESEARCH |
| 1.23 | 2026-04-21 | Коммиты 2363124, 4eef113: Goal Discovery → post-MVP; Telegram Bot / telegram repo → не в MVP; Harness Engineering + водоплав в RESEARCH; уточнён размах Samara Pub |
| 1.22 | 2026-04-05 | MVP Partner selection flagged as critical pre-MVP step; Instructions IP model clarified; BACKLOG cleaned up |
| 1.21 | 2026-04-02 | Рефакторинг структуры репо: README (EN), BACKLOG, HISTORY, RESEARCH |
